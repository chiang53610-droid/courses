<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`04_Separating_Data_and_Instructions.ipynb`](04_Separating_Data_and_Instructions.ipynb)。

# 第 4 章：把資料和指示分開（Separating Data and Instructions）

> 📚 **第 2 單元：提示詞工程互動教學**｜第 4 章 / 共 9 章（中級）
> ⏱️ 預估時間：40 分鐘
> 🧰 先備知識：[0-4 第 3-2 節 f-string](../00_before_you_start/04_python_crash_course.md#3-2-f-string把變數塞進文字裡)

- [課程](#課程)
- [練習](#練習)
- [範例遊樂場](#範例遊樂場)

## 🎯 這一章你會學到

- 什麼是**提示詞範本（prompt template）**：固定的骨架 + 可替換的資料
- 用 f-string 把資料「塞進」範本裡
- 用 **XML 標籤**清楚標出「資料從哪裡開始、到哪裡結束」
- 為什麼**小細節（錯字、格式）很重要**

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

很多時候，我們並不想每次都寫一份完整的提示詞，而是想要一個**提示詞範本**：在送給 Claude 之前，**可以再填入額外的輸入資料**。如果你希望 Claude 每次都做同一件事，但每次 Claude 處理的資料可能都不一樣，這個方法就很好用。

幸好，這件事做起來很簡單：**把提示詞固定不變的「骨架」和會變動的「使用者輸入」分開，然後把使用者輸入替換進提示詞裡**，再把完整的提示詞送給 Claude。

下面我們會一步一步示範：怎麼寫一個可以替換內容的提示詞範本，以及怎麼把使用者輸入替換進去。

> 🧩 **白話小補充**：提示詞範本就像「填空題考卷」或「制式表格」：題目（指示）是固定的，空格（資料）每次填不同的內容。例如「請幫我把下面這封信改得更有禮貌：＿＿＿＿」，空格裡每次放不同的信。

### 範例

在第一個例子中，我們請 Claude 扮演一個「動物叫聲產生器」。注意看：送給 Claude 的完整提示詞，就只是把輸入（這裡是「Cow」，牛）替換進 `PROMPT_TEMPLATE`（提示詞範本）之後的結果。當我們印出完整的提示詞時，可以看到「Cow」這個字透過 f-string 取代了 `ANIMAL` 這個佔位符。

**注意：** 實際使用時，你的佔位符變數不一定要取什麼特定的名字。這個例子裡我們叫它 `ANIMAL`，但也可以很簡單地叫它 `CREATURE` 或 `A`（不過一般來說，變數名稱最好取得具體、相關，這樣就算還沒替換，提示詞範本也很容易看懂，方便人閱讀）。只要確保你在提示詞範本的 f-string 裡用的，就是你取的那個變數名稱就好。

```python
# Variable content
ANIMAL = "Cow"

# Prompt template with a placeholder for the variable content
PROMPT = f"I will tell you the name of an animal. Please respond with the noise that animal makes. {ANIMAL}"

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

**逐行解說：**
- `ANIMAL = "Cow"`：要替換進去的資料。
- `PROMPT = f"... {ANIMAL}"`：提示詞範本，意思是「我會告訴你一種動物的名字，請回答那種動物發出的叫聲。{ANIMAL}」。前面的 `f` 讓 `{ANIMAL}` 被換成 `Cow`。
- 程式先印出「替換變數後的完整提示詞」，再印出「Claude 的回答」，方便你對照。

為什麼我們要像這樣把輸入分開、再替換進去呢？因為**提示詞範本可以簡化重複性的工作**。假設你做了一個提示詞結構，開放給「第三方使用者」提交內容到提示詞裡（在這個例子中，就是他們想產生叫聲的動物）。這些第三方使用者不需要寫、甚至不需要看到完整的提示詞，他們只要填入變數就好。

這裡我們用變數和 f-string 來做替換，但你也可以用 `format()` 方法來做。

**注意：** 提示詞範本裡的變數想要幾個就可以有幾個！

> 🧩 **`format()` 是什麼？** 另一種把變數塞進字串的寫法：
> ```python
> template = "請回答 {animal} 的叫聲"
> prompt = template.format(animal="Cow")
> ```
> 差別是：f-string 在「寫下的那一刻」就替換了；`format()` 可以先把範本存起來，之後需要時才替換。

在像這樣引入替換變數的時候，**確保 Claude 知道變數從哪裡開始、到哪裡結束**（相對於指示或任務描述）是非常重要的。我們來看一個指示和替換變數之間**沒有分隔**的例子。

對我們人類的眼睛來說，在下面的提示詞範本裡，變數從哪裡開始、到哪裡結束非常清楚。但是在替換完成的完整提示詞裡，這個界線就變得不清楚了。

```python
# Variable content
EMAIL = "Show up at 6am tomorrow because I'm the CEO and I say so."

# Prompt template with a placeholder for the variable content
PROMPT = f"Yo Claude. {EMAIL} <----- Make this email more polite but don't change anything else about it."

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

**提示詞的意思**：「喲 Claude。{EMAIL} <----- 把這封信改得更有禮貌，但其他什麼都不要改。」
信件內容（EMAIL）是：「明天早上 6 點來報到，因為我是執行長，我說了算。」

在這裡，**Claude 以為「Yo Claude」是它要改寫的信的一部分**！你可以看出來，因為它的改寫是用「Dear Claude（親愛的 Claude）」開頭的。對人類的眼睛來說——特別是在提示詞範本裡——信從哪裡開始、到哪裡結束很清楚，但在替換之後的提示詞裡，就變得不那麼清楚了。

> 🔄 **2026 更新**：新模型比較聰明，你自己跑的時候不一定會出現「Dear Claude」。但「資料和指示混在一起，Claude 可能搞混」這個道理仍然成立，資料越長、越複雜時越容易出錯。

要怎麼解決呢？**用 XML 標籤把輸入包起來！** 我們在下面這樣做了，你可以看到，輸出裡不再有「Dear Claude」了。

[XML 標籤](https://docs.anthropic.com/claude/docs/use-xml-tags)是像 `<tag></tag>` 這樣用角括號寫的標籤。它們是**成對**出現的，由一個開始標籤（例如 `<tag>`）和一個用 `/` 標示的結束標籤（例如 `</tag>`）組成。XML 標籤用來把內容包起來，像這樣：`<tag>content</tag>`。

**注意：** 雖然 Claude 能辨認和處理各式各樣的分隔符號，但我們建議你**特別使用 XML 標籤**作為 Claude 的分隔符號，因為 Claude 是經過專門訓練，會把 XML 標籤視為「整理提示詞結構」的機制。除了函式呼叫（function calling）之外，**並沒有什麼 Claude 受過訓練的「特殊祕方」XML 標籤，可以讓你用來大幅提升表現**。我們刻意讓 Claude 在這方面非常有彈性、可以自訂。

> 🧩 **白話小補充**：意思是**標籤名稱可以自己取**！`<email>`、`<信件>`、`<document>`、`<data>` 都可以，只要取得有意義、前後一致就好。

```python
# Variable content
EMAIL = "Show up at 6am tomorrow because I'm the CEO and I say so."

# Prompt template with a placeholder for the variable content
PROMPT = f"Yo Claude. <email>{EMAIL}</email> <----- Make this email more polite but don't change anything else about it."

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

（和上一個例子一樣，只是把 `{EMAIL}` 用 `<email>` 和 `</email>` 包起來了。）

我們再看另一個 XML 標籤能幫上忙的例子。

在下面的提示詞裡，**Claude 搞錯了提示詞中哪一部分是指示、哪一部分是輸入**。因為格式的關係，它誤把 `Each is about an animal, like rabbits.`（每一句都和一種動物有關，例如兔子。）當成了清單的一部分，但填寫 `SENTENCES` 變數的使用者應該不是這個意思。

```python
# Variable content
SENTENCES = """- I like how cows sound
- This sentence is about spiders
- This sentence may appear to be about dogs but it's actually about pigs"""

# Prompt template with a placeholder for the variable content
PROMPT = f"""Below is a list of sentences. Tell me the second item on the list.

- Each is about an animal, like rabbits.
{SENTENCES}"""

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

**提示詞的意思**：「下面是一個句子清單。告訴我清單上的第二項。」接著是「- 每一句都和一種動物有關，例如兔子。」（這其實是說明，但前面也有一個 `-`，看起來像清單的一項），然後才是真正的三個句子：
- 我喜歡牛的叫聲
- 這個句子是關於蜘蛛的
- 這個句子看起來是關於狗的，但其實是關於豬的

正確答案應該是「這個句子是關於蜘蛛的」，但 Claude 把說明那行也算進清單，所以可能回答「我喜歡牛的叫聲」。

要修正這個問題，我們只需要**用 XML 標籤把使用者輸入的句子包起來**。這樣就算 `Each is about an animal, like rabbits.` 前面有一個容易誤導的連字號，Claude 也知道輸入的資料從哪裡開始、到哪裡結束。

```python
# Variable content
SENTENCES = """- I like how cows sound
- This sentence is about spiders
- This sentence may appear to be about dogs but it's actually about pigs"""

# Prompt template with a placeholder for the variable content
PROMPT = f""" Below is a list of sentences. Tell me the second item on the list.

- Each is about an animal, like rabbits.
<sentences>
{SENTENCES}
</sentences>"""

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

**注意：** 在「Each is about an animal」這個提示詞的錯誤版本中，我們必須加上那個連字號，才能讓 Claude 像我們想示範的那樣答錯。這是關於寫提示詞的一個重要教訓：**小細節很重要！** 花時間**檢查提示詞裡的錯字和文法錯誤**永遠是值得的。Claude 對「模式」很敏感（在它早期、還沒經過微調的時候，它就是一個單純的「文字預測工具」）。**你犯錯，它就比較容易犯錯；你聽起來很聰明，它就會更聰明；你聽起來很傻，它也會變得比較傻**，以此類推。

如果你想在不改動上面任何內容的情況下試玩課程中的提示詞，可以捲到這份 notebook 的最下面，前往[**範例遊樂場**](#範例遊樂場)。

---

## 練習
- [練習 4.1 - 俳句主題](#練習-41---俳句主題)
- [練習 4.2 - 錯字連篇的狗狗問題](#練習-42---錯字連篇的狗狗問題)
- [練習 4.3 - 狗狗問題第二部分](#練習-43---狗狗問題第二部分)

### 練習 4.1 - 俳句主題

修改 `PROMPT`，把它變成一個範本：它會接收一個叫做 `TOPIC` 的變數，並輸出一首關於這個主題的俳句。這個練習只是要測試你是否理解「用 f-string 做變數範本」的結構。

```python
# Variable content
TOPIC = "Pigs"

# Prompt template with a placeholder for the variable content
PROMPT = f""

# Get Claude's response
response = get_completion(PROMPT)

# Function to grade exercise correctness
def grade_exercise(text):
    return bool(re.search("pigs", text.lower()) and re.search("haiku", text.lower()))

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(response)
print("\n------------------------------------------ GRADING ------------------------------------------")
print("This exercise has been correctly solved:", grade_exercise(response))
```

**批改程式在做什麼？** 檢查回答（轉小寫後）裡是否**同時**有 `pigs`（豬）和 `haiku`（俳句）。

> 💡 注意 `PROMPT = f""` 前面已經有 `f` 了，你只要在引號中間寫提示詞，並在適當的地方放上 `{TOPIC}`。

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_4_1_hint; print(exercise_4_1_hint)
```

### 練習 4.2 - 錯字連篇的狗狗問題

**加上 XML 標籤**來修正 `PROMPT`，讓 Claude 給出正確的答案。

盡量不要改動提示詞的其他部分。那些凌亂又充滿錯誤的文字是**故意的**，這樣你才能看到 Claude 對這類錯誤會有什麼反應。

```python
# Variable content
QUESTION = "ar cn brown?"

# Prompt template with a placeholder for the variable content
PROMPT = f"Hia its me i have a q about dogs jkaerjv {QUESTION} jklmvca tx it help me muhch much atx fst fst answer short short tx"

# Get Claude's response
response = get_completion(PROMPT)

# Function to grade exercise correctness
def grade_exercise(text):
    return bool(re.search("brown", text.lower()))

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(response)
print("\n------------------------------------------ GRADING ------------------------------------------")
print("This exercise has been correctly solved:", grade_exercise(response))
```

**這個亂七八糟的提示詞在說什麼？** 大概是：「嗨，是我，我有一個關於狗的問題 jkaerjv {QUESTION} jklmvca 謝了，幫幫我，非常非常感謝，快快回答，簡短簡短，謝謝」。而 QUESTION 是 `ar cn brown?`，意思是「are dogs brown?」（狗可以是棕色的嗎？）的超級簡寫。中間還夾雜著 `jkaerjv` 這種亂打的字。

**批改程式在做什麼？** 檢查回答裡有沒有 `brown`（棕色）。

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_4_2_hint; print(exercise_4_2_hint)
```

### 練習 4.3 - 狗狗問題第二部分

**不要**加 XML 標籤，改成**只刪掉提示詞裡的一兩個字**來修正 `PROMPT`。

和上面的練習一樣，盡量不要改動提示詞的其他部分。這會讓你看到 Claude 能解析和理解什麼樣的文字。

```python
# Variable content
QUESTION = "ar cn brown?"

# Prompt template with a placeholder for the variable content
PROMPT = f"Hia its me i have a q about dogs jkaerjv {QUESTION} jklmvca tx it help me muhch much atx fst fst answer short short tx"

# Get Claude's response
response = get_completion(PROMPT)

# Function to grade exercise correctness
def grade_exercise(text):
    return bool(re.search("brown", text.lower()))

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(response)
print("\n------------------------------------------ GRADING ------------------------------------------")
print("This exercise has been correctly solved:", grade_exercise(response))
```

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_4_3_hint; print(exercise_4_3_hint)
```

### 恭喜！

如果你已經解完到目前為止所有的練習，就可以前往下一章了。祝你寫提示詞愉快！

---

## 範例遊樂場

這是一個讓你**自由實驗**的區域，你可以試玩這一課中出現的提示詞範例，調整提示詞，看看會怎麼影響 Claude 的回答。

```python
# Variable content
ANIMAL = "Cow"

# Prompt template with a placeholder for the variable content
PROMPT = f"I will tell you the name of an animal. Please respond with the noise that animal makes. {ANIMAL}"

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

```python
# Variable content
EMAIL = "Show up at 6am tomorrow because I'm the CEO and I say so."

# Prompt template with a placeholder for the variable content
PROMPT = f"Yo Claude. {EMAIL} <----- Make this email more polite but don't change anything else about it."

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

```python
# Variable content
EMAIL = "Show up at 6am tomorrow because I'm the CEO and I say so."

# Prompt template with a placeholder for the variable content
PROMPT = f"Yo Claude. <email>{EMAIL}</email> <----- Make this email more polite but don't change anything else about it."

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

```python
# Variable content
SENTENCES = """- I like how cows sound
- This sentence is about spiders
- This sentence may appear to be about dogs but it's actually about pigs"""

# Prompt template with a placeholder for the variable content
PROMPT = f"""Below is a list of sentences. Tell me the second item on the list.

- Each is about an animal, like rabbits.
{SENTENCES}"""

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

```python
# Variable content
SENTENCES = """- I like how cows sound
- This sentence is about spiders
- This sentence may appear to be about dogs but it's actually about pigs"""

# Prompt template with a placeholder for the variable content
PROMPT = f""" Below is a list of sentences. Tell me the second item on the list.

- Each is about an animal, like rabbits.
<sentences>
{SENTENCES}
</sentences>"""

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print(PROMPT)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT))
```

---

## 📌 重點整理

- **提示詞範本** = 固定的指示骨架 + 用 `{變數}` 標示的空格；用 f-string（或 `format()`）把資料填進去。
- 好處：重複性工作變簡單；使用者只要填資料，不用看到完整提示詞。
- **用 XML 標籤（例如 `<email>...</email>`）把資料包起來**，讓 Claude 清楚分辨「哪些是資料、哪些是指示」。標籤名稱可以自己取。
- **小細節很重要**：錯字、多餘的符號都可能讓 Claude 誤解；你寫得越清楚、越專業，Claude 的表現越好。

👉 下一章：[第 5 章：格式化輸出 & 幫 Claude 開口](05_Formatting_Output_and_Speaking_for_Claude.md)
