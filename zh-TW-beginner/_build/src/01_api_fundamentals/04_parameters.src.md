<!--meta {"orig": "anthropic_api_fundamentals/04_parameters.ipynb", "out": "01_api_fundamentals/04_parameters"} -->
# 1-4 模型參數（Parameters）

> 📚 **第 1 單元：Claude API 基礎**｜第 4 課 / 共 6 課
> ⏱️ 預估時間：45 分鐘

## 🎯 這一課你會學到

* 了解 `max_tokens` 參數的作用
* 使用 `temperature` 參數控制模型的回應
* 說明 `stop_sequence`（停止序列）的用途
* （加碼）使用 `system` 系統提示詞

> 🧩 **白話小補充：「參數」是什麼？** 呼叫 `client.messages.create(...)` 時，括號裡寫的 `model=...`、`max_tokens=...` 這些就叫「參數」。它們就像點餐時的客製化選項：「大杯、少冰、半糖」。不同的參數會改變 Claude 回答的方式。

---

一如往常，我們先匯入 `anthropic` SDK 並讀取 API 金鑰：

{{cell 2}}

---

## Max tokens（最大 token 數）

每次對 Claude 送出請求時，有 **3 個必填的參數**：

* `model`（模型）
* `max_tokens`（最大 token 數）
* `messages`（訊息）

到目前為止，我們每一個請求都有用到 `max_tokens` 參數，但一直沒有停下來好好談談它是什麼。

這是我們送出的第一個請求：

```py
our_first_message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=500,
    messages=[
        {"role": "user", "content": "Hi there! Please write me a haiku about a pet chicken"}
    ]
)
```

那麼，`max_tokens` 的用途到底是什麼呢？

### Token

簡單來說，`max_tokens` 控制的是 **Claude 在回答中最多可以產生多少個 token**。在進一步說明之前，我們先停下來談談 token。

大部分的大型語言模型並不是用「完整的單字」在「思考」，而是處理一連串叫做 **token** 的「單字片段」。token 是 Claude 處理、理解和產生文字時使用的小積木。當我們把提示詞交給 Claude，提示詞會先被轉換成 token，再傳給模型。接著，模型會開始**一次產生一個 token** 的方式產生輸出。

對 Claude 來說，一個 token 大約等於 3.5 個英文字元，不過確切的數字會因為使用的語言而有所不同。

> 🧩 **白話小補充**：可以把 token 想成「樂高積木」。一句話會被拆成一塊一塊的積木，Claude 每次只能放一塊積木，一塊一塊接下去，最後拼成完整的回答。中文的話，大約 1 個中文字是 1～2 個 token。

### 使用 `max_tokens`

`max_tokens` 參數讓我們可以設定 Claude 產生 token 數量的**上限**。舉例來說，假設我們請 Claude 寫一首詩，並把 `max_tokens` 設成 10。Claude 會開始產生 token，並在產生到第 10 個 token 時**立刻停下來**。這常常會造成輸出被截斷、不完整。我們來試試看！

{{cell 6}}

這是 Claude 回傳給我們的內容：

>Here is a poem for you:
>
>The

（意思是：「這是給你的一首詩：\n\n那個」——寫到一半就被切斷了。）

如果你執行上面的程式碼，很可能會得到不一樣、但同樣被截斷的結果。Claude 開始幫我們寫詩，然後在產生 10 個 token 時就立刻停止了。

我們也可以查看回應物件（Message）的 **`stop_reason`** 屬性，看看模型**為什麼**停止產生文字。在這個例子中，可以看到它的值是 `"max_tokens"`，告訴我們模型停下來是因為它碰到了我們設定的 token 上限！

{{cell 9}}

當然，如果我們把 `max_tokens` 設大一點、再請它寫一次詩，很可能就會得到一首完整的詩：

{{cell 11}}

這是 `max_tokens` 設成 500 時，Claude 產生的內容（原課程另一次執行的結果）：

```
Here is a poem for you:

Whispers of the Wind

The wind whispers softly,
Caressing my face with care.
Its gentle touch, a fleeting breath,
Carries thoughts beyond compare.

Rustling leaves dance in rhythm,
Swaying to the breeze's song.
Enchanting melodies of nature,
Peaceful moments linger long.

The wind's embrace, a soothing balm,
Calms the restless soul within.
Embracing life's fleeting moments,
As the wind's sweet song begins.
```

（一首名為〈風的低語〉的英文詩，內容是風輕撫臉龐、樹葉隨風起舞、風的擁抱撫慰不安的心靈。）

