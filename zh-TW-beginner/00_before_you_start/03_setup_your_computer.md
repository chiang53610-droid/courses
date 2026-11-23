<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`03_setup_your_computer.ipynb`](03_setup_your_computer.ipynb)。

# 0-3 準備你的電腦

> 🎯 **這一課你會學到：**
> 1. 安裝 Python 和「可以執行 notebook 的程式」
> 2. 下載課程檔案
> 3. 安裝課程需要的套件
> 4. 申請 API 金鑰，並安全地存起來
> 5. 為什麼這個版本的模型名稱和原課程不一樣（🔄 2026 更新）
> 6. 跑一次測試，確認一切正常
>
> ⏱️ 預估時間：30～60 分鐘（第一次裝環境比較花時間，之後就不用再弄了）

---

## 步驟 1：安裝 Python

**Python** 是一種程式語言。我們要先在電腦裡裝好「Python 翻譯官」，電腦才看得懂 Python 程式。

1. 到 Python 官網 <https://www.python.org/downloads/> 下載最新版（建議 3.10 以上）。
2. **Windows 使用者**：安裝畫面最下面有一個 **「Add python.exe to PATH」** 的勾選框，**一定要打勾！** 否則之後打指令會找不到 Python。
3. **Mac 使用者**：下載 macOS 版安裝即可。Mac 上的指令通常要打 `python3`、`pip3`（多一個 3）。

**怎麼確認裝好了？** 打開「終端機」：

- **Windows**：按開始鍵，搜尋「命令提示字元」或「PowerShell」。
- **Mac**：按 `Command + 空白鍵`，搜尋「終端機」（Terminal）。

然後輸入下面這行，按 Enter：

```
python --version
```

（Mac 請輸入 `python3 --version`）

如果看到類似 `Python 3.12.4` 的文字，就代表成功了！

> 🧩 **白話小補充：終端機是什麼？**
> 終端機是一個「用打字來指揮電腦」的視窗。平常我們用滑鼠點來點去，在終端機裡則是打一行指令、按 Enter，電腦就照做。整套課程只會用到少數幾個指令，不用怕。

---

## 步驟 2：安裝可以打開 notebook（`.ipynb`）的程式

課程檔案大多是 **Jupyter Notebook**（副檔名 `.ipynb`）。它是一種特別的檔案：**說明文字和程式碼混在一起，而且程式碼可以一格一格執行**，執行結果就直接顯示在下面。非常適合學習。

有兩種方式可以打開它，**選一種就好**：

### 方式 A（推薦）：VS Code

1. 到 <https://code.visualstudio.com/> 下載安裝 VS Code（免費）。
2. 打開 VS Code，點左邊的「延伸模組」圖示（四個方塊），搜尋並安裝 **Python** 和 **Jupyter** 這兩個延伸模組（都是 Microsoft 出的）。
3. 之後用 VS Code 打開 `.ipynb` 檔，右上角選擇「核心（Kernel）」→ 選你剛裝的 Python，就可以執行了。

### 方式 B：Jupyter Notebook（瀏覽器版）

在終端機輸入：

```
pip install notebook
```

裝好之後，到課程資料夾裡輸入：

```
jupyter notebook
```

瀏覽器就會自動打開，點選檔案即可。

### 怎麼執行一格程式碼？

- 點一下程式碼格，按 **`Shift + Enter`**：執行這一格，並跳到下一格。
- 程式碼格左邊會出現數字，例如 `[1]`，代表「這是第 1 個被執行的格子」；如果顯示 `[*]`，代表「正在執行中，請稍等」。

> ⚠️ **很重要：請從上往下，依序執行！**
> notebook 裡後面的程式碼常常會用到前面建立的東西（例如前面設定好的 API 金鑰）。如果跳著執行，就會出現「找不到某某東西」的錯誤（`NameError`）。
> 如果整個亂掉了，可以選「重新啟動核心（Restart Kernel）」，然後從第一格重新開始跑。

---

## 步驟 3：下載課程檔案

1. 打開這個課程的 GitHub 頁面。
2. 點綠色的 **「Code」** 按鈕 → **「Download ZIP」**。
3. 把下載的 ZIP 檔解壓縮，放在你找得到的地方（例如「文件」資料夾）。

（如果你會用 git，也可以用 `git clone` 下載。）

解壓縮之後，資料夾結構大概長這樣：

```
courses/                         ← 課程最上層資料夾（我們叫它「根目錄」）
├── anthropic_api_fundamentals/  ← 原始英文課程（圖片也放在這裡）
├── prompt_engineering_interactive_tutorial/
├── real_world_prompting/
├── prompt_evaluations/
├── tool_use/
└── zh-TW-beginner/              ← 👈 你現在在讀的新手白話版
```

---

## 步驟 4：安裝課程需要的套件

<strong>套件（package）</strong>就是別人寫好、可以直接拿來用的程式工具。我們需要兩個：

