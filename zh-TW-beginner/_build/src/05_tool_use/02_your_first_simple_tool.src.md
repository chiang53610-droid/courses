<!--meta {"orig": "tool_use/02_your_first_simple_tool.ipynb", "out": "05_tool_use/02_your_first_simple_tool"} -->
# 5-2 你的第一個簡單工具

> 📚 **第 5 單元：工具使用**｜第 2 課 / 共 6 課
> ⏱️ 預估時間：50 分鐘

## 🎯 這一課你會學到

- 寫一個真正的**計算機工具**：先寫 Python 函式，再寫**工具定義**
- 工具定義的三個部分：`name`、`description`、`input_schema`（JSON Schema）
- 用 `tools=[...]` 把工具交給 Claude，並從回應中擷取 `tool_use` 內容區塊
- 用系統提示詞避免 Claude 在不需要時亂用工具

> 🔄 **2026 更新**：這一課原本使用 `claude-3-haiku-20240307`，新手版換成 `claude-haiku-4-5`。下面顯示的執行結果是原課程用舊模型跑出來的（例如回應的類別名稱 `ToolsBetaMessage`，是當時工具功能還在「測試版」時的名稱，現在會顯示為 `Message`）。

---

在上一課，我們走過了工具使用的流程。現在是時候真正動手，實作一個簡單的工具使用範例了。複習一下，工具使用的流程最多有 4 個步驟：

1. **提供 Claude 工具和使用者提示詞**：（API 請求）
    * 定義你想讓 Claude 使用的一組工具，包括它們的名稱、描述和輸入格式。
    * 提供一個可能需要用到其中一個或多個工具才能回答的使用者提示詞。

2. **Claude 使用工具**：（API 回應）
    * Claude 評估使用者的提示詞，判斷可用的工具中有沒有能幫上使用者問題或任務的。如果有，它也會決定要用哪個（哪些）工具、輸入什麼。
    * Claude 輸出一個格式正確的工具使用請求。
    * API 回應的 `stop_reason` 會是 `tool_use`，表示 Claude 想使用一個外部工具。

3. **擷取工具輸入、執行程式碼、回傳結果**：（API 請求）
    * 在客戶端，你要從 Claude 的工具使用請求中擷取出工具名稱和輸入。
    * 在客戶端執行真正的工具程式碼。
    * 繼續這段對話，送出一則包含 `tool_result` 內容區塊的新使用者訊息，把結果回傳給 Claude。

4. **Claude 使用工具結果組織回答**：（API 回應）
    * 收到工具結果之後，Claude 會用這些資訊，針對原本的使用者提示詞組織出最終的回答。

我們先從一個只需要和 Claude「說話」一次的簡單示範開始（別擔心，很快就會有更精彩的例子！）。這代表我們**先不處理第 4 步**。我們會請 Claude 回答一個問題，Claude 會要求使用一個工具來回答，然後我們擷取工具的輸入、執行程式碼，並得到結果。

現今的大型語言模型**不太擅長數學運算**，下面的程式碼就是證明。

我們請 Claude「把 1984135 乘以 9343116」：

{{cell 2}}

（提示詞最後加了「Only respond with the result（只回答結果）」。）

多執行上面的程式碼幾次，很可能會得到不同的答案，但這是 Claude 回答過的其中一個答案：

```
18593367726060
```

真正的正確答案是：

```
18538003464660
```

Claude 只差了「一點點」——`55364261400`！（大約 553 億 😅）

> 🔄 **2026 更新**：新模型的計算能力比較好，你跑出來的答案可能比較接近，甚至剛好答對。但對於更大、更複雜的計算，LLM 還是可能出錯——**需要精確答案時，交給程式算最可靠**，這就是工具的價值。

---

## 工具使用來救援！

Claude 不太擅長做複雜的數學，所以我們讓 Claude 使用一個**計算機工具**，來增強它的能力。

這是一張說明流程的簡單圖：

![計算機工具的流程圖](@orig/images/chickens_calculator.png)

第一步是定義真正的計算機函式，並確保它能正常運作——這和 Claude 完全無關。我們會寫一個**非常**簡單的函式，它接收三個參數：
* 一個運算，例如 `"add"`（加）或 `"multiply"`（乘）
* 兩個運算元（要計算的兩個數字）

這是一個基本的實作：

{{cell 5}}

