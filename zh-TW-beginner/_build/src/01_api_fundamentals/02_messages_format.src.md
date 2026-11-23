<!--meta {"orig": "anthropic_api_fundamentals/02_messages_format.ipynb", "out": "01_api_fundamentals/02_messages_format"} -->
# 1-2 訊息格式（Messages）

> 📚 **第 1 單元：Claude API 基礎**｜第 2 課 / 共 6 課
> ⏱️ 預估時間：40 分鐘
> 🧰 先備知識：[0-4 Python 速成](../00_before_you_start/04_python_crash_course.md) 的第 5～7 節（串列、字典、訊息格式）

## 🎯 這一課你會學到

- 了解 Messages API 的訊息格式
- 學會讀懂、使用模型回傳的「回應物件」
- 做出一個簡單的「多回合」聊天機器人

> 🧩 **白話小補充**：「多回合（multi-turn）」就是你一句、它一句、你再一句⋯⋯可以一直聊下去的對話，而且 Claude 記得前面聊過什麼。

---

## 基本設定

首先，我們要匯入需要的套件，並建立客戶端物件。
怎麼取得 API 金鑰、怎麼安全地存放它，請參考上一課。

{{cell 3}}

**逐行解說：**
- `load_dotenv()`：讀取 `.env` 檔案裡的 API 金鑰（變成環境變數）。
- `client = Anthropic()`：建立客戶端。它會自動去找名叫 `ANTHROPIC_API_KEY` 的環境變數。

> ⚠️ 這一格**一定要先執行**，後面所有的程式碼都會用到 `client`。

---

## 訊息格式

就像上一課看到的，我們可以用 `client.messages.create()` 傳訊息給 Claude 並取得回應：

{{cell 5}}

這次我們不只印出文字，而是用 `print(response)` 把**整個回應物件**印出來。問題是「Dr. Pepper（一種美國汽水）用了哪些口味？」。可以看到回應裡除了 Claude 的回答文字，還有很多其他資訊（`id`、`model`、`usage`⋯⋯），等一下會一一說明。

我們先仔細看看這一段：

```py
messages=[
        {"role": "user", "content": "What flavors are used in Dr. Pepper?"}
    ]
```

`messages` 參數是跟 Claude API 互動時**最關鍵的部分**。你可以透過它提供「對話紀錄」和「上下文」，讓 Claude 根據這些資訊產生合適的回答。

`messages` 參數需要的是**一個串列，裡面裝著好幾個「訊息字典」**，每一個字典代表對話中的一則訊息。
每一個訊息字典都必須有下面這兩個 key：

* **`role`（角色）**：一個字串，表示「這則訊息是誰說的」。只能是 `"user"`（使用者傳的訊息）或 `"assistant"`（Claude 傳的訊息）。
* **`content`（內容）**：訊息的實際內容，可以是**一個字串**，或是**一個「內容字典」的串列**。如果給的是字串，它會被當成一個單純的文字內容區塊。如果給的是內容字典的串列，每個字典都要有 `"type"`（類型，例如 `"text"` 文字或 `"image"` 圖片）以及對應的內容。目前我們先讓 `content` 維持單純的字串就好。（傳圖片的寫法會在第 6 課教。）

下面是一個只有一則使用者訊息的 `messages` 串列範例：

```py
messages = [
    {"role": "user", "content": "Hello Claude! How are you today?"}
]
```

（使用者說：「哈囉 Claude！你今天好嗎？」）

下面則是一個有多則訊息、代表一段對話的範例：

```py
messages = [
    {"role": "user", "content": "Hello Claude! How are you today?"},
    {"role": "assistant", "content": "Hello! I'm doing well, thank you. How can I assist you today?"},
    {"role": "user", "content": "Can you tell me a fun fact about ferrets?"},
    {"role": "assistant", "content": "Sure! Did you know that excited ferrets make a clucking vocalization known as 'dooking'?"},
]
```

