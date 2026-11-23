<!--meta {"orig": "anthropic_api_fundamentals/05_Streaming.ipynb", "out": "01_api_fundamentals/05_Streaming"} -->
# 1-5 串流（Streaming）

> 📚 **第 1 單元：Claude API 基礎**｜第 5 課 / 共 6 課
> ⏱️ 預估時間：45 分鐘
> 🧰 這一課的程式碼比較長，看不懂的語法可以先跳過，**抓住觀念最重要**。

## 🎯 這一課你會學到

* 了解串流（streaming）是怎麼運作的
* 學會處理串流「事件（event）」

> 🧩 **白話小補充：串流是什麼？**
> 想像你在等外送：
> - **不用串流**：店家把所有菜都做完，才一次全部送來。你要等很久才看到第一道菜。
> - **用串流**：店家做好一道就送一道。你很快就能開始吃第一道，雖然全部送完的時間差不多。
>
> Claude 的回答也一樣：用串流的話，Claude 每寫出一小段文字，就馬上傳給你，你不用等它全部寫完。你在 claude.ai 網頁上看到文字「一個字一個字跑出來」，就是串流的效果。

---

我們先匯入 `anthropic` SDK，並設定好客戶端：

{{cell 2}}

到目前為止，我們都是用下面這種寫法傳訊息給 Claude：

{{cell 4}}

（請 Claude「寫一篇關於亞馬遜雨林裡的金剛鸚鵡和『黏土舔食地』的文章」。注意這裡有用到上一課學的 `temperature=0`。）

這樣寫完全沒問題，但要記得：用這種方法，我們必須**等到所有內容都產生完畢**，才會從 API 拿到內容。試著再執行一次上面那一格，你會發現在整個回答一次全部印出來之前，畫面上什麼都不會出現。這在很多情況下沒有關係，但如果你在做一個應用程式，讓使用者一直乾等整個回答產生完畢，使用者體驗就會很差。

**這時候就輪到串流登場了！**

串流讓我們可以寫出「**模型一邊產生內容、我們一邊接收**」的應用程式，而不用等整個回答都產生完。claude.ai 這類應用程式就是這樣運作的：模型產生回答的同時，內容就被串流到使用者的瀏覽器上顯示出來：

![claude.ai 一邊產生一邊顯示文字的動畫](@orig/images/claude_streaming.gif)

---

## 使用串流

要從 API 取得串流回應，非常簡單：只要在 `client.messages.create` 裡加上 **`stream=True`** 就好。這是簡單的部分。比較麻煩的地方在於：之後要怎麼處理這個串流回應、怎麼處理一筆一筆進來的資料。

{{cell 7}}

（請 Claude「寫一個由 3 個字組成的句子，不要開場白，只要給我 3 個字」。）

我們來看看 `stream` 這個變數：

{{cell 9}}

沒什麼東西可以看！這個串流物件本身不會幫我們做太多事。串流物件是一個「**產生器（generator）物件**」，它會在收到 API 傳來的資料時，一個一個地吐出「**伺服器推送事件（server-sent events，簡稱 SSE）**」。我們需要寫程式去**一個一個地讀取**它，處理每一個伺服器推送事件。記住：我們的資料不再是一整塊、已經完成的資料了。我們來試試看用迴圈讀取這個串流回應：

{{cell 11}}

> 🧩 **白話小補充**：「產生器」就像一台「出餐機」，你每跟它要一次，它才給你下一份。用 `for event in stream:` 就是「一直跟它要，直到它說沒有了為止」。
>
> ⚠️ **注意**：一個串流**只能讀一次**。上面的迴圈讀完之後，`stream` 就空了。想再讀一次，必須重新送出請求。

可以看到，我們從 API 收到了**很多個**伺服器推送事件。我們來仔細看看這些事件代表什麼意思。下面是用顏色標示的說明：

![串流事件的顏色標示說明](@orig/images/streaming_output.png)

