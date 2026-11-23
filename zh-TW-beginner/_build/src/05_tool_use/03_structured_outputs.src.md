<!--meta {"orig": "tool_use/03_structured_outputs.ipynb", "out": "05_tool_use/03_structured_outputs"} -->
# 5-3 用工具使用強制輸出 JSON

> 📚 **第 5 單元：工具使用**｜第 3 課 / 共 6 課
> ⏱️ 預估時間：40 分鐘

## 🎯 這一課你會學到

* 了解怎麼用工具來**強制得到結構化的回答**
* 運用這個「小技巧」產生結構化的 JSON
* 用 `tool_choice` 強制 Claude 使用某個特定的工具

> 🔄 **2026 更新**：
> - 這一課原本使用 `claude-3-sonnet-20240229` 和 `claude-3-haiku-20240307`，新手版換成 `claude-sonnet-4-6` 和 `claude-haiku-4-5`。
> - 現在 Claude API 也有專門的「**結構化輸出（structured outputs）**」功能（`output_config.format`），以及工具定義上的 `"strict": true` 選項，可以**保證**輸出完全符合你給的 JSON Schema。不過這一課教的「用工具定義來規定格式」的技巧至今仍然很常用，而且觀念相通。
> - 另外要注意：**最新一代的部分模型（例如 Opus 5.5、Sonnet 5.5）不支援用 `tool_choice` 強制使用特定工具**（`{"type": "tool", ...}` 會回傳錯誤），在那些模型上要改用 `{"type": "auto"}` 加上明確的提示詞，或改用結構化輸出功能。新手版使用的 Sonnet 4.6 支援 `tool_choice` 強制。

---

利用工具使用的一個比較有趣的方式，是**強制 Claude 用結構化的內容（例如 JSON）回答**。有很多情況我們會想從 Claude 得到標準化的 JSON 回答：擷取實體、摘要資料、分析情緒等等。

一種做法是直接請 Claude 用 JSON 回答，但這可能需要額外的工作，才能從 Claude 回傳的一大串文字中真正擷取出 JSON，或確保 JSON 完全符合我們想要的格式。

好消息是：**每當 Claude 想使用一個工具時，它就已經會用我們在定義工具時告訴它的、結構完美的格式來回應了。**

在上一課，我們給了 Claude 一個計算機工具。當它想使用這個工具時，它回應的內容像這樣：

```
{
    'operand1': 1984135, 
    'operand2': 9343116, 
    'operation': 'multiply'
}
```

這看起來可疑地像 JSON！

如果我們想要 Claude 產生結構化的 JSON，就可以好好利用這一點。我們只需要**定義一個描述特定 JSON 結構的工具**，然後告訴 Claude 就好。就這樣。Claude 會回應，以為它在「呼叫一個工具」，但其實我們在意的只是它給我們的**結構化回答**。

> 🧩 **白話小補充**：這就像給員工一張「訂單表格」，說「請把客人的需求填在這張表上交給我」。員工以為要送去某個部門處理，但其實你只是想要一張**格式整齊的表格**。工具定義裡的 `input_schema` 就是那張表格的欄位設計。

---

# 觀念概覽

這和上一課做的有什麼不同？這是上一課工作流程的圖：

![上一課：真的執行計算機工具](@orig/images/chickens_calculator.png)

在上一課，我們讓 Claude 使用一個工具，Claude 想呼叫它，然後我們**真的**呼叫了背後的工具函式。

在這一課，我們要「騙」一下 Claude：告訴它有一個特定的工具，但我們**不需要真的呼叫**背後的工具函式。我們把工具當作「強制得到特定結構回答」的方法，就像這張圖：

![這一課：只拿工具輸入的結構化資料](@orig/images/structured_response.png)

---

## 情緒分析

我們從一個簡單的例子開始。假設我們想要 Claude 分析一段文字的情緒，並用符合這個形狀的 JSON 物件回答：

```
{
  "negative_score": 0.6,
  "neutral_score": 0.3,
  "positive_score": 0.1
}
```