**逐行解說：**
- `def calculator(operation, operand1, operand2):`：定義計算機函式。
- `if operation == "add": return operand1 + operand2`：如果是 `"add"` 就相加。`subtract` 相減、`multiply` 相乘、`divide` 相除。
- `if operand2 == 0: raise ValueError("Cannot divide by zero.")`：除數是 0 時，主動丟出錯誤「不能除以零」。
- `else: raise ValueError(f"Unsupported operation: {operation}")`：其他不認識的運算，丟出錯誤「不支援的運算」。

請注意，這個簡單的函式用途相當有限，因為它只能處理像 `234 + 213` 或 `3 * 9` 這樣的簡單運算式。這裡的重點是透過一個非常簡單的教學範例，走過使用工具的流程。

我們來測試一下函式，確保它能正常運作。

{{cells 7-8}}

（`200 / 25` 的結果是 `8.0`——Python 的除法 `/` 一定會得到小數。）

下一步是**定義我們的工具**，並告訴 Claude。定義工具時，我們要遵循一個非常特定的格式。每個工具定義都包含：

* **`name`**：工具的名稱。必須符合正規表達式 `^[a-zA-Z0-9_-]{1,64}$`。（白話：只能用英文字母、數字、底線 `_`、連字號 `-`，長度 1～64 個字元。）
* **`description`**：用純文字詳細描述這個工具**做什麼**、**什麼時候應該使用它**，以及**它的行為**。
* **`input_schema`**：一個 **JSON Schema** 物件，定義工具預期的參數。

