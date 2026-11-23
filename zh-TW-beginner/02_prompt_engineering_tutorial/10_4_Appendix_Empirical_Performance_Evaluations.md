<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`10_4_Appendix_Empirical_Performance_Evaluations.ipynb`](10_4_Appendix_Empirical_Performance_Evaluations.ipynb)。

# 附錄 10.4（加碼）：評估 AI 模型——程式評分、人工評分、模型評分

> 📚 **第 2 單元：提示詞工程互動教學**｜加碼附錄
> ⏱️ 預估時間：30 分鐘
>
> 💡 **這篇從哪裡來？** 這篇附錄只出現在原課程的 **Amazon Bedrock 版本**（`AmazonBedrock/anthropic/10_3_Appendix_Empirical_Performance_Evaluations.ipynb`），`Anthropic 1P` 版沒有。為了「完整保留內容」，新手版把它也翻譯進來，並改寫成用 Anthropic API 金鑰就能執行（不需要 AWS 帳號）。
>
> 這篇是第 4 單元「提示詞評估」的**預告片**：先在這裡認識三種評分方法，到第 4 單元會深入學習。

## 🎯 這一章你會學到

- 評估 AI 模型表現的三種常用方法：**程式評分**、**人工評分**、**模型評分**
- 每種方法適合什麼樣的任務，以及它們的優缺點

## 準備工作（新手版改寫）

原課程這一篇是用 AWS Bedrock 連線到 Claude（`AnthropicBedrock` 客戶端、模型名稱 `anthropic.claude-3-haiku-20240307-v1:0`、還要設定 AWS 區域）。新手版改成用一般的 Anthropic 客戶端，這樣只需要 `.env` 裡的 API 金鑰就能執行：

```python
%pip install "anthropic<1" python-dotenv --quiet

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()                      # 從 .env 讀取 ANTHROPIC_API_KEY
client = Anthropic()               # 原課程是：client = AnthropicBedrock(aws_region=AWS_REGION)
MODEL_NAME = "claude-haiku-4-5"    # 原課程是："anthropic.claude-3-haiku-20240307-v1:0"
```

> 🧩 **白話小補充**：Amazon Bedrock 是 AWS（亞馬遜雲端）提供的服務，可以透過 AWS 帳號使用 Claude。除了「怎麼連線」不同之外，送出的訊息格式和 Claude 的回答都是一樣的，所以後面的程式碼完全不用改。

---

# 評估 AI 模型：程式、人工和模型評分

在這份 notebook 中，我們會深入介紹三種廣泛使用的技巧，用來評估像 Claude v3 這類 AI 模型的成效：

1. 程式評分（Code-based grading）
2. 人工評分（Human grading）
3. 模型評分（Model-based grading）

我們會用範例說明每一種方法，並在衡量 AI 表現時，檢視它們各自的優點和限制。

> 🧩 **白話小補充：為什麼要「評估」？** 你改了提示詞之後，怎麼知道它真的變好了？靠感覺不準。「評估」就是準備一些**考題**和**標準答案**，讓 Claude 作答，然後**打分數**。分數高了，才代表真的進步了。

## 程式評分範例：情緒分析

在這個例子中，我們要評估 Claude 把電影影評的情緒分類成「正面」或「負面」的能力。我們可以用程式碼檢查模型的輸出是否符合預期的情緒。

```python
# Function to build the input prompt for sentiment analysis
def build_input_prompt(review):
    user_content = f"""Classify the sentiment of the following movie review as either 'positive' or 'negative' provide only one of those two choices:
    <review>{review}</review>"""
    return [{"role": "user", "content": user_content}]

# Define the evaluation data
eval = [
    {
        "review": "This movie was amazing! The acting was superb and the plot kept me engaged from start to finish.",
        "golden_answer": "positive"
    },
    {
        "review": "I was thoroughly disappointed by this film. The pacing was slow and the characters were one-dimensional.",
        "golden_answer": "negative"
    }
]

# Function to get completions from the model
def get_completion(messages):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=messages
    )
    return message.content[0].text

# Get completions for each input
outputs = [get_completion(build_input_prompt(item["review"])) for item in eval]

# Print the outputs and golden answers
for output, question in zip(outputs, eval):
    print(f"Review: {question['review']}\nGolden Answer: {question['golden_answer']}\nOutput: {output}\n")

# Function to grade the completions
def grade_completion(output, golden_answer):
    return output.lower() == golden_answer.lower()

# Grade the completions and print the accuracy
grades = [grade_completion(output, item["golden_answer"]) for output, item in zip(outputs, eval)]
print(f"Accuracy: {sum(grades) / len(grades) * 100}%")
```