每一個串流都包含一連串**依照下面順序**出現的事件：
* **MessageStartEvent**（訊息開始事件）：一則內容是空的訊息
* **一連串的內容區塊（content block）**，每一個內容區塊包含：
    * 一個 **ContentBlockStartEvent**（內容區塊開始事件）
    * 一個或多個 **ContentBlockDeltaEvent**（內容區塊增量事件）
    * 一個 **ContentBlockStopEvent**（內容區塊結束事件）
* 一個或多個 **MessageDeltaEvent**（訊息增量事件），表示最終訊息在最上層有了變化
* 最後一個 **MessageStopEvent**（訊息結束事件）

上面那個回應中只有一個內容區塊。這張圖顯示了跟它相關的所有事件：

![一個內容區塊相關的所有串流事件](@orig/images/content_block_streaming.png)

> 🧩 **白話小補充**：「delta（增量）」的意思是「新增加的那一小塊」。每個 ContentBlockDeltaEvent 都帶著 Claude 新寫出來的一小段文字，把所有的 delta 依序接起來，就是完整的回答。

我們真正在意的「模型產生的內容」，全部都來自 **ContentBlockDeltaEvent**，它們的 `type` 都是 `"content_block_delta"`。要取得內容本身，我們要讀取 `delta` 裡面的 `text` 屬性。我們來試試看**只印出**產生的文字：

{{cell 16}}

**逐行解說：**
- `for event in stream:`：一個一個讀取事件。
- `if event.type == "content_block_delta":`：只處理「內容增量」事件，其他事件都忽略。
- `print(event.delta.text)`：印出這次新增加的那一小段文字。

我們成功地印出了內容，不過格式有點難讀（每一小段都換了一行）。用 Python 的 `print()` 函式印出串流文字時，多加兩個參數會很有用：
* **`end=""`**：在預設情況下，`print()` 函式會在印出的文字最後面加上一個換行字元（`\n`）。設定 `end=""`，就是指定印出的文字後面**不要**加換行字元。這代表下一次 `print()` 會在同一行繼續印。
* **`flush=True`**：把 `flush` 參數設成 `True`，會強迫輸出**立刻**顯示在螢幕上，而不是等到遇到換行字元、或緩衝區滿了才顯示。這確保文字從串流回應收到時，就能即時顯示出來。

我們來加上這兩個修改：

{{cell 18}}

文字這麼短的話，可能看不太出串流的效果。我們請模型產生長一點的內容試試看：

{{cell 20}}

（問題：「大型語言模型是怎麼運作的？」）

如果你還沒執行過上面那一格，試著執行看看。你應該會看到文字**一點一點地**印出來！

我們已經知道，ContentBlockDeltaEvent 裡裝著模型產生的文字內容。還有很多其他的事件，我們需要在意它們嗎？需要！這裡舉一個簡單的例子：

如果我們想知道 token 的用量資訊，就需要看兩個地方：

* **`MessageStartEvent`** 裡有我們的輸入（提示詞）token 用量資訊
* **`MessageDeltaEvent`** 裡有模型產生了多少輸出 token 的資訊

![token 用量資訊在哪些事件裡](@orig/images/streaming_tokens.png)

我們來修改上面的程式碼，印出提示詞用了多少 token、模型產生了多少 token：

{{cell 23}}

**逐行解說：**
- `if event.type == "message_start":`：如果是「訊息開始」事件 → 從 `event.message.usage.input_tokens` 拿到輸入 token 數，印出來。
- `elif event.type == "content_block_delta":`：如果是「內容增量」事件 → 印出文字。
- `elif event.type == "message_delta":`：如果是「訊息增量」事件 → 從 `event.usage.output_tokens` 拿到輸出 token 數，印出來。

### 其他串流事件類型

使用串流時，你可能還會遇到其他類型的事件，包括：

* **Ping 事件**：串流裡可能會包含任意數量的 ping 事件。（🧩 ping 就像「我還在喔」的打招呼訊號，用來確認連線沒斷，可以忽略。）
* **錯誤事件（Error events）**：你偶爾可能會在事件串流中看到錯誤事件。例如在使用量很高的時候，你可能會收到 `overloaded_error`（伺服器過載錯誤），在不使用串流的情況下，它通常對應到 HTTP 529 錯誤。