翻成中文是這樣的一段對話：
- 👤 使用者：「哈囉 Claude！你今天好嗎？」
- 🤖 Claude：「哈囉！我很好，謝謝。今天有什麼可以幫你的嗎？」
- 👤 使用者：「可以告訴我一個關於雪貂的有趣小知識嗎？」
- 🤖 Claude：「當然！你知道嗎？興奮的雪貂會發出一種咯咯叫的聲音，叫做『dooking』。」

請記住：**訊息一定是 `user` 和 `assistant` 輪流交替出現的。**

![訊息必須在 user 與 assistant 之間交替](@orig/images/alternating_messages.png)

訊息格式讓我們可以用「對話」的形式來組織對 Claude 的 API 呼叫，達到<strong>保留上下文（context preservation）</strong>的效果：訊息格式可以保存整段對話紀錄（包含使用者和 Claude 雙方的訊息），這確保 Claude 在產生回答時能看到完整的對話脈絡，回答也就會更連貫、更切題。

**注意：很多使用情境根本不需要對話紀錄，`messages` 串列裡只放一則訊息，完全沒有問題！**

> 🧩 **白話小補充：Claude 其實「沒有記憶」！**
> 這是新手最容易誤會的一點：每次呼叫 API，Claude 都是**從零開始**，它不會記得你上一次問了什麼。
> 我們之所以能「多回合聊天」，是因為**每次都把完整的對話紀錄重新傳一次給它**。就像每次見面都把之前的聊天紀錄整本拿給對方看，對方才能接著聊。

---

## 🧠 小測驗

每一則訊息必須有的兩個 key 是什麼？

* **a)** `"sender"` 和 `"text"`
* **b)** `"role"` 和 `"content"`
* **c)** `"user"` 和 `"assistant"`
* **d)** `"input"` 和 `"output"`

<details>
  <summary>點這裡看答案</summary>

  **正確答案是 b。每一則訊息都要有 `"role"`（角色）和 `"content"`（內容）。**

  （c 是常見的錯誤答案：`"user"` 和 `"assistant"` 是 `role` 可以填的「值」，不是 key。）

</details>

---

## 檢查回應的內容

接下來，我們來看看 Claude 傳回來的回應長什麼樣子。

先請 Claude 做一件簡單的事——「把 hello 翻成法文，只用一個字回答」：

{{cell 11}}

現在來檢查我們拿到的 `response` 裡面有什麼：

{{cell 13}}

> 💡 **小提醒**：在 notebook 裡，如果一格程式碼的**最後一行只寫一個變數名稱**（像上面的 `response`），notebook 就會自動把它的內容顯示出來，效果跟 `print(response)` 很像。

我們拿到的是一個 **`Message` 物件**，它裡面有好幾個屬性。範例如下：

```
Message(id='msg_01Mq5gDnUmDESukTgwPV8xtG', content=[TextBlock(text='Bonjour.', type='text')], model='claude-3-haiku-20240307', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(input_tokens=19, output_tokens=8))
```

其中**最重要的資訊是 `content` 屬性**：它裝著模型真正為我們產生的內容。`content` 是一個**內容區塊（content block）的串列**，每個區塊都有一個 `type`（類型），類型決定了這個區塊長什麼樣子。

![content 屬性裡裝的就是模型產生的內容](images/message_content.png)

（圖中藍色框框標示的 `content=[TextBlock(text='Bonjour', type="text")]` 就是「模型產生的內容」。）

要取出模型回答的文字內容，我們需要這樣寫：

{{cell 15}}

> 🧩 **白話小補充：一層一層拆開**
> - `response.content` → `[TextBlock(text='Bonjour.', type='text')]`，一個串列
> - `response.content[0]` → `TextBlock(text='Bonjour.', type='text')`，串列裡的第一個區塊
> - `response.content[0].text` → `'Bonjour.'`，那個區塊的文字

除了 `content` 以外，`Message` 物件還包含下面這些資訊：

* `id`：這個物件獨一無二的識別碼（就像訂單編號）。
* `type`：物件的類型，永遠都是 `"message"`。
* `role`：這則產生出來的訊息在對話中的角色，永遠都是 `"assistant"`。
* `model`：處理這個請求、產生這個回應的模型。
* `stop_reason`：模型**停止產生文字的原因**。我們之後會學到更多。
* `stop_sequence`：我們很快就會學到這是什麼。
* `usage`：計費和用量限制相關的資訊，包含：
    * `input_tokens`：這次使用了多少個「輸入 token」（你傳進去的文字）。
    * `output_tokens`：這次使用了多少個「輸出 token」（Claude 回答的文字）。