如果我們查看這個回應的 `stop_reason`，會看到值是 **`"end_turn"`**，這是模型告訴我們「**我是自然地寫完了**」的方式。它幫我們寫完了一首詩，沒有別的話要說了，所以就停下來了！

{{cell 14}}

> 📝 **`stop_reason` 小整理**
> | 值 | 意思 |
> |---|---|
> | `"end_turn"` | Claude 自然地說完了 |
> | `"max_tokens"` | 碰到 `max_tokens` 上限，被切斷了 |
> | `"stop_sequence"` | 產生了你指定的「停止序列」（下面會教） |
> | `"tool_use"` | Claude 想使用工具（第 5 單元會教） |

很重要的一點是：模型在產生內容時，**並不「知道」`max_tokens` 的存在**。改變 `max_tokens` 並不會改變 Claude 產生輸出的方式，它只是給模型「繼續寫下去的空間」（`max_tokens` 設很大時），或是把輸出「切斷」（`max_tokens` 設很小時）。

> 🧩 **白話小補充**：就像給一個人一張紙寫作文。紙的大小（`max_tokens`）不會改變他想寫什麼，只是紙不夠大的時候，文章會寫到一半就沒地方寫了。所以如果你想要「短一點的回答」，應該在**提示詞裡**告訴 Claude「請簡短回答」，而不是把 `max_tokens` 設很小。

另外也要知道：把 `max_tokens` 調大，**並不保證** Claude 真的會產生那麼多 token。如果我們請 Claude 講一個笑話，並把 `max_tokens` 設成 1000，我們幾乎一定會得到一個遠少於 1000 個 token 的回答。

{{cell 17}}

{{cell 18}}

{{cell 19}}

在上面的例子中，我們請 Claude「講個笑話」，並把 `max_tokens` 設成 1000。它產生了這個笑話：

```
Here's a classic dad joke for you:

Why don't scientists trust atoms? Because they make up everything!

How was that? I tried to keep it clean and mildly amusing. Let me know if you'd like to hear another joke.
```

（翻譯：「來個經典的老爸笑話：為什麼科學家不相信原子？因為它們組成（make up，也有『捏造』的意思）了一切！怎麼樣？我盡量讓它乾淨又有點好笑。想再聽一個的話跟我說。」——這是一個英文雙關語笑話。）

這段產生的內容只有 55 個 token。我們給了 Claude 1000 個 token 的上限，但這並不代表它會產生 1000 個 token。

### 為什麼要調整 max tokens？

使用 Claude 時，了解 token 是非常重要的，特別是因為下面這些原因：

* **API 用量限制**：你的輸入文字和產生的回應，它們的 token 數量都會計入 API 的使用限制。每個 API 請求能處理的 token 數量都有上限。了解 token 能幫助你保持在 API 的限制之內，並有效地管理用量。
* **效能**：Claude 產生的 token 數量，會直接影響 API 的處理時間和記憶體用量。越長的輸入文字、越大的 `max_tokens`，需要越多的運算資源。了解 token 能幫助你最佳化 API 請求，得到更好的效能。
* **回應品質**：設定適當的 `max_tokens` 值，能確保產生的回應有足夠的長度、包含必要的資訊。如果 `max_tokens` 太小，回應可能會被截斷或不完整。試試看不同的 `max_tokens` 值，能幫助你在特定的使用情境中找到最好的平衡點。

我們來看看 Claude 產生的 token 數量如何影響效能。下面的函式會請 Claude 產生一段**非常長**的兩個角色之間的對話，總共請求三次，每次用不同的 `max_tokens` 值。接著它會印出實際產生了多少 token，以及產生花了多少時間。

{{cell 23}}

**逐行解說：**
- `token_counts = [100,1000,4096]`：三個要測試的 `max_tokens` 值。
- `task = """..."""`：提示詞的意思是「創作一段又長又詳細、至少 5000 字的對話，兩個角色在討論社群媒體對心理健康的影響。兩個角色要有不同的意見，進行一場互相尊重又深入的辯論。」——故意要求很長的內容，這樣才看得出 `max_tokens` 切斷的效果。
- `for num_tokens in token_counts:`：三個值輪流測試，每次都計時。
- `max_tokens=num_tokens`：這次的上限。

{{cell 24}}

你執行程式碼時得到的確切數值可能會不同，不過上面是一個範例輸出：產生 100 個 token 花了 1.51 秒、1000 個花了 8.33 秒、3433 個花了 28.80 秒。

可以看到，**Claude 產生的 token 越多，花的時間就越長！**

（第三次只產生了 3433 個 token，沒有到達 4096 的上限，因為 Claude 在那之前就自然地寫完了。）

