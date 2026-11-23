"""
新手白話版課程的建置腳本（給維護者用，學習者不需要執行）。

每一課的「原稿」放在 _build/src/**/*.src.md，格式是一般 Markdown，再加上幾個特殊指令：

  <!--meta {...JSON...} -->   檔案開頭的設定：
        orig    : 原始英文 notebook 的路徑（相對於 repo 根目錄），可省略
        md_only : true 代表只輸出 .md（純閱讀頁面，沒有程式碼要執行）
        out     : 輸出位置（相對於 zh-TW-beginner/，不含副檔名）
        replace : [[舊字串, 新字串], ...]，套用在「從原始 notebook 複製過來的程式碼」上
        models  : {舊模型: 新模型}，覆寫預設的模型對照表
  {{cell 5}}            從原始 notebook 複製第 5 格（程式碼含輸出）
  {{cell 5 noout}}      複製第 5 格，但不要輸出結果
  {{cell 5 img=路徑}}   這格的輸出是圖片；在 .md 中改用這個圖片檔顯示（路徑可用 @orig/）
  {{cells 5-9}}         複製第 5 到第 9 格
  ```python run         新寫的、可以執行的程式碼格
  <!-- split -->        把 Markdown 切成兩格
  @orig/                換成「從輸出檔到原始課程資料夾」的相對路徑（給圖片用）
  @root/                換成「從輸出檔到 repo 根目錄」的相對路徑

每一課會同時輸出 .ipynb（可以執行）和 .md（方便閱讀）。
用法：python zh-TW-beginner/_build/build.py [只建置檔名含有這段文字的原稿]
"""
import copy
import glob
import json
import os
import re
import sys

import nbformat

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)            # zh-TW-beginner/
ROOT = os.path.dirname(BASE)            # repo 根目錄

# 原課程用的 Claude 3 系列模型已經全部停用（retired），呼叫會失敗。
# 這裡換成「目前還能用、而且行為最接近原課程」的模型：
#   - 都支援 temperature 參數（搭配 0.x 版 SDK）
#   - 預設不開啟 extended thinking，所以 response.content[0].text 一定是文字
#   - claude-haiku-4-5 支援「預先填寫 Claude 的回答（prefill）」；
#     Sonnet 4.6 / Opus 4.6 不支援 prefill，用到 prefill 的課會在 meta 的 models 裡個別改用 Haiku 4.5
DEFAULT_MODELS = {
    "claude-3-haiku-20240307": "claude-haiku-4-5",
    "claude-3-sonnet-20240229": "claude-sonnet-4-6",
    "claude-3-5-sonnet-20240620": "claude-sonnet-4-6",
    "claude-3-opus-20240229": "claude-opus-4-6",
}

PIP_RE = re.compile(r"(pip install[^\n]*?)(?<![\w\-\"'])anthropic(?![\w<>=\-\[\"'])")


def rel(from_dir, to_path):
    return os.path.relpath(to_path, from_dir).replace(os.sep, "/")


def fix_code(src, meta):
    models = dict(DEFAULT_MODELS)
    models.update(meta.get("models", {}))
    for old, new in models.items():
        src = src.replace(old, new)
    src = PIP_RE.sub(r'\1"anthropic<1"', src)
    for old, new in meta.get("replace", []):
        src = src.replace(old, new)
    return src


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", text, re.S)
    if not m:
        raise SystemExit(f"{path}: 缺少 <!--meta ... --> 設定")
    meta = json.loads(m.group(1))
    return meta, text[m.end():]


