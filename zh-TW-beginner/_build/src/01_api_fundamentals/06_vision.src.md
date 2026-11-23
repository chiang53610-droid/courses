<!--meta {"orig": "anthropic_api_fundamentals/06_vision.ipynb", "out": "01_api_fundamentals/06_vision", "replace": [["./prompting_images/", "../../anthropic_api_fundamentals/prompting_images/"], ["./images/research_paper/", "../../anthropic_api_fundamentals/images/research_paper/"]]} -->
# 1-6 用圖片下提示詞（Vision 視覺能力）

> 📚 **第 1 單元：Claude API 基礎**｜第 6 課 / 共 6 課
> ⏱️ 預估時間：50 分鐘

## 🎯 這一課你會學到

- 怎麼把**圖片**傳給 Claude，讓它看圖回答問題
- `content` 可以是「內容區塊的串列」，裡面混合文字和圖片
- 怎麼讀取電腦裡的圖片、網路上的圖片，並轉成 Claude 看得懂的格式（base64）
- 用圖片下提示詞的小技巧

> 🔄 **2026 更新**：原課程這一課使用 `claude-3-5-sonnet-20240620`（視覺能力最強），新手版換成 `claude-sonnet-4-6`；原本用 `claude-3-haiku-20240307` 的地方換成 `claude-haiku-4-5`。另外，因為這份 notebook 放在 `zh-TW-beginner` 資料夾裡，程式碼裡的圖片路徑已改成 `../../anthropic_api_fundamentals/...`，指向原始課程資料夾裡的圖片。

---

## 視覺能力

Claude 3 家族的模型都具備**視覺能力**，讓 Claude 可以理解和分析圖片。現在，我們可以同時提供文字和圖片作為輸入，讓對話更豐富，也開啟了許多強大的新用途。Opus、Sonnet 和 Haiku 都能理解和處理圖片。因為 Claude 3.5 Sonnet 的視覺能力最強，所以這一課我們都會使用它。

要把圖片提供給 Claude，我們只要使用和純文字對話一樣的 `messages` 格式就好。一個典型的純文字使用者訊息長這樣：

```py
messages = [
    {
        "role": "user",
        "content": "tell me a joke"
    }
]
```

{{cell 3}}

（請 Claude「講個笑話」。這是我們已經很熟悉的寫法。）

我們還沒看過的是：訊息裡的 `content` 也可以設定成**一個內容區塊（content block）的串列**。也就是說，原本是這樣：

```py
messages = [
    {"role": "user", "content": "tell me a joke"}
]
```

我們也可以改寫成這樣：

```py
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "tell me a joke"},
        ]
    }
]
```

下面這兩則訊息是**完全一樣**的：

```py
{"role": "user", "content": "Tell me a story"}
```

```py
{"role": "user", "content": [{"type": "text", "text": "Tell me a story"}]}
```

> 🧩 **白話小補充**：第一種寫法是「簡寫」，第二種是「完整寫法」。完整寫法中，每一個內容區塊都是一個字典，用 `"type"` 說明它是什麼類型（`"text"` 文字），再用 `"text"` 放文字內容。

我們來試試看：

{{cell 5}}

可以看到，它能正常運作！我們可以在串列裡加入任意多個內容區塊，就像這個例子：

{{cell 7}}

（三個文字區塊分別是「who」「made」「you?」，合起來就是「誰創造了你？」）

為什麼要這樣寫呢？如果只有文字，我們大概不會這樣寫，但在處理**多模態（multimodal）提示詞**時，就**必須**使用這種格式！

> 🧩 **白話小補充**：「多模態」就是「不只一種形式的資料」，例如「文字 + 圖片」。

當我們要提供圖片給 Claude 時，必須寫一個**圖片內容區塊**。範例如下：

```py
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": "/9j/4AAQSkZJRg..."
                }
            }
        ]
    }
]
```

這張圖說明了提供圖片給 Claude 時，需要哪些重要的資訊：

![圖片內容區塊的格式說明](@orig/images/image_message_format.png)

訊息裡的 `content` 是一個字典，它的 `source`（來源）包含下面這些屬性：

* `type`：圖片的編碼格式。目前必須是 `base64`。
* `media_type`：圖片的媒體類型。目前支援 `image/jpeg`、`image/png`、`image/gif` 和 `image/webp`。
* `data`：圖片資料本身。

