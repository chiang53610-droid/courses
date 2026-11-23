<!--meta {"orig": "prompt_engineering_interactive_tutorial/Anthropic 1P/00_Tutorial_How-To.ipynb", "out": "02_prompt_engineering_tutorial/00_Tutorial_How-To"} -->
# 第 2 單元：提示詞工程互動教學

## 單元介紹（原課程 README 翻譯）

### 課程簡介與目標

這門課的目的，是讓你**一步一步、全面地了解**怎麼在 Claude 上設計出最好的提示詞（prompt）。

**完成這門課之後，你將能夠：**
- 掌握一個好提示詞的基本結構
- 認出常見的失敗情況，並學會用「80/20」的技巧解決它們
- 了解 Claude 的強項和弱點
- 從零開始，為常見的使用情境寫出強大的提示詞

> 🧩 **白話小補充**：「80/20 技巧」是指「花 20% 的力氣，就能解決 80% 問題」的關鍵技巧。

### 課程結構與內容

這門課的設計，是讓你有**很多機會自己動手**寫提示詞、修正提示詞。整門課分成 **9 章，每章都附有練習**，另外還有一個收錄更進階方法的附錄。建議你**照章節順序**學習。

**每一課的最下面都有一個「範例遊樂場（Example Playground）」區域**，你可以在那裡自由地試玩課程中的範例，親自體驗「改變提示詞會怎麼改變 Claude 的回答」。原課程另外還提供了一份[參考答案](https://docs.google.com/spreadsheets/d/1jIxjzUWG-6xBVIa2ay6yDpLyeuOh_hR_ZB75a47KX_E/edit?usp=sharing)（Google 試算表，英文）。

注意：這個教學使用的是我們最小、最快、最便宜的模型 Claude 3 Haiku。Anthropic 還有[另外兩個模型](https://docs.anthropic.com/claude/docs/models-overview)：Claude 3 Sonnet 和 Claude 3 Opus，它們比 Haiku 聰明，其中 Opus 最聰明。

*這個教學也有 [Google 試算表版本](https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8/edit?usp=sharing)，使用 Anthropic 的「Claude for Sheets」擴充功能。原課程推薦使用那個版本，因為對使用者比較友善。*

> 🔄 **2026 更新**：Claude 3 Haiku 已停用，新手版換成 **`claude-haiku-4-5`**。它支援本單元會大量使用的「預先填寫 Claude 的回答（prefill）」技巧和 `temperature` 參數，所以所有練習都能照原樣進行。

### 目錄

每一章都包含一堂課和一組練習。

**初級**
- [第 1 章：提示詞的基本結構](01_Basic_Prompt_Structure.md)
- [第 2 章：清楚、直接](02_Being_Clear_and_Direct.md)
- [第 3 章：指定角色](03_Assigning_Roles_Role_Prompting.md)

**中級**
- [第 4 章：把資料和指示分開](04_Separating_Data_and_Instructions.md)
- [第 5 章：格式化輸出 & 幫 Claude 開口](05_Formatting_Output_and_Speaking_for_Claude.md)
- [第 6 章：預先思考（一步一步想）](06_Precognition_Thinking_Step_by_Step.md)
- [第 7 章：使用範例](07_Using_Examples_Few-Shot_Prompting.md)

**進階**
- [第 8 章：避免幻覺](08_Avoiding_Hallucinations.md)
- [第 9 章：從零打造複雜的提示詞（產業使用案例）](09_Complex_Prompts_from_Scratch.md)
  - 從零打造複雜提示詞：聊天機器人
  - 法律服務的複雜提示詞
  - 練習：財務服務的複雜提示詞
  - 練習：程式設計的複雜提示詞
  - 恭喜 & 下一步

**附錄：超越標準提示詞**
- [附錄 10.1：串連提示詞（Chaining Prompts）](10_1_Appendix_Chaining_Prompts.md)
- [附錄 10.2：工具使用（Tool Use）](10_2_Appendix_Tool_Use.md)
- [附錄 10.3：搜尋與檢索（Search & Retrieval）](10_3_Appendix_Search_and_Retrieval.md)
- [附錄 10.4（加碼，原本只在 Bedrock 版）：實證效能評估](10_4_Appendix_Empirical_Performance_Evaluations.md)

> 💡 **關於 Amazon Bedrock 版本**：原課程資料夾裡還有一個 `AmazonBedrock` 版本，內容和這裡（`Anthropic 1P` 版）幾乎一樣，差別只在於「怎麼連線到 Claude」（透過 AWS 的 Bedrock 服務，而不是直接用 Anthropic 的 API 金鑰）。新手版以 `Anthropic 1P` 版為準，Bedrock 版的差異整理在[這份說明](bedrock_version_notes.md)裡。

---

# 教學使用說明（Tutorial How-To）

> 📚 **第 2 單元：提示詞工程互動教學**｜第 0 課：使用說明
> ⏱️ 預估時間：10 分鐘

這個教學**需要 API 金鑰**才能互動。如果你還沒有 API 金鑰，可以到 [Anthropic Console（主控台）](https://console.anthropic.com/) 註冊申請，或者改看原課程的[靜態參考答案](https://docs.google.com/spreadsheets/u/0/d/1jIxjzUWG-6xBVIa2ay6yDpLyeuOh_hR_ZB75a47KX_E/edit)。

## 如何開始

1. 把這個 repository（課程檔案）下載到你的電腦。（方法請見 [0-3 準備你的電腦](../00_before_you_start/03_setup_your_computer.md#步驟-3下載課程檔案)。）

2. 執行下面的指令，安裝需要的套件：

{{cell 2}}

3. 設定你的 API 金鑰和模型名稱。

原課程的寫法是直接把金鑰寫在程式碼裡（把 `"your_api_key_here"` 換成你自己的 Anthropic API 金鑰）：

```python
API_KEY = "your_api_key_here"
MODEL_NAME = "claude-3-haiku-20240307"

# Stores the API_KEY & MODEL_NAME variables for use across notebooks within the IPython store
%store API_KEY
%store MODEL_NAME
```

新手版建議改用下面這個寫法：**從 `.env` 檔讀取金鑰**（你在 [0-3 步驟 6](../00_before_you_start/03_setup_your_computer.md#步驟-6把-api-金鑰安全地存起來env-檔) 已經建立好了），這樣金鑰就不會出現在程式碼裡：

```python run
from dotenv import load_dotenv
import os

load_dotenv()                                  # 讀取 .env 檔
API_KEY = os.getenv("ANTHROPIC_API_KEY")       # 從 .env 拿到 API 金鑰
# 如果你沒有 .env 檔，也可以把上一行改成：API_KEY = "your_api_key_here"（填入你的金鑰）
MODEL_NAME = "claude-haiku-4-5"                # 原課程是 "claude-3-haiku-20240307"（已停用）

# 把 API_KEY 和 MODEL_NAME 這兩個變數存進 IPython 的儲存區，讓其他 notebook 也能使用
%store API_KEY
%store MODEL_NAME
```

**逐行解說：**
- `API_KEY = os.getenv("ANTHROPIC_API_KEY")`：從環境變數（`.env` 讀進來的）拿到金鑰。
- `MODEL_NAME = "claude-haiku-4-5"`：整個單元都會用這個模型。
- `%store API_KEY`、`%store MODEL_NAME`：這是 notebook 的「魔法指令」，把這兩個變數**存起來**。之後每一章的 notebook 開頭都會用 `%store -r API_KEY` 把它們**讀回來**（`-r` = read）。這樣你只要在這裡設定一次就好。（詳見 [0-4 第 16-5 節](../00_before_you_start/04_python_crash_course.md#16-5-storenotebook-專用)）

> ⚠️ **注意**：
> - **這一格一定要執行！** 否則後面每一章都會出現「找不到 API_KEY」的錯誤。
> - `%store` 會把金鑰存在你電腦裡 IPython 的設定資料夾中（明文）。在自己的電腦上沒問題，但不要在公用電腦上這樣做。

4. 依照說明，**按順序**執行 notebook 的各個格子。

---

## 使用注意事項與小技巧 💡

- 這門課使用 Claude 3 Haiku，並把 temperature 設為 0。我們會在課程後面詳細討論 temperature。現在只要知道：這樣的設定會讓結果比較穩定、比較一致就好。這門課所有的提示詞工程技巧，也同樣適用於上一代的舊版 Claude 模型，例如 Claude 2 和 Claude Instant 1.2。
  - 🔄 新手版改用 Claude Haiku 4.5，一樣設定 temperature 為 0。這些技巧也同樣適用於更新的模型。

- 你可以按 **`Shift + Enter`** 執行目前這一格，並移到下一格。

- 讀到一個教學頁面的最下面時，請前往資料夾裡下一個編號的檔案；如果這一章的內容都讀完了，就前往下一個編號的章節。

### Anthropic SDK 與 Messages API

這個教學全程會使用 [Anthropic Python SDK](https://docs.anthropic.com/claude/reference/client-sdks) 和 [Messages API](https://docs.anthropic.com/claude/reference/messages_post)。

下面示範在這個教學中執行一個提示詞會是什麼樣子。首先，我們建立 **`get_completion`**，它是一個**輔助函式**：把提示詞傳給 Claude，並回傳 Claude 產生的回答。現在就執行那一格吧。

{{cell 7}}

**逐行解說：**
- `import anthropic`：匯入 anthropic 套件。
- `client = anthropic.Anthropic(api_key=API_KEY)`：用你的金鑰建立客戶端。（這跟第 1 單元的 `from anthropic import Anthropic` + `Anthropic()` 是一樣的意思，只是寫法不同。）
- `def get_completion(prompt: str):`：定義一個函式，參數是 `prompt`。`: str` 是「型別提示」，說明 `prompt` 應該是字串，只是給人看的說明，不影響執行。
- `client.messages.create(...)`：送出請求。`temperature=0.0` 讓回答比較穩定。
- `return message.content[0].text`：把 Claude 的回答文字交回去。

> 🧩 **白話小補充**：有了 `get_completion` 這個「小幫手」，之後每次只要寫 `get_completion("你的提示詞")` 就能得到 Claude 的回答，不用每次都寫一大串 `client.messages.create(...)`。整個單元都會一直用到它。

現在，我們寫一個範例提示詞給 Claude，並執行 `get_completion` 輔助函式印出 Claude 的輸出。執行下面這格，Claude 的回答就會印在它的下方。

你可以隨意修改提示詞字串，看看 Claude 會怎麼回應。

{{cell 9}}

（試著把 `"Hello, Claude!"` 改成中文，例如 `"你好，Claude！請自我介紹。"`）

前面定義的 `API_KEY` 和 `MODEL_NAME` 變數會在整個教學中使用。只要記得：每一個教學頁面都要**從上到下**執行各個格子。

---

## 📌 重點整理

- 這個單元共 9 章 + 附錄，每章有**課程、練習、範例遊樂場**三部分。
- 先在這一頁設定 `API_KEY` 和 `MODEL_NAME`，用 `%store` 存起來；之後每章開頭用 `%store -r` 讀回來。
- `get_completion(prompt)` 是整個單元會一直用到的小幫手函式。
- 練習有自動批改，卡住時可以執行「提示（hint）」格子。

👉 下一章：[第 1 章：提示詞的基本結構](01_Basic_Prompt_Structure.md)
