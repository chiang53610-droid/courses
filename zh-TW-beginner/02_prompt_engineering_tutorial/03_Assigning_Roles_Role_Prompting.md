<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`03_Assigning_Roles_Role_Prompting.ipynb`](03_Assigning_Roles_Role_Prompting.ipynb)。

# 第 3 章：指定角色（Role Prompting 角色提示）

> 📚 **第 2 單元：提示詞工程互動教學**｜第 3 章 / 共 9 章（初級）
> ⏱️ 預估時間：25 分鐘

- [課程](#課程)
- [練習](#練習)
- [範例遊樂場](#範例遊樂場)

## 🎯 這一章你會學到

- 什麼是「角色提示（role prompting）」
- 指定角色如何改變 Claude 回答的**語氣、風格和內容**
- 指定角色也能讓 Claude **更擅長數學和邏輯題**

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

---

## 課程

延續「除了你說的話以外，Claude 沒有任何背景資訊」這個主題：有時候，**請 Claude 扮演一個特定的角色（並提供所有必要的背景資訊）**是很重要的。這就叫做**角色提示（role prompting）**。角色的背景描述得越詳細越好。

**先給 Claude 一個角色，可以提升 Claude 在各種領域的表現**，從寫作、寫程式到摘要都是。這就像有時候告訴人「用＿＿＿＿的角度想一想」，會對他們有幫助一樣。角色提示也可以改變 Claude 回答的風格、語氣和方式。

**注意：** 角色提示可以寫在**系統提示詞**裡，也可以寫在 **User 訊息回合**裡。

> 🧩 **白話小補充**：就像你請朋友幫忙看合約，說「你現在是一位資深律師」，他就會用更專業、更謹慎的角度去看。Claude 也一樣，給它一個角色，它就會「進入狀況」。

### 範例

在下面的例子中，可以看到：**沒有**角色提示的時候，請 Claude 用一句話說說它對滑板的看法，Claude 給出的是一個**直接、沒有特別風格**的回答。

但當我們先讓 Claude 扮演**一隻貓**，Claude 的觀點就改變了，因此 **Claude 回答的語氣、風格和內容，都會配合新的角色而調整**。

**注意：** 你還可以使用一個加分技巧：**告訴 Claude 它的目標聽眾是誰**。在下面的例子中，我們也可以調整提示詞，告訴 Claude 它在跟誰說話。「你是一隻貓」和「你是一隻正在對一群玩滑板的人說話的貓」，會產生相當不同的回答。

下面是系統提示詞裡**沒有**角色提示的提示詞：

```python
# Prompt
PROMPT = "In one sentence, what do you think about skateboarding?"

# Print Claude's response
print(get_completion(PROMPT))
```

（「用一句話說說，你覺得滑板怎麼樣？」）

下面是同樣的使用者問題，但**加上了角色提示**：

```python
# System prompt
SYSTEM_PROMPT = "You are a cat."

# Prompt
PROMPT = "In one sentence, what do you think about skateboarding?"

# Print Claude's response
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

（系統提示詞：「你是一隻貓。」）

你可以用角色提示讓 Claude 模仿某種寫作風格、用某種口吻說話，或是引導它回答的複雜程度。**角色提示也可以讓 Claude 更擅長做數學或邏輯任務。**

例如，在下面的例子中，有一個明確的正確答案：「是」。但是 Claude 答錯了，它以為資訊不足，但其實資訊是足夠的：

```python
# Prompt
PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don’t know if Anne is married. Is a married person looking at an unmarried person?"

# Print Claude's response
print(get_completion(PROMPT))
```

**題目翻譯**：「傑克在看安妮。安妮在看喬治。傑克已婚，喬治未婚，我們不知道安妮是否已婚。請問：是否有一位已婚的人正在看著一位未婚的人？」

> 🧩 **白話小補充：為什麼答案是「是」？** 分兩種情況想：
> - 如果安妮**已婚** → 安妮（已婚）在看喬治（未婚）→ 是。
> - 如果安妮**未婚** → 傑克（已婚）在看安妮（未婚）→ 是。
>
> 不管哪種情況，答案都是「是」，所以其實不需要知道安妮是否已婚。

那如果我們**先讓 Claude 扮演一個邏輯機器人**呢？這會怎麼改變 Claude 的答案？

結果是：有了這個新的角色設定，Claude 答對了。（不過值得注意的是，它的理由並不完全正確。）

```python
# System prompt
SYSTEM_PROMPT = "You are a logic bot designed to answer complex logic problems."

# Prompt
PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don’t know if Anne is married. Is a married person looking at an unmarried person?"

# Print Claude's response
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

（系統提示詞：「你是一個專門用來回答複雜邏輯問題的邏輯機器人。」）

> 🔄 **2026 更新**：新手版使用的 Claude Haiku 4.5 比原課程的 Claude 3 Haiku 聰明很多，所以你自己跑的時候，**很可能不用角色提示也答對了**。這不影響本章的重點：角色提示是一個能提升表現的好工具，在更難的題目上效果會更明顯。

**注意：** 在這門課裡你會學到，**有很多不同的提示詞工程技巧都能達到類似的效果**。要用哪一種技巧，取決於你和你的偏好！我們鼓勵你**多多實驗，找出你自己的提示詞工程風格**。

如果你想在不改動上面任何內容的情況下試玩課程中的提示詞，可以捲到這份 notebook 的最下面，前往[**範例遊樂場**](#範例遊樂場)。

---

## 練習
- [練習 3.1 - 數學批改](#練習-31---數學批改)

### 練習 3.1 - 數學批改

在某些情況下，**Claude 可能會在數學上出錯**，就算是很簡單的數學也一樣。在下面的例子中，Claude 錯誤地判斷這道數學題「解對了」，但其實第二步有一個很明顯的計算錯誤。注意：Claude 在一步一步檢查的時候其實**有發現**這個錯誤，但卻沒有因此得出「整個解答是錯的」這個結論。

修改 `PROMPT` 和／或 `SYSTEM_PROMPT`，讓 Claude 判定這個解答是**錯誤的（incorrectly solved）**，而不是正確的。

```python
# System prompt - if you don't want to use a system prompt, you can leave this variable set to an empty string
SYSTEM_PROMPT = ""

# Prompt
PROMPT = """Is this equation solved correctly below?

2x - 3 = 9
2x = 6
x = 3"""

# Get Claude's response
response = get_completion(PROMPT, SYSTEM_PROMPT)

# Function to grade exercise correctness
def grade_exercise(text):
    if "incorrect" in text or "not correct" in text.lower():
        return True
    else:
        return False

# Print Claude's response and the corresponding grade
print(response)
print("\n--------------------------- GRADING ---------------------------")
print("This exercise has been correctly solved:", grade_exercise(response))
```

**題目翻譯**：「下面這個方程式解對了嗎？ 2x - 3 = 9 → 2x = 6 → x = 3」
（錯在第二步：兩邊加 3 應該得到 2x = **12**，所以 x = 6。）

**批改程式在做什麼？** 檢查回答裡有沒有 `incorrect`（不正確）或 `not correct`（不正確）。

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_3_1_hint; print(exercise_3_1_hint)
```

### 恭喜！

如果你已經解完到目前為止所有的練習，就可以前往下一章了。祝你寫提示詞愉快！

---

## 範例遊樂場

這是一個讓你**自由實驗**的區域，你可以試玩這一課中出現的提示詞範例，調整提示詞，看看會怎麼影響 Claude 的回答。

```python
# Prompt
PROMPT = "In one sentence, what do you think about skateboarding?"

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# System prompt
SYSTEM_PROMPT = "You are a cat."

# Prompt
PROMPT = "In one sentence, what do you think about skateboarding?"

# Print Claude's response
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

```python
# Prompt
PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don’t know if Anne is married. Is a married person looking at an unmarried person?"

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# System prompt
SYSTEM_PROMPT = "You are a logic bot designed to answer complex logic problems."

# Prompt
PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don’t know if Anne is married. Is a married person looking at an unmarried person?"

# Print Claude's response
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

---

## 📌 重點整理

- **角色提示**：請 Claude 扮演某個角色（例如「你是一隻貓」、「你是邏輯機器人」、「你是資深律師」），角色描述越詳細越好。
- 角色可以寫在**系統提示詞**或 **user 訊息**裡。
- 角色會改變回答的**語氣、風格、內容**，也能提升**數學、邏輯**等任務的表現。
- 加分技巧：告訴 Claude **它在對誰說話**（目標聽眾）。
- 很多技巧都能達到類似效果，多實驗、找出自己的風格。

👉 下一章：[第 4 章：把資料和指示分開](04_Separating_Data_and_Instructions.md)