- **`anthropic`**：Anthropic 官方的 Python SDK，用來跟 Claude 溝通。
- **`python-dotenv`**：用來從 `.env` 檔案讀取 API 金鑰。

在 notebook 裡，可以直接執行下面這格來安裝（前面的 `%pip` 是 notebook 專用的安裝指令）：

```python
%pip install "anthropic<1" python-dotenv
```

**逐行解說：**
- `%pip install`：在 notebook 裡安裝套件的指令。如果是在終端機裡，就改成 `pip install "anthropic<1" python-dotenv`（Mac 可能要用 `pip3`）。
- `"anthropic<1"`：安裝 `anthropic` 套件，但**版本要小於 1**（也就是 0.x 版）。為什麼要指定舊版本？請看下面的「🔄 2026 更新」。

---

## 🔄 2026 更新：為什麼模型名稱和原課程不一樣？

原課程是 2024 年製作的，當時用的是 **Claude 3** 系列模型。到了現在，這些模型<strong>全部都已經停用（retired）</strong>了，用舊名字呼叫會得到錯誤。所以在這個新手版裡，**所有「可以執行的程式碼」都已經自動換成目前還能用的模型**：

| 原課程的模型名稱 | 已經停用的日期 | 新手版換成 |
|---|---|---|
| `claude-3-haiku-20240307`（Claude 3 Haiku） | 2026/4/20 | **`claude-haiku-4-5`**（Claude Haiku 4.5） |
| `claude-3-sonnet-20240229`（Claude 3 Sonnet） | 2025/7/21 | **`claude-sonnet-4-6`**（Claude Sonnet 4.6） |
| `claude-3-5-sonnet-20240620`（Claude 3.5 Sonnet） | 2025/10/28 | **`claude-sonnet-4-6`**（Claude Sonnet 4.6） |
| `claude-3-opus-20240229`（Claude 3 Opus） | 2026/1/5 | **`claude-opus-4-6`**（Claude Opus 4.6） |

**為什麼不直接換成最新的模型？**
因為最新一代的模型（例如 Claude Haiku 5.5、Sonnet 5.5、Opus 5.5）有幾個行為和舊課程的寫法不相容：

1. **不支援「預先填寫 Claude 的回答」（prefill）**：這是原課程第 2 單元第 5 章等地方會教的技巧，新模型會直接回傳錯誤。
2. **不支援 `temperature` 等取樣參數**：第 1 單元第 4 課會教這個參數。
3. **預設會先「思考」**：回應的第一塊可能是「思考內容」而不是文字，原課程常用的 `response.content[0].text` 寫法就會出錯。

所以我們選了「還在服務中、而且行為最接近原課程」的模型，讓你**不用改任何程式碼就能跑完整套課程**。其中 Haiku 4.5 是課程裡用最多的模型，它支援上面全部三件事。（Sonnet 4.6 和 Opus 4.6 支援 temperature，但不支援 prefill；有用到 prefill 的地方，新手版會特別處理或提醒。）

**為什麼安裝 `anthropic<1`（0.x 版的 SDK）？**
同樣的原因：新版（1.0 以後）的 `anthropic` 套件拿掉了 `temperature` 參數，2.0 以後更會改用新版 API 規則。為了讓原課程的程式碼**原封不動**就能執行，我們安裝最後一個 0.x 版。

> 💡 **小提醒：學完之後要做自己的專案時**，建議改用最新版 SDK（`pip install -U anthropic`）和最新模型（例如 `claude-opus-5-5`、`claude-sonnet-5-5`、`claude-haiku-5-5`），並且：
> - 用「系統提示詞」或「結構化輸出（structured outputs）」取代 prefill；
> - 不要傳 `temperature`；
> - 讀取回答時，找出 `type == "text"` 的那一塊，而不是直接拿 `content[0]`。
>
> 這些都是進階議題，學完整套課程再回頭看就會懂。

> ⚠️ **注意：課程裡顯示的「原課程執行結果」是用舊的 Claude 3 模型跑出來的。** 你用新模型跑的時候，回答的內容、長度、速度都會不同——通常新模型會更聰明。這不是你做錯了！

---

## 步驟 5：申請 API 金鑰

1. 到 Anthropic 主控台（Console）<https://console.anthropic.com/> 註冊帳號並登入。
2. 到「API Keys」頁面，按 **「Create Key」**，幫金鑰取個名字（例如 `course`），按建立。
3. **立刻把金鑰複製下來**——離開那個頁面之後就再也看不到了！
4. 到「Billing」（帳務）頁面儲值一點點金額（例如 5 美元），API 才能使用。

（第 1 單元第 1 課會再詳細說明一次。）

---

## 步驟 6：把 API 金鑰安全地存起來（`.env` 檔）