再看一個更明顯的例子：我們請 Claude 把一段非常長的文字照著重複一次，並用 `max_tokens` 在各種不同的輸出長度把它切斷。每種長度重複 50 次，再計算平均的產生時間。可以看到，輸出長度越長，花的時間也越長！請看下面這張圖：

![輸出長度與產生時間的關係圖](@orig/images/output_length.png)

---

## Stop sequences（停止序列）

另一個我們還沒看過的重要參數是 **`stop_sequences`**（停止序列）。它讓我們可以提供模型一組字串，當產生的回應中出現這些字串時，模型就會**停止產生**。基本上，它就是告訴 Claude：「**如果你寫出了這串字，就不要再寫下去了！**」

下面是一個**沒有**使用 `stop_sequences` 的請求範例：

{{cell 28}}

上面的程式碼請 Claude 產生一個代表「一個人」的 JSON 物件，包含名字、email 和電話號碼。這是 Claude 產生的範例輸出：

```
Here's an example of a JSON object representing a person with a name, email, and phone number:

{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phoneNumber": "123-456-7890"
}


In this example, the JSON object has three key-value pairs:

1. "name": The person's name, which is a string value of "John Doe".
2. "email": The person's email address, which is a string value of "johndoe@example.com".
3. "phoneNumber": The person's phone number, which is a string value of "123-456-7890".

You can modify the values to represent a different person with their own name, email, and phone number.
```

（大意：「這是一個代表一個人的 JSON 物件範例……〔JSON〕……在這個範例中，JSON 物件有三組 key-value：1. name 是人名……2. email 是電子郵件……3. phoneNumber 是電話號碼……你可以修改這些值來代表另一個人。」）

Claude 確實產生了我們要的物件，但後面**還附上了一段說明**。如果我們希望 Claude 一寫出 JSON 物件的結尾大括號 `}` 就停下來，可以修改程式碼，加上 `stop_sequences` 參數。

{{cell 30}}

模型產生了下面的輸出：

```
Here's a JSON object representing a person with a name, email, and phone number:
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "555-1234"

```

**重要提醒：** 注意看，產生的輸出**不包含** `}` 這個停止序列本身。如果我們想把它當成 JSON 來使用和解析，就需要自己把結尾的 `}` 加回去。

> 🧩 **白話小補充**：停止序列就像跟人說「聽到『好了』這兩個字就停下來」。對方一說出「好了」就閉嘴——而且「好了」這兩個字本身也不會出現在紀錄裡。

拿到 Claude 的回應之後，我們可以檢查 `stop_reason` 屬性，看看模型為什麼停止產生文字。如下所示，上一個回應停下來的原因是 `'stop_sequence'`，意思是模型產生了我們提供的其中一個停止序列，於是立刻停止。

{{cell 33}}

我們也可以查看回應的 **`stop_sequence`** 屬性（注意：這個沒有 s），確認是哪一個停止序列讓模型停下來的：

{{cell 35}}

我們可以提供**多個**停止序列。如果提供了好幾個，模型只要碰到**其中任何一個**就會停止。回應物件上的 `stop_sequence` 屬性會告訴我們實際碰到的是哪一個。

下面的函式請 Claude 寫一首詩，並且只要它寫出字母「b」或「c」就停止。總共做三次：

{{cell 37}}

{{cell 38}}

這是一個範例輸出（就是上面顯示的結果）：

```
Response 1 stopped because stop_sequence.  The stop sequence was c
Response 2 stopped because stop_sequence.  The stop sequence was b
Response 3 stopped because stop_sequence.  The stop sequence was b
```

（第 1 次回應因為停止序列而停下，停止序列是 c；第 2、3 次都是 b。）

第一次，Claude 因為寫出了字母「c」而停止寫詩。接下來兩次，則是因為寫出了字母「b」而停止。你真的會這樣用嗎？大概不會吧！（這只是為了示範「多個停止序列」的效果。）

---

## Temperature（溫度）

**`temperature`** 參數用來控制產生回應的「**隨機性**」和「**創意程度**」。它的範圍是 **0 到 1**，數值越高，回應越多樣、越難預測，用詞也會有更多變化。溫度越低，輸出就越「固定」，會傾向使用最可能出現的用詞和答案。**temperature 的預設值是 1。**

在產生文字的時候，Claude 會預測「下一個 token（一個字或字的一部分）」的**機率分布**。temperature 參數的作用，就是在「抽出」下一個 token 之前，先調整這個機率分布。如果溫度很低（接近 0.0），機率分布會變得比較「尖」，最可能的 token 會分到很高的機率。這會讓模型更固定、更專注在最可能或最「安全」的選擇上。如果溫度很高（接近 1.0），機率分布會變得比較「平」，原本比較不可能的 token，機率會提高。這會讓模型更隨機、更願意探索，產生更多樣、更有創意的輸出。

