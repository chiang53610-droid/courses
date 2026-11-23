#!/usr/bin/env python3
"""
把新手白話版的 .md 課程轉成「網頁版」（單頁式網站，可以直接發佈或用任何靜態網站主機放上網）。

用法（在 repo 根目錄執行）：
    pip install markdown-it-py pygments
    python zh-TW-beginner/_build/build_html.py                # 輸出到 zh-TW-beginner/_build/site/
    python zh-TW-beginner/_build/build_html.py 其他輸出資料夾

輸出內容：
    index.html          網頁外殼：側邊目錄、全文搜尋、深色模式、字體大小、學習進度
    lessons/<id>.json   每一課轉好的 HTML
    search.json         全文搜尋索引（第一次打開搜尋時才會下載）
    img/...             課程用到的圖片（保留它們在 repo 裡的路徑）
    files.json          所有輸出檔案的清單

課程順序、單元名稱、側邊欄的短標題，全部讀自 README.md 的「完整目錄」表格；
指向 .ipynb 或其他檔案的連結，會改成指向 GitHub 上的檔案（可用環境變數 GH_REF 指定分支）。
"""
import html
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.parse

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

try:
    from PIL import Image  # 有裝 Pillow 的話，幫圖片加上寬高，載入時版面不會跳動
except ImportError:
    Image = None

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)  # zh-TW-beginner/
ROOT = os.path.dirname(BASE)  # repo 根目錄
BASE_REL = os.path.relpath(BASE, ROOT).replace(os.sep, "/")  # "zh-TW-beginner"
REPO = os.environ.get("GH_REPO", "chiang53610-droid/courses")


