<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`07_Using_Examples_Few-Shot_Prompting.ipynb`](07_Using_Examples_Few-Shot_Prompting.ipynb)。

# 第 7 章：使用範例（Few-Shot Prompting 少量範例提示）

> 📚 **第 2 單元：提示詞工程互動教學**｜第 7 章 / 共 9 章（中級）
> ⏱️ 預估時間：35 分鐘

- [課程](#課程)
- [練習](#練習)
- [範例遊樂場](#範例遊樂場)

## 🎯 這一章你會學到

- 為什麼「給範例」是讓 Claude 照你意思做事**最有效**的方法之一
- zero-shot、one-shot、few-shot（零樣本、單樣本、少量樣本）是什麼意思
- 用範例同時控制**答案內容**和**輸出格式**

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

**給 Claude 範例，示範你希望它怎麼做（或你不希望它怎麼做），效果非常好**，可以用來：
- 得到正確的答案
- 得到格式正確的答案

這種提示方式也叫做「**少量範例提示（few shot prompting）**」。你也可能會遇到「zero-shot（零樣本）」、「n-shot（n 個樣本）」或「one-shot（單樣本）」這些說法。「shot（樣本）」的數量，指的是提示詞裡用了**幾個範例**。

> 🧩 **白話小補充**：
> - **zero-shot**：完全不給範例，直接叫它做。
> - **one-shot**：給 1 個範例。
> - **few-shot**：給幾個（通常 2～5 個）範例。
>
> 就像教新同事填表格：與其講一大堆規則，不如直接給他看兩張「填好的範本」，他馬上就懂了。

### 範例

假設你是一位開發者，想做一個能回答小孩問題的「家長機器人」。**Claude 預設的回答相當正式、像機器人一樣**。這會讓小孩很傷心的。

```python
# Prompt
PROMPT = "Will Santa bring me presents on Christmas?"

# Print Claude's response
print(get_completion(PROMPT))
```

（「聖誕老公公會在聖誕節送我禮物嗎？」——Claude 可能會很「誠實」地解釋聖誕老公公的由來⋯⋯）

你可以花時間描述你想要的語氣，但更簡單的方法是：**直接給 Claude 幾個理想回答的範例**。

```python
# Prompt
PROMPT = """Please complete the conversation by writing the next line, speaking as "A".
Q: Is the tooth fairy real?
A: Of course, sweetie. Wrap up your tooth and put it under your pillow tonight. There might be something waiting for you in the morning.
Q: Will Santa bring me presents on Christmas?"""

# Print Claude's response
print(get_completion(PROMPT))
```

**提示詞翻譯**：
「請用『A』的身分寫出下一句話，完成這段對話。
Q：牙仙子是真的嗎？
A：當然是真的呀，寶貝。今天晚上把你的牙齒包好，放在枕頭底下。明天早上可能會有東西在那裡等你喔。
Q：聖誕老公公會在聖誕節送我禮物嗎？」

（Claude 看了牙仙子的範例，就知道要用溫柔、配合孩子想像力的語氣回答。）

在下面這個「格式」範例中，我們可以一步一步地教 Claude 一套格式指示：怎麼擷取人名和職業、再完全照我們想要的方式排版；**或者，我們也可以直接提供 Claude 幾個格式正確的範例，讓 Claude 自己舉一反三**。注意 `assistant` 回合裡的 `<individuals>`（prefill），讓 Claude 從一開始就走在正確的方向上。

```python
# Prompt template with a placeholder for the variable content
PROMPT = """Silvermist Hollow, a charming village, was home to an extraordinary group of individuals.
Among them was Dr. Liam Patel, a neurosurgeon who revolutionized surgical techniques at the regional medical center.
Olivia Chen was an innovative architect who transformed the village's landscape with her sustainable and breathtaking designs.
The local theater was graced by the enchanting symphonies of Ethan Kovacs, a professionally-trained musician and composer.
Isabella Torres, a self-taught chef with a passion for locally sourced ingredients, created a culinary sensation with her farm-to-table restaurant, which became a must-visit destination for food lovers.
These remarkable individuals, each with their distinct talents, contributed to the vibrant tapestry of life in Silvermist Hollow.
<individuals>
1. Dr. Liam Patel [NEUROSURGEON]
2. Olivia Chen [ARCHITECT]
3. Ethan Kovacs [MISICIAN AND COMPOSER]
4. Isabella Torres [CHEF]
</individuals>

At the heart of the town, Chef Oliver Hamilton has transformed the culinary scene with his farm-to-table restaurant, Green Plate. Oliver's dedication to sourcing local, organic ingredients has earned the establishment rave reviews from food critics and locals alike.
Just down the street, you'll find the Riverside Grove Library, where head librarian Elizabeth Chen has worked diligently to create a welcoming and inclusive space for all. Her efforts to expand the library's offerings and establish reading programs for children have had a significant impact on the town's literacy rates.
As you stroll through the charming town square, you'll be captivated by the beautiful murals adorning the walls. These masterpieces are the work of renowned artist, Isabella Torres, whose talent for capturing the essence of Riverside Grove has brought the town to life.
Riverside Grove's athletic achievements are also worth noting, thanks to former Olympic swimmer-turned-coach, Marcus Jenkins. Marcus has used his experience and passion to train the town's youth, leading the Riverside Grove Swim Team to several regional championships.
<individuals>
1. Oliver Hamilton [CHEF]
2. Elizabeth Chen [LIBRARIAN]
3. Isabella Torres [ARTIST]
4. Marcus Jenkins [COACH]
</individuals>

Oak Valley, a charming small town, is home to a remarkable trio of individuals whose skills and dedication have left a lasting impact on the community.
At the town's bustling farmer's market, you'll find Laura Simmons, a passionate organic farmer known for her delicious and sustainably grown produce. Her dedication to promoting healthy eating has inspired the town to embrace a more eco-conscious lifestyle.
In Oak Valley's community center, Kevin Alvarez, a skilled dance instructor, has brought the joy of movement to people of all ages. His inclusive dance classes have fostered a sense of unity and self-expression among residents, enriching the local arts scene.
Lastly, Rachel O'Connor, a tireless volunteer, dedicates her time to various charitable initiatives. Her commitment to improving the lives of others has been instrumental in creating a strong sense of community within Oak Valley.
Through their unique talents and unwavering dedication, Laura, Kevin, and Rachel have woven themselves into the fabric of Oak Valley, helping to create a vibrant and thriving small town."""

# Prefill for Claude's response
PREFILL = "<individuals>"

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print("USER TURN:")
print(PROMPT)
print("\nASSISTANT TURN:")
print(PREFILL)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT, prefill=PREFILL))
```

**這個提示詞的結構（看得懂就好，內容是虛構的小鎮故事）：**
1. **範例 1（文章）**：介紹「銀霧谷（Silvermist Hollow）」村裡的幾位人物——神經外科醫師 Liam Patel、建築師 Olivia Chen、音樂家兼作曲家 Ethan Kovacs、主廚 Isabella Torres。
2. **範例 1（標準答案）**：用 `<individuals>` 標籤列出「1. 人名 [職業大寫]」的清單。（原文的 MISICIAN 是原作者的拼字錯誤，應為 MUSICIAN。）
3. **範例 2（文章 + 標準答案）**：另一個小鎮「河畔林（Riverside Grove）」的主廚 Oliver Hamilton、圖書館館長 Elizabeth Chen、藝術家 Isabella Torres、游泳教練 Marcus Jenkins，同樣附上格式正確的清單。
4. **真正要處理的文章**：「橡樹谷（Oak Valley）」的有機農夫 Laura Simmons、舞蹈老師 Kevin Alvarez、志工 Rachel O'Connor。
5. **Prefill** `<individuals>`：Claude 就會照前面範例的格式，列出 Oak Valley 的三個人和他們的職業。

> 💡 **小提醒**：我們從頭到尾都**沒有**用文字解釋「請用編號、人名後面加方括號、職業要大寫」這些規則——Claude 是看範例自己學會的。這就是範例的威力。

如果你想在不改動上面任何內容的情況下試玩課程中的提示詞，可以捲到這份 notebook 的最下面，前往[**範例遊樂場**](#範例遊樂場)。

---

## 練習
- [練習 7.1 - 用範例控制電子郵件分類的格式](#練習-71---用範例控制電子郵件分類的格式)

### 練習 7.1 - 用範例控制電子郵件分類的格式

我們要重做[練習 6.2](06_Precognition_Thinking_Step_by_Step.md#練習-62---電子郵件分類的格式)，但這次要修改 `PROMPT`，使用「**少量範例**」——幾封信 + 正確的分類（和格式）——讓 Claude 輸出正確的答案。我們希望 Claude 輸出的**最後一個字元**，就是類別的字母。

如果你忘了每封信正確的分類字母是什麼，請參考 `EMAILS` 串列裡每封信旁邊的註解。

提醒一下，電子郵件的類別如下：
- (A) Pre-sale question（售前問題）
- (B) Broken or defective item（商品損壞或有瑕疵）
- (C) Billing question（帳務問題）
- (D) Other (please explain)（其他，請說明）

```python
# Prompt template with a placeholder for the variable content
PROMPT = """Please classify this email as either green or blue: {email}"""

# Prefill for Claude's response
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

# Iterate through list of emails
for i,email in enumerate(EMAILS):
    
    # Substitute the email text into the email placeholder variable
    formatted_prompt = PROMPT.format(email=email)
   
    # Get Claude's response
    response = get_completion(formatted_prompt, prefill=PREFILL)

    # Grade Claude's response
    grade = any([bool(re.search(ans, response[-1])) for ans in ANSWERS[i]])
    
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

**批改程式在做什麼？** `response[-1]` 是回答的**最後一個字元**（[0-4 第 5-1 節](../00_before_you_start/04_python_crash_course.md#5-1-用編號拿出裡面的東西)：-1 代表最後一個）。最後一個字元必須是正確的字母（例如 `B`）才算對。

> ⚠️ 注意：最後一個字元不能是句點、空白或換行！你的範例格式要設計成「答案以字母結尾」。

❓ 如果你需要提示，執行下面這格！

```python
from hints import exercise_7_1_hint; print(exercise_7_1_hint)
```

還是卡住了嗎？執行下面這格，看一個參考答案。

```python
from hints import exercise_7_1_solution; print(exercise_7_1_solution)
```

### 恭喜！

如果你已經解完到目前為止所有的練習，就可以前往下一章了。祝你寫提示詞愉快！

---

## 範例遊樂場

這是一個讓你**自由實驗**的區域，你可以試玩這一課中出現的提示詞範例，調整提示詞，看看會怎麼影響 Claude 的回答。

```python
# Prompt
PROMPT = "Will Santa bring me presents on Christmas?"

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# Prompt
PROMPT = """Please complete the conversation by writing the next line, speaking as "A".
Q: Is the tooth fairy real?
A: Of course, sweetie. Wrap up your tooth and put it under your pillow tonight. There might be something waiting for you in the morning.
Q: Will Santa bring me presents on Christmas?"""

# Print Claude's response
print(get_completion(PROMPT))
```

```python
# Prompt template with a placeholder for the variable content
PROMPT = """Silvermist Hollow, a charming village, was home to an extraordinary group of individuals.
Among them was Dr. Liam Patel, a neurosurgeon who revolutionized surgical techniques at the regional medical center.
Olivia Chen was an innovative architect who transformed the village's landscape with her sustainable and breathtaking designs.
The local theater was graced by the enchanting symphonies of Ethan Kovacs, a professionally-trained musician and composer.
Isabella Torres, a self-taught chef with a passion for locally sourced ingredients, created a culinary sensation with her farm-to-table restaurant, which became a must-visit destination for food lovers.
These remarkable individuals, each with their distinct talents, contributed to the vibrant tapestry of life in Silvermist Hollow.
<individuals>
1. Dr. Liam Patel [NEUROSURGEON]
2. Olivia Chen [ARCHITECT]
3. Ethan Kovacs [MISICIAN AND COMPOSER]
4. Isabella Torres [CHEF]
</individuals>

At the heart of the town, Chef Oliver Hamilton has transformed the culinary scene with his farm-to-table restaurant, Green Plate. Oliver's dedication to sourcing local, organic ingredients has earned the establishment rave reviews from food critics and locals alike.
Just down the street, you'll find the Riverside Grove Library, where head librarian Elizabeth Chen has worked diligently to create a welcoming and inclusive space for all. Her efforts to expand the library's offerings and establish reading programs for children have had a significant impact on the town's literacy rates.
As you stroll through the charming town square, you'll be captivated by the beautiful murals adorning the walls. These masterpieces are the work of renowned artist, Isabella Torres, whose talent for capturing the essence of Riverside Grove has brought the town to life.
Riverside Grove's athletic achievements are also worth noting, thanks to former Olympic swimmer-turned-coach, Marcus Jenkins. Marcus has used his experience and passion to train the town's youth, leading the Riverside Grove Swim Team to several regional championships.
<individuals>
1. Oliver Hamilton [CHEF]
2. Elizabeth Chen [LIBRARIAN]
3. Isabella Torres [ARTIST]
4. Marcus Jenkins [COACH]
</individuals>

Oak Valley, a charming small town, is home to a remarkable trio of individuals whose skills and dedication have left a lasting impact on the community.
At the town's bustling farmer's market, you'll find Laura Simmons, a passionate organic farmer known for her delicious and sustainably grown produce. Her dedication to promoting healthy eating has inspired the town to embrace a more eco-conscious lifestyle.
In Oak Valley's community center, Kevin Alvarez, a skilled dance instructor, has brought the joy of movement to people of all ages. His inclusive dance classes have fostered a sense of unity and self-expression among residents, enriching the local arts scene.
Lastly, Rachel O'Connor, a tireless volunteer, dedicates her time to various charitable initiatives. Her commitment to improving the lives of others has been instrumental in creating a strong sense of community within Oak Valley.
Through their unique talents and unwavering dedication, Laura, Kevin, and Rachel have woven themselves into the fabric of Oak Valley, helping to create a vibrant and thriving small town."""

# Prefill for Claude's response
PREFILL = "<individuals>"

# Print Claude's response
print("--------------------------- Full prompt with variable substutions ---------------------------")
print("USER TURN:")
print(PROMPT)
print("\nASSISTANT TURN:")
print(PREFILL)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT, prefill=PREFILL))
```

---

## 📌 重點整理

- **給範例**是控制 Claude「回答內容」和「輸出格式」最有效的方法之一。
- zero-shot = 不給範例；one-shot = 1 個；few-shot = 幾個。
- 範例比文字說明更直觀：想要什麼語氣、格式，**直接示範給它看**。
- 範例的格式要**完全**是你想要的樣子，Claude 會照著模仿；可以用 `<example>` 等 XML 標籤把範例框起來。
- 範例 + prefill 一起用效果更好。

👉 下一章：[第 8 章：避免幻覺](08_Avoiding_Hallucinations.md)