（負面分數、中立分數、正面分數。）

我們只需要定義一個用 JSON Schema 描述這個形狀的工具。這是一種可能的實作：

{{cell 5}}

（工具名稱 `print_sentiment_scores`（印出情緒分數），說明「印出給定文字的情緒分數」。三個欄位都是 `number`，說明都是「⋯⋯情緒分數，範圍從 0.0 到 1.0」，而且三個都必填。）

現在我們可以告訴 Claude 有這個工具，並**明確地叫 Claude 使用它**，確保它真的會用。我們應該會得到一個表示 Claude 想使用工具的回應。工具使用的回應應該會以我們想要的確切格式包含所有資料。

{{cell 7}}

（推文內容：「我超級討厭酸黃瓜。我真的很鄙視酸黃瓜。它們是垃圾。」提示詞最後一句：「Only use the print_sentiment_scores tool.（只使用 print_sentiment_scores 工具。）」）

{{cell 8}}

我們來看看 Claude 回傳的回應。我們把重要的部分標成粗體：

>ToolsBetaMessage(id='msg_01BhF4TkK8vDM6z5m4FNGRnB', content=[TextBlock(text='Here is the sentiment analysis for the given text:', >type='text'), ToolUseBlock(id='toolu_01Mt1an3KHEz5RduZRUUuTWz', **input={'positive_score': 0.0, 'negative_score': 0.791, 'neutral_score': 0.209}**, name='print_sentiment_scores', type='tool_use')], model='claude-3-sonnet-20240229', role='assistant', stop_reason='tool_use', stop_sequence=None, type='message', usage=Usage(input_tokens=374, output_tokens=112))

（注意這次 `content` 裡有**兩個**區塊：先是一個文字區塊「這是給定文字的情緒分析：」，然後才是工具使用區塊。所以不能直接用 `content[0]`！）

Claude 「以為」它在呼叫一個會使用這些情緒分析資料的工具，但其實我們只是要擷取這些資料，把它變成 JSON：

{{cell 10}}

**逐行解說：**
- `for content in response.content:`：逐一檢查每個內容區塊。
- `if content.type == "tool_use" and content.name == "print_sentiment_scores":`：找到「類型是工具使用、而且工具名稱正確」的那一塊。
- `json_sentiment = content.input`：它的 `input` 就是我們要的結構化資料（一個 Python 字典）。
- `break`：找到了就跳出迴圈。
- `json.dumps(json_sentiment, indent=2)`：把字典轉成排版好的 JSON 文字（`indent=2` 代表每層縮排 2 個空格）。

成功了！現在我們把它變成一個可以重複使用的函式：接收一則推文或文章，然後印出或回傳 JSON 格式的情緒分析。

{{cell 12}}

{{cells 13-14}}

（「天啊我超愛泡泡浴的！！！！」→ 正面 0.8；「說實話我對泡澡沒什麼意見」→ 中立 0.879。）

---

## 用 `tool_choice` 強制使用工具

目前我們是透過**提示詞**「強制」Claude 使用 `print_sentiment_scores` 工具。我們在提示詞裡寫了 `Only use the print_sentiment_scores tool.`，這通常有效，但還有更好的方法！我們其實可以用 **`tool_choice` 參數**，強制 Claude 使用某個特定的工具：

```python
tool_choice={"type": "tool", "name": "print_sentiment_scores"}
```

上面的程式碼告訴 Claude：它**必須**用呼叫 `print_sentiment_scores` 工具的方式來回應。我們來更新函式，使用它：

{{cell 19}}

（和之前的函式一樣，只多了 `tool_choice={"type": "tool", "name": "print_sentiment_scores"},` 這一行。）

我們會在之後的課程中更詳細地介紹 `tool_choice`。

> 🧩 **白話小補充**：用 `tool_choice` 強制使用某個工具時，Claude 會**直接**輸出工具使用區塊，通常不會在前面加文字說明。

---

## 實體擷取的例子