看看這張圖，可以直觀地了解溫度的影響：

![溫度對機率分布的影響示意圖](@orig/images/temperature.png)

> 🧩 **白話小補充：用「抽籤」來想**
> 假設 Claude 要決定下一個字，有三個候選字，機率分別是 A 70%、B 20%、C 10%。
> - **溫度低（例如 0）**：幾乎每次都抽 A（最可能的那個）→ 回答穩定、可預測。
> - **溫度高（例如 1）**：B 和 C 也有不小的機會被抽中 → 回答多變、比較有創意。

為什麼要調整溫度呢？

**分析類的任務，溫度用接近 0.0 的值；創意和產生類的任務，溫度用接近 1.0 的值。**

我們來做個快速的示範。看看下面這個函式：分別用溫度 0 和溫度 1，各對 Claude 送出三次請求，請它「幫一顆外星行星取個名字，只用一個單字回答。」

{{cell 42}}

**逐行解說：**
- `temperatures = [0, 1]`：要測試的兩個溫度。
- 外層迴圈：兩個溫度輪流。
- 內層迴圈 `for i in range(3)`：每個溫度問 3 次。
- `temperature=temperature`：左邊是參數名稱，右邊是迴圈裡的變數（這次的溫度值）。

{{cell 43}}

這是執行上面函式的結果（你的結果可能會不同）：

```
Prompting Claude three times with temperature of 0
================
Response 1: Xendor.
Response 2: Xendor.
Response 3: Xendor.
Prompting Claude three times with temperature of 1
================
Response 1: Xyron.
Response 2: Xandar.
Response 3: Zyrcon.
```

注意到了嗎？溫度 0 的時候，三次回答都一樣。不過要注意：**就算溫度是 0.0，結果也不是百分之百固定的。** 但跟溫度 1 的結果比起來，差異非常明顯：溫度 1 的每一次回答，都是完全不同的外星行星名字。

下面這張圖說明了溫度對 Claude 輸出的影響。我們用這個提示詞：「選世界上任何一種動物。只用一個單字回答：動物的名字。」用溫度 0 問了 Claude 100 次，接著再用溫度 1 問了 100 次。下圖顯示了 Claude 回答每種動物的次數。

![溫度 0 和溫度 1 時，Claude 選擇各種動物的次數分布圖](@orig/images/temperature_plot.png)

可以看到，溫度 0 的時候，Claude **每一次**都回答「Giraffe（長頸鹿）」。請記住：溫度 0 並不保證結果完全固定，但它確實讓 Claude 更有可能每次都回答類似的內容。溫度 1 的時候，Claude 還是有超過一半的時間選擇長頸鹿，但回答中也出現了很多其他種類的動物！

> 🔄 **2026 更新**：
> - 新手版使用的 `claude-haiku-4-5` 搭配 0.x 版 SDK，可以正常使用 `temperature`。
> - 但**最新一代的模型**（例如 Haiku 5.5、Sonnet 5.5、Opus 4.7 以後）已經**不接受**（或只接受預設值的）`temperature`，而且新版的 SDK 和 API 版本也拿掉了這個參數。所以未來做自己的專案時，要控制回答的風格，請改用「在提示詞裡說清楚」的方式（例如「請只回答一個單字」、「請給我 5 個很有創意、彼此不同的點子」）。

---

## System prompt（系統提示詞）

**系統提示詞**（在程式裡的參數名稱是 `system`）是傳訊息給 Claude 時**可以選擇加上**的參數。它透過給 Claude 高層次的指示、定義它的角色、或提供應該影響它回答的背景資訊，來為整段對話「**定調**」。

關於系統提示詞的重點：

* 它是**選填**的，但對設定對話的語氣和背景很有用。
* 它作用在**整段對話**的層級，會影響 Claude 在這段對話中的**所有**回答。
* 它可以幫助引導 Claude 的行為，而不需要在每一則使用者訊息裡都重複寫指示。

要注意的是：在大部分情況下，系統提示詞裡只應該放**語氣、背景和角色**相關的內容。**詳細的指示、外部輸入的內容（例如文件）、以及範例**，放在**第一個 `User` 回合**裡效果會比較好。之後的每一個 `User` 回合不需要再重複這些內容。

> 🧩 **白話小補充**：系統提示詞就像演戲前導演給演員的「角色設定」：「你是一位很嚴格但很有愛心的法文老師」。演員（Claude）在整場戲裡都會照著這個設定演。