> 🧩 **白話小補充：base64 是什麼？** 圖片在電腦裡是一堆 0 和 1 的「二進位資料」，沒辦法直接放進文字訊息裡。**base64** 是一種把二進位資料「翻譯」成一長串英文字母和數字的方法，這樣圖片就能像文字一樣被傳送了。你不需要知道它的原理，只要會用下面教的幾行程式把圖片轉過去就好。
>
> 🔄 **2026 更新**：現在除了 base64，API 也支援直接給圖片網址（`"source": {"type": "url", "url": "..."}`）或先用 Files API 上傳。不過這一課照原課程教 base64，因為它是最基本、到處都能用的方法。

---

## 只用圖片下提示詞

大多數時候，我們會在提示詞裡同時提供文字和圖片，但**只提供一張圖片**也完全沒問題。我們來試試看！這一課準備了幾張圖片，放在 `prompting_images` 資料夾裡。我們先用 Python 看看其中一張圖片：

{{cell 11 img=@orig/prompting_images/uh_oh.png}}

（`from IPython.display import Image` 是 notebook 裡顯示圖片的工具。）

圖片來源：Wikimedia Commons，CC-BY-SA 授權

現在，我們來把這張圖片提供給 Claude。第一步是取得「base64 編碼的圖片資料字串」，這個字串就是我們要傳給模型的東西。程式碼看起來可能有點複雜，但其實就是下面幾個步驟：

1. 用「讀取二進位（read binary）」模式打開檔案。
2. 把檔案的全部二進位內容讀成一個 bytes 物件。
3. 用 base64 編碼這些二進位資料。
4. 把 base64 編碼後的二進位資料轉成字串。

{{cell 14}}

**逐行解說：**
- `import base64`：匯入 Python 內建的 base64 工具。
- `with open("...uh_oh.png", "rb") as image_file:`：打開圖片檔。`"rb"` = read binary（用二進位模式讀取）。
- `binary_data = image_file.read()`：把整個檔案讀進來（一堆 bytes）。
- `base_64_encoded_data = base64.b64encode(binary_data)`：轉成 base64（但還是 bytes 格式）。
- `base64_string = base_64_encoded_data.decode('utf-8')`：把 bytes 轉成一般的字串。

我們可以看看得到的 `base64_string` 變數，但對我們人類來說它根本看不懂。我們來看前 100 個字元：

{{cell 16}}

（`[:100]` 的意思是「取前 100 個字元」。）

現在我們已經把圖片資料變成字串了，下一步是正確地組好要傳給 Claude 的訊息串列：

{{cell 18}}

最後一步就是把訊息串列傳給 Claude，看看會得到什麼樣的回應！

{{cell 20}}

（Claude 描述了圖片：一個在海灘上的男人，皮膚紅通通的，顯然嚴重曬傷，表情很痛苦⋯⋯並提醒防曬的重要性。）

Claude 開始描述這張圖片，因為我們沒有給它任何其他明確的指示。

---

## 圖片 + 文字的提示詞

現在，我們來試試傳送一個**同時包含圖片和文字**的提示詞。我們只需要在使用者的訊息裡加入第二個區塊——一個簡單的文字區塊。

{{cell 23}}

（文字區塊的內容是：「這個人原本可以怎麼做來避免這種情況？」）

下面這張圖標示出了圖片區塊和文字區塊：

![提示詞中的圖片區塊和文字區塊](@orig/images/image_and_text_prompt.png)

我們把請求傳給 Claude，看看會怎樣：

{{cell 26}}

（Claude 回答：這個人應該是曬太久又沒做好防護。可以預防的方法包括：1. 定時大量塗抹高係數防曬乳 2. 穿戴帽子和抗 UV 衣物 3. 在陽光最強的時段（大約早上 10 點到下午 4 點）待在陰影下 4. 使用海灘傘⋯⋯等等。）

---

## 多張圖片

我們可以在使用者訊息的 `content` 裡加入**多個圖片區塊**，一次提供多張圖片給 Claude。下面是一個包含多張圖片的範例：

```py
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image1_media_type,
                    "data": image1_data,
                },
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image2_media_type,
                    "data": image2_data,
                },
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image3_media_type,
                    "data": image3_data,
                },
            },
            {"type": "text", "text": "How are these images different?"},
        ],
    }
]

```

（最後的文字區塊是：「這些圖片有什麼不同？」）

### 寫一個圖片小幫手函式

處理圖片的時候，特別是在動態的程式裡，每次都要手動建立圖片內容區塊會很煩。我們來寫一個小小的**輔助函式**，自動產生格式正確的圖片區塊。