我們用同樣的方法，讓 Claude 產生排版好的 JSON，裡面包含從一段文字中擷取出的**實體**，例如人、組織和地點：

{{cell 23}}

**這個工具定義比較複雜，我們拆開看：**
- `"entities"`：型別是 `"array"`（陣列/串列）。
- `"items"`：說明「陣列裡的每一個東西」長什麼樣子——每個都是一個 `"object"`（物件/字典），包含：
  - `name`：擷取出的實體名稱
  - `type`：實體類型（例如 PERSON 人、ORGANIZATION 組織、LOCATION 地點）
  - `context`：這個實體在文字中出現的上下文
- 要分析的文字：「John 在紐約的 Google 上班。他上週在舊金山和 Acme 公司的執行長 Sarah 見面。」

> 🧩 **白話小補充：什麼是「實體（entity）」？** 在自然語言處理裡，「實體」指的是文字中提到的具體事物，例如人名、公司名、地名、日期。「實體擷取」就是把這些找出來並分類。

我們使用的是和之前一樣的「小技巧」。我們告訴 Claude 它可以使用一個工具，藉此讓 Claude 用特定的資料格式回答。然後我們擷取出 Claude 回答的格式化資料，就大功告成了。

記住，在這個使用情境中，**明確告訴 Claude 我們想要它使用某個工具**會有幫助：

>Use the print_entities tool.
>（使用 print_entities 工具。）

---

## 更複雜資料的維基百科摘要例子

我們來試一個稍微複雜一點的例子。我們會用 Python 的 `wikipedia` 套件取得整篇維基百科頁面的文章，並把它傳給 Claude。我們會用 Claude 產生一個包含下面這些內容的回答：

* 文章的主要主題
* 文章的摘要
* 文章中提到的關鍵字和主題清單
* 文章的分類清單（娛樂、政治、商業等）以及**分類分數**（也就是這個主題有多強烈地屬於那個分類）

如果我們把關於華特·迪士尼的維基百科文章傳給 Claude，可能會預期得到像這樣的結果：

```
{
  "subject": "Walt Disney",
  "summary": "Walter Elias Disney was an American animator, film producer, and entrepreneur. He was a pioneer of the American animation industry and introduced several developments in the production of cartoons. He held the record for most Academy Awards earned and nominations by an individual. He was also involved in the development of Disneyland and other theme parks, as well as television programs.",
  "keywords": [
    "Walt Disney",
    "animation",
    "film producer",
    "entrepreneur",
    "Disneyland",
    "theme parks",
    "television"
  ],
  "categories": [
    {
      "name": "Entertainment",
      "score": 0.9
    },
    {
      "name": "Business",
      "score": 0.7
    },
    {
      "name": "Technology",
      "score": 0.6
    }
  ]
}
```

（摘要大意：「華特·伊萊亞斯·迪士尼是美國的動畫師、電影製片人和企業家。他是美國動畫產業的先驅，在卡通製作上引進了多項發展。他保持個人獲得奧斯卡獎和提名次數最多的紀錄。他也參與了迪士尼樂園等主題樂園以及電視節目的開發。」分類：娛樂 0.9、商業 0.7、科技 0.6。）

下面是一個函式的實作範例：它接收一個維基百科頁面主題、找到文章、下載內容、傳給 Claude，然後印出產生的 JSON 資料。我們使用同樣的策略：定義一個工具來「指導」Claude 回答的形狀。

注意：如果你的電腦上還沒有 `wikipedia` 套件，記得先 `pip install wikipedia`！

{{cell 29}}

**逐行解說（重點）：**
- 工具 `print_article_classification`（印出文章分類結果）的 `input_schema` 有四個欄位：`subject`（主題，字串）、`summary`（一段摘要，字串）、`keywords`（關鍵字，**字串的陣列**）、`categories`（分類，**物件的陣列**，每個物件有 `name` 名稱和 `score` 0.0～1.0 的分數）。
- `wikipedia.page(subject, auto_suggest=True)`：取得維基百科頁面（`auto_suggest=True` 讓它自動修正拼字）。
- `page.content`：整篇文章的文字，放進 `<document>` 標籤。
- 提示詞：「使用 print_article_classification 工具。分類的例子有：政治、運動、科技、娛樂、商業。」