下面是一個錯誤事件的範例：

```
event: error
data: {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}
```

---

## 第一個 token 的等待時間（TTFT）

使用串流**最主要的原因**，就是改善「**第一個 token 的等待時間**」（Time To First Token，簡稱 **TTFT**）：也就是你或你的使用者收到「模型產生的第一點內容」所需要的時間。
我們來示範一下串流對 TTFT 的影響。

先從「不使用串流」的方法開始。我們請模型產生一段非常長的文字，但在 500 個 token 時切斷：

{{cell 26}}

（提示詞：「寫一篇很長的文章，解釋美國獨立革命的歷史」。原文的 `mme` 是原作者的錯字，應該是 `me`，不影響結果。）

{{cell 27}}

接著，用串流的方法做同樣的事：

{{cell 29}}

**逐行解說（重點部分）：**
- `have_received_first_token = False`：一個「開關」，記錄「是不是已經收到第一個 token 了」，一開始是「還沒」。
- 收到第一個 `content_block_delta` 時：計算 `ttft = 現在時間 - 開始時間`，然後把開關設成 `True`，之後就不會再算了。
- 收到 `message_delta` 時：記下輸出 token 數和總共花的時間。

{{cell 30}}

我們來比較一下結果。

* **不使用串流**
    * **收到第一個 token 的時間：** 4.194 秒
    * **收到完整回應的時間：** 4.194 秒
    * **產生的 token 總數：** 500
* **使用串流**
    * **收到第一個 token 的時間：** 0.492 秒
    * **收到完整回應的時間：** 4.274 秒
    * **產生的 token 總數：** 500

可以看到，TTFT 的差異非常大！這個示範只產生了 500 個 token，而且用的是我們最快的模型 Haiku。如果我們試一個用 Opus 產生 1000 個 token 的例子，數字會差得更多！

{{cell 32}}

（這個函式裡面「定義了兩個小函式」：一個用串流、一個不用串流，都請 Opus 寫「一篇非常非常長的美國獨立革命史文章」，最多 1000 個 token，然後比較兩者的 TTFT。）

{{cell 33}}

> ⚠️ 上面那格的註解寫著「**不要執行這格！** 它要跑超過一分鐘，而且會用 Opus 產生大約 2000 個 token！」——Opus 比較貴，看原課程的結果就好。

當我們用 Opus 產生比較長的文字時，串流對 TTFT 的影響就更明顯了。不用串流的話，我們等了 **47 秒**才拿到第一個 token。用串流的話，只要 **1.8 秒**就拿到第一個 token 了！

**注意：記住，串流並不會神奇地縮短模型產生回應的「總時間」。我們拿到第一批資料的速度快很多，但從送出請求到收到最後一個產生的 token，花的時間還是一樣的。**

---

## 串流小幫手（Streaming helpers）

Python SDK 提供了好幾個讓串流更方便的工具。我們可以不用「`client.messages.create` 加上 `stream=True`」的寫法，改用 **`client.messages.stream`**，就能使用一些好用的小幫手方法。`client.messages.stream()` 會回傳一個 `MessageStreamManager`，它是一個「**情境管理器（context manager）**」，會產生一個 `MessageStream`——這個 MessageStream 可以用迴圈讀取、會發出事件，而且會幫你把訊息累積起來。