**逐行解說：**
- `build_input_prompt(review)`：把一篇影評組成提示詞——「把下面這篇電影影評的情緒分類成『positive（正面）』或『negative（負面）』，只能回答這兩個選項的其中一個：`<review>`⋯⋯`</review>`」，並包成訊息串列回傳。
- `eval = [...]`：**評估資料集**，每一筆都有一篇影評 `review` 和**標準答案** `golden_answer`：
  1. 「這部電影太棒了！演技一流，劇情從頭到尾都讓我目不轉睛。」→ positive
  2. 「這部片讓我非常失望。節奏很慢，角色很扁平。」→ negative
- `get_completion(messages)`：呼叫 Claude 的小幫手。
- `outputs = [get_completion(...) for item in eval]`：用串列生成式（[0-4 第 16-2 節](../00_before_you_start/04_python_crash_course.md#16-2-串列生成式list-comprehension)）對每一筆資料取得 Claude 的答案。
- `zip(outputs, eval)`：把「Claude 的答案」和「題目」一對一配對起來，方便一起印出。
- `grade_completion(output, golden_answer)`：**評分函式**——把兩邊都轉成小寫後，看是不是**完全一樣**。
- `sum(grades) / len(grades) * 100`：答對的數量 ÷ 總題數 × 100 = **正確率**（`True` 在加總時會被當成 1，`False` 當成 0）。

> ⚠️ **小提醒**：這種「完全一樣才算對」的評分很嚴格。如果 Claude 回答 `Positive.`（多了句點）就會被判錯。實務上常會先清理答案（例如去掉標點、空白），或改用「答案裡有沒有包含某個字」來判斷。第 4 單元會詳細討論。

## 人工評分範例：作文評分

有些任務，例如替作文打分數，很難只用程式碼來評估。在這種情況下，我們可以提供評分準則給人類評分者，讓他們評估模型的輸出。

```python
# Function to build the input prompt for essay generation
def build_input_prompt(topic):
    user_content = f"""Write a short essay discussing the following topic:
    <topic>{topic}</topic>"""
    return [{"role": "user", "content": user_content}]

# Define the evaluation data
eval = [
    {
        "topic": "The importance of education in personal development and societal progress",
        "golden_answer": "A high-scoring essay should have a clear thesis, well-structured paragraphs, and persuasive examples discussing how education contributes to individual growth and broader societal advancement."
    }
]

# Get completions for each input
outputs = [get_completion(build_input_prompt(item["topic"])) for item in eval]

# Print the outputs and golden answers
for output, item in zip(outputs, eval):
    print(f"Topic: {item['topic']}\n\nGrading Rubric:\n {item['golden_answer']}\n\nModel Output:\n{output}\n")
```

**逐行解說：**
- 提示詞：「寫一篇短文，討論下面的主題：`<topic>`⋯⋯`</topic>`」
- 主題：「教育對個人發展和社會進步的重要性」
- 這次的 `golden_answer` 不是標準答案，而是**評分準則（rubric）**：「一篇高分的文章應該要有清楚的論點、結構良好的段落，以及有說服力的例子，討論教育如何促進個人成長和更廣泛的社會進步。」
- 程式只負責印出「主題、評分準則、模型輸出」，**分數由人來打**。

> 🧩 **白話小補充**：人工評分最準確、最有彈性，但缺點是**慢、貴、不同人標準可能不一致**，沒辦法大量進行。

## 模型評分範例

我們可以用 Claude 來替它自己的輸出評分：提供模型的回答和一份評分準則給 Claude。這樣就能把那些通常需要人類判斷的任務，自動化地進行評估。

### 範例 1：摘要

在這個例子中，我們用 Claude 來評估它自己產生的摘要品質。當你需要評估模型能否從一段長文中，簡潔又準確地抓出關鍵資訊時，這就很有用。透過提供一份列出「應該涵蓋哪些重點」的評分準則，我們可以把評分過程自動化，快速評估模型在摘要任務上的表現。

```python
# Function to build the input prompt for summarization
def build_input_prompt(text):
    user_content = f"""Please summarize the main points of the following text:
    <text>{text}</text>"""
    return [{"role": "user", "content": user_content}]

# Function to build the grader prompt for assessing summary quality
def build_grader_prompt(output, rubric):
    user_content = f"""Assess the quality of the following summary based on this rubric:
    <rubric>{rubric}</rubric>
    <summary>{output}</summary>
    Provide a score from 1-5, where 1 is poor and 5 is excellent."""
    return [{"role": "user", "content": user_content}]

# Define the evaluation data
eval = [
    {
        "text": "The Magna Carta, signed in 1215, was a pivotal document in English history. It limited the powers of the monarchy and established the principle that everyone, including the king, was subject to the law. This laid the foundation for constitutional governance and the rule of law in England and influenced legal systems worldwide.",
        "golden_answer": "A high-quality summary should concisely capture the key points: 1) The Magna Carta's significance in English history, 2) Its role in limiting monarchical power, 3) Establishing the principle of rule of law, and 4) Its influence on legal systems around the world."
    }
]

# Get completions for each input
outputs = [get_completion(build_input_prompt(item["text"])) for item in eval]

# Grade the completions
grades = [get_completion(build_grader_prompt(output, item["golden_answer"])) for output, item in zip(outputs, eval)]

# Print the summary quality score
print(f"Summary quality score: {grades[0]}")
```

**逐行解說：**
- `build_input_prompt(text)`：「請摘要下面這段文字的重點：`<text>`⋯⋯`</text>`」
- `build_grader_prompt(output, rubric)`：**評分用的提示詞**——「根據這份評分準則，評估下面這份摘要的品質：`<rubric>`⋯⋯`</rubric>` `<summary>`⋯⋯`</summary>` 請給出 1 到 5 分的分數，1 分是很差，5 分是非常好。」
- 要摘要的文字（大意）：「1215 年簽署的《大憲章》是英國歷史上的關鍵文件。它限制了君主的權力，並確立了『包括國王在內，人人都要受法律約束』的原則。這為英國的憲政治理和法治奠定了基礎，也影響了全世界的法律體系。」
- 評分準則：「一份高品質的摘要應該簡潔地抓到這些重點：1)《大憲章》在英國歷史上的重要性 2) 它在限制君權上的角色 3) 確立法治原則 4) 它對全世界法律體系的影響。」
- 流程：**先讓 Claude 寫摘要 → 再讓 Claude 當評審，替摘要打分數**。