我們**不要**把金鑰直接寫在程式碼裡（萬一程式碼分享出去，金鑰就外流了）。
比較安全的做法是：把金鑰存在一個叫 **`.env`** 的檔案裡，程式執行時再去讀它。

1. 在**課程根目錄**（就是 `courses` 資料夾，和 `zh-TW-beginner` 同一層）建立一個新檔案，檔名就叫 `.env`（**前面有一個點，沒有其他副檔名**）。
2. 用記事本或 VS Code 打開它，輸入一行（把後面換成你的金鑰）：

```
ANTHROPIC_API_KEY=sk-ant-api03-你的金鑰貼在這裡
```

3. 存檔。

> 💡 **小提醒**：
> - 等號兩邊**不要**有空格，金鑰**不用**加引號。
> - Windows 的記事本有時候會偷偷把檔名存成 `.env.txt`，請在檔案總管開啟「顯示副檔名」確認。
> - 為什麼放在根目錄？因為 `python-dotenv` 找不到 `.env` 時會**往上一層一層找**，放在根目錄的話，所有課程資料夾裡的 notebook 都找得到它。
> - 這個 repo 的 `.gitignore` 已經設定好忽略 `.env`，所以就算你用 git，它也不會被上傳。

---

## 步驟 7：測試看看！

執行下面這格。它會讀取你的金鑰，並請 Claude 打個招呼：

```python
from dotenv import load_dotenv   # 從 dotenv 套件拿出「讀取 .env 檔」的功能
import os                        # os 是 Python 內建的工具，可以讀取環境變數

load_dotenv()                    # 去找 .env 檔，把裡面的設定讀進來
key = os.getenv("ANTHROPIC_API_KEY")   # 取出名叫 ANTHROPIC_API_KEY 的值

if key is None:
    print("❌ 找不到 API 金鑰！請確認 .env 檔的位置和內容。")
else:
    # 只印出前 10 個字，確認有讀到就好（不要把整把金鑰印出來）
    print("✅ 有讀到金鑰，開頭是：", key[:10], "...")
```

如果上面顯示 ✅，再執行下面這格，真的呼叫一次 Claude：

```python
from anthropic import Anthropic

client = Anthropic()   # 會自動使用 ANTHROPIC_API_KEY 這個環境變數

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    messages=[{"role": "user", "content": "請用一句繁體中文跟我打招呼，並祝我學習順利！"}],
)
print(response.content[0].text)
```

看到 Claude 的回答了嗎？🎉 **恭喜！你的環境已經準備好了！**

---

## 常見錯誤排除

程式出錯時，notebook 會顯示一大段紅色或彩色文字，**看最後一行**通常就知道問題在哪。

| 錯誤訊息（最後一行） | 白話意思 | 怎麼解決 |
|---|---|---|
| `ModuleNotFoundError: No module named 'anthropic'` | 找不到 `anthropic` 套件 | 執行上面的安裝格。VS Code 使用者要確認右上角選的「核心」跟安裝套件的是同一個 Python。裝完可能需要「重新啟動核心」。 |
| `NameError: name 'client' is not defined` | 用到了還沒建立的東西 | 你跳過了前面的格子。從上往下重新執行。 |
| `AuthenticationError` / `401` / `invalid x-api-key` | API 金鑰錯誤 | 檢查 `.env` 裡的金鑰有沒有複製完整、有沒有多餘的空格或引號。 |
| `TypeError: ... api_key ... must be set` 或金鑰是 `None` | 沒讀到 `.env` | 確認 `.env` 檔名正確（不是 `.env.txt`）、放在課程根目錄。 |
| `Your credit balance is too low` | 帳戶沒錢了 | 到 Console 的 Billing 頁面儲值。 |
| `NotFoundError` / `404` / `not_found_error ... model` | 模型名稱錯誤或已停用 | 確認模型名稱，請參考上面「2026 更新」的對照表。 |
| `RateLimitError` / `429` | 短時間內呼叫太多次 | 等一下再試。 |
| `OverloadedError` / `529` | Anthropic 的伺服器暫時太忙 | 等幾秒鐘再試一次。 |
| `TypeError: ... got an unexpected keyword argument 'temperature'` | 你裝到新版（1.0 以後）的 SDK | 執行 `%pip install "anthropic<1"`，然後重新啟動核心。 |

---

## 📌 重點整理

- 需要安裝：**Python**、**VS Code（或 Jupyter）**、套件 **`anthropic<1`** 和 **`python-dotenv`**。
- notebook 用 **`Shift + Enter`** 執行，而且要**從上往下依序執行**。
- API 金鑰存在課程根目錄的 **`.env`** 檔案裡，**不要寫死在程式碼裡、不要外流**。
- 原課程的 Claude 3 模型都停用了，新手版已換成 **`claude-haiku-4-5`** 等模型；你跑出的結果會和課程顯示的不同，這是正常的。

👉 下一課：[0-4 Python 速成：只學課程會用到的](04_python_crash_course.md)