{{cell 29}}

**逐行解說：**
- `def create_image_message(image_path):`：定義一個函式，給它圖片的路徑。
- 中間幾行和前面一樣：打開檔案 → 讀取 → base64 編碼 → 轉成字串。
- `mime_type, _ = mimetypes.guess_type(image_path)`：根據副檔名（`.png`、`.jpg`⋯⋯）**自動猜出**圖片的媒體類型（例如 `image/png`）。這個函式會回傳兩個值，我們只需要第一個，第二個用 `_` 接住（`_` 是「我不需要這個值」的慣用寫法）。
- `image_block = {...}`：組出圖片內容區塊的字典。
- `return image_block`：把它交回去。

上面這個函式接收一個圖片路徑，然後回傳一個「可以直接放進給 Claude 的訊息裡」的字典。它甚至會用一些邏輯自動判斷圖片的 MIME 類型。

> 🧩 **白話小補充**：MIME 類型（media type）就是「這是什麼種類的檔案」的標準寫法，例如 `image/png` 代表 PNG 圖片、`image/jpeg` 代表 JPG 圖片。

我們來試試看一張新的圖片：

{{cell 31 img=@orig/prompting_images/animal1.png}}

用我們新的圖片區塊小幫手函式，送出請求給 Claude：

{{cell 33}}

（Claude 描述：一隻威風的白頭海鵰，停在水邊的水泥或石頭結構上，白色的頭、黃色的鳥喙和深色的身體形成對比⋯⋯）

我們來試一個在提示詞中結合文字和圖片的例子：

{{cell 35}}

（問題：「我在世界上哪些地方可以找到這種動物？」Claude 回答：白頭海鵰主要分布在北美洲，最常見於阿拉斯加和加拿大⋯⋯）

現在，我們來試試看一次提供多張圖片給 Claude。我們有 3 張不同的動物圖片：

{{cell 37 img=@orig/prompting_images/animal1.png}}

{{cell 38 img=@orig/prompting_images/animal2.png}}

{{cell 39 img=@orig/prompting_images/animal3.png}}

我們試著在同一則訊息中傳入全部 3 張圖片，再加上一個文字提示詞問：「這些是什麼動物？」

{{cell 41}}

（Claude 正確地說出：1. 白頭海鵰 2. 在水中游泳的熊（可能是灰熊或棕熊）3. 豪豬。）

效果很好！不過要注意的是，如果我們用能力稍弱一點的 Claude 模型（例如 Claude 3 Haiku）來做這件事，結果可能會比較差：

{{cell 43}}

這個回應還有很大的改進空間。整理一下：我們傳給 Claude 一張白頭海鵰的圖片、一張在水裡的灰熊圖片、一張豪豬的特寫圖片，然後問「這些是什麼動物？」。這是 Claude 的回答：

>The image shows a porcupine. The animal has distinctive long, coarse fur that appears spiky and bristly. Porcupines are known for their quills or sharp spines that cover their body, which serves as a defense mechanism. This close-up shot captures the intricate details and texture of the porcupine's fur and facial features.

（翻譯：「這張圖片是一隻豪豬。這種動物有明顯的長而粗的毛，看起來刺刺的⋯⋯」——它只回答了最後一張圖！）

那白頭海鵰和灰熊的圖片呢？這在 Claude 3.5 Sonnet 上不是問題，但在使用其他模型時，**幫每張圖片加上一個文字標籤**會很有幫助。就算只是很簡單地標示成「Image 1」「Image 2」⋯⋯也能造成很大的差別。

> 🔄 **2026 更新**：新手版把這格的模型換成了 `claude-haiku-4-5`，它比當年的 Claude 3 Haiku 聰明很多，所以你自己跑的時候**很可能三張圖都答對**，不會出現上面的問題。不過「幫每張圖片加標籤」仍然是很好的習慣，特別是圖片很多的時候。

我們來試試看：

{{cell 45}}

（每張圖片前面都多了一個文字區塊：`"Image 1:"`、`"Image 2:"`、`"Image 3:"`。這次 Claude 把三張圖都正確辨認出來了。）

**好多了！**

---

## 使用不在電腦裡的圖片（網路上的圖片）

有時候你可能需要提供 Claude 一張不在你電腦裡的圖片。做法有很多種，但都可以歸納成同一個步驟：