### 範例 2：事實查核

在這個例子中，我們用 Claude 來查核一個說法的真偽，然後再評估它的事實查核是否準確。當你需要評估模型分辨正確與錯誤資訊的能力時，這就很有用。透過提供一份列出「正確的事實查核應該涵蓋哪些重點」的評分準則，我們可以把評分過程自動化，快速評估模型在事實查核任務上的表現。

```python
# Function to build the input prompt for fact-checking
def build_input_prompt(claim):
    user_content = f"""Determine if the following claim is true or false:
    <claim>{claim}</claim>"""
    return [{"role": "user", "content": user_content}]

# Function to build the grader prompt for assessing fact-check accuracy
def build_grader_prompt(output, rubric):
    user_content = f"""Based on the following rubric, assess whether the fact-check is correct:
    <rubric>{rubric}</rubric>
    <fact-check>{output}</fact-check>"""
    return [{"role": "user", "content": user_content}]

# Define the evaluation data
eval = [
    {
        "claim": "The Great Wall of China is visible from space.",
        "golden_answer": "A correct fact-check should state that this claim is false. While the Great Wall is an impressive structure, it is not visible from space with the naked eye."
    }
]

# Get completions for each input
outputs = [get_completion(build_input_prompt(item["claim"])) for item in eval]

grades = []
for output, item in zip(outputs, eval):
    # Print the claim, fact-check, and rubric
    print(f"Claim: {item['claim']}\n")
    print(f"Fact-check: {output}]\n")
    print(f"Rubric: {item['golden_answer']}\n")
    
    # Grade the fact-check
    grader_prompt = build_grader_prompt(output, item["golden_answer"])
    grade = get_completion(grader_prompt)
    grades.append("correct" in grade.lower())

# Print the fact-checking accuracy
accuracy = sum(grades) / len(grades)
print(f"Fact-checking accuracy: {accuracy * 100}%")
```

**逐行解說：**
- 要查核的說法：「從太空中可以看到中國的萬里長城。」
- 評分準則：「正確的事實查核應該指出這個說法是**錯的**。雖然長城是一座令人印象深刻的建築，但從太空中用肉眼是看不到的。」
- 評審提示詞：「根據下面的評分準則，評估這份事實查核是否正確：⋯⋯」
- `grades.append("correct" in grade.lower())`：如果評審的回答裡有 `correct` 這個字，就算正確。

