<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`06_Precognition_Thinking_Step_by_Step.ipynb`](06_Precognition_Thinking_Step_by_Step.ipynb)。

# 第 6 章：預先思考——一步一步想（Precognition: Thinking Step by Step）

> 📚 **第 2 單元：提示詞工程互動教學**｜第 6 章 / 共 9 章（中級）
> ⏱️ 預估時間：45 分鐘

- [課程](#課程)
- [練習](#練習)
- [範例遊樂場](#範例遊樂場)

## 🎯 這一章你會學到

- 為什麼「讓 Claude 先思考再回答」可以提升準確度
- **思考一定要「說出來」才算數**
- 用 XML 標籤（例如 `<brainstorm>`）讓 Claude 把思考過程寫出來
- Claude 對**選項的順序**很敏感

> 🧩 **白話小補充**：「Precognition」原意是「預知」，這裡指的是「在回答之前先想清楚」。

## 準備工作

執行下面這個準備格，載入你的 API 金鑰，並建立 `get_completion` 輔助函式（和第 5 章一樣，有 `prefill` 參數）。

```python
%pip install "anthropic<1"

# Import python's built-in regular expression library
import re
import anthropic

# Retrieve the API_KEY & MODEL_NAME variables from the IPython store
%store -r API_KEY
%store -r MODEL_NAME

client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt: str, system_prompt="", prefill=""):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        system=system_prompt,
        messages=[
          {"role": "user", "content": prompt},
          {"role": "assistant", "content": prefill}
        ]
    )
    return message.content[0].text
```

---

## 課程

如果有人把你叫醒，然後立刻開始問你好幾個複雜的問題，而且你必須馬上回答，你會表現得怎麼樣？大概不會像「**先讓你好好想過答案**」的時候那麼好吧。

你猜怎麼著？Claude 也一樣。

**給 Claude 時間一步一步地思考，有時候能讓 Claude 更準確**，特別是對複雜的任務來說。不過，**思考只有在「說出來」的時候才算數**。你不能叫 Claude 思考、但只輸出答案——在這種情況下，實際上並沒有發生任何思考。

> 🧩 **白話小補充：為什麼思考一定要「說出來」？** 還記得 Claude 是「一個 token 接一個 token」產生文字的嗎？它寫下的每一個字，都會成為它寫下一個字的參考。所以把推理過程**寫出來**，就等於給自己打草稿，後面的答案就能根據草稿來寫。如果直接跳到答案，就沒有草稿可以參考了。

### 範例

在下面的提示詞裡，對人類讀者來說很清楚：第二句話推翻了第一句話。但是 **Claude 把「unrelated（不相關）」這個字理解得太字面了**。

```python
# Prompt
PROMPT = """Is this movie review sentiment positive or negative?

This movie blew my mind with its freshness and originality. In totally unrelated news, I have been living under a rock since the year 1900."""

# Print Claude's response
print(get_completion(PROMPT))
```

**題目翻譯**：「這篇影評的情緒是正面還是負面？
這部電影的新鮮感和原創性讓我大開眼界。另外，跟這完全不相關的消息是：我從 1900 年起就一直住在石頭底下。」

> 🧩 **白話小補充**：「living under a rock（住在石頭底下）」是英文俗語，意思是「與世隔絕、什麼都不知道」。從 1900 年起就與世隔絕的人，當然覺得什麼電影都很「新鮮」——所以這其實是一句**諷刺**，整體情緒是**負面**的。

為了改善 Claude 的回答，我們**讓 Claude 在回答之前先把事情想清楚**。做法是把 Claude 處理和思考這個任務應該採取的步驟，**一字一句地寫出來**。再加上一點點角色提示，就能讓 Claude 更深入地理解這篇影評。

```python
# System prompt
SYSTEM_PROMPT = "You are a savvy reader of movie reviews."

# Prompt
PROMPT = """Is this review sentiment positive or negative? First, write the best arguments for each side in <positive-argument> and <negative-argument> XML tags, then answer.

This movie blew my mind with its freshness and originality. In totally unrelated news, I have been living under a rock since 1900."""

# Print Claude's response
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

**提示詞翻譯**：
- 系統提示詞：「你是一位很會讀影評的精明讀者。」
- 使用者提示詞：「這篇影評的情緒是正面還是負面？**首先，把雙方最有力的論點分別寫在 `<positive-argument>`（正面論點）和 `<negative-argument>`（負面論點）XML 標籤裡，然後再回答。**」

**Claude 有時候對「順序」很敏感。** 這個例子已經接近 Claude 理解細膩文字能力的極限了。當我們把上一個例子中論點的順序對調——變成負面在前、正面在後——Claude 的整體判斷就變成了正面。

在大部分情況下（但不是全部，這點有點令人困惑），**Claude 比較傾向選擇兩個選項中的第二個**，可能是因為在它從網路上學到的訓練資料中，第二個選項比較常是正確的。

```python
# Prompt
PROMPT = """Is this review sentiment negative or positive? First write the best arguments for each side in <negative-argument> and <positive-argument> XML tags, then answer.

This movie blew my mind with its freshness and originality. Unrelatedly, I have been living under a rock since 1900."""

# Print Claude's response
print(get_completion(PROMPT))
```

（和上一個例子一樣，但問題改成「負面還是正面」，論點標籤的順序也改成 `<negative-argument>` 在前、`<positive-argument>` 在後。）

> 💡 **小提醒**：所以當你請 Claude 在選項之間做選擇時，可以試試看**對調選項的順序**，確認答案是否穩定。

**讓 Claude 思考，可以把 Claude 的答案從錯誤變成正確。** 在很多 Claude 犯錯的情況下，就是這麼簡單！

我們來看一個 Claude 答錯的例子，看看請 Claude 思考是怎麼修正錯誤的。

```python
# Prompt
PROMPT = "Name a famous movie starring an actor who was born in the year 1956."

# Print Claude's response
print(get_completion(PROMPT))
```

（「說出一部由 1956 年出生的演員主演的知名電影。」）

我們來修正這個問題：請 Claude 一步一步思考，這次用 `<brainstorm>` 標籤。

```python
# Prompt
PROMPT = "Name a famous movie starring an actor who was born in the year 1956. First brainstorm about some actors and their birth years in <brainstorm> tags, then give your answer."

# Print Claude's response
print(get_completion(PROMPT))
```

（「說出一部由 1956 年出生的演員主演的知名電影。**先在 `<brainstorm>`（腦力激盪）標籤裡，想一想一些演員和他們的出生年份**，然後再給出你的答案。」）

> 🧩 **白話小補充**：先列出「演員 + 出生年份」，再從裡面挑出 1956 年出生的（例如湯姆·漢克斯 Tom Hanks 就是 1956 年出生），答案自然就準確多了。
>
> 🔄 **2026 更新**：新一代模型內建了「延伸思考（extended thinking）」功能，可以在給出答案前先在內部思考。不過「在提示詞裡請它把思考過程寫在標籤裡」這個技巧，在任何模型上都適用，而且能讓**你**看到它的推理過程。

如果你想在不改動上面任何內容的情況下試玩課程中的提示詞，可以捲到這份 notebook 的最下面，前往[**範例遊樂場**](#範例遊樂場)。

---

## 練習
- [練習 6.1 - 分類電子郵件](#練習-61---分類電子郵件)
- [練習 6.2 - 電子郵件分類的格式](#練習-62---電子郵件分類的格式)

### 練習 6.1 - 分類電子郵件

在這個練習中，我們要請 Claude 把電子郵件分到下面這些類別：
- (A) Pre-sale question（售前問題）
- (B) Broken or defective item（商品損壞或有瑕疵）
- (C) Billing question（帳務問題）
- (D) Other (please explain)（其他，請說明）

練習的第一部分：修改 `PROMPT`，**讓 Claude 輸出正確的分類，而且只輸出分類**。你的答案需要**包含正確選項的字母（A～D）和括號，以及類別的名稱**。

每封信屬於哪個類別，請參考 `EMAILS` 串列裡每封信旁邊的註解。

```python
# Prompt template with a placeholder for the variable content
PROMPT = """Please classify this email as either green or blue: {email}"""

# Prefill for Claude's response, if any
PREFILL = ""

# Variable content stored as a list
EMAILS = [
    "Hi -- My Mixmaster4000 is producing a strange noise when I operate it. It also smells a bit smoky and plasticky, like burning electronics.  I need a replacement.", # (B) Broken or defective item
    "Can I use my Mixmaster 4000 to mix paint, or is it only meant for mixing food?", # (A) Pre-sale question OR (D) Other (please explain)
    "I HAVE BEEN WAITING 4 MONTHS FOR MY MONTHLY CHARGES TO END AFTER CANCELLING!!  WTF IS GOING ON???", # (C) Billing question
    "How did I get here I am not good with computer.  Halp." # (D) Other (please explain)
]

# Correct categorizations stored as a list of lists to accommodate the possibility of multiple correct categorizations per email
ANSWERS = [
    ["B"],
    ["A","D"],
    ["C"],
    ["D"]
]

# Dictionary of string values for each category to be used for regex grading
REGEX_CATEGORIES = {
    "A": "A\) P",
    "B": "B\) B",
    "C": "C\) B",
    "D": "D\) O"
}

# Iterate through list of emails
for i,email in enumerate(EMAILS):
    
    # Substitute the email text into the email placeholder variable
    formatted_prompt = PROMPT.format(email=email)
   
    # Get Claude's response
    response = get_completion(formatted_prompt, prefill=PREFILL)

    # Grade Claude's response
    grade = any([bool(re.search(REGEX_CATEGORIES[ans], response)) for ans in ANSWERS[i]])
    
    # Print Claude's response
    print("--------------------------- Full prompt with variable substutions ---------------------------")
    print("USER TURN")
    print(formatted_prompt)
    print("\nASSISTANT TURN")
    print(PREFILL)
    print("\n------------------------------------- Claude's response -------------------------------------")
    print(response)
    print("\n------------------------------------------ GRADING ------------------------------------------")
    print("This exercise has been correctly solved:", grade, "\n\n\n\n\n\n")
```

**這段程式碼在做什麼？（逐段解說）**
- `PROMPT = """...{email}"""`：提示詞範本。**目前的內容是故意寫錯的**（「請把這封信分類成綠色或藍色」），你要把它改掉。注意 `{email}` 是佔位符，但這裡**沒有**在字串前面加 `f`，因為等一下會用 `.format()` 替換（[第 4 章](04_Separating_Data_and_Instructions.md)提過）。
- `PREFILL = ""`：如果想幫 Claude 開口，可以寫在這裡。
- `EMAILS = [...]`：4 封測試用的信（中文意思）：
  1. 「嗨——我的 Mixmaster4000 運轉時發出奇怪的聲音，還有一點煙味和塑膠味，像是電子零件燒焦了。我需要換一台。」→ 正確答案 (B)
  2. 「我可以用 Mixmaster 4000 攪拌油漆嗎？還是它只能用來攪拌食物？」→ (A) 或 (D) 都算對
  3. 「我取消之後已經等了 4 個月，每月扣款還是沒停！！到底怎麼回事？？？」→ (C)
  4. 「我怎麼會在這裡 我不太會用電腦。救命。」→ (D)
- `ANSWERS = [...]`：每封信的正確答案（用串列，因為有的信不只一個正確答案）。
- `REGEX_CATEGORIES = {...}`：批改用的規則。例如 `"B": "B\) B"` 代表回答裡要出現 `B) B`（字母 B + 右括號 + 空格 + 類別名稱的開頭 B，也就是 "B) Broken..."）。`\)` 的 `\` 是因為括號在正規表達式裡有特殊意義，要加 `\` 表示「真的括號字元」。
- `for i, email in enumerate(EMAILS):`：`enumerate` 會同時給你「編號 i」和「內容 email」，讓 4 封信一封一封跑。
  - `PROMPT.format(email=email)`：把信件內容填進範本。
  - `any([...])`：只要符合其中**任何一個**正確答案就算對。

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_6_1_hint; print(exercise_6_1_hint)
```

還是卡住了嗎？執行下面這格，看一個參考答案。

```python
from hints import exercise_6_1_solution; print(exercise_6_1_solution)
```

### 練習 6.2 - 電子郵件分類的格式

在這個練習中，我們要改良上面那個提示詞的輸出，讓答案的格式**完全**符合我們的要求。

用你最喜歡的輸出格式技巧，讓 Claude **只**把正確分類的**字母**包在 `<answer></answer>` 標籤裡。例如，第一封信的答案裡應該要有一模一樣的字串 `<answer>B</answer>`。

如果你忘了每封信正確的分類字母是什麼，請參考 `EMAILS` 串列裡每封信旁邊的註解。

```python
# Prompt template with a placeholder for the variable content
PROMPT = """Please classify this email as either green or blue: {email}"""

# Prefill for Claude's response, if any
PREFILL = ""

# Variable content stored as a list
EMAILS = [
    "Hi -- My Mixmaster4000 is producing a strange noise when I operate it. It also smells a bit smoky and plasticky, like burning electronics.  I need a replacement.", # (B) Broken or defective item
    "Can I use my Mixmaster 4000 to mix paint, or is it only meant for mixing food?", # (A) Pre-sale question OR (D) Other (please explain)
    "I HAVE BEEN WAITING 4 MONTHS FOR MY MONTHLY CHARGES TO END AFTER CANCELLING!!  WTF IS GOING ON???", # (C) Billing question
    "How did I get here I am not good with computer.  Halp." # (D) Other (please explain)
]

# Correct categorizations stored as a list of lists to accommodate the possibility of multiple correct categorizations per email
ANSWERS = [
    ["B"],
    ["A","D"],
    ["C"],
    ["D"]
]

# Dictionary of string values for each category to be used for regex grading
REGEX_CATEGORIES = {
    "A": "<answer>A</answer>",
    "B": "<answer>B</answer>",
    "C": "<answer>C</answer>",
    "D": "<answer>D</answer>"
}

# Iterate through list of emails
for i,email in enumerate(EMAILS):
    
    # Substitute the email text into the email placeholder variable
    formatted_prompt = PROMPT.format(email=email)
   
    # Get Claude's response
    response = get_completion(formatted_prompt, prefill=PREFILL)

    # Grade Claude's response
    grade = any([bool(re.search(REGEX_CATEGORIES[ans], response)) for ans in ANSWERS[i]])
    
    # Print Claude's response
    print("--------------------------- Full prompt with variable substutions ---------------------------")
    print("USER TURN")
    print(formatted_prompt)
    print("\nASSISTANT TURN")
    print(PREFILL)
    print("\n------------------------------------- Claude's response -------------------------------------")
    print(response)
    print("\n------------------------------------------ GRADING ------------------------------------------")
    print("This exercise has been correctly solved:", grade, "\n\n\n\n\n\n")
```

**批改程式在做什麼？** 這次的規則改成檢查回答裡有沒有 `<answer>B</answer>` 這樣的字串（其他部分和上一題一樣）。

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_6_2_hint; print(exercise_6_2_hint)
```

### 恭喜！

如果你已經解完到目前為止所有的練習，就可以前往下一章了。祝你寫提示詞愉快！

---

## 範例遊樂場

這是一個讓你**自由實驗**的區域，你可以試玩這一課中出現的提示詞範例，調整提示詞，看看會怎麼影響 Claude 的回答。

```python
# Prompt
PROMPT = """Is this movie review sentiment positive or negative?

This movie blew my mind with its freshness and originality. In totally unrelated news, I have been living under a rock since the year 1900."""

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# System prompt
SYSTEM_PROMPT = "You are a savvy reader of movie reviews."

# Prompt
PROMPT = """Is this review sentiment positive or negative? First, write the best arguments for each side in <positive-argument> and <negative-argument> XML tags, then answer.

This movie blew my mind with its freshness and originality. In totally unrelated news, I have been living under a rock since 1900."""

# Print Claude's response
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

```python
# Prompt
PROMPT = """Is this review sentiment negative or positive? First write the best arguments for each side in <negative-argument> and <positive-argument> XML tags, then answer.

This movie blew my mind with its freshness and originality. Unrelatedly, I have been living under a rock since 1900."""

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# Prompt
PROMPT = "Name a famous movie starring an actor who was born in the year 1956."

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# Prompt
PROMPT = "Name a famous movie starring an actor who was born in the year 1956. First brainstorm about some actors and their birth years in <brainstorm> tags, then give your answer."

# Print Claude's response
print(get_completion(PROMPT))
```

---

## 📌 重點整理

- **讓 Claude 先思考再回答**，複雜任務的準確度會提升。
- **思考要「說出來」才算數**：請 Claude 把推理寫在標籤裡（例如 `<brainstorm>`、`<thinking>`、`<positive-argument>`），再給答案。
- 可以**明確列出思考步驟**（「先寫出雙方論點，再回答」），再搭配角色提示。
- Claude 對**選項順序**敏感，常傾向選第二個；重要的判斷可以對調順序檢查。

👉 下一章：[第 7 章：使用範例](07_Using_Examples_Few-Shot_Prompting.md)
