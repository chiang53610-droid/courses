<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`03_models.ipynb`](03_models.ipynb)。

# 1-3 模型（Models）

> 📚 **第 1 單元：Claude API 基礎**｜第 3 課 / 共 6 課
> ⏱️ 預估時間：25 分鐘

## 🎯 這一課你會學到

* 認識 Claude 的各種模型
* 比較各個 Claude 模型的速度和能力

> 🔄 **2026 更新（請先讀這段）**：這一課原本比較的是 2024 年的 Claude 3 / 3.5 系列模型，它們現在都已經停用了。新手版的做法是：
> - **文字內容**：完整翻譯原課程的說明（原課程的觀念——「速度、能力、成本之間的取捨」——到今天都還是完全適用）。
> - **程式碼**：換成目前還能用的模型，讓你可以實際執行比較。
> - **執行結果**：保留原課程用舊模型跑出來的結果，讓你看到當時的比較。
>
> 這一課最後有一張「2026 年目前的模型一覽」，可以對照著看。

---

我們先匯入 `anthropic` SDK，並讀取 API 金鑰：

```python
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
```

---

## Claude 的模型

Claude 的 Python SDK 支援好幾種模型，每一種都有不同的能力和效能特色。下面這張圖比較了 Claude 3 和 3.5 系列模型的「成本 vs. 速度」，展示了在「成本」和「聰明程度」之間各種不同的取捨：

![Claude 3 / 3.5 模型的成本與智慧比較圖](../../anthropic_api_fundamentals/images/models.png)

（圖的橫軸是成本，縱軸是智慧程度：越往右上角越聰明、也越貴。）

選擇模型時，有幾個重要的因素要考慮：

* 模型的**延遲**（latency）——它有多快？
* 模型的**能力**（capabilities）——它有多聰明？
* 模型的**成本**（cost）——它有多貴？

> 🧩 **白話小補充**：「延遲」就是「從你送出問題，到收到回答，要等多久」。延遲越低 = 越快。