> ⚠️ **小提醒**：用 `"correct" in ...` 判斷有一個陷阱——`incorrect`（不正確）裡面也包含 `correct`！所以就算評審說「incorrect」，也會被算成正確。這是原課程程式碼的一個小漏洞，也正好提醒我們：**評分邏輯本身也要仔細檢查**。比較好的做法是請評審用固定格式回答，例如 `<verdict>CORRECT</verdict>` 或 `<verdict>INCORRECT</verdict>`。

### 範例 3：語氣分析

在這個例子中，我們用 Claude 分析一段文字的語氣，然後再評估它的分析是否準確。當你需要評估模型辨識、解讀文字中表達的情緒和態度的能力時，這就很有用。透過提供一份列出「應該辨識出哪些語氣面向」的評分準則，我們可以把評分過程自動化，快速評估模型在語氣分析任務上的表現。

```python
# Function to build the input prompt for tone analysis
def build_input_prompt(text):
    user_content = f"""Analyze the tone of the following text:
    <text>{text}</text>"""
    return [{"role": "user", "content": user_content}]

# Function to build the grader prompt for assessing tone analysis accuracy
def build_grader_prompt(output, rubric):
    user_content = f"""Assess the accuracy of the following tone analysis based on this rubric:
    <rubric>{rubric}</rubric>
    <tone-analysis>{output}</tone-analysis>"""
    return [{"role": "user", "content": user_content}]

# Define the evaluation data
eval = [
    {
        "text": "I can't believe they canceled the event at the last minute. This is completely unacceptable and unprofessional!",
        "golden_answer": "The tone analysis should identify the text as expressing frustration, anger, and disappointment. Key words like 'can't believe', 'last minute', 'unacceptable', and 'unprofessional' indicate strong negative emotions."
    }
]

# Get completions for each input
outputs = [get_completion(build_input_prompt(item["text"])) for item in eval]

# Grade the completions
grades = [get_completion(build_grader_prompt(output, item["golden_answer"])) for output, item in zip(outputs, eval)]

# Print the tone analysis quality
print(f"Tone analysis quality: {grades[0]}")
```

**逐行解說：**
- 要分析的文字：「我不敢相信他們在最後一刻取消了活動。這完全不能接受，而且非常不專業！」
- 評分準則：「語氣分析應該辨識出這段文字表達了**挫折、憤怒和失望**。像『不敢相信』、『最後一刻』、『不能接受』和『不專業』這些關鍵字，都顯示出強烈的負面情緒。」
- 評審提示詞：「根據這份評分準則，評估下面這份語氣分析的準確度：⋯⋯」

---

這些範例展示了程式評分、人工評分和模型評分，可以怎麼用來評估像 Claude 這樣的 AI 模型在各種任務上的表現。要選擇哪一種評估方法，取決於任務的性質和可用的資源。模型評分提供了一種很有前景的方法，可以把那些原本需要人類判斷的複雜任務評估自動化。

---

## 📌 重點整理

| 方法 | 怎麼做 | 優點 | 缺點 | 適合的任務 |
|---|---|---|---|---|
| **程式評分** | 用程式比對答案（完全相同、包含關鍵字、正規表達式⋯⋯） | 快、便宜、穩定、可以大量執行 | 只適合有明確答案的任務 | 分類、選擇題、擷取特定資訊 |
| **人工評分** | 由人根據評分準則打分數 | 最有彈性、最能判斷細微品質 | 慢、貴、標準可能不一致 | 作文、創意寫作、需要專業判斷的任務 |
| **模型評分** | 請另一個（或同一個）LLM 根據評分準則打分數 | 能自動化評估開放式任務 | 評審本身也可能出錯；評分提示詞要寫好 | 摘要、語氣、事實查核等開放式任務 |

- 評估的核心：**評估資料集**（題目 + 標準答案或評分準則）+ **評分方法**。
- 評分邏輯本身也要仔細檢查（例如 `"correct"` 也出現在 `"incorrect"` 裡）。

👉 想深入學習評估？請前往 **第 4 單元「提示詞評估」**：[4-1 評估入門](../04_prompt_evaluations/01_intro_to_evals.md)
👉 或繼續第 3 單元：[第 3 單元：真實世界的提示詞](../03_real_world_prompting/01_prompting_recap.md)