* 用某種「網路請求函式庫」取得圖片資料
* 用 base64 編碼圖片內容的二進位資料
* 用 UTF-8 把編碼後的資料從 bytes 轉成字串

我們會用 **`httpx`** 這個套件，從網址下載圖片資料。下面範例裡的網址，是一張教堂上空出現北極光的圖片。

> 💡 **小提醒**：如果執行時出現 `ModuleNotFoundError: No module named 'httpx'`，請先執行 `%pip install httpx`。（通常安裝 `anthropic` 時就會一起裝好了。）

{{cell 48}}

**逐行解說：**
- `image_url = "https://..."`：圖片的網址。
- `image_media_type = "image/jpeg"`：我們知道它是 JPG 圖片。
- `httpx.get(image_url).content`：從網址下載圖片，`.content` 是下載到的二進位資料。
- `base64.b64encode(...).decode("utf-8")`：轉成 base64 字串（把前面的步驟寫成一行）。
- 後面組訊息、送請求，跟之前一樣。文字區塊是「描述這張圖片」。

（Claude 描述：一幅壯觀的北極光景象，綠色的極光在一座偏遠雪地中的小教堂上空舞動，教堂是白色的、有紅色屋頂的尖塔⋯⋯）

就像前面做的一樣，我們可以定義一個輔助函式，從網址產生圖片區塊。下面是一個非常簡單的版本，它接收一個網址，然後：

* 用 `httpx` 下載圖片資料
* 用非常簡單的字串處理判斷 MIME 類型：取最後一個 `.` 後面的內容（副檔名）。這**不是**萬無一失的方法
* 用 base64 編碼圖片資料，再把 bytes 解碼成 UTF-8 字串
* 回傳一個格式正確的圖片區塊，可以直接放進 Claude 的提示詞裡！

如果我們呼叫 `get_image_dict_from_url("https://somewebsite.com/cat.png")`，它會回傳下面這個字典：

```py
{
    "type": "image",
    "source": {
        "type": "base64",
        "media_type": "image/png",
        "data": <actual image data>
    },
}
```

{{cell 50}}

**逐行解說：**
- `image_url.split(".")[-1].lower()`：用 `.` 把網址切開，取最後一段（`[-1]`），轉成小寫 → 得到副檔名，例如 `png`。
- `if ... elif ... else`：根據副檔名決定媒體類型；不認識的格式就 `raise ValueError(...)`（主動丟出一個錯誤，告訴使用者「不支援這種圖片格式」）。

現在來試試看！下面的例子使用兩個圖片網址：

* 一張消防車的 PNG 圖片
* 一架緊急救援直升機的 JPG 圖片

這是這兩張圖片：

![消防車](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Rincon_fire_truck.png/1600px-Rincon_fire_truck.png)
圖片來源：Wikimedia Commons，CC-BY-SA 授權
![直升機](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Ornge_C-GYNP.jpg/1600px-Ornge_C-GYNP.jpg)
圖片來源：Wikimedia Commons，CC-BY-SA 授權

我們把兩張圖片都傳給 Claude，再加上一個文字提示詞問：「這些圖片有什麼共同點？」

{{cell 53}}

Claude 成功辨認出兩張圖片都是**緊急救援交通工具**！更重要的是，我們現在學會了怎麼把從網址下載的圖片提供給 Claude。

---

## 用圖片下提示詞的小技巧

### 技巧 1：說得具體一點

就像純文字提示詞一樣，寫出**具體、詳細**的多模態提示詞，可以從 Claude 得到更好的結果。我們來看一個例子。

這是一群朋友的照片。照片裡有 8 個人，但其中 2 個人被照片的邊緣切掉了一部分。

{{cell 57 img=@orig/prompting_images/people.png}}

如果我們只是簡單地問 Claude「這張圖片裡有幾個人？」，很可能會得到「7 個人」的回答：

{{cell 59}}

如果我們改用一些基本的提示詞工程技巧——例如請 Claude **一步一步地思考**、告訴它**它是數人頭的專家**、提醒它要**注意被照片切掉的「不完整」的人**——就會得到更好的結果：

{{cell 61}}

**這個提示詞的意思是**：「你的視力完美，而且非常注重細節，這讓你成為數圖片中物體的專家。這張照片裡有幾個人？有些人可能被部分遮住、被照片邊緣切掉，或只露出一隻手臂。就算你只看到一個身體部位，也請把那個人算進去。在用 `<answer>` 標籤提供答案之前，請先在 `<thinking>` 標籤裡一步一步地思考，並分析圖片的每一個部分。」

