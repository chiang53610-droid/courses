<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`01_Basic_Prompt_Structure.ipynb`](01_Basic_Prompt_Structure.ipynb)。

# 第 1 章：提示詞的基本結構

> 📚 **第 2 單元：提示詞工程互動教學**｜第 1 章 / 共 9 章（初級）
> ⏱️ 預估時間：30 分鐘

- [課程](#課程)
- [練習](#練習)
- [範例遊樂場](#範例遊樂場)

## 🎯 這一章你會學到

- 用 Messages API 呼叫 Claude 時，最少需要哪些參數
- 什麼樣的訊息格式是「正確的」、什麼樣的會出錯
- 什麼是**系統提示詞（system prompt）**，以及怎麼使用它

> 💡 如果你讀過第 1 單元的 [1-2 訊息格式](../01_api_fundamentals/02_messages_format.md) 和 [1-4 參數](../01_api_fundamentals/04_parameters.md)，這一章會覺得很熟悉，可以當作複習。

## 準備工作

執行下面這個準備格，載入你的 API 金鑰，並建立 `get_completion` 輔助函式。

```python
%pip install "anthropic<1"

# Import python's built-in regular expression library
import re
import anthropic

# Retrieve the API_KEY & MODEL_NAME variables from the IPython store
%store -r API_KEY
%store -r MODEL_NAME

client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt: str, system_prompt=""):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        system=system_prompt,
        messages=[
          {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text
```

**逐行解說：**
- `%pip install "anthropic<1"`：安裝套件（已經裝過的話會很快跳過）。
- `import re`：匯入 Python 內建的**正規表達式**工具，練習的自動批改會用到（[0-4 第 14 節](../00_before_you_start/04_python_crash_course.md#14-正規表達式-re在文字裡找東西)）。
- `%store -r API_KEY`、`%store -r MODEL_NAME`：把在[第 0 課](00_Tutorial_How-To.md)存起來的金鑰和模型名稱讀回來。
- `def get_completion(prompt: str, system_prompt=""):`：這一版的小幫手多了一個 `system_prompt` 參數（預設是空字串，也就是「沒有系統提示詞」）。
- `system=system_prompt`：把系統提示詞傳給 Claude。

> ⚠️ 如果出現 `NameError: name 'API_KEY' is not defined` 或金鑰相關錯誤，代表你還沒執行過[第 0 課](00_Tutorial_How-To.md)裡設定 `API_KEY` 的那一格。

---

## 課程

Anthropic 提供兩種 API：舊版的 [Text Completions API](https://docs.anthropic.com/claude/reference/complete_post) 和目前的 [Messages API](https://docs.anthropic.com/claude/reference/messages_post)。這個教學**只會使用 Messages API**。

使用 Messages API 呼叫 Claude 時，**最少**需要下面這些參數：
- **`model`**：你想呼叫的模型的 [API 模型名稱](https://docs.anthropic.com/claude/docs/models-overview#model-recommendations)。

- **`max_tokens`**：停止前最多產生多少個 token。注意：Claude 可能在達到這個上限之前就停下來。這個參數只是指定「最多」產生多少個 token。此外，這是一個**硬性**的停止，也就是說它可能讓 Claude 在一個字或一句話的中間就停下來。

- **`messages`**：輸入訊息的陣列（串列）。我們的模型被訓練成在「`user`（使用者）和 `assistant`（助理）輪流交替的對話回合」上運作。建立一則新的 `Message` 時，你用 `messages` 參數指定之前的對話回合，模型就會產生對話中的下一則 `Message`。
  - 每一則輸入訊息都必須是一個有 `role`（角色）和 `content`（內容）的物件。你可以只指定一則 `user` 角色的訊息，也可以包含多則 `user` 和 `assistant` 訊息（如果是這樣，它們必須輪流交替）。**第一則訊息一定要使用 `user` 角色。**

另外還有一些**選填**的參數，例如：
- **`system`**：系統提示詞——下面會詳細說明。

- **`temperature`**：Claude 回答的變化程度。在這些課程和練習中，我們把 `temperature` 設為 0。

完整的 API 參數清單，請參考我們的 [API 文件](https://docs.anthropic.com/claude/reference/messages_post)。

### 範例

我們來看看 Claude 對一些**格式正確**的提示詞會怎麼回應。下面每一格，執行它（`Shift + Enter`），Claude 的回答就會出現在格子下方。

```python
# Prompt
PROMPT = "Hi Claude, how are you?"

# Print Claude's response
print(get_completion(PROMPT))
```

（「嗨 Claude，你好嗎？」）

```python
# Prompt
PROMPT = "Can you tell me the color of the ocean?"

# Print Claude's response
print(get_completion(PROMPT))
```

（「你可以告訴我海洋是什麼顏色嗎？」）

```python
# Prompt
PROMPT = "What year was Celine Dion born in?"

# Print Claude's response
print(get_completion(PROMPT))
```

（「席琳·狄翁是哪一年出生的？」）

現在，我們來看一些**沒有**使用正確 Messages API 格式的提示詞。對於這些格式錯誤的提示詞，Messages API 會回傳錯誤。

首先，這是一個 `messages` 陣列裡**缺少 `role` 和 `content` 欄位**的 Messages API 呼叫範例。

```python
# Get Claude's response
response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=[
          {"Hi Claude, how are you?"}
        ]
    )

# Print Claude's response
print(response[0].text)
```

> 🧩 **白話小補充**：注意 `{"Hi Claude, how are you?"}`——大括號裡只有一段文字，沒有 `"role": ...` 和 `"content": ...`，所以它不是一則正確的訊息。執行這格**會出現錯誤，這是預期中的**，不用緊張！

下面是一個**沒有讓 `user` 和 `assistant` 角色輪流交替**的提示詞。

```python
# Get Claude's response
response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=[
          {"role": "user", "content": "What year was Celine Dion born in?"},
          {"role": "user", "content": "Also, can you tell me some other facts about her?"}
        ]
    )

# Print Claude's response
print(response[0].text)
```

> 🔄 **2026 更新**：這格原本是要示範「兩則 user 訊息連在一起會出錯」。現在的 API 可能會把連續的 user 訊息自動合併，所以 API 本身不一定報錯；但最後一行 `print(response[0].text)` 的寫法本身就是錯的（應該是 `response.content[0].text`），所以這格**一樣會出現錯誤**。重點是記住下面的規則。

`user` 和 `assistant` 訊息**必須輪流交替**，而且訊息**必須以 `user` 回合開始**。一個提示詞裡可以有好幾組 `user` & `assistant`（就像在模擬多回合的對話）。你也可以在**最後一則 `assistant` 訊息**裡先寫好一些字，讓 Claude 從你停下來的地方接著寫下去（之後的章節會詳細介紹）。

#### 系統提示詞（System Prompts）

你也可以使用**系統提示詞**。系統提示詞是一種在「User 回合」向 Claude 提出問題或任務**之前**，先**提供 Claude 背景、指示和準則**的方法。

在結構上，系統提示詞和 `user` & `assistant` 訊息串列是**分開**的，所以它屬於一個獨立的 `system` 參數（可以看看這份 notebook [準備工作](#準備工作)區塊裡 `get_completion` 輔助函式的結構）。

在這個教學中，只要是可能用到系統提示詞的地方，我們都已經在 completion 函式裡幫你準備好了 `system` 欄位。如果你不想使用系統提示詞，只要把 `SYSTEM_PROMPT` 變數設成空字串就好。

#### 系統提示詞範例

```python
# System prompt
SYSTEM_PROMPT = "Your answer should always be a series of critical thinking questions that further the conversation (do not provide answers to your questions). Do not actually answer the user question."

# Prompt
PROMPT = "Why is the sky blue?"

# Print Claude's response
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

**這個系統提示詞的意思是**：「你的回答永遠應該是一連串能推進對話的『批判性思考問題』（不要提供這些問題的答案）。不要真的回答使用者的問題。」
使用者問的是：「天空為什麼是藍色的？」——Claude 不會直接回答，而是反問你一連串引導思考的問題。

為什麼要使用系統提示詞？**寫得好的系統提示詞可以從很多方面提升 Claude 的表現**，例如讓 Claude 更能遵守規則和指示。想了解更多，請參考我們關於[如何在 Claude 上使用系統提示詞](https://docs.anthropic.com/claude/docs/how-to-use-system-prompts)的文件。

現在我們要開始做一些練習了。如果你想在**不改動上面任何內容**的情況下試玩課程中的提示詞，可以捲到這份 notebook 的最下面，前往[**範例遊樂場**](#範例遊樂場)。

---

## 練習
- [練習 1.1 - 數到三](#練習-11---數到三)
- [練習 1.2 - 系統提示詞](#練習-12---系統提示詞)

> 🧩 **練習怎麼做？**
> 1. 只修改程式碼裡標示「**this is the only field you should change**（這是你唯一應該修改的欄位）」的那個變數（把 `"[Replace this text]"` 換成你的提示詞）。
> 2. 執行那一格。下方會印出 Claude 的回答，以及一行 `This exercise has been correctly solved: True/False`（這個練習是否已正確解答：是/否）。
> 3. 看到 `True` 就代表過關！如果是 `False`，修改提示詞再試一次。
> 4. 卡住的話，執行下面的「提示」格，會印出中文提示。
>
> 自動批改是用正規表達式檢查 Claude 的回答裡有沒有特定的字，所以提示裡會告訴你「批改程式在找什麼」。

### 練習 1.1 - 數到三

使用正確的 `user` / `assistant` 格式，修改下面的 `PROMPT`，讓 Claude **數到三**。輸出結果也會顯示你的答案是否正確。

```python
# Prompt - this is the only field you should change
PROMPT = "[Replace this text]"

# Get Claude's response
response = get_completion(PROMPT)

# Function to grade exercise correctness
def grade_exercise(text):
    pattern = re.compile(r'^(?=.*1)(?=.*2)(?=.*3).*$', re.DOTALL)
    return bool(pattern.match(text))

# Print Claude's response and the corresponding grade
print(response)
print("\n--------------------------- GRADING ---------------------------")
print("This exercise has been correctly solved:", grade_exercise(response))
```

**批改程式在做什麼？** `grade_exercise` 用一個正規表達式檢查 Claude 的回答裡是不是**同時包含** `1`、`2`、`3` 這三個數字。

> 💡 提示詞可以用中文寫！例如 `PROMPT = "請從 1 數到 3"`。

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_1_1_hint; print(exercise_1_1_hint)
```

### 練習 1.2 - 系統提示詞

修改 `SYSTEM_PROMPT`，讓 Claude 用**像一個 3 歲小孩**的方式回答。

```python
# System prompt - this is the only field you should change
SYSTEM_PROMPT = "[Replace this text]"

# Prompt
PROMPT = "How big is the sky?"

# Get Claude's response
response = get_completion(PROMPT, SYSTEM_PROMPT)

# Function to grade exercise correctness
def grade_exercise(text):
    return bool(re.search(r"giggles", text) or re.search(r"soo", text))

# Print Claude's response and the corresponding grade
print(response)
print("\n--------------------------- GRADING ---------------------------")
print("This exercise has been correctly solved:", grade_exercise(response))
```

**批改程式在做什麼？** 檢查 Claude 的回答裡有沒有 `giggles`（咯咯笑）或 `soo`（例如 "sooo big" 這種小孩拉長音的說法）。
（使用者的問題是：「天空有多大？」）

> 💡 因為批改程式找的是英文字，這題的系統提示詞建議用英文寫，或者在中文提示詞裡要求 Claude 用英文回答。

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_1_2_hint; print(exercise_1_2_hint)
```

### 恭喜！

如果你已經解完到目前為止所有的練習，就可以前往下一章了。祝你寫提示詞愉快！

---

## 範例遊樂場

這是一個讓你**自由實驗**的區域，你可以試玩這一課中出現的提示詞範例，調整提示詞，看看會怎麼影響 Claude 的回答。

（下面的格子和課程中的範例一模一樣，隨便改、隨便玩，改壞了也沒關係。）

```python
# Prompt
PROMPT = "Hi Claude, how are you?"

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# Prompt
PROMPT = "Can you tell me the color of the ocean?"

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# Prompt
PROMPT = "What year was Celine Dion born in?"

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# Get Claude's response
response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=[
          {"Hi Claude, how are you?"}
        ]
    )

# Print Claude's response
print(response[0].text)
```

```python
# Get Claude's response
response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=[
          {"role": "user", "content": "What year was Celine Dion born in?"},
          {"role": "user", "content": "Also, can you tell me some other facts about her?"}
        ]
    )

# Print Claude's response
print(response[0].text)
```

```python
# System prompt
SYSTEM_PROMPT = "Your answer should always be a series of critical thinking questions that further the conversation (do not provide answers to your questions). Do not actually answer the user question."

# Prompt
PROMPT = "Why is the sky blue?"

# Print Claude's response
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

---

## 📌 重點整理

- Messages API 最少需要 **`model`**、**`max_tokens`**、**`messages`** 三個參數。
- 每則訊息都要有 **`role`** 和 **`content`**；**以 `user` 開頭**、**`user`/`assistant` 輪流交替**。
- **系統提示詞**放在獨立的 `system` 參數，用來在提問之前先給 Claude 背景、指示和準則；寫得好能提升 Claude 遵守規則的能力。
- 練習的做法：只改指定的變數 → 執行 → 看到 `True` 就過關。

👉 下一章：[第 2 章：清楚、直接](02_Being_Clear_and_Direct.md)
