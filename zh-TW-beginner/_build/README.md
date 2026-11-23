# 建置說明（給維護者）

新手白話版的每一課，都是從 `src/` 裡的原稿（`*.src.md`）自動產生的，**請修改原稿，不要直接修改產生出來的 `.md` 和 `.ipynb`**。

## 檔案

| 檔案 | 用途 |
|---|---|
| `build.py` | 把 `src/**/*.src.md` 轉成可執行的 `.ipynb` 和方便閱讀的 `.md` |
| `assets.py` | 把第 4 單元 promptfoo 課程（第 5～9 課）需要的設定檔、資料檔複製過來，並更新模型名稱、加上中文註解 |
| `dump.py` | 把原始英文 notebook 印成「編號 + 內容」，方便對照翻譯時查格子編號 |
| `src/` | 每一課的原稿 |

## 原稿格式

原稿就是一般的 Markdown，加上幾個指令（詳見 `build.py` 開頭的說明）：

- 檔案開頭的 `<!--meta {...} -->`：設定原始 notebook（`orig`）和輸出位置（`out`）等。
- `{{cell 5}}`、`{{cells 5-9}}`：從原始 notebook 複製程式碼格（含原本的執行結果），並自動把已停用的模型名稱換成目前可用的模型、把 `pip install anthropic` 換成 `pip install "anthropic<1"`。
- `{{cell 5 img=路徑}}`：這格的輸出是圖片時，在 `.md` 裡改用指定的圖片檔顯示。
- ` ```python run `：新寫的、可以執行的程式碼格（一般的 ` ```python ` 只顯示、不執行）。
- `@orig/`、`@root/`：自動換成指向原始課程資料夾／repo 根目錄的相對路徑。

## 指令

在 repo 根目錄執行：

```bash
pip install nbformat
python zh-TW-beginner/_build/build.py            # 建置全部
python zh-TW-beginner/_build/build.py 05_tool    # 只建置路徑含有 05_tool 的原稿
python zh-TW-beginner/_build/assets.py           # 更新 promptfoo 課程的附屬檔案
python zh-TW-beginner/_build/dump.py tool_use/02_your_first_simple_tool.ipynb   # 查看原始 notebook 的格子編號
```