對 JSON Schema 不熟嗎？[在這裡了解更多](https://json-schema.org/learn/getting-started-step-by-step)。

> 🧩 **白話小補充：JSON Schema 是什麼？** 它是一種「描述 JSON 資料應該長什麼樣子」的規格，就像一張**表單的欄位說明**：有哪些欄位、每個欄位是什麼型別（文字 `string`、數字 `number`、整數 `integer`、布林 `boolean`、陣列 `array`、物件 `object`）、哪些是必填的。Claude 會照著這張「表單說明」來填寫工具的輸入。

這是一個假想工具的簡單範例：

```json
{
  "name": "send_email",
  "description": "Sends an email to the specified recipient with the given subject and body.",
  "input_schema": {
    "type": "object",
    "properties": {
      "to": {
        "type": "string",
        "description": "The email address of the recipient"
      },
      "subject": {
        "type": "string",
        "description": "The subject line of the email"
      },
      "body": {
        "type": "string",
        "description": "The content of the email message"
      }
    },
    "required": ["to", "subject", "body"]
  }
}
```

這個叫做 `send_email`（寄送電子郵件）的工具（說明：「用給定的主旨和內文，寄一封電子郵件給指定的收件人」），預期有下面這些輸入：
* `to`（收件人的電子郵件地址）：字串，必填
* `subject`（信件主旨）：字串，必填
* `body`（信件內容）：字串，必填

這是另一個叫做 `search_product`（搜尋商品）的工具定義：

```json
{
  "name": "search_product",
  "description": "Search for a product by name or keyword and return its current price and availability.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The product name or search keyword, e.g. 'iPhone 13 Pro' or 'wireless headphones'"
      },
      "category": {
        "type": "string",
        "enum": ["electronics", "clothing", "home", "toys", "sports"],
        "description": "The product category to narrow down the search results"
      },
      "max_price": {
        "type": "number",
        "description": "The maximum price of the product, used to filter the search results"
      }
    },
    "required": ["query"]
  }
}
```

（說明：「用名稱或關鍵字搜尋商品，並回傳它目前的價格和庫存狀況。」）

這個工具有 3 個輸入：
* 必填的 `query`（查詢）字串，代表商品名稱或搜尋關鍵字（例如「iPhone 13 Pro」或「無線耳機」）
* 選填的 `category`（分類）字串，必須是預先定義好的值之一（電子產品、服飾、居家、玩具、運動），用來縮小搜尋範圍。注意定義裡的 **`"enum"`**。
* 選填的 `max_price`（最高價格）數字，用來篩選低於某個價格的結果

> 🧩 **白話小補充**：
> - `"enum": [...]`（列舉）：限定只能填清單裡的其中一個值，就像表單的「下拉式選單」。
> - 沒有列在 `"required"` 裡的欄位就是**選填**的，Claude 可以不填。

### 我們的計算機工具定義

我們來為前面寫的計算機函式，定義對應的工具。我們知道計算機函式有 3 個必填的參數：
* `operation`（運算）：只能是 `"add"`、`"subtract"`、`"multiply"` 或 `"divide"`
* `operand1`（第一個運算元）：應該是一個數字
* `operand2`（第二個運算元）：也應該是一個數字

這是工具定義：

{{cell 11}}

（`description`：「一個執行基本算術運算的簡單計算機。」`operation` 用 `enum` 限定四種運算；兩個運算元的型別是 `number`（數字）；三個都是必填。）

---

## ✏️ 練習

我們來練習寫一個格式正確的工具定義，用下面這個函式當作範例：

{{cell 14}}

（這個函式什麼都不做，註解說：「你不需要碰它或對它做任何事！」）

這個假想的 `inventory_lookup`（庫存查詢）函式應該像這樣被呼叫：

{{cell 16}}

（查詢「AA 電池」最多 4 筆結果、查詢「生日蠟燭」最多 10 筆結果。）

你的任務是寫一個對應的、格式正確的工具定義。假設在你的工具定義中，**兩個參數都是必填的**。

```python run
# 在這裡寫你的 inventory_lookup 工具定義
inventory_lookup_tool = {

}
```

<details>
<summary>👀 點這裡看參考答案（新手版補充，原課程沒有提供答案）</summary>

```python
inventory_lookup_tool = {
    "name": "inventory_lookup",
    "description": "Looks up a product in the store's inventory by name and returns up to max_results matching items.",
    "input_schema": {
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "description": "The name of the product to search for, e.g. 'AA batteries'"
            },
            "max_results": {
                "type": "integer",
                "description": "The maximum number of results to return"
            }
        },
        "required": ["product_name", "max_results"]
    }
}
```

（`max_results` 用 `integer`（整數）比 `number` 更精確，因為結果的筆數不會是小數。）

</details>

---

### 把工具交給 Claude

現在回到前面的計算機函式。到目前為止，**Claude 對計算機工具一無所知！** 它只是一個小小的 Python 字典。在對 Claude 送出請求時，我們可以傳入一個工具清單，「告訴」Claude 有哪些工具。我們現在就來試試：

{{cell 20}}

（註解「Tell Claude about our tool」= 告訴 Claude 我們的工具。重點是 `tools=[calculator_tool]` 這個參數。）

接著，我們看看 Claude 回傳給我們的回應：

{{cell 22}}

```
ToolsBetaMessage(id='msg_01UfKwdmEsgTh99wfpgW4NJ7', content=[ToolUseBlock(id='toolu_015wQ7Wipo589yT9B3YTwjF1', input={'operand1': 1984135, 'operand2': 9343116, 'operation': 'multiply'}, name='calculator', type='tool_use')], model='claude-3-haiku-20240307', role='assistant', stop_reason='tool_use', stop_sequence=None, type='message', usage=Usage(input_tokens=420, output_tokens=93))
```

你可能會注意到，我們的回應看起來和平常有點不一樣！具體來說，我們拿到的不是一般的 `Message`，而是一個 `ToolsMessage`。（🔄 現在的 SDK 會顯示為一般的 `Message`。）

另外，我們可以檢查 `response.stop_reason`，看到 Claude 停下來是因為它決定**該使用工具了**：

{{cell 25}}

`response.content` 包含一個串列，裡面有一個 **`ToolUseBlock`（工具使用區塊）**，它本身包含了工具名稱和輸入的資訊：

{{cell 27}}

> 🧩 **白話小補充：`ToolUseBlock` 裡有什麼？**
> - `id`：這次工具呼叫的編號（例如 `toolu_015wQ...`），回傳結果時會用到（第 4 課）。
> - `name`：Claude 想用的工具名稱 → `'calculator'`
> - `input`：Claude 填好的輸入（一個字典）→ `{'operand1': 1984135, 'operand2': 9343116, 'operation': 'multiply'}`
> - `type`：區塊類型 → `'tool_use'`

{{cell 28}}

（`response.content[0].name` 取出工具名稱，`response.content[0].input` 取出輸入。印出：「Claude 想呼叫的工具名稱：calculator」、「Claude 想用來呼叫它的輸入：{...}」。）

> ⚠️ **小提醒**：新模型有時候會在 `tool_use` 區塊**前面**先加一段文字說明（例如「我來用計算機算一下」），這時候 `content[0]` 會是文字區塊，`content[1]` 才是工具使用區塊。比較保險的寫法是「找出 `type == "tool_use"` 的那一塊」，例如：
> ```python
> tool_use = next(block for block in response.content if block.type == "tool_use")
> ```
> 下面「全部組合起來」的程式碼用的是 `response.content[-1]`（最後一塊），也是一種處理方式。

下一步很簡單：拿 Claude 提供給我們的工具名稱和輸入，真的去呼叫我們前面寫的計算機函式。然後我們就有最終答案了！

{{cell 30}}

我們得到了正確答案 `18538003464660`！！！我們不再依賴 Claude 把數學算對，而是**問 Claude 一個問題，並給它一個在必要時可以決定使用的工具**。

#### 重要提醒

如果我們問 Claude 一個**不需要**使用工具的問題——在這個例子中，就是和數學或計算無關的事——我們大概會希望它照常回答。Claude 通常會這樣做，但有時候 Claude **非常熱衷於使用它的工具**！

下面這個例子中，Claude 有時候會嘗試使用計算機，即使使用它根本不合理。我們來看看問 Claude「綠寶石是什麼顏色？」會發生什麼事：

{{cell 32}}

{{cell 33}}

Claude 給了我們這個回應：

```
ToolsBetaMessage(id='msg_01Dj82HdyrxGJpi8XVtqEYvs', content=[ToolUseBlock(id='toolu_01Xo7x3dV1FVoBSGntHNAX4Q', input={'operand1': 0, 'operand2': 0, 'operation': 'add'}, name='calculator', type='tool_use')], model='claude-3-haiku-20240307', role='assistant', stop_reason='tool_use', stop_sequence=None, type='message', usage=Usage(input_tokens=409, output_tokens=89))

```

Claude 想要我們呼叫計算機工具？（還要算 0 + 0 🤔）一個非常簡單的修正方法，是調整提示詞，或加上一個系統提示詞，大概這樣說：`You have access to tools, but only use them when necessary. If a tool is not required, respond as normal`（你可以使用工具，但只在必要時使用。如果不需要工具，就照常回答）：

{{cell 35}}

{{cell 36}}

現在 Claude 回覆了適當的內容，沒有在不合理的時候硬要使用工具。這是我們得到的新回應：

```
'Emeralds are green in color.'
```

（「綠寶石是綠色的。」）

我們也可以看到，`stop_reason` 現在是 `end_turn`，而不是 `tool_use`。

{{cell 38}}

> 🔄 **2026 更新**：新模型判斷「該不該用工具」的能力好很多，你跑的時候 Claude 很可能**不加系統提示詞也不會亂用計算機**。不過加上「只在必要時使用工具」的提示，仍然是很好的習慣。

---

### 全部組合起來

{{cell 41}}

**逐行解說 `prompt_claude(prompt)`：**
- 送出請求時帶上系統提示詞（只在必要時用工具）和 `tools=[calculator_tool]`。
- `if response.stop_reason == "tool_use":`：如果 Claude 想用工具：
  - `tool_use = response.content[-1]`：取出最後一個內容區塊（工具使用區塊通常在最後）。
  - 取出 `name` 和 `input`。
  - 如果工具名稱是 `"calculator"`，就取出三個輸入，呼叫 `calculator(...)`。
  - `try` / `except ValueError as e:`：如果計算時出錯（例如除以零），印出錯誤訊息而不是讓程式當掉。
- `elif response.stop_reason == "end_turn":`：如果 Claude 沒有用工具，就直接印出它的回答。

{{cells 42-44}}

（「我有 23 隻雞，但飛走了 2 隻，還剩幾隻？」→ 用計算機算出 21；「201 乘以 2 是多少？」→ 402；「寫一首關於海洋的俳句」→ 不用工具，直接回答。注意：原課程的輸出顯示「Claude want to」，但程式碼裡寫的是「Claude wants to」——輸出是更早版本的程式碼跑出來的，不影響理解。）

---

## ✏️ 練習：研究助理

你的任務是幫忙用 Claude 打造一個**研究助理**。使用者可以輸入一個想研究的主題，然後得到一份**維基百科文章連結清單**，存進一個 markdown 檔案，方便之後閱讀。我們可以試著直接請 Claude 產生一份文章網址清單，但 **Claude 對網址並不可靠，可能會幻想出不存在的文章網址**。而且，真正存在的文章在 Claude 的訓練資料截止日之後，也可能已經搬到新的網址了。所以，我們要使用一個**連接到真正維基百科 API 的工具**來完成這件事！

我們會讓 Claude 使用一個工具：它接收一份 Claude 產生的「可能的維基百科文章標題」清單（這些標題可能是幻想出來的）。我們可以用這個工具搜尋維基百科，找出**真正的**維基百科文章標題和網址，確保最終的清單裡都是真正存在的文章。然後，我們會把這些文章網址存進一個 markdown 檔案，方便之後閱讀。

我們提供了兩個函式來幫助你：

> 💡 **新手版補充：開始之前**
> 1. 這個練習需要 `wikipedia` 套件，請先執行 `%pip install wikipedia`。
> 2. 程式會把結果寫進 `output/research_reading.md`。原課程說這個檔案「在這個 repo 裡已經存在」，但實際上沒有，所以請先執行下面這格建立 `output` 資料夾（在這份 notebook 所在的資料夾裡）：

```python run
%pip install wikipedia
import os
os.makedirs("output", exist_ok=True)   # 建立 output 資料夾；已經存在的話也不會出錯
print("output 資料夾準備好了！")
```

{{cell 47}}

第一個函式 `generate_wikipedia_reading_list`，預期會收到一個研究主題（例如「夏威夷的歷史」或「世界各地的海盜」），以及一份我們會請 Claude 產生的「可能的維基百科文章名稱」清單。這個函式使用 `wikipedia` 套件，搜尋對應的**真正**維基百科頁面，並建立一個包含文章標題和網址的字典串列。

接著，它會呼叫 `add_to_research_reading_file`，傳入維基百科文章資料的串列和整體的研究主題。這個函式只是把每篇維基百科文章的 markdown 連結，加到一個叫做 `output/research_reading.md` 的檔案裡。檔名目前是寫死的，而且函式假設這個檔案已經存在。它在這個 repo 裡已經存在了，但如果你在別的地方執行，就需要自己建立它。

> 🧩 **逐行解說（重點）：**
> - `wikipedia.search(t)`：用標題 `t` 搜尋維基百科，回傳一串可能的結果。
> - `wikipedia.page(results[0])`：取第一個搜尋結果的頁面。
> - `page.title`、`page.url`：真正的文章標題和網址。
> - `try: ... except: continue`：如果找不到或出錯，就跳過這個標題，繼續下一個。
> - `open("output/research_reading.md", "a", encoding="utf-8")`：`"a"` 是「append（附加）」模式——把內容加到檔案最後面，而不是覆蓋掉。
> - `file.write(f"* [{title}]({url}) \n")`：寫入一行 markdown 連結，例如 `* [Piracy](https://en.wikipedia.org/wiki/Piracy)`。

我們的想法是：讓 Claude 用一份「可能真實、也可能不存在」的文章標題清單，「呼叫」`generate_wikipedia_reading_list`。Claude 可能會傳入下面這份文章標題清單，其中有些是真正的維基百科文章，有些不是：

```py
["Piracy", "Famous Pirate Ships", "Golden Age Of Piracy", "List of Pirates", "Pirates and Parrots", "Piracy in the 21st Century"]
```

（海盜行為、著名海盜船、海盜黃金時代、海盜列表、海盜與鸚鵡、21 世紀的海盜行為。）

`generate_wikipedia_reading_list` 函式會逐一處理這些文章標題，收集所有真正存在的維基百科文章的真實標題和對應網址。然後它會呼叫 `add_to_research_reading_file`，把這些內容寫進一個 markdown 檔案，方便之後參考。

### 最終目標

你的工作是實作一個叫做 **`get_research_help`** 的函式，它接收一個研究主題和想要的文章數量。這個函式應該使用 Claude 真正產生「可能的維基百科文章」清單，並呼叫上面的 `generate_wikipedia_reading_list` 函式。下面是幾個呼叫範例：

```py
get_research_help("Pirates Across The World", 7)

get_research_help("History of Hawaii", 3)

get_research_help("are animals conscious?", 3)
```

（世界各地的海盜 7 篇、夏威夷的歷史 3 篇、動物有意識嗎？3 篇。）

執行這 3 個函式呼叫之後，我們輸出的 `research_reading.md` 檔案長這樣（可以自己在 `output/research_reading.md` 看看）：

![research_reading.md 檔案的內容](@orig/images/research_reading.png)

要完成這個任務，你需要做下面這些事：

* 為 `generate_wikipedia_reading_list` 函式寫一個**工具定義**
* 實作 `get_research_help` 函式
    * 寫一個給 Claude 的提示詞，告訴它你需要幫忙蒐集某個特定主題的研究資料，以及你想要它產生幾個文章標題
    * 告訴 Claude 它可以使用的工具
    * 把請求送給 Claude
    * 檢查 Claude 有沒有呼叫工具。如果有，你需要把它產生的文章標題和主題傳給我們提供的 `generate_wikipedia_reading_list` 函式。那個函式會蒐集真正的維基百科文章連結，然後呼叫 `add_to_research_reading_file`，把連結寫進 `output/research_reading.md`
    * 打開 `output/research_reading.md` 看看是否成功！

##### 起始程式碼

{{cell 52}}

（註解「Here's your starter code!」= 這是你的起始程式碼！`get_research_help` 裡的註解「Implement this function!」= 實作這個函式！`pass` 代表「這裡先什麼都不做」，是 Python 的佔位寫法。）

<details>
<summary>👀 點這裡看參考答案（新手版補充，原課程沒有提供答案）</summary>

```python
# 1. 工具定義
wikipedia_tool = {
    "name": "generate_wikipedia_reading_list",
    "description": "Generates a list of real Wikipedia articles for a research topic. "
                   "Takes a list of possible Wikipedia article titles, finds the real matching articles, "
                   "and saves their titles and URLs to a reading list file.",
    "input_schema": {
        "type": "object",
        "properties": {
            "research_topic": {
                "type": "string",
                "description": "The topic being researched, e.g. 'History of Hawaii'"
            },
            "article_titles": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of possible Wikipedia article titles related to the topic"
            }
        },
        "required": ["research_topic", "article_titles"]
    }
}

# 2. 實作 get_research_help
def get_research_help(topic, num_articles=3):
    prompt = f"""I need your help gathering research on the topic: {topic}.
Please come up with {num_articles} possible Wikipedia article titles about this topic,
and use the generate_wikipedia_reading_list tool to save them to my reading list."""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
        tools=[wikipedia_tool],
    )

    if response.stop_reason == "tool_use":
        # 找出 tool_use 區塊（前面可能還有一段文字區塊）
        tool_use = next(block for block in response.content if block.type == "tool_use")
        if tool_use.name == "generate_wikipedia_reading_list":
            print("Claude 想查的文章標題：", tool_use.input["article_titles"])
            generate_wikipedia_reading_list(
                tool_use.input["research_topic"],
                tool_use.input["article_titles"],
            )
            print("完成！請打開 output/research_reading.md 看看結果")
    else:
        print("Claude 沒有使用工具，它說：", response.content[0].text)

get_research_help("Pirates Across The World", 7)
get_research_help("History of Hawaii", 3)
get_research_help("are animals conscious?", 3)
```

**重點說明：**
- `"type": "array", "items": {"type": "string"}`：代表這個參數是「**一串字串**」（字串的陣列/串列）。
- 在提示詞中**明確請 Claude 使用這個工具**，它就會照做。下一課（5-3）和第 5 課（5-5）會教更直接的方法：用 `tool_choice` 強制 Claude 使用某個工具。

</details>

---

## 📌 重點整理

- 實作工具的第一步：**先寫好 Python 函式，並確認它單獨就能正常運作**。
- **工具定義**三要素：
  - `name`：英數字、底線、連字號，1～64 字元
  - `description`：詳細說明做什麼、什麼時候用
  - `input_schema`：JSON Schema（`type`、`properties`、`required`；可以用 `enum` 限定選項、`array` 表示清單）
- 呼叫時加上 `tools=[工具定義]`；如果 Claude 想用工具，`stop_reason == "tool_use"`，`content` 裡會有 `type == "tool_use"` 的區塊（含 `id`、`name`、`input`）。
- 取出 `name` 和 `input` → 呼叫你自己的函式 → 得到結果。
- 用系統提示詞「只在必要時使用工具」，避免 Claude 亂用工具。

👉 下一課：[5-3 用工具使用強制輸出 JSON](03_structured_outputs.md)