（Claude 先在 `<thinking>` 裡從左到右逐一分析，最後在 `<answer>` 裡回答 8——答對了！）

> 🧩 **白話小補充**：這裡用到了好幾個第 2 單元會教的技巧：**給角色**（第 3 章）、**用 XML 標籤**（第 4 章）、**請它一步一步思考**（第 6 章）。先有個印象就好。

### 技巧 2：使用範例

在提示詞中加入**範例**，不管是文字還是圖片輸入的提示詞，都能幫助提升 Claude 回答的品質。

為了示範這一點，我們會用一系列的投影片圖片。我們的目標是讓 Claude 產生投影片內容的 **JSON 描述**。先看看第一張圖片：

{{cell 63 img=@orig/prompting_images/slide1.png}}

我們的目標是讓 Claude 產生一個 JSON 格式的回答，內容包含投影片的背景顏色、標題、內文，以及圖片的描述。上面這張圖片的 JSON 可能長這樣：

```json
{
    "background": "#F2E0BD",
    "title": "Haiku",
    "body": "Our most powerful model, delivering state-of-the-art performance on highly complex tasks and demonstrating fluency and human-like understanding",
    "image": "The image shows a simple line drawing of a human head in profile view, facing to the right. The head is depicted using thick black lines against a pale yellow background. Inside the outline of the head, there appears to be a white, spoked wheel or starburst pattern, suggesting a visualization of mental activity or thought processes. The overall style is minimalist and symbolic rather than realistic."
}
```

（`background` 是背景顏色的色碼；`title` 是標題；`body` 是內文；`image` 是對投影片上那張圖的文字描述：「一個面向右邊的人頭側面簡單線條畫⋯⋯頭裡面有一個白色的輪輻或星芒圖案，象徵思考活動⋯⋯」）

這正是一個很適合「在提示詞中加入範例」的使用情境，可以精確地教 Claude 我們想要它產生什麼樣的回答。作為參考，這是另外兩張投影片圖片：

{{cell 66 img=@orig/prompting_images/slide2.png}}

{{cell 67 img=@orig/prompting_images/slide3.png}}

為了做到這一點，我們會利用「對話訊息格式」，提供 Claude 一組「之前的輸入」和「對應的輸出」作為範例：

{{cell 69}}

**逐行解說：**
- `slide1_response = """{...}"""`：我們自己寫好的「第一張投影片的標準答案」（JSON 範例）。
- `messages` 裡有三則訊息：
  1. 👤 user：第一張投影片的圖片 + 「請產生這張投影片的 JSON 表示，要包含背景顏色、標題、內文和圖片描述」
  2. 🤖 assistant：我們寫好的標準答案（假裝這是 Claude 之前的回答）
  3. 👤 user：**新的**投影片圖片 + 同樣的要求
- Claude 看到「上一次是這樣回答的」，就會用一模一樣的格式回答新的投影片。這就是 [1-2 課](02_messages_format.md) 學過的**少量範例提示（few-shot）**！

{{cell 70 img=@orig/prompting_images/slide2.png}}

{{cell 71 img=@orig/prompting_images/slide3.png}}

---

## ✏️ 練習

這個練習要請你用 Claude 來**轉錄並摘要**一篇 Anthropic 的研究論文。在 `images` 資料夾裡，有一個 `research_paper` 資料夾，裡面有這篇研究論文的 5 張截圖。為了幫你一把，我們已經把 5 張圖片的路徑放在一個串列裡了：

{{cell 73}}

我們先看看第一張圖片：

{{cell 75 img=@orig/images/research_paper/page1.png}}

### 你的任務

請用 Claude 完成下面這些事：
* **轉錄**這 5 張研究論文圖片裡的文字（也就是把圖片上的字「打」出來）
* 把每張圖片的文字**合併**成一份完整的轉錄稿
* 把整份轉錄稿交給 Claude，請它為整篇論文寫一份**非技術性的摘要**（一般人也看得懂的摘要）

範例輸出可能長得像這樣：

>This paper explores a new type of attack on large language models (LLMs) like ChatGPT, called "Many-shot Jailbreaking" (MSJ). As LLMs have recently gained the ability to process much longer inputs, this attack takes advantage of that by showing the AI hundreds of examples of harmful or undesirable behavior. The researchers found that this method becomes increasingly effective as more examples are given, following a predictable pattern.