知道這些資訊都拿得到是很重要的，不過如果你只能記住一件事，請記住這個：**`content` 裝著模型真正產生的內容。**

---

## ✏️ 練習：翻譯函式

寫一個叫做 `translate` 的函式，它需要兩個參數：
* 一個單字（word）
* 一種語言（language）

當你呼叫 `translate` 函式時，它應該回傳「請 Claude 把 `word` 翻譯成 `language`」的結果。例如：

```py
translate("hello", "Spanish")
# 'The word "hello" translated into Spanish is: Hola'

translate("chicken", "Italian")
# 'The Italian word for "chicken" is: pollo'
```

**加分題**：如果你能寫出一個提示詞，讓 Claude **只回答翻譯後的單字**、不要有任何開場白，那就更棒了。像這樣：

```py
translate("chicken", "Italian")
# 'pollo'
```

> 💡 **提示**：用 [0-4 第 10 節](../00_before_you_start/04_python_crash_course.md#10-函式function) 學到的 `def` 定義函式，再用 f-string 把 `word` 和 `language` 塞進提示詞裡。

```python run
# 在這裡寫你的 translate 函式

```

<details>
  <summary>👀 點這裡看參考答案</summary>

  這是其中一種寫法：

  ```py
  def translate(word, language):
      response = client.messages.create(
          model="claude-haiku-4-5",
          max_tokens=1000,
          messages=[
              {"role": "user", "content": f"Translate the word {word} into {language}.  Only respond with the translated word, nothing else"}
          ]
      )
      return response.content[0].text

  print(translate("chicken", "Italian"))
  ```

  （原課程的參考答案用的是 `claude-3-opus-20240229`，已停用，這裡換成 `claude-haiku-4-5`。提示詞的意思是：「把 {word} 這個字翻譯成 {language}。只回答翻譯後的字，其他什麼都不要說。」）

</details>

---

## 訊息串列的常見錯誤

### 錯誤 1：用 assistant 訊息開頭

剛開始使用時，很容易在 `messages` 串列上犯錯。**訊息串列必須以 `user` 訊息開頭。** 下面的程式碼會產生錯誤，因為訊息串列是用 assistant 訊息開頭的：

{{cell 21}}

錯誤訊息的重點是：`first message must use the "user" role`（第一則訊息必須使用 "user" 角色）。

> 🧩 **白話小補充**：`BadRequestError: Error code: 400` 的意思是「你的請求格式不對，伺服器不接受」。400 是一種錯誤代碼，代表「是你這邊（送請求的人）的問題」。

### 錯誤 2：沒有正確交替

訊息必須在 `user` 和 `assistant` 之間**輪流交替**，如果沒有遵守這個規則，就會出錯：

{{cell 23}}

錯誤訊息的重點是：`roles must alternate between "user" and "assistant", but found multiple "assistant" roles in a row`（角色必須在 user 和 assistant 之間交替，但發現連續出現了好幾個 assistant）。

> 🔄 **2026 更新**：這兩個錯誤是原課程（2024 年）執行時的結果。之後 API 對這類格式規則可能有放寬（例如連續出現的相同角色訊息，可能會被自動合併成一則），所以你現在執行這兩格時，**不一定會看到一模一樣的錯誤**。不管有沒有報錯，「以 user 開頭、user 和 assistant 輪流交替」都是最穩當、最建議的寫法，請照著這個規則寫。

---

## 訊息串列的使用技巧

### 技巧 1：「幫 Claude 先說幾個字」（Putting words in Claude's mouth）

另一個能得到非常特定輸出的常見策略，是「**把話塞進 Claude 的嘴裡**」。我們不只提供 `user` 訊息給 Claude，也可以提供一則 `assistant` 訊息，讓 Claude 在產生回答時接著使用。

使用 Anthropic 的 API 時，你不只能傳 `user` 訊息。如果你提供了一則 `assistant` 訊息，**Claude 會從最後那則 `assistant` 訊息的最後一個 token 開始，接著繼續寫下去**。只是要記得：訊息還是必須以 `user` 訊息開頭。

假設我想請 Claude 幫我寫一首俳句，而且第一句必須是「calming mountain air」（寧靜的山間空氣）。我可以提供這樣的對話紀錄：

```py
messages=[
        {"role": "user", "content": f"Generate a beautiful haiku"},
        {"role": "assistant", "content": "calming mountain air"}
    ]
```

我們告訴 Claude「我們想要一首俳句」，**而且**把俳句的第一句「塞進 Claude 的嘴裡」。

{{cell 26}}

注意看結果：Claude 回答的開頭是一個逗號 `,`——因為它是**接著**「calming mountain air」繼續寫的，第一句不會再重複一次。

要得到「從我們提供的那一句開始」的完整俳句，可以把兩段接起來：

{{cell 28}}

> 🧩 **白話小補充**：這個技巧在其他課程裡也叫做 **prefill（預先填寫回答）**。在第 2 單元第 5 章會學到更多用法，例如先幫 Claude 寫好 `{`，逼它用 JSON 格式回答。
>
> 🔄 **2026 更新**：最新一代的模型（例如 Claude Haiku 5.5、Sonnet 4.6 以後、Opus 4.6 以後）**不支援** prefill，會回傳錯誤。新手版用的 `claude-haiku-4-5` 支援，所以這裡可以正常執行。

### 技巧 2：少量範例提示（Few-shot prompting）

最實用的提示策略之一叫做「**少量範例提示（few-shot prompting）**」，做法是提供模型少量的**範例**。這些範例能引導 Claude 產生你想要的輸出。而訊息格式的「對話紀錄」，正是提供範例給 Claude 的簡單方法。

舉例來說，假設我們想用 Claude 分析推文（tweet）裡的情緒。我們可以先直接問 Claude「請分析這則推文的情緒：」，看看會得到什麼樣的輸出：

{{cell 30}}

（推文內容：「剛吃了 @PickleCo 新出的辣味酸黃瓜，我的味蕾在跳快樂的舞！🌶️🥒 #愛酸黃瓜 #辣味美食」）

第一次執行上面的程式碼時，Claude 產生了一大段很長的回答（內容大意如下）：

> 這則推文的情緒非常正面。使用者用熱情的語言和表情符號，表達了對 @PickleCo 新款辣味酸黃瓜的喜愛。
>
> 正面的跡象：
> 1. 「我的味蕾在跳快樂的舞！」——這句話表示使用者非常滿意酸黃瓜的味道，滿意到產生了開心的身體反應。
> 2. 表情符號——辣椒 🌶️ 和小黃瓜 🥒 的表情符號，進一步強調了使用者對辣味酸黃瓜的興奮。
> 3. 主題標籤——#pickleslove 和 #spicyfood 表示使用者非常喜歡酸黃瓜和辣的食物，而這個新產品完全符合他的喜好。
> 4. 驚嘆號——第一句結尾的驚嘆號，加強了使用者正面體驗的語氣。
>
> 整體來說，這則推文傳達了對品嚐新款辣味酸黃瓜強烈的滿足、興奮和享受。

這是個很棒的回答，但它提供的資訊可能**遠超過我們需要的**——特別是如果我們想要「自動化」地分析大量推文的情緒時。

我們可能比較希望 Claude 用一種**標準化的格式**回答，例如一個單字（POSITIVE 正面、NEUTRAL 中立、NEGATIVE 負面）或一個數字（1、0、-1）。為了好讀又簡單，我們就讓 Claude 只回答「POSITIVE」或「NEGATIVE」。其中一種做法就是用少量範例提示。我們可以提供一段對話紀錄，**直接示範**我們希望它怎麼回答：

```py
messages=[
        {"role": "user", "content": "Unpopular opinion: Pickles are disgusting. Don't @ me"},
        {"role": "assistant", "content": "NEGATIVE"},
        {"role": "user", "content": "I think my love for pickles might be getting out of hand. I just bought a pickle-shaped pool float"},
        {"role": "assistant", "content": "POSITIVE"},
        {"role": "user", "content": "Seriously why would anyone ever eat a pickle?  Those things are nasty!"},
        {"role": "assistant", "content": "NEGATIVE"},
        {"role": "user", "content": "Just tried the new spicy pickles from @PickleCo, and my taste buds are doing a happy dance! 🌶️🥒 #pickleslove #spicyfood"},
    ]
```

這段「假的對話紀錄」翻成中文是：
- 👤「不受歡迎的意見：酸黃瓜超噁心。不要來吵我。」 → 🤖「NEGATIVE」
- 👤「我覺得我對酸黃瓜的愛可能有點失控了，我剛買了一個酸黃瓜造型的泳池浮板。」 → 🤖「POSITIVE」
- 👤「說真的，怎麼會有人想吃酸黃瓜？那東西超難吃！」 → 🤖「NEGATIVE」
- 👤（我們真正想分析的那則推文）

Claude 看了前面三個「範例」，就知道該怎麼回答第四個了：

{{cell 33}}

> 🧩 **白話小補充**：前面三組 user/assistant 對話其實**從來沒有真的發生過**，是我們自己編的範例。但 Claude 會把它們當成「之前的對話」，自然就學會了回答的格式。這就是「用範例教 Claude」的威力。第 2 單元第 7 章會更深入介紹。

---

## ✏️ 練習：做一個聊天機器人

### 你的任務：做一個聊天機器人

寫一個簡單的、可以多回合對話的「命令列聊天機器人」程式。訊息格式非常適合拿來做聊天類的應用程式。要用 Claude 做一個聊天機器人，步驟其實很簡單：

1. 準備一個串列，用來存放對話紀錄。
2. 用 `input()` 請使用者輸入訊息，然後把使用者的輸入加進訊息串列。
3. 把整個訊息紀錄傳給 Claude。
4. 把 Claude 的回答印出來給使用者看。
5. 把 Claude 的回答（assistant 訊息）也加進對話紀錄。
6. 回到第 2 步，一直重複！（用迴圈來做，並且要讓使用者有辦法結束對話！）

> 💡 **提示**：用 `while True:` 迴圈，當使用者輸入 `quit` 時用 `break` 跳出（[0-4 第 9 節](../00_before_you_start/04_python_crash_course.md#9-迴圈for-與-while)）。

```python run
# 在這裡寫你的聊天機器人

```

<details>
    <summary>👀 點這裡看參考答案</summary>

```py
conversation_history = []                      # 1. 準備一個空串列存放對話紀錄

while True:                                    # 6. 一直重複
    user_input = input("User: ")               # 2. 請使用者輸入

    if user_input.lower() == "quit":           # 輸入 quit 就結束
        print("Conversation ended.")
        break

    conversation_history.append({"role": "user", "content": user_input})   # 2. 加進紀錄

    response = client.messages.create(         # 3. 把整個對話紀錄傳給 Claude
        model="claude-haiku-4-5",
        messages=conversation_history,
        max_tokens=500
    )

    assistant_response = response.content[0].text
    print(f"Assistant: {assistant_response}")  # 4. 印出 Claude 的回答
    conversation_history.append({"role": "assistant", "content": assistant_response})  # 5. 加進紀錄
```

（每一行後面的中文註解，對應到上面的步驟編號。）
</details>

---

## 📌 重點整理

- `messages` 是**串列裡裝字典**，每則訊息都有 **`role`**（`"user"` 或 `"assistant"`）和 **`content`**。
- 訊息必須**以 `user` 開頭**，並且 **`user`、`assistant` 輪流交替**。
- Claude **沒有記憶**；多回合對話是靠每次都傳送完整的對話紀錄。
- 回應物件裡最重要的是 **`content`**；文字在 `response.content[0].text`。`usage` 記錄了 token 用量。
- **技巧**：最後放一則 `assistant` 訊息可以「幫 Claude 先說幾個字」（prefill）；放幾組假的 user/assistant 對話可以當作「範例」（few-shot）。

👉 下一課：[1-3 模型](03_models.md)