> 🧩 **白話小補充**：「情境管理器」就是可以搭配 `with` 使用的東西（[0-4 第 16-1 節](../00_before_you_start/04_python_crash_course.md#16-1-with用完自動收拾)），區塊結束時會自動幫你收尾（關閉連線）。

下面的程式碼使用 `client.messages.stream`，讓我們可以用像 **`stream.text_stream`** 這樣的小幫手，輕鬆取得串流進來的文字內容，而不需要自己手動檢查串流事件的類型。`stream.text_stream` 提供一個**只包含文字增量**的迭代器。

還有其他好用的小幫手方法，例如 **`get_final_message`**，它會在串流完全讀完之後，回傳「累積起來的完整最終訊息」。如果你既想用串流，又需要在完成時取得整段完成的產生內容，這就很有用。你當然也可以自己寫程式累積訊息，但這個小幫手方法讓事情變得很簡單。

下面的範例會在收到每一段文字時印出來，並在串流完成時印出最終的完整訊息：

{{cell 37}}

**逐行解說：**
- `from anthropic import AsyncAnthropic`、`client = AsyncAnthropic()`：這次用的是「**非同步（async）**」版本的客戶端。
- `async def` / `async with` / `async for` / `await`：非同步寫法的關鍵字（[0-4 第 16-4 節](../00_before_you_start/04_python_crash_course.md#16-4-async--await)）。新手不用深究，知道「非同步版本要這樣寫」即可。
- `async with client.messages.stream(...) as stream:`：開啟一個串流。
- `async for text in stream.text_stream:`：**直接拿到每一段文字**，不用自己判斷事件類型——這就是小幫手的方便之處。
- `final_message = await stream.get_final_message()`：串流結束後，拿到完整的訊息物件。
- `print(final_message.to_json())`：把完整訊息用 JSON 格式印出來。
- 最後一行 `await streaming_with_helpers()`：執行這個非同步函式。（在 notebook 裡可以直接寫 `await`；如果是一般的 `.py` 程式檔，要改用 `asyncio.run(streaming_with_helpers())`。）

（提示詞是「寫一首關於蘭花的十四行詩（sonnet）」。）

> 💡 **小提醒**：這個小幫手也有「一般（非 async）」版本，寫法更簡單：
> ```python
> with client.messages.stream(model="claude-haiku-4-5", max_tokens=1024,
>                             messages=[{"role": "user", "content": "Write me sonnet about orchids"}]) as stream:
>     for text in stream.text_stream:
>         print(text, end="", flush=True)
> final_message = stream.get_final_message()
> ```
> （這裡的 `client` 要是一般的 `Anthropic()`，不是 `AsyncAnthropic()`。）

使用 `client.messages.stream()` 時，我們還可以定義**自訂的事件處理器（event handler）**，讓它在任何串流事件發生時、或只在產生文字時執行⋯⋯等等。

下面的範例使用了兩個自訂事件處理器。我們用 `client.messages.stream()` 請模型「產生一首 5 個字的詩」。我們定義了自己的 `MyStream` 類別，裡面有兩個事件處理器：

* **`on_text`**：在累積「文字內容區塊」時觸發。第一個參數是這次的文字增量，第二個參數是目前累積起來的文字。在下面的範例中，我們用這個事件處理器把產生的文字在串流進來時印出來。文字會用**綠色**印出，比較容易看。
* **`on_stream_event`**：只要從 API 收到**任何**事件就會觸發。在下面的範例中，每次收到事件，我們就印出事件的類型。

接著，我們把 `event_handler` 參數傳給 `client.messages.stream`，註冊這些「在特定事件發生時會被呼叫的回呼（callback）方法」：

{{cell 39}}

**逐行解說：**
- `green = '\033[32m'`、`reset = '\033[0m'`：這兩串奇怪的文字是「終端機顏色代碼」，`\033[32m` 代表「接下來的字用綠色」，`\033[0m` 代表「恢復正常顏色」。
- `class MyStream(AsyncMessageStream):`：定義一個新的「類別（class）」，它**繼承**自 SDK 提供的 `AsyncMessageStream`。你可以想成：「我要一個跟 AsyncMessageStream 一樣的東西，但其中某些行為我想自己改寫」。
- `async def on_text(self, text, snapshot):`：改寫「收到文字時」要做的事 → 用綠色印出文字。
- `async def on_stream_event(self, event):`：改寫「收到任何事件時」要做的事 → 印出事件類型。
- `event_handler=MyStream`：告訴串流「請用我的 MyStream 來處理事件」。

> 🧩 **白話小補充：「回呼（callback）」是什麼？** 就像在餐廳拿到「取餐呼叫器」：你不用一直盯著櫃台，餐點好了呼叫器會「叫你」。事件處理器就是你事先交給 SDK 的「呼叫器」：某個事件發生時，SDK 會自動呼叫你寫好的函式。

Python SDK 還提供了其他幾個可以使用的事件處理器，包括：

##### `on_message(message: Message)`
當一個完整的 Message 物件累積完成時觸發。對應到 `message_stop` 這個 SSE 事件。

##### `on_content_block(content_block: ContentBlock)`
當一個完整的 ContentBlock 物件累積完成時觸發。對應到 `content_block_stop` 這個 SSE 事件。

##### `on_exception(exception: Exception)`
在串流回應的過程中遇到例外（錯誤）時觸發。

##### `on_timeout()`
請求逾時（等太久）時觸發。

##### `on_end()`
串流中最後一個被觸發的事件。

---

## ✏️ 練習

寫一個使用串流的簡單 Claude 聊天機器人。下面的動畫示範了它應該怎麼運作。請注意：輸出的顏色標示完全是選擇性的，主要只是為了讓動畫更好讀、更好看：

![使用串流的聊天機器人示範動畫](@orig/images/streaming_chat_exercise.gif)

> 💡 **提示**：把 [1-2 課](02_messages_format.md) 的聊天機器人練習，和這一課的 `stream=True` 結合起來。關鍵是：一邊印出串流的文字，一邊把文字**累積**起來（`assistant_response += content`），最後把累積好的完整回答加進對話紀錄。

```python run
# 在這裡寫你的串流聊天機器人

```

### 參考答案

下面這個答案是上面練習的一種簡單寫法。為了得到最好的體驗，建議把它存成一個獨立的 Python 程式檔（例如 `chatbot.py`）來執行，而不是在這個 notebook 的格子裡執行：

{{cell 43}}

**逐行解說（重點部分）：**
- `BLUE`、`GREEN`、`RESET`：終端機顏色代碼（藍色、綠色、恢復正常）。
- `conversation = []`：對話紀錄。
- `while True:` ... `if user_input.lower() == 'quit': break`：一直聊，輸入 quit 就結束。
- `stream=True`：用串流方式取得回答。
- `assistant_response = ""`：準備一個空字串，用來累積 Claude 的完整回答。
- `assistant_response += content`：每收到一小段文字，就接到 `assistant_response` 後面（`+=` 是「接上去」的意思）。
- `conversation.append({"role": "assistant", "content": assistant_response})`：把完整回答加進對話紀錄，下一輪 Claude 才記得自己說過什麼。
- `if __name__ == "__main__":`：這是 Python 程式檔的慣用寫法，意思是「如果這個檔案是被直接執行的，就呼叫 `chat_with_claude()`」。

> 💡 **怎麼存成程式檔執行？** 把上面的程式碼複製到一個新檔案 `chatbot.py`，在檔案最上面加上 `from dotenv import load_dotenv` 和 `load_dotenv()` 兩行（才能讀到 API 金鑰），然後在終端機輸入 `python chatbot.py`（Mac 用 `python3 chatbot.py`）。

---

## 📌 重點整理

- **串流** = Claude 寫一點就傳一點，使用者不用乾等。主要好處是大幅縮短 **TTFT（第一個 token 的等待時間）**，但**總時間不變**。
- 寫法一：`client.messages.create(..., stream=True)`，再用 `for event in stream:` 讀取事件。
  - 文字在 `event.type == "content_block_delta"` 的 `event.delta.text` 裡。
  - 輸入 token 數在 `message_start` 事件，輸出 token 數在 `message_delta` 事件。
- 事件順序：`message_start` → (`content_block_start` → 多個 `content_block_delta` → `content_block_stop`) → `message_delta` → `message_stop`。
- 寫法二（小幫手）：`client.messages.stream(...)`，用 `stream.text_stream` 直接拿文字，用 `get_final_message()` 拿完整訊息；還可以自訂事件處理器（`on_text`、`on_stream_event`⋯⋯）。
- 印串流文字時用 `print(text, end="", flush=True)`。

👉 下一課：[1-6 視覺（傳圖片給 Claude）](06_vision.md)