def git_ref():
    try:
        ref = subprocess.check_output(
            ["git", "-C", ROOT, "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
        return ref if ref and ref != "HEAD" else "master"
    except Exception:
        return "master"


GH_REF = os.environ.get("GH_REF") or git_ref()
GH = f"https://github.com/{REPO}"


def gh_url(repo_path):
    """repo 內的路徑 → GitHub 網址（資料夾用 tree，檔案用 blob）"""
    kind = "tree" if os.path.isdir(os.path.join(ROOT, repo_path)) else "blob"
    return f"{GH}/{kind}/{GH_REF}/{urllib.parse.quote(repo_path)}"


# ---------------------------------------------------------------- 讀取目錄

def read_toc():
    """從 README.md 的「完整目錄」讀出單元與課程順序"""
    txt = open(os.path.join(BASE, "README.md"), encoding="utf-8").read()
    toc = txt.split("## 📚 完整目錄", 1)[1].split("\n## ", 1)[0]
    units = []
    for block in re.split(r"^### ", toc, flags=re.M)[1:]:
        head, body = block.split("\n", 1)
        m = re.match(r"(\d+)\.\s*(.+)", head.strip())
        n, title = int(m.group(1)), m.group(2).strip()
        q = re.search(r"^> (.+)$", body, flags=re.M)
        lessons = []
        for row in re.finditer(r"^\| \[([^\]]+)\]\(([^)]+\.md)\) \| ([^|]+)\|", body, flags=re.M):
            label, path, desc = row.group(1).strip(), row.group(2).strip(), row.group(3).strip()
            lessons.append({"label": label, "path": f"{BASE_REL}/{path}", "desc": desc})
        units.append({"n": n, "title": title, "note": q.group(1).strip() if q else "", "lessons": lessons})
    return units


def chip_and_label(label):
    m = re.match(r"(\d+)-(\d+)\s+(.*)", label)
    if m:
        return f"{m.group(1)}-{m.group(2)}", m.group(3)
    m = re.match(r"第\s*(\d+)\s*[課章]\s+(.*)", label)
    if m:
        return f"2-{m.group(1)}", m.group(2)
    m = re.match(r"附錄\s*([\d.]+)\s+(.*)", label)
    if m:
        return f"附 {m.group(1)}", m.group(2)
    return "附註", label


def lesson_id(unit_n, path):
    stem = path.split("/")[-2] if path.endswith("/lesson.md") else path.split("/")[-1][:-3]
    m = re.match(r"(\d+(?:_\d+)?)", stem)
    key = m.group(1).replace("_", "-") if m else re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return f"u{unit_n}-{key}"


# ---------------------------------------------------------------- 文字工具

def gh_slug(text):
    """和 GitHub 一樣的標題錨點規則（中文標題的 #錨點 要對得起來）"""
    text = re.sub(r"<[^>]+>", "", text.strip().lower())
    out = [ch for ch in text if ch in " -_" or unicodedata.category(ch)[0] in "LN"]
    return "".join(out).replace(" ", "-")


def inline_text(tok):
    """把 inline token 轉成純文字（給目錄和搜尋用）"""
    parts = []
    for c in tok.children or []:
        if c.type in ("text", "code_inline"):
            parts.append(c.content)
        elif c.type in ("softbreak", "hardbreak"):
            parts.append(" ")
        elif c.type == "image":
            parts.append(c.content)
    return "".join(parts).strip()


# ---------------------------------------------------------------- 程式碼上色

LANG_ALIAS = {"py": "python", "python3": "python", "ipython": "python", "sh": "bash", "shell": "bash",
              "console": "bash", "zsh": "bash", "yml": "yaml", "js": "javascript", "txt": "text",
              "plain": "text", "": "text"}
LANG_LABEL = {"python": "Python", "bash": "終端機指令", "yaml": "YAML", "json": "JSON", "text": "文字",
              "xml": "XML", "javascript": "JavaScript", "html": "HTML", "csv": "CSV", "markdown": "Markdown",
              "powershell": "PowerShell", "toml": "TOML", "ini": "設定檔"}
FORMATTER = HtmlFormatter(nowrap=True)


def do_highlight(code, lang, attrs):
    lang = LANG_ALIAS.get((lang or "").strip().lower(), (lang or "").strip().lower())
    label = LANG_LABEL.get(lang, lang or "文字")
    body = None
    if lang != "text":
        try:
            body = highlight(code, get_lexer_by_name(lang), FORMATTER)
        except ClassNotFound:
            body = None
    cls = "hl" if body is not None else "plain"
    if body is None:
        body = html.escape(code)
    if body.endswith("\n"):
        body = body[:-1]
    return f'<pre class="code {cls}" data-lang="{html.escape(label)}"><code>{body}</code></pre>'


MD = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
MD.options["highlight"] = do_highlight


# ---------------------------------------------------------------- 主要轉換

CALLOUTS = [
    ("🧩", "c-plain"), ("🔄", "c-update"), ("💡", "c-tip"), ("⚠", "c-warn"), ("❗", "c-warn"),
    ("📚", "c-meta"), ("⏱", "c-meta"), ("📓", "c-nb"), ("📁", "c-files"), ("🧰", "c-files"),
    ("🎯", "c-goal"), ("📝", "c-note"), ("📌", "c-note"), ("✅", "c-ok"), ("🐛", "c-warn"),
]
IMG_EXT = (".png", ".gif", ".jpg", ".jpeg", ".svg", ".webp")
MAX_W = 1600  # 網頁上最寬只顯示約 780px，1600px 已經夠高解析度螢幕用


def optimize_image(src, out, pub):
    """複製圖片；太大的 PNG 會縮小尺寸、減少顏色或改存成 JPEG。回傳 (發佈路徑, (寬, 高))"""
    dst = os.path.join(out, pub)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if Image is None:
        shutil.copyfile(src, dst)
        return pub, None
    im = Image.open(src)
    size = im.size
    if not pub.lower().endswith(".png") or os.path.getsize(src) < 250_000:
        shutil.copyfile(src, dst)
        return pub, size
    im.load()
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    alpha = im.mode in ("RGBA", "LA", "PA") and im.getchannel("A").getextrema()[0] < 255
    base = im.convert("RGBA" if alpha else "RGB")

    def save(img, fmt, **kw):
        buf = io.BytesIO()
        img.save(buf, fmt, **kw)
        return buf.getvalue()

    full = save(base, "PNG", optimize=True)
    quant = save(base.quantize(256, method=Image.Quantize.FASTOCTREE if alpha else Image.Quantize.MEDIANCUT),
                 "PNG", optimize=True)
    best, ext = (quant, ".png") if len(quant) < len(full) else (full, ".png")
    if not alpha:
        jpg = save(base, "JPEG", quality=84, optimize=True, progressive=True)
        if len(jpg) * 1.3 < len(best):
            best, ext = jpg, ".jpg"
    if ext != ".png":
        pub = pub[:-4] + ext
        dst = os.path.join(out, pub)
    with open(dst, "wb") as f:
        f.write(best)
    return pub, base.size


class Site:
    def __init__(self, out):
        self.out = out
        self.units = read_toc()
        self.lessons = []  # 依照順序
        for u in self.units:
            for les in u["lessons"]:
                chip, short = chip_and_label(les["label"])
                les.update({"id": lesson_id(u["n"], les["path"]), "unit": u["n"], "chip": chip, "short": short})
                self.lessons.append(les)
        self.pages = {les["path"]: les for les in self.lessons}
        self.pages[f"{BASE_REL}/README.md"] = {"id": "home", "path": f"{BASE_REL}/README.md", "unit": None,
                                              "chip": "", "short": "課程首頁", "desc": ""}
        self.pages[f"{BASE_REL}/GLOSSARY.md"] = {"id": "glossary", "path": f"{BASE_REL}/GLOSSARY.md", "unit": None,
                                                "chip": "", "short": "名詞小辭典", "desc": ""}
        self.slugs = {}  # path → {github slug: html id}
        self.images = {}  # repo 路徑 → (發佈路徑, 寬高)
        self.missing = []

    # -- 第一輪：讀檔、算出每個標題的錨點
    def prepare(self):
        for path, page in self.pages.items():
            src = open(os.path.join(ROOT, path), encoding="utf-8").read()
            src = re.sub(r"\A<!--.*?-->\s*\n", "", src, flags=re.S)
            m = re.match(r"> 📓 [^\n]*\[`([^`]+\.ipynb)`\]\(([^)]+)\)[^\n]*\n+", src)
            page["nb"] = None
            if m:
                page["nb"] = posixpath.normpath(posixpath.join(posixpath.dirname(path), m.group(2)))
                src = src[m.end():]
            page["src"] = src
            tokens = MD.parse(src)
            page["tokens"] = tokens
            seen, mapping, heads = {}, {}, []
            k = 0
            for i, t in enumerate(tokens):
                if t.type != "heading_open":
                    continue
                inline = tokens[i + 1]
                s = gh_slug(inline.content)
                if s in seen:
                    seen[s] += 1
                    s = f"{s}-{seen[s]}"
                else:
                    seen[s] = 0
                k += 1
                hid = f"{page['id']}_s{k}"
                t.attrSet("id", hid)
                mapping[s] = hid
                heads.append({"id": hid, "level": int(t.tag[1]), "text": inline_text(inline)})
                if t.tag == "h1" and "title" not in page:
                    page["title"] = inline_text(inline)
            self.slugs[path] = mapping
            page["heads"] = heads

    def resolve(self, href, page, is_image=False):
        """把 .md 裡的相對連結改成網頁版能用的連結。回傳 (新網址, 是否外部連結)"""
        if re.match(r"^[a-z]+:", href):
            return href, True
        path, _, frag = href.partition("#")
        frag = urllib.parse.unquote(frag)
        if not path:
            hid = self.slugs[page["path"]].get(frag)
            if not hid:
                self.missing.append((page["path"], href))
            return f"#{hid or page['id']}", False
        target = posixpath.normpath(posixpath.join(posixpath.dirname(page["path"]), urllib.parse.unquote(path)))
        if is_image or target.lower().endswith(IMG_EXT):
            if not os.path.exists(os.path.join(ROOT, target)):
                self.missing.append((page["path"], href))
            if target not in self.images:
                pub = "img/" + (target[len(BASE_REL) + 1:] if target.startswith(BASE_REL + "/") else target)
                if os.path.exists(os.path.join(ROOT, target)):
                    self.images[target] = optimize_image(os.path.join(ROOT, target), self.out, pub)
                else:
                    self.images[target] = (pub, None)
            return self.images[target][0], False
        if target in self.pages:
            tgt = self.pages[target]
            if frag:
                hid = self.slugs[target].get(frag)
                if not hid:
                    self.missing.append((page["path"], href))
                return f"#{hid or tgt['id']}", False
            return f"#{tgt['id']}", False
        if not os.path.exists(os.path.join(ROOT, target)):
            self.missing.append((page["path"], href))
        return gh_url(target), True

    def render(self, page):
        tokens = page["tokens"]

        def walk(toks):
            for t in toks:
                if t.type == "link_open":
                    new, ext = self.resolve(t.attrGet("href"), page)
                    t.attrSet("href", new)
                    if ext:
                        t.attrSet("target", "_blank")
                        t.attrSet("rel", "noopener")
                        t.attrSet("class", "ext")
                elif t.type == "image":
                    new, _ = self.resolve(t.attrGet("src"), page, is_image=True)
                    t.attrSet("src", new)
                    wh = next((v[1] for v in self.images.values() if v[0] == new), None)
                    if wh:
                        t.attrSet("width", str(wh[0]))
                        t.attrSet("height", str(wh[1]))
                    t.attrSet("loading", "lazy")
                    t.attrSet("decoding", "async")
                if t.children:
                    walk(t.children)

        walk(tokens)
        out = MD.renderer.render(tokens, MD.options, {})

        # 原課程執行結果：標籤和輸出框換成專屬樣式
        out = re.sub(r"<p><strong>(▶[^<]*?)：?</strong></p>", r'<p class="out-label">\1</p>', out)
        out = re.sub(r'(<p class="out-label">[^<]*</p>\s*)<pre class="code plain" data-lang="[^"]*"',
                     r'\1<pre class="code plain output" data-lang="執行結果"', out)
        out = re.sub(r'(<summary>▶[^<]*</summary>\s*)<pre class="code plain" data-lang="[^"]*"',
                     r'\1<pre class="code plain output" data-lang="執行結果"', out)
        out = re.sub(r"<details>\s*<summary>▶", '<details class="out-details">\n<summary>▶', out)

        # 提醒框（白話小補充、2026 更新、注意⋯⋯）
        def callout(m):
            first = m.group(1)
            for emo, cls in CALLOUTS:
                if first.startswith(emo):
                    return f'<blockquote class="callout {cls}">\n<p>{first}'
            return m.group(0)

        out = re.sub(r"<blockquote>\n<p>(.)", callout, out)
        out = out.replace("\n⏱", "<br>\n⏱")  # 「第幾課／預估時間」分兩行顯示
        # 表格可以左右捲動，不會把手機畫面撐破
        out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
        out = out.replace("<details>", '<details class="fold">')
        # 外部（http）連結：開新分頁
        out = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener" class="ext">', out)
        # 檢查：中文標點旁邊的 **粗體** 有時候會失效（CommonMark 的規則），提醒維護者改用 <strong>
        for i, part in enumerate(re.split(r"(<pre.*?</pre>|<code>.*?</code>)", out, flags=re.S)):
            if i % 2 == 0 and "**" in part:
                for m in re.finditer(r".{0,15}\*\*.{0,15}", part):
                    self.missing.append((page["path"], "粗體沒有生效，請改用 <strong>：" + m.group(0)))
        return out

    def search_sections(self, page):
        """把一課切成一段一段（以標題分段），只留說明文字，不含程式碼和執行結果"""
        secs, cur = [], {"s": page["id"], "h": "", "t": []}
        tokens = page["tokens"]
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.type == "heading_open":
                if cur["t"] or cur["h"]:
                    secs.append(cur)
                cur = {"s": t.attrGet("id"), "h": inline_text(tokens[i + 1]), "t": []}
                i += 3
                continue
            if t.type == "inline":
                cur["t"].append(inline_text(t))
            i += 1
        secs.append(cur)
        res = []
        for s in secs:
            text = re.sub(r"\s+", " ", " ".join(s["t"])).strip()
            if text or s["h"]:
                res.append({"s": s["s"], "h": s["h"], "t": text})
        return res

    def build(self):
        self.prepare()
        if os.path.exists(self.out):
            shutil.rmtree(self.out)
        os.makedirs(os.path.join(self.out, "lessons"))
        index = []
        order = [les["id"] for les in self.lessons]
        for path, page in self.pages.items():
            body = self.render(page)
            data = {
                "id": page["id"],
                "title": page.get("title", page["short"]),
                "html": body,
                "heads": [h for h in page["heads"] if h["level"] in (2, 3)],
                "nb": gh_url(page["nb"]) if page.get("nb") else None,
                "nbName": page["nb"].split("/")[-1] if page.get("nb") else None,
                "folder": gh_url(posixpath.dirname(path)) if path.endswith("/lesson.md") else None,
                "src": gh_url(path),
            }
            with open(os.path.join(self.out, "lessons", page["id"] + ".json"), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
            for s in self.search_sections(page):
                index.append([page["id"], s["s"], s["h"], s["t"]])
        with open(os.path.join(self.out, "search.json"), "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, separators=(",", ":"))

        manifest = {
            "units": [{"n": u["n"], "title": u["title"],
                       "lessons": [{k: les[k] for k in ("id", "chip", "short", "desc")} | {"title": self.pages[les["path"]].get("title", les["short"])}
                                   for les in u["lessons"]]}
                      for u in self.units],
            "order": order,
            "gh": gh_url(BASE_REL),
        }
        shell = open(os.path.join(HERE, "html_shell.html"), encoding="utf-8").read()
        shell = shell.replace("/*__MANIFEST__*/null", json.dumps(manifest, ensure_ascii=False, separators=(",", ":")))
        with open(os.path.join(self.out, "index.html"), "w", encoding="utf-8") as f:
            f.write(shell)

        files = []
        for dp, _, fns in os.walk(self.out):
            for fn in fns:
                files.append(os.path.relpath(os.path.join(dp, fn), self.out).replace(os.sep, "/"))
        files = sorted(f for f in files if f not in ("index.html", "files.json"))
        with open(os.path.join(self.out, "files.json"), "w", encoding="utf-8") as f:
            json.dump(files, f, ensure_ascii=False, indent=1)
        return files


if __name__ == "__main__":
    out = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "site")
    site = Site(out)
    files = site.build()
    size = sum(os.path.getsize(os.path.join(out, f)) for f in files + ["index.html"])
    print(f"✔ {len(site.pages)} 頁、{len(site.images)} 張圖片，共 {len(files) + 1} 個檔案、{size / 1e6:.1f} MB → {out}")
    if site.missing:
        print("⚠ 找不到的連結：")
        for p, h in site.missing:
            print("  ", p, h)