>The study tested MSJ on several popular AI models and found it could make them produce harmful content they were originally designed to avoid. This includes things like violent or sexual content, deception, and discrimination. The researchers also discovered that larger AI models tend to be more susceptible to this type of attack, which is concerning as AI technology continues to advance.

>The paper also looked at potential ways to defend against MSJ attacks. They found that current methods of training AI to be safe and ethical (like supervised learning and reinforcement learning) can help somewhat, but don't fully solve the problem. The researchers suggest that new approaches may be needed to make AI models truly resistant to these kinds of attacks. They emphasize the importance of continued research in this area to ensure AI systems remain safe and reliable as they become more powerful and widely used.

**範例輸出翻譯：**
> 這篇論文探討一種針對大型語言模型（LLM，例如 ChatGPT）的新型攻擊，叫做「多樣本越獄（Many-shot Jailbreaking，MSJ）」。由於 LLM 最近能夠處理長很多的輸入，這種攻擊就利用這一點，給 AI 看數百個有害或不當行為的範例。研究人員發現，給的範例越多，這個方法就越有效，而且遵循一個可以預測的規律。
>
> 這項研究在幾個熱門的 AI 模型上測試了 MSJ，發現它能讓這些模型產生原本被設計成要避免的有害內容，包括暴力或色情內容、欺騙和歧視等。研究人員也發現，越大的 AI 模型往往越容易受到這種攻擊，隨著 AI 技術持續進步，這一點令人擔憂。
>
> 這篇論文也研究了防禦 MSJ 攻擊的可能方法。他們發現，目前訓練 AI 變得安全、合乎道德的方法（例如監督式學習和強化學習）能有一些幫助，但無法完全解決問題。研究人員建議，可能需要新的方法，才能讓 AI 模型真正抵抗這類攻擊。他們強調，持續在這個領域做研究非常重要，才能確保 AI 系統在變得更強大、更普及的同時，仍然安全可靠。

為了得到最好的結果，我們建議**每一頁分開用一個請求來轉錄**，而不是一次把 5 張圖片全部丟給 Claude、要求它轉錄整篇論文。

> 💡 **提示**：
> 1. 寫一個函式 `transcribe_single_page(page_path)`：用 `create_image_message` 把一頁圖片傳給 Claude，請它轉錄文字，回傳文字。
> 2. 寫一個函式 `summarize_paper(pages)`：用 `for` 迴圈對每一頁呼叫上面的函式，把文字用 `+=` 接起來，最後把完整文字放進提示詞，請 Claude 寫摘要。

```python run
# 在這裡寫你的答案

```

### 參考答案

{{cell 78}}

**逐行解說（重點部分）：**
- 前半段重新定義了 `create_image_message`（和前面一樣）。
- `transcribe_single_page(page_url)`：把一頁圖片和「請盡可能準確地轉錄這頁研究論文的文字」的指示傳給 Claude，回傳轉錄的文字。
- `summarize_paper(pages)`：
  - `complete_paper_text = ""`：準備一個空字串。
  - `for page in pages:` → 每一頁都轉錄，印出前 200 個字讓你看進度，再用 `+=` 接到 `complete_paper_text` 後面。
  - 最後把整篇論文放進 `<paper>...</paper>` 標籤裡，請 Claude：「這是一篇研究論文轉錄後的內容。請為非研究背景的讀者摘要這篇論文，至少寫 3 段。請務必解釋所有縮寫和專業術語，並盡可能使用比喻。」

{{cell 79}}

---

## 📌 重點整理

- `content` 可以是**字串**，也可以是**內容區塊的串列**；要傳圖片就必須用串列寫法。
- 圖片區塊格式：
  ```python
  {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": base64字串}}
  ```
- 把圖片轉成 base64：`base64.b64encode(檔案內容).decode("utf-8")`；網路圖片先用 `httpx.get(網址).content` 下載。
- 一則訊息可以放多張圖片 + 文字；**幫每張圖加上「Image 1:」之類的標籤**效果更好。
- 看圖的提示詞一樣適用提示詞技巧：**說得具體**、**請它一步步思考**、**給範例**。

🎉 **恭喜你完成第 1 單元「Claude API 基礎」！** 你已經會用程式跟 Claude 對話、調整參數、使用串流和傳送圖片了。

👉 下一個單元：[第 2 單元：提示詞工程互動教學](../02_prompt_engineering_tutorial/00_Tutorial_How-To.md)