{{cells 30-32}}

（分別分析演員傑夫·高布倫、章魚、美國第 31 任總統赫伯特·胡佛的維基百科文章。）

---

## ✏️ 練習

用上面的策略寫一個叫做 `translate` 的函式：它接收一個英文單字或片語，產生一個結構化的 JSON 輸出，包含**原本的英文片語**，以及翻譯成**西班牙文、法文、日文和阿拉伯文**的片語。

下面是它應該怎麼運作的範例。

如果我們這樣呼叫：

```python
translate("how much does this cost")
```

（「這個多少錢」）

我們預期會得到像這樣的輸出：

```json
{
  "english": "how much does this cost",
  "spanish": "¿cuánto cuesta esto?",
  "french": "combien ça coûte?",
  "japanese": "これはいくらですか",
  "arabic": "كم تكلفة هذا؟"
}
```

**注意：如果你想印出結果，這行程式碼能幫你把它們漂亮地印出來：**

```python
print(json.dumps(translations_from_claude, ensure_ascii=False, indent=2))
```

（`ensure_ascii=False` 讓日文、阿拉伯文等非英文字元正常顯示，而不是變成 `こ` 這種跳脫碼。`translations_from_claude` 是你從 Claude 回應中取出的字典。）

> ⚠️ 原課程把上面兩段也放成程式碼格，但因為 `translate` 和 `translations_from_claude` 都還沒定義，直接執行會出錯，所以新手版改成只顯示的格式。

```python run
# 在這裡寫你的 translate 函式

```

<details>
<summary>👀 點這裡看參考答案（新手版補充，原課程沒有提供答案）</summary>

```python
translation_tools = [
    {
        "name": "print_translations",
        "description": "Prints a phrase in English along with its translations into Spanish, French, Japanese, and Arabic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "english": {"type": "string", "description": "The original phrase in English"},
                "spanish": {"type": "string", "description": "The phrase translated into Spanish"},
                "french": {"type": "string", "description": "The phrase translated into French"},
                "japanese": {"type": "string", "description": "The phrase translated into Japanese"},
                "arabic": {"type": "string", "description": "The phrase translated into Arabic"},
            },
            "required": ["english", "spanish", "french", "japanese", "arabic"],
        },
    }
]

def translate(phrase):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        tools=translation_tools,
        tool_choice={"type": "tool", "name": "print_translations"},   # 強制使用這個工具
        messages=[{"role": "user", "content": f"Translate this phrase: <phrase>{phrase}</phrase>"}],
    )
    translations_from_claude = None
    for content in response.content:
        if content.type == "tool_use" and content.name == "print_translations":
            translations_from_claude = content.input
            break
    if translations_from_claude:
        print(json.dumps(translations_from_claude, ensure_ascii=False, indent=2))
    else:
        print("沒有拿到翻譯結果")

translate("how much does this cost")
```

</details>

---

## 📌 重點整理

- **技巧**：定義一個工具，它的 `input_schema` 就是你想要的 **JSON 結構**；Claude 「呼叫」這個工具時，`input` 就是格式完美的資料——你**不需要真的執行**任何工具函式。
- 回應的 `content` 可能有好幾個區塊（例如先有文字再有工具使用），所以要用迴圈找出 `type == "tool_use"` 且 `name` 正確的那一塊。
- 讓 Claude 一定使用工具的兩種方法：
  1. 提示詞裡寫「Only use the xxx tool.」
  2. **`tool_choice={"type": "tool", "name": "xxx"}`**（更可靠）
- JSON Schema 可以描述複雜結構：`array` + `items`（清單）、`object` + `properties`（巢狀物件）。
- 印出含中日文等字元的 JSON：`json.dumps(資料, ensure_ascii=False, indent=2)`。

👉 下一課：[5-4 完整的工具使用流程](04_complete_workflow.md)
