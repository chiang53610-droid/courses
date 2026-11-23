"""把原始 notebook 印成「編號 + 內容」的純文字，方便對照翻譯。
用法: python dump.py path/to/notebook.ipynb [max_code_chars]
"""
import json, sys

path = sys.argv[1]
max_code = int(sys.argv[2]) if len(sys.argv) > 2 else 2500
nb = json.load(open(path, encoding="utf-8"))
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"])
    t = c["cell_type"]
    print(f"\n===== [{i}] {t} =====")
    if t == "code" and len(src) > max_code:
        print(src[:max_code // 2])
        print(f"\n... <<省略 {len(src) - max_code} 字元>> ...\n")
        print(src[-max_code // 2:])
    else:
        print(src)
    if t == "code":
        outs = []
        for o in c.get("outputs", []):
            if "text" in o:
                outs.append("".join(o["text"]))
            elif "data" in o:
                d = o["data"]
                if "text/plain" in d:
                    outs.append("".join(d["text/plain"]))
                else:
                    outs.append(f"<{','.join(d.keys())}>")
            elif o.get("output_type") == "error":
                outs.append("ERROR: " + o.get("ename", "") + ": " + o.get("evalue", "")[:200])
        if outs:
            o = "\n".join(outs)
            if len(o) > 600:
                o = o[:450] + f"\n...<<輸出省略 {len(o)-600} 字元>>...\n" + o[-150:]
            print("----- output -----")
            print(o)