def build(src_path):
    meta, body = parse(src_path)
    out_noext = os.path.join(BASE, meta["out"])
    out_dir = os.path.dirname(out_noext)
    os.makedirs(out_dir, exist_ok=True)

    orig_nb = None
    orig_dir = None
    if meta.get("orig"):
        orig_path = os.path.join(ROOT, meta["orig"])
        orig_nb = json.load(open(orig_path, encoding="utf-8"))
        orig_dir = os.path.dirname(orig_path)

    body = body.replace("@root/", rel(out_dir, ROOT) + "/")
    if orig_dir:
        body = body.replace("@orig/", rel(out_dir, orig_dir) + "/")

    cells = []          # (kind, payload)
    md_buf = []

    def flush_md():
        txt = "\n".join(md_buf).strip("\n")
        md_buf.clear()
        if txt.strip():
            cells.append(("md", txt))

    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        m = re.fullmatch(r"\{\{cells?\s+(\d+)(?:-(\d+))?((?:\s+[\w]+(?:=\S+)?)*)\}\}", s)
        if m:
            flush_md()
            a = int(m.group(1))
            b = int(m.group(2) or a)
            opts = dict((o.split("=", 1) + [True])[:2] for o in m.group(3).split())
            for k in range(a, b + 1):
                cells.append(("orig", (k, opts)))
            i += 1
            continue
        if s == "<!-- split -->":
            flush_md()
            i += 1
            continue
        if s.startswith("```") and re.fullmatch(r"```+\s*(python|bash|sh)?\s+run", s):
            fence = re.match(r"`+", s).group(0)
            flush_md()
            j = i + 1
            code = []
            while j < len(lines) and lines[j].strip() != fence:
                code.append(lines[j])
                j += 1
            if j >= len(lines):
                raise SystemExit(f"{src_path}: 第 {i+1} 行的程式碼區塊沒有結束")
            cells.append(("code", "\n".join(code)))
            i = j + 1
            continue
        if s.startswith("```"):
            # 一般（只顯示、不執行）的程式碼區塊：原封不動放進 Markdown
            fence = re.match(r"`+", s).group(0)
            md_buf.append(line)
            j = i + 1
            while j < len(lines):
                md_buf.append(lines[j])
                if lines[j].strip() == fence:
                    break
                j += 1
            i = j + 1
            continue
        md_buf.append(line)
        i += 1
    flush_md()

    # ---------- 產生 .ipynb ----------
    nb = nbformat.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    }
    md_out = []
    for kind, payload in cells:
        if kind == "md":
            nb.cells.append(nbformat.v4.new_markdown_cell(payload))
            md_out.append(payload)
        elif kind == "code":
            nb.cells.append(nbformat.v4.new_code_cell(payload))
            md_out.append(render_code_md(payload, []))
        else:
            k, opts = payload
            noout = bool(opts.get("noout"))
            if orig_nb is None:
                raise SystemExit(f"{src_path}: 用了 {{{{cell}}}} 但沒有設定 orig")
            oc = copy.deepcopy(orig_nb["cells"][k])
            src = "".join(oc["source"])
            if oc["cell_type"] == "code":
                src = fix_code(src, meta)
                outputs = [] if noout else oc.get("outputs", [])
                cell = nbformat.v4.new_code_cell(src)
                cell.outputs = [nbformat.from_dict(o) for o in outputs]
                for o in cell.outputs:
                    if o.get("output_type") == "execute_result":
                        o["execution_count"] = None
                nb.cells.append(cell)
                md_out.append(render_code_md(src, outputs, opts.get("img")))
            else:
                nb.cells.append(nbformat.v4.new_markdown_cell(src))
                md_out.append(src)
    for n, c in enumerate(nb.cells):
        c["id"] = f"c{n:03d}"      # 固定的格子編號，重新建置時檔案差異才不會亂跳
    nbformat.validate(nb)
    if not meta.get("md_only"):
        nbformat.write(nb, out_noext + ".ipynb")

    # ---------- 產生 .md ----------
    header = "<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->\n"
    if not meta.get("md_only"):
        header += (
            f"> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 "
            f"[`{os.path.basename(out_noext)}.ipynb`]({os.path.basename(out_noext)}.ipynb)。\n\n"
        )
    with open(out_noext + ".md", "w", encoding="utf-8") as f:
        f.write(header + "\n\n".join(md_out) + "\n")
    return out_noext


def output_text(outputs, img=None):
    parts = []
    for o in outputs:
        t = o.get("output_type")
        if t == "stream":
            parts.append("".join(o.get("text", "")))
        elif t in ("execute_result", "display_data"):
            d = o.get("data", {})
            if "text/plain" in d and not any(k.startswith("image/") for k in d):
                parts.append("".join(d["text/plain"]))
            elif any(k.startswith("image/") for k in d):
                parts.append(IMG_MARK if img else "[這裡原本會顯示一張圖片，請打開 .ipynb 檔查看]")
            elif "text/html" in d:
                parts.append("[這裡原本是網頁格式的輸出，請打開 .ipynb 檔查看]")
        elif t == "error":
            parts.append(f"錯誤 {o.get('ename','')}: {o.get('evalue','')}")
    txt = "\n".join(p.rstrip("\n") for p in parts if p is not None)
    txt = re.sub(r"\x1b\[[0-9;]*m", "", txt)   # 去掉終端機的顏色控制碼
    return txt


def fenced(text, lang=""):
    longest = max([len(m) for m in re.findall(r"`{3,}", text)] + [2])
    fence = "`" * (longest + 1)
    return f"{fence}{lang}\n{text}\n{fence}"


IMG_MARK = "\x00IMG\x00"


def render_code_md(src, outputs, img=None):
    block = fenced(src, "python")
    if img:
        # 這格的輸出是一張圖片：在 .md 裡直接顯示原始圖片檔
        txt = output_text(outputs, img).replace(IMG_MARK, "").strip()
        block += f"\n\n**▶ 執行結果（顯示圖片）：**\n\n![執行結果的圖片]({img})"
        if txt:
            block += "\n\n" + fenced(txt, "text")
        return block
    if len(src) > 4000:
        block = (
            "<details>\n<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>\n\n"
            + block + "\n\n</details>"
        )
    out = output_text(outputs)
    if out.strip():
        oblock = fenced(out, "text")
        label = "▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）"
        if len(out) > 3000:
            block += f"\n\n<details>\n<summary>{label}——內容很長，點這裡展開</summary>\n\n{oblock}\n\n</details>"
        else:
            block += f"\n\n**{label}：**\n\n{oblock}"
    return block


if __name__ == "__main__":
    pattern = sys.argv[1] if len(sys.argv) > 1 else ""
    srcs = sorted(glob.glob(os.path.join(HERE, "src", "**", "*.src.md"), recursive=True))
    n = 0
    for s in srcs:
        if pattern in s:
            out = build(s)
            print("✔", os.path.relpath(out, BASE))
            n += 1
    print(f"共建置 {n} 課")