想看 Claude 家族各個模型的主要功能和能力比較，可以參考[這張官方比較表](https://docs.anthropic.com/en/docs/about-claude/models#model-comparison-table)。

---

## 比較模型的速度

下面是一個簡單的函式：它會讓每個模型都回答同一個提示詞，然後印出每個模型的回答，以及每個請求花了多少時間。

> 🔄 **2026 更新**：原課程比較的是 4 個模型：`claude-3-5-sonnet-20240620`、`claude-3-opus-20240229`、`claude-3-sonnet-20240229`、`claude-3-haiku-20240307`。新手版改成比較目前還能用的 3 個模型：Opus 4.6、Sonnet 4.6、Haiku 4.5。

```python
import time
def compare_model_speeds():
    models = ["claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5"]
    task = "Explain the concept of photosynthesis in a concise paragraph."

    for model in models:
        start_time = time.time()

        response = client.messages.create(
            model=model,
            max_tokens=500,
            messages=[{"role": "user", "content": task}]
        )

        end_time = time.time()
        execution_time = end_time - start_time
        tokens = response.usage.output_tokens
        time_per_token = execution_time/tokens

        print(f"Model: {model}")
        print(f"Response: {response.content[0].text}")
        print(f"Generated Tokens: {tokens}")
        print(f"Execution Time: {execution_time:.2f} seconds")
        print(f"Time Per Token: {time_per_token:.2f} seconds\n")
```

**逐行解說：**
- `import time`：匯入 Python 內建的「時間」工具，用來計時。
- `def compare_model_speeds():`：定義一個函式（這一格只是「定義」，還沒有真的執行）。
- `models = [...]`：要比較的模型名稱清單。
- `task = "..."`：要問的問題——「用一段簡潔的文字解釋光合作用的概念」。
- `for model in models:`：對清單裡的每一個模型，都做下面縮排的這些事：
  - `start_time = time.time()`：記下「開始的時間」。
  - `response = client.messages.create(model=model, ...)`：用這個模型問問題。
  - `end_time = time.time()`：記下「結束的時間」。
  - `execution_time = end_time - start_time`：結束減開始 = 花了幾秒。
  - `tokens = response.usage.output_tokens`：Claude 的回答有幾個 token。
  - `time_per_token = execution_time/tokens`：平均每個 token 花幾秒。
  - 最後幾行 `print(...)` 把結果印出來。`{execution_time:.2f}` 的意思是「顯示到小數點後 2 位」。

下面這格才是真的「執行」上面定義好的函式（下方顯示的是**原課程用 4 個舊模型**跑出來的結果）：

```python
compare_model_speeds()
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
Model: claude-3-5-sonnet-20240620
Response: Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy. These organisms use sunlight, water, and carbon dioxide to produce glucose (a type of sugar) and oxygen. The process occurs primarily in the chloroplasts of plant cells, where chlorophyll, a green pigment, absorbs light energy. This energy is then used to drive a series of chemical reactions that ultimately result in the production of glucose, which serves as food for the plant and can be stored for later use. Oxygen is released as a byproduct of this process, making photosynthesis crucial for maintaining Earth's atmosphere and supporting life on the planet.
Generated Tokens: 146
Execution Time: 2.56 seconds
Time Per Token: 0.02 seconds

Model: claude-3-opus-20240229
Response: Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize nutrients from carbon dioxide and water. In plants, photosynthesis occurs mainly within the leaves. This process involves the green pigment chlorophyll and generates oxygen as a byproduct. The energy from light is used to convert water, carbon dioxide, and minerals into oxygen and energy-rich organic compounds such as glucose, which are used by the plant for growth and reproduction. Photosynthesis is essential for life on Earth as it provides food for plants, which in turn provide food for other organisms, and it also releases oxygen into the atmosphere, which most living creatures need to survive.
Generated Tokens: 146
Execution Time: 7.32 seconds
Time Per Token: 0.05 seconds

Model: claude-3-sonnet-20240229
Response: Photosynthesis is the process by which plants and certain other organisms convert light energy from the sun into chemical energy in the form of glucose (sugar). During this process, carbon dioxide from the air and water from the soil are absorbed by the plant's leaves. With the aid of chlorophyll (a green pigment) and sunlight, these raw materials are transformed into oxygen, which is released into the atmosphere, and glucose, which serves as the plant's food source and building block for growth and development.
Generated Tokens: 108
Execution Time: 2.64 seconds
Time Per Token: 0.02 seconds

Model: claude-3-haiku-20240307
Response: Photosynthesis is the process by which plants, algae, and some bacteria convert light energy from the sun into chemical energy in the form of carbohydrates. During this process, carbon dioxide and water, with the aid of chlorophyll, are converted into glucose and oxygen through a series of chemical reactions driven by the energy from sunlight. The glucose produced is used by the plant as a source of energy, while the oxygen is released into the atmosphere. This process is essential for the survival of most life on Earth, as it provides the primary source of food and oxygen for many organisms.
Generated Tokens: 126
Execution Time: 1.09 seconds
Time Per Token: 0.01 seconds
```

你自己執行上面程式碼時得到的回答一定會不一樣，不過下面這張表整理了原課程當時那一次執行的結果：

| 模型 | 產生的 token 數 | 執行時間（秒） | 每個 token 花的時間（秒） |
|-------|------------------|--------------------------|--------------------------|
| claude-3-5-sonnet-20240620 | 146 | 2.56 | 0.02 |
| claude-3-opus-20240229 | 146 | 7.32 | 0.05 |
| claude-3-sonnet-20240229 | 108 | 2.64 | 0.02 |
| claude-3-haiku-20240307 | 126 | 1.09 | 0.01 |

另外要注意的是：像「用一段簡潔的文字解釋光合作用的概念」這麼簡單的提示詞，**所有模型的表現都很好**。在這種情況下，選擇最快、最便宜的那一個，應該是最合理的。

上面的例子只是簡單示範模型之間的速度差異，並不是很嚴謹的比較。下面這張圖是我們更嚴謹的測試結果：給所有 3 個模型同一個輸入提示詞、各跑 50 次，然後計算每個模型的平均回應時間。為了確保比較「公平」，我們請模型產生非常長的輸出，再用 `max_tokens`（下一課會教）把所有模型的回答都在**完全相同的 token 數**切斷。

![三個模型的平均回應速度比較圖](../../anthropic_api_fundamentals/images/speed_comparison.png)

---

## 比較模型的能力

很明顯，Haiku 是最快的模型，那我們為什麼還要用其他模型呢？這一切都取決於**模型速度、成本和整體能力之間的取捨**。Haiku 最快，但在某些情況下，它輸出的品質可能比不上 Opus。話雖如此，要特別指出的是：在**很多**情況下，Haiku 的表現可以跟一些更強的模型一樣好。要真正知道哪個模型對你的特定用途來說是「最好的」，**唯一的方法就是實際試用，並評估它們的表現。**

一般來說，我們建議在下面這些用途上，使用我們能力最強的模型 Claude 3.5 Sonnet：
* **寫程式**：Claude 3.5 Sonnet 能自主地撰寫、編輯和執行程式碼，讓程式碼轉換更順暢，更新和遷移也能更快、更準確。
* **客服**：Claude 3.5 Sonnet 能理解使用者的情境，並安排多步驟的工作流程，實現 24 小時全天候服務、更快的回應，以及更高的顧客滿意度。
* **資料科學與分析**：Claude 3.5 Sonnet 能處理非結構化的資料、產生洞見，並製作視覺化圖表和預測，強化資料科學的專業能力。
* **視覺處理**：Claude 3.5 Sonnet 擅長解讀圖表、圖形和圖片，能準確地轉錄文字，得到比單純文字更多的洞見。
* **寫作**：Claude 3.5 Sonnet 在理解細微差異和幽默感方面有顯著進步，能產出高品質、真實、引起共鳴的內容。

如果你對 Claude 家族各模型的基準測試（benchmark）比較有興趣，請閱讀我們的 [Claude 家族模型卡（model card）](https://www-cdn.anthropic.com/f2986af8d052f26236f6251da62d16172cfabd6e/claude-3-model-card.pdf)了解更多資訊。

> 🔄 **2026 更新**：上面「能力最強的是 Claude 3.5 Sonnet」是 2024 年的說法。現在能力最強的模型請看本課最後的「2026 年目前的模型一覽」。

### 能力示範

很難用一個示範就展現每個模型的各種能力，但下面這個函式試著做到這一點。
我們請每個模型解這道數學題：

```
What is the geometric monthly fecal coliform mean of a distribution system with the following FC
 counts: 24, 15, 7, 16, 31 and 23? The result will be inputted into a NPDES DMR, therefore, round
 to the nearest whole number
```

**題目翻譯**：某個配水系統的糞便大腸桿菌（fecal coliform，FC）檢測數量分別是 24、15、7、16、31 和 23，請問它的「每月幾何平均數」是多少？這個結果要填進 NPDES DMR（美國污染物排放許可的排放監測報告），所以請四捨五入到最接近的整數。

**注意：正確答案是 18。**

> 🧩 **白話小補充：幾何平均數怎麼算？** 把 6 個數字全部乘起來（得到 28,748,160），再開 6 次方根，大約是 17.5，四捨五入就是 18。這題需要「多步驟計算」，對 AI 來說有點難度，所以很適合拿來比較模型能力。

我們請每個模型把這道題目解 7 次，記錄每一次的答案：

```python
def compare_model_capabilities():
    models = ["claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5"]
    task = """
    What is the geometric monthly fecal coliform mean of a distribution system with the following FC
 counts: 24, 15, 7, 16, 31 and 23? The result will be inputted into a NPDES DMR, therefore, round
 to the nearest whole number.  Respond only with a number and nothing else.
    """

    for model in models:
        answers = []
        for attempt in range(7):
            response = client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[{"role": "user", "content": task}]
            )
            answers.append(response.content[0].text)

        print(f"Model: {model}")
        print(f"Answers: ", answers)
```

**逐行解說：**
- 提示詞最後多加了一句 `Respond only with a number and nothing else.`（只用一個數字回答，其他什麼都不要說），方便我們比較答案。
- 外層 `for model in models:`：每個模型輪流。
- `answers = []`：準備一個空串列，裝這個模型的 7 個答案。
- 內層 `for attempt in range(7):`：同一個模型重複問 7 次。
- `answers.append(response.content[0].text)`：把每次的答案加進串列。
- 最後把這個模型的 7 個答案印出來。

（新手版同樣把模型清單換成目前可用的 3 個模型；下面顯示的是原課程用 4 個舊模型的結果。）

```python
compare_model_capabilities()
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
Model: claude-3-5-sonnet-20240620
Answers:  ['18', '18', '18', '18', '18', '18', '18']
Model: claude-3-opus-20240229
Answers:  ['18', '18', '18', '18', '18', '18', '18']
Model: claude-3-sonnet-20240229
Answers:  ['18', '17', '16', '17', '19', '18', '18']
Model: claude-3-haiku-20240307
Answers:  ['17', '17', '18', '17', '17', '17', '18']
```

每個模型每次得到的輸出都會不一樣，不過下面是原課程某一次執行結果的整理：

* `claude-3-5-sonnet-20240620`：答對 **7/7** 次
* `claude-3-opus-20240229`：答對 **7/7** 次
* `claude-3-sonnet-20240229`：答對 **3/7** 次
* `claude-3-haiku-20240307`：答對 **2/7** 次

很明顯，在這道數學題上，Claude 3.5 Sonnet 和 Claude 3 Opus 的表現最好。

**注意：這只是一個非常簡化的模型能力示範，完全不是嚴謹的比較，只是為了教學而設計的簡單範例。如果想看更嚴謹、量化的比較（使用業界標準的基準測試），請參考 Claude 3 的模型卡。**

> 🧩 **白話小補充**：注意到了嗎？**同一個模型、同一個問題，問 7 次可能得到不同的答案！** 這是因為 LLM 產生文字時有一定的「隨機性」。下一課的 `temperature` 參數就是用來調整這個隨機程度的。

---

## 選擇模型

接下來很自然的問題就是：我應該用哪一個模型？在不知道應用程式的具體任務和需求的情況下，這是個很難回答的問題。模型的選擇會大大影響應用程式的表現、使用者體驗和成本效益：

* **能力（Capabilities）**
  * 第一個、也是最重要的考量是：這個模型是否具備處理你的應用程式特定任務和使用情境所需的能力。不同模型在不同領域的表現程度不一樣，例如一般語言理解、特定任務的知識、推理能力和產生內容的品質。讓模型的強項和應用程式的需求對上，才能確保最好的結果。
* **速度（Speed）**
  * 模型處理和產生回應的速度是另一個關鍵因素，特別是對於需要即時或接近即時互動的應用程式。越快的模型能提供越即時、越流暢的使用者體驗，降低延遲、提升整體可用性。不過，在速度和模型能力之間取得平衡很重要，因為最快的模型不一定最適合你的特定需求。
* **成本（Cost）**
  * 使用特定模型的相關成本是一個實際的考量，會影響應用程式是否可行、能不能擴大規模。能力越強的模型通常價格也越高——不管是 API 使用費，還是需要的運算資源。評估不同模型的成本影響、並找出「仍然符合應用程式需求、又最划算」的選項，是非常重要的。

#### 一種方法：從 Haiku 開始

在做實驗的時候，我們通常建議**從 Haiku 模型開始**。Haiku 是一個輕量又快速的模型，對很多應用程式來說都是很棒的起點。它的速度和成本效益，讓它成為初期實驗和製作原型時很有吸引力的選擇。在很多使用情境中，Haiku 完全能夠產生符合應用程式需求的高品質回應。從 Haiku 開始，你可以快速地反覆修改你的應用程式、測試不同的提示詞和設定，並在不花太多錢、不用等太久的情況下評估模型的表現。如果你對回應不滿意，要「升級」到像 Claude 3.5 Sonnet 這樣的模型也很容易。

> 🧩 **白話小補充**：「原型（prototype）」就是「先做一個陽春版試試看」。這也是為什麼整套課程大部分都用 Haiku——便宜又快，很適合學習和實驗。

#### 評估與升級

在你開發、改良應用程式的過程中，針對你的使用情境和提示詞，建立一套完整的<strong>評估（evaluation）</strong>是非常重要的。這些評估就像一把尺，可以用來衡量你選擇的模型表現如何，並幫助你在考慮升級時做出明智的決定。

如果你發現 Haiku 的回應不符合應用程式的需求，或是你希望得到更高的精緻度和準確度，你可以很輕鬆地換成能力更強的模型，例如 Sonnet 或 Opus。這些模型的能力更強，能處理更複雜的任務、理解更細微的語言差異。

建立一套嚴謹的評估架構，你就能客觀地比較不同模型在你的特定使用情境下的表現。這些「實際測試出來的證據」會引導你做決定，確保你選到最符合應用程式需求的模型。

> 🧩 **白話小補充**：「怎麼建立評估」是一整門課，就是本套課程的**第 4 單元「提示詞評估」**。

---

## 🔄 2026 年目前的模型一覽（新手版補充）

下面是截至 2026 年 11 月、Anthropic API 上的主要模型（價格是每 100 萬個 token 的美元價格，可能會變動，請以[官方網站](https://docs.anthropic.com/en/docs/about-claude/models)為準）：

| 模型 | 模型名稱（程式裡填的字串） | 輸入價格 | 輸出價格 | 說明 |
|---|---|---|---|---|
| Claude Fable 5.2 | `claude-fable-5-2` | $8 | $40 | 目前一般大眾可用、能力最強的模型 |
| Claude Opus 5.5 | `claude-opus-5-5` | $4 | $20 | 目前最新的 Opus，官方預設推薦的模型 |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | $2 | $10 | 目前最新的 Sonnet，速度和能力平衡 |
| Claude Haiku 5.5 | `claude-haiku-5-5` | $0.10 | $0.50 | 目前最新的 Haiku，最便宜 |
| Claude Opus 4.6 | `claude-opus-4-6` | $5 | $25 | 新手版用來代替 Claude 3 Opus |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | $3 | $15 | 新手版用來代替 Claude 3 / 3.5 Sonnet |
| Claude Haiku 4.5 | `claude-haiku-4-5` | $1 | $5 | 新手版用來代替 Claude 3 Haiku（整套課程最常用） |

**為什麼新手版不直接用最新的 5 系列模型？** 因為它們不支援原課程會用到的某些寫法（預先填寫回答、`temperature` 參數），而且預設會先「思考」，回應格式和原課程不同。詳細原因請看 [0-3 的說明](../00_before_you_start/03_setup_your_computer.md#-2026-更新為什麼模型名稱和原課程不一樣)。
學完這套課程、要做自己的專案時，再換成最新的模型就好。

---

## 📌 重點整理

- 選模型要考慮三件事：**速度（延遲）**、**能力（聰明程度）**、**成本**——三者通常互相取捨。
- **Haiku** 最快最便宜、**Sonnet** 平衡、**Opus** 最聰明（也最貴最慢）。
- 簡單的任務，所有模型都做得好 → 選便宜快速的就好。
- 同一個問題問很多次，答案可能不一樣（LLM 有隨機性）。
- 建議做法：**先用 Haiku 開始**，建立**評估**，不夠好再升級到 Sonnet 或 Opus。

👉 下一課：[1-4 模型參數](04_parameters.md)