我們來試試看：

{{cell 47}}

**逐行解說：**
- `system="You are a helpful foreign language tutor that always responds in French."`：系統提示詞的意思是「你是一位樂於助人的外語家教，永遠用法文回答。」
- 注意 `system` 是一個**獨立的參數**，不是放在 `messages` 裡面。
- 使用者說的是英文「嘿，你好嗎？！」，但 Claude 用法文回答：「你好！很高興認識你。你今天好嗎？」——因為系統提示詞規定它永遠用法文。

---

## ✏️ 練習

寫一個叫做 `generate_questions` 的函式，它要做到以下幾件事：
* 接受兩個參數：`topic`（主題）和 `num_questions`（問題數量）
* 針對提供的 `topic`，產生 `num_questions` 個「發人深省的問題」，用**編號清單**的格式呈現
* 把產生的問題印出來

舉例來說，呼叫 `generate_questions(topic="free will", num_questions=3)`（主題：自由意志，3 個問題）可能會得到下面的輸出：

> 1. To what extent do our decisions and actions truly originate from our own free will, rather than being shaped by factors beyond our control, such as our genes, upbringing, and societal influences?
> 2. If our decisions are ultimately the result of a complex interplay of biological, psychological, and environmental factors, does that mean we lack the ability to make authentic, autonomous choices, or is free will compatible with determinism?
> 3. What are the ethical and philosophical implications of embracing or rejecting the concept of free will? How might our views on free will impact our notions of moral responsibility, punishment, and the nature of the human condition?

（翻譯：1. 我們的決定和行為，有多少程度真的出於我們自己的自由意志，而不是被基因、成長環境、社會影響這些我們無法控制的因素所塑造？ 2. 如果我們的決定最終是生物、心理和環境因素複雜交互作用的結果，這是否代表我們沒有能力做出真正自主的選擇？還是自由意志和決定論可以並存？ 3. 接受或否定自由意志的概念，在倫理和哲學上有什麼意義？我們對自由意志的看法，會如何影響我們對道德責任、懲罰以及人類處境本質的理解？）

在你的寫法中，請使用下面這些參數：
* **`max_tokens`**：把回應限制在 1000 個 token 以下。
* **`system`**：提供一個系統提示詞，告訴模型「它是這個 `topic` 的專家」，而且應該產生一份編號清單。
* **`stop_sequences`**：確保模型在產生正確數量的問題後就停止。（如果我們要 3 個問題，就要確保模型一寫出「4.」就停下來；如果要 5 個問題，就要確保模型一寫出「6.」就停下來。）

> 💡 **提示**：停止序列可以用 f-string 動態產生，例如 `f"{num_questions+1}."`——如果 `num_questions` 是 3，這個字串就是 `"4."`。

```python run
# 在這裡寫你的 generate_questions 函式

```

#### 參考答案

{{cell 50}}

**逐行解說：**
- `def generate_questions(topic, num_questions=3):`：`num_questions` 沒給的話，預設是 3。
- `system=f"You are an expert on {topic}. Generate thought-provoking questions about this topic."`：系統提示詞——「你是 {topic} 的專家。請產生關於這個主題、發人深省的問題。」
- `messages=[...]`：使用者訊息——「請以編號清單產生 {num_questions} 個關於 {topic} 的問題。」
- `stop_sequences=[f"{num_questions+1}."]`：如果要 3 題，停止序列就是 `"4."`，Claude 一寫到第 4 題就會停下。

{{cell 51}}

---

## 📌 重點整理

| 參數 | 必填？ | 作用 | 小提醒 |
|---|---|---|---|
| `model` | ✅ | 選哪個模型 | |
| `max_tokens` | ✅ | 回答最多幾個 token | 只是「上限」，太小會被切斷（`stop_reason` = `"max_tokens"`）；想要短回答請寫在提示詞裡 |
| `messages` | ✅ | 對話內容 | |
| `stop_sequences` | 選填 | 寫出這些字就停 | 停止序列本身**不會**出現在回答裡（`stop_reason` = `"stop_sequence"`） |
| `temperature` | 選填 | 0～1，越高越隨機、越有創意 | 預設 1；分析任務用低溫、創意任務用高溫；最新模型已不支援 |
| `system` | 選填 | 系統提示詞：角色、語氣、背景 | 詳細指示和文件放在第一個 user 訊息效果更好 |

- token 越多，花的時間越長、費用越高。
- 用 `response.stop_reason` 可以知道 Claude 為什麼停下來。

👉 下一課：[1-5 串流（Streaming）](05_Streaming.md)
