<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`01_prompting_recap.ipynb`](01_prompting_recap.ipynb)。

# 3-1 必備提示詞技巧總複習

> 📚 **第 3 單元：真實世界的提示詞**｜第 1 課 / 共 5 課
> ⏱️ 預估時間：45 分鐘（這一課是純閱讀，沒有程式碼）

## 第 3 單元簡介（原課程 README 翻譯）

歡迎來到 Anthropic 完整的「真實世界提示詞」教學！這門課是為**已經稍微接觸過提示詞工程的開發者**設計的，特別是已經完成我們完整的 **[提示詞工程互動教學](../02_prompt_engineering_tutorial/00_Tutorial_How-To.md)**（也就是本套課程的第 2 單元）的人。如果你還沒讀過那個教學，我們強烈建議你先完成它再繼續，因為它透過動手練習，深入探討了各種提示詞技巧。

在五堂課中，你會學到如何把關鍵的提示詞技巧，融入複雜的、真實世界的提示詞中。建議從第一課「提示詞技巧總複習」開始，因為每一課都建立在前面課程的關鍵觀念之上。

**目錄**
* [3-1 提示詞技巧總複習](01_prompting_recap.md)（就是這一課）
* [3-2 醫療提示詞實作演練](02_medical_prompt.md)
* [3-3 提示詞工程的流程](03_prompt_engineering.md)
* [3-4 通話摘要提示詞實作演練](04_call_summarizer.md)
* [3-5 客服機器人提示詞實作演練](05_customer_support_ai.md)

> 💡 原課程另外有一個 [Google Vertex AI 版本](https://github.com/anthropics/courses/tree/vertex/real_world_prompting)，內容相同，只是連線方式改用 Google Cloud。

---

# 第 1 課：必備提示詞技巧總複習

## 簡介

歡迎來到「應用提示詞（Applied Prompting）」課程的第一課！這門課是為已經稍微接觸過提示詞工程的資深開發者設計的，特別是已經完成我們完整的 **[提示詞工程互動教學](../02_prompt_engineering_tutorial/00_Tutorial_How-To.md)** 的人。如果你還沒讀過那個教學，我們強烈建議你先完成它再繼續，因為它透過動手練習，深入探討了各種提示詞技巧。

在這堂簡短的第一課「必備提示詞技巧總複習」中，我們的目標是**複習**整門課都會用到的基礎提示詞知識。這門課的目的不是重講基礎，而是透過展示這些技巧在**高風險、大規模的正式上線（production）環境**中有多重要，來強化你對這些技巧的掌握。

我們開始吧，看看這些基本技巧能如何改變你在正式上線環境中與 Claude 互動的方式。

> 🧩 **白話小補充**：「正式上線環境（production）」就是「真的給客戶、使用者用的產品」，相對於「自己做實驗」。在 production 裡，提示詞會被執行成千上萬次，一點點小錯誤都可能造成大問題，所以要寫得更嚴謹。

## 重要的提示詞技巧

這一課會介紹下面這些關鍵的提示詞技巧：

0. [使用提示詞產生器（Prompt Generator）](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator)
1. [清楚、直接](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct)
2. [使用 XML 標籤](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
3. [使用範例（多樣本提示）](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)
4. [讓 Claude 思考（思維鏈提示）](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)
5. [給 Claude 一個角色（系統提示詞）](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)
6. [長文本提示技巧](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)

（原課程的編號有點亂，新手版依照下面內容的實際順序重新編號。）

> 💡 **閱讀小提示**：這一課有很多「好的／壞的提示詞範例」。新手版把每個範例的**中文翻譯**直接顯示出來，**英文原文**收在可以點開的「📄 英文原文」裡，需要時再展開對照。

---

## 0. 使用提示詞產生器

開始寫出有效提示詞最簡單的方法，就是使用我們新的**提示詞產生器（Prompt Generator）**工具。我們做了一個工具，可以引導 Claude 產生專門為你的任務量身打造的高品質提示詞。提示詞產生器特別適合用來解決「**空白頁問題**」（不知道從何下筆），給你一個起點，方便接下來的測試和反覆修改，而且它產生的提示詞會遵循我們的一些最佳做法，例如思維鏈和「資料與指示分開」。

使用方法：到 Console（主控台），選擇「Generate a prompt（產生提示詞）」。

![Console 上的「Generate a prompt」按鈕](../../real_world_prompting/images/console.png)

接著，輸入你對想要的提示詞的初步想法。想寫多詳細都可以——Claude 會把你給的所有背景都考慮進去來打造提示詞。

![在提示詞產生器輸入想法](../../real_world_prompting/images/prompt_generator_input.png)

按下「Generate prompt」，等待 Claude 為你產生一個高品質的提示詞，就像下面這樣：

![提示詞產生器產生的結果](../../real_world_prompting/images/prompt_generator_output.png)

我們來仔細看看它幫我們產生的提示詞：

**輸入的文字：**「判斷一篇新聞文章是不是假新聞」

**產生的提示詞（中文翻譯）：**

> 你的任務是判斷一篇新聞文章是假新聞還是真實的新聞。我會提供文章的內容，你需要仔細閱讀和分析它，然後做出判斷。
>
> 這是文章的內容：
> `<article>`
> `{{ARTICLE_TEXT}}`
> `</article>`
>
> 請先仔細閱讀這篇文章，尋找任何可能是假新聞的跡象。注意這些事情：
> - 使用聳動或情緒化的語言
> - 缺乏可信的來源或證據來支持說法
> - 極端的政治偏見或宣揚陰謀論
> - 看起來離譜、不合理或與其他已知事實相矛盾的說法
> - 正規新聞來源應該會寫對的基本資訊，卻出現事實錯誤
>
> 分析完文章後，請在 `<reasoning>` 區塊寫出你的推理過程和你注意到的重點。說明文章中具體是什麼讓你認為它可能是假的或真的。
>
> 最後，根據你的分析，明確判斷你認為這篇文章是假新聞（FAKE）還是真新聞（REAL）。把你的最終答案寫在 `<answer>` 區塊裡。
>
> 記住，假新聞可能很難辨認，所以請批判性地思考，在仔細權衡證據之前不要妄下結論。如果你不確定，判斷時寧可謹慎一點。

<details>
<summary>📄 英文原文</summary>

```
Your task is to determine whether a given news article is fake news or legitimate news. I will provide you with the text of the article, and you will need to carefully read and analyze it to make a determination.

Here is the text of the article:
<article>
{{ARTICLE_TEXT}}
</article>

Please begin by thoroughly reading the article, looking for any potential signs that it may be fake news. Pay attention to things like:
- The use of sensationalized or emotionally charged language
- A lack of credible sources or evidence to support claims
- Extreme political bias or the promotion of conspiracy theories
- Claims that seem outlandish, implausible or contrary to other known facts
- Factual inaccuracies or errors in basic information that a legitimate news source would get right

After analyzing the article, please write out your reasoning and the key points you noticed in a <reasoning> section. Explain what specifically in the article led you to believe it may be fake or legitimate.

Finally, based on your analysis, make a clear determination of whether you believe this article is FAKE news or REAL news. State your final answer in an <answer> section.

Remember, fake news can be tricky to spot, so think critically and don't jump to any conclusions before carefully weighing the evidence. If you're not sure, err on the side of caution in your determination.
```

</details>

> 🧩 **白話小補充**：`{{ARTICLE_TEXT}}` 是 Console 使用的**變數寫法**（兩層大括號），代表「之後要填入文章內容的地方」。這跟第 2 單元在 Python 裡用 f-string 的 `{變數}` 是同一個概念。

這個提示詞融合了許多我們最重要的提示詞工程技巧，包括：
- 清楚、直接的任務定義
- 輸出結構的指示
- 使用 XML 標籤清楚地切分提示詞

**注意：提示詞產生器產生的提示詞，最好當作「起點」，之後再反覆修改。了解我們的關鍵提示詞技巧、以及它們為什麼有效，仍然非常重要，因為這能幫助你改善提示詞產生器做出來的提示詞。**

接下來，我們來複習一些最重要的提示詞工程技巧。

---

## 1. 清楚、直接

### 是什麼：

毫無疑問，**最重要的提示詞技巧也是最簡單的**：寫出明確、詳細、不留模糊空間的指示。這代表要具體說明想要的輸出格式、長度和風格，而且**不要假設 Claude 了解你的使用情境**。說起來容易做起來難，但值得把它做好。

### 為什麼重要：

清楚和精確是最重要的。模糊或含糊的提示詞可能導致誤解、浪費時間，甚至造成代價高昂的錯誤。只要清楚、直接，就能確保 Claude 理解你確切的需求，減少來回釐清的需要，提升提示詞整體的成效。

### 壞的範例：分析顧客意見

想像你是一位產品經理，想要把新版軟體的顧客意見分類並做摘要。

**User（使用者）：**
> 這是一些顧客意見。你可以告訴我大家怎麼想嗎？
> `{{CUSTOMER_FEEDBACK}}`

<details>
<summary>📄 英文原文</summary>

```
Here's some customer feedback. Can you tell me what people think?
{{CUSTOMER_FEEDBACK}}
```

</details>

這個提示詞很模糊，缺乏具體的指示。Claude 可能會給一個籠統的摘要，但不一定會包含你做決策時需要的結構化洞見。

### 好的範例：分析顧客意見

**User（使用者）：**
> 我需要你分析我們最近這次軟體發布的顧客意見：
> `<feedback>{{CUSTOMER_FEEDBACK}}</feedback>`
>
> 請提供一份詳細的報告，包含以下幾個部分：
>
> 1. 摘要（50～100 字）：簡潔地概述整體情緒和主要主題。
> 2. 功能分析：
>    - 列出最受好評的 3 個功能（條列式）
>    - 列出最受批評的 3 個功能（條列式）
> 3. 使用者體驗問題：
>    - 列出最常被回報的 3 個使用問題（條列式）
>    - 每個問題都建議一個可能的修正方式（放在括號裡）
> 4. 情緒分布：
>    - 正面：X%
>    - 中立：Y%
>    - 負面：Z%
> 5. 可執行的洞見（3～5 點）：根據意見得出的重點和建議行動。
>
> 請用 XML 標籤組織你的回答，方便解析：
> `<summary></summary>`
> `<feature_analysis></feature_analysis>`
> `<ux_issues></ux_issues>`
> `<sentiment></sentiment>`
> `<insights></insights>`

<details>
<summary>📄 英文原文</summary>

```
I need you to analyze this customer feedback for our recent software release:
<feedback>{{CUSTOMER_FEEDBACK}}</feedback>

Please provide a detailed report with the following sections:

1. Summary (50-100 words): Concise overview of the general sentiment and main themes.
2. Feature Analysis:
- List top 3 most praised features (bullet points)
- List top 3 most criticized features (bullet points)
3. User Experience Issues:
- List top 3 reported usability problems (bullet points)
- For each issue, suggest a potential fix (in parentheses)
4. Sentiment Breakdown:
- Positive: X%
- Neutral: Y%
- Negative: Z%
5. Actionable Insights (3-5 bullet points): Key takeaways and recommended actions based on the feedback.

Use XML tags to structure your response for easy parsing:
<summary></summary>
<feature_analysis></feature_analysis>
<ux_issues></ux_issues>
<sentiment></sentiment>
<insights></insights>
```

</details>

這個提示詞之所以清楚、直接，是因為它：
- 具體說明了輸入的性質（軟體發布的顧客意見）
- 列出了想要的輸出格式（摘要、條列、編號清單）
- 設定了明確的字數限制（摘要 50～100 字）
- 提供了詳細的回答結構

在這方面，提示詞產生器能幫的忙有限。**在寫提示詞之前，先把你確切的需求規劃清楚是非常關鍵的。** 提示詞產生器可以建議可能的提示詞指示，但最好先自己整理出需求，再去找提示詞產生器幫忙。

### 重點整理

#### 什麼時候用這個技巧
* **永遠都要用**，特別是複雜或關鍵的任務
* 當你需要非常特定的輸出時
* 處理多步驟流程時

#### 它解決的問題
* 誤解指示
* 模糊或不相關的回答
* 任務沒有完整執行

---

## 2. 用 XML 組織提示詞

### 是什麼：

使用 XML 標籤（像 `<tag></tag>`）把提示詞中不同的部分包起來、劃分清楚，例如指示、輸入資料或範例。這個技巧能幫助整理包含多個部分的複雜提示詞。

### 為什麼重要：

要特別說明的是：**寫出有效的 Claude 提示詞並不一定要用 XML 標籤。** 一般來說，複雜的提示詞之所以困難，是因為它們通常會把「指示」和「你塞進去的外部資料」混在同一段沒有結構的文字裡。當這些元素混在同一個提示詞裡，模型就很難分辨哪些是你的指示、哪些是輸入資料，導致混淆。

XML 標籤提供了一種解決方法：在提示詞中把資料和指示分開。我們喜歡用 XML 標籤，因為它們簡短又有資訊量，但你也可以自己想一套獨特的提示詞結構系統。**重要的是，要用某種語法把複雜提示詞的各個部分分開。** 整門課我們都會使用 XML 標籤，因為這是最「Claude 風格」的做法。

### 壞的範例：產品瑕疵分析

你是一家電子產品製造商的品管經理。在顧客客訴激增之後，你需要分析新款智慧手錶的瑕疵報告：

**User（使用者）：**
> 這是 SmartTime 3000 智慧手錶的瑕疵報告摘要：製造品質問題——30% 的產品。電池續航力只有 12 小時，宣傳是 48 小時。健康追蹤資料誤差 25%。軟體錯誤導致 App 當機。
>
> 這是我們目前的庫存：倉庫有 50,000 支，從供應商運送中的有 100,000 支。
>
> 零售價是 299。每支生產成本是 120。
>
> 分析這些瑕疵、它們對我們品牌的影響，並建議應採取的行動。

<details>
<summary>📄 英文原文</summary>

```
Here's a summary of defect reports for the SmartTime 3000 smartwatch: Manufacturing quality issues - 30% of units. Battery life only 12 hours vs advertised 48 hours. Health tracking data inaccurate by 25%. Software bugs causing app crashes.

Here's our current inventory: 50,000 units in the warehouse, 100,000 in transit from suppliers.

Retail price is 299. Production cost is 120 per unit.

Analyze the defects, their impact on our brand, and recommend actions.
```

</details>

這個提示詞有問題，因為：
- 資料、指示和預期的輸出格式全部混在一起。
- Claude 可能會把部分輸入資料誤認為指示，或漏掉關鍵資料。
- 沒有指定輸出結構，Claude 的回答可能很難解析，也很難整合進管理報告裡。

### 好的範例：產品瑕疵分析

現在，我們用 XML 標籤來組織這個提示詞：

**User（使用者）：**
> 我需要你分析我們 SmartTime 3000 智慧手錶的品質問題，並建議應採取的行動。資料如下：
>
> `<defect_report>`（瑕疵報告）
> - 製造品質問題：30% 的產品受影響
> - 電池續航力：12 小時（宣傳：48 小時）
> - 健康追蹤資料：誤差 25%
> - 軟體：回報了多起 App 當機
> `</defect_report>`
>
> `<inventory>`（庫存）
> - 倉庫庫存：50,000 支
> - 運送中：100,000 支
> `</inventory>`
>
> `<financials>`（財務）
> - 零售價：299
> - 每支生產成本：120
> `</financials>`
>
> 請提供一份詳細的報告，包含以下部分：
>
> 1. `<defect_analysis>` 分析每個瑕疵的嚴重程度，以及對使用者體驗和品牌聲譽的潛在影響。`</defect_analysis>`
> 2. `<financial_impact>` 計算因退貨、保固索賠和銷售損失可能造成的損失。同時考慮立即的影響和長期的品牌傷害。`</financial_impact>`
> 3. `<action_plan>` 建議處理這些問題的優先行動，包含時程、成本估計和預期成果。`</action_plan>`

<details>
<summary>📄 英文原文</summary>

```
I need you to analyze the quality issues with our SmartTime 3000 smartwatch and recommend actions. Here's the data:

<defect_report>
- Manufacturing quality issues: 30% of units affected
- Battery life: 12 hours (advertised: 48 hours)
- Health tracking data: 25% inaccuracy
- Software: Multiple app crashes reported
</defect_report>

<inventory>
- Warehouse stock: 50,000 units
- In transit: 100,000 units
</inventory>

<financials>
- Retail price: 299
- Production cost: 120 per unit
</financials>

Please provide a detailed report with the following sections:

1. <defect_analysis> Analyze each defect's severity and potential impact on user experience and brand reputation. </defect_analysis>
2. <financial_impact> Calculate potential losses due to returns, warranty claims, and lost sales. Consider both immediate impact and long-term brand damage. </financial_impact>
3. <action_plan> Recommend prioritized actions to address these issues. Include timelines, cost estimates, and expected outcomes. </action_plan>
```

</details>

這個改寫過的提示詞好很多：

1. **結構化的資料**：每一份資訊都用有描述性的 XML 標籤（`<defect_report>`、`<inventory>`、`<financials>`）包起來。這讓 Claude 非常清楚它處理的是哪一種資訊。
2. **清楚的回答結構**：`<defect_analysis>`、`<financial_impact>` 和 `<action_plan>` 標籤，引導 Claude 用一種方便你和團隊審閱、採取行動的方式組織它的回答。

### 重點整理

#### 什麼時候用這個技巧
* 有多個部分的複雜提示詞
* 需要清楚地把指示和資料分開時
* 要在提示詞中整理不同類型的資訊時

#### 它解決的問題
* 指示和輸入資料之間的混淆
* 對提示詞不同部分的處理不一致
* 複雜提示詞難以解析或理解

---

## 3. 使用範例：「示範教學」的力量

### 是什麼：

提供 Claude 你想要的輸出格式、風格或內容的範例。這些範例就像 Claude 可以照著做的**範本**，幫助它確切了解會收到什麼樣的輸入、以及它產生的輸出應該長什麼樣子。範例確實可能讓提示詞變長，但**在任何正式上線等級的提示詞中，範例幾乎都值得加進去**。

### 為什麼重要：

範例就像具體的範本，讓 Claude 更容易理解並複製你想要的輸出。這在需要格式一致、使用特定行話、或遵守產業標準的任務中特別關鍵。提供範例可以降低誤解的機率，確保 Claude 的輸出符合你的特定需求。**比起試圖用文字描述所有的細微差異，直接給 Claude 看一兩個你想要的輸出範例，通常有效率得多。**

### 壞的範例：撰寫產品發表信

想像你是一家科技公司的行銷總監，需要寫一系列產品發表的電子郵件。沒有範例的話，你的提示詞可能長這樣：

**User（使用者）：**
> 請為我們新的 AI 驅動 CRM 軟體「AcmeAI」寫一封產品發表信。要包含它的主要功能、好處，以及行動呼籲。信件應該專業、吸引人，並強調這個產品能如何改變顧客關係。記得提到它的 AI 能力、價格和上市時間。

<details>
<summary>📄 英文原文</summary>

```
Please write a product announcement email for our new AI-powered CRM software, 'AcmeAI'. Include its key features, benefits, and a call to action. The email should be professional, engaging, and highlight how this product can transform customer relationships. Make sure to mention its AI capabilities, pricing, and availability.
```

</details>

> 🧩 **白話小補充**：CRM（Customer Relationship Management）是「顧客關係管理」軟體，用來管理客戶資料、銷售紀錄等。「行動呼籲（call to action）」是信件結尾請讀者採取行動的那句話，例如「立即預約展示！」

雖然 Claude 很可能會寫出一封還不錯的信，但它不一定能完全符合你們公司的風格、語氣或排版偏好。它也可能漏掉你們這類信件通常會包含的關鍵元素。

### 好的範例：撰寫產品發表信

現在，我們提供範例來引導 Claude：

**User（使用者）（中文翻譯，範例信的內容摘要說明）：**
> 請為我們科技公司最新的創新產品寫一封產品發表信。請依照這些範例的風格和結構：
>
> `<examples>`
> `<example>`
> **主旨：隆重介紹 AcmeDataPulse：重新想像即時分析**
> 親愛的合作夥伴：
> 我們非常興奮地宣布推出 AcmeDataPulse，這是我們劃時代的即時分析平台，旨在改變企業運用資料的方式。
> [主要功能]
> - 即時資料串流：即時處理和分析資料，把決策延遲最多降低 80%。
> - AI 驅動的洞見：我們獨家的機器學習演算法能找出隱藏的模式，讓你取得競爭優勢。
> - 可擴充的架構：不管是 GB 還是 PB 等級的資料，AcmeDataPulse 都能隨你的資料成長。
> [好處]
> - 更快的決策：在幾秒內把資料變成可執行的洞見。
> - 成本效益：按用量付費的模式，用多少付多少。
> - 無縫整合：提供 REST API 和預先建置的連接器，接上你現有的系統。
> AcmeDataPulse 現已上市，每月 499 起。立即預約展示，看看我們如何為你的資料策略加速。
> 祝好，Acme 團隊
> `</example>`
>
> `<example>`
> **主旨：用 AcmeSmartCart Pro 提升你的電商事業**
> 電商領袖們好：
> 我們很興奮地介紹 AcmeSmartCart Pro，這個新世代的購物車解決方案將徹底改變線上零售。
> [主要功能]
> - AI 推薦：用我們先進的推薦引擎，把交叉銷售提升 30%。
> - 一鍵結帳：用簡化的流程把購物車放棄率降低 25%。
> - 多幣別支援：自動換算幣別，打進全球市場。
> [好處]
> - 提高轉換率：零阻力的結帳代表更多銷售。
> - 全球觸及：不用煩惱幣別問題就能賣給全世界的顧客。
> - 永不過時：定期的 AI 更新讓你保持領先。
> 立即入手 AcmeSmartCart Pro，每月 $299 起，前 30 天免費。準備好升級了嗎？請聯絡 sales@acme.com。
> 祝順心，eComCo Innovations 團隊
> `</example>`
> `</examples>`
>
> 請為我們新的 AI 驅動 CRM 軟體「AcmeAI」起草一封產品發表信。重點放在它的主要功能、好處，以及行動呼籲。

<details>
<summary>📄 英文原文</summary>

```
Please write a product announcement email for our tech company's latest innovation. Follow the style and structure of these examples:

<examples>
<example>
Subject: Introducing AcmeDataPulse: Real-time Analytics Reimagined

Dear Valued Partner,

We are thrilled to announce the launch of AcmeDataPulse, our groundbreaking real-time analytics platform designed to transform the way businesses harness data.

[Key Features]
- Live Data Streaming: Process and analyze data in real-time, reducing decision latency by up to 80%.
- AI-Driven Insights: Our proprietary machine learning algorithms uncover hidden patterns, giving you a competitive edge.
- Scalable Infrastructure: Whether it's gigabytes or petabytes, AcmeDataPulse grows with your data.

[Benefits]
- Faster Decision-Making: Turn data into actionable insights within seconds.
- Cost Efficiency: Our pay-as-you-go model means you only pay for what you use.
- Seamless Integration: REST APIs and pre-built connectors for your existing stack.

AcmeDataPulse is now available, starting at 499/month. Schedule a demo today to see how we can supercharge your data strategy.

Best regards,
The Acme Team
</example>

<example>
Subject: Elevate Your eCommerce with AcmeSmartCart Pro

Hello eCommerce Leaders,

We're excited to introduce AcmeSmartCart Pro, the next-gen shopping cart solution that's set to revolutionize online retail.

[Key Features]
- AI-powered Recommendations: Boost cross-sells by 30% with our advanced recommendation engine.
- One-Click Checkout: Reduce cart abandonment by 25% with our streamlined process.
- Multi-currency Support: Tap into global markets with automatic currency conversion.

[Benefits]
- Increased Conversions: Frictionless checkout means more sales.
- Global Reach: Sell to customers worldwide without currency hassles.
- Future-Proof: Regular AI updates keep you ahead of the curve.

Get AcmeSmartCart Pro today starting at $299/month. First 30 days are on us. Ready to upgrade? Contact sales@acme.com.

Cheers,
The eComCo Innovations Team
</example>
</examples>

Please draft a product announcement email for our new AI-powered CRM software, 'AcmeAI'. Focus on its key features, benefits, and a call to action.
```

</details>

在這個例子中，提供的範例依照其他科技公司的標準，示範了產品發表信清楚的結構和語氣。它們強調主要功能和好處、用可量化的數據展現價值、包含價格資訊，並以清楚的行動呼籲作結。Claude 可以用這些範例為 AcmeAI 產生一封類似的信，完美符合這類發表信所期望的風格、結構和內容類型。

透過提供這些範例，我們確保 Claude 會：

1. 使用能吸引讀者注意、並總結發表內容的主旨。
2. 介紹產品時強調它的創新本質。
3. 列出主要功能，附上技術細節和可量化的好處。
4. 強調能打動商業目標（例如顧客滿意度和銷售成長）的整體好處。
5. 提供價格資訊和行動呼籲。
6. 全程使用專業又吸引人的語氣。

這種結構化的做法讓產生的信件只需要極少的修改就能直接使用，既節省時間，又能確保所有產品發表信的一致性。

為了充分發揮範例的效果，請參考下面這些「如何提供最有效的範例」的準則：

* **相關性**：確保你的範例和你預期 Claude 會處理的輸入和輸出非常相似。範例越接近你實際的使用情境，Claude 的表現就越好。
* **多樣性**：包含各種不同的範例，涵蓋不同的情境、邊緣情況和可能的挑戰。這能幫助 Claude 更好地「舉一反三」，處理更廣泛的輸入。
* **數量**：雖然最佳的範例數量沒有硬性規定，但建議一開始至少提供 **3～5 個範例**，給 Claude 一個穩固的基礎。如果 Claude 的表現不如預期，你隨時可以再加入更有針對性的範例。記住：**就算只有一個範例，也比零個範例好。**

### 重點整理

#### 什麼時候用這個技巧
* 要示範想要的輸出格式或風格時
* 解釋複雜或細膩的任務時
* 要讓各種不同輸入的回答更一致時

#### 它解決的問題
* 回答不一致
* 誤解想要的輸出格式
* 不熟悉或複雜的任務結構難以處理

---

## 4. 讓 Claude 思考：強化分析和解決問題的能力

### 是什麼：

「讓 Claude 思考」或「**思維鏈提示（chain of thought prompting）**」，是一種明確指示 Claude 把複雜的問題拆解成一連串邏輯步驟、說明每一步的推理，再根據這些推理給出最終答案或解決方案的技巧。這就像請同事在解決問題時「**邊想邊說出來**」。

### 為什麼重要：

在撰寫高風險的提示詞時，**得出結果的過程往往和決定本身一樣重要**。當 Claude 展示它的推導過程，我們可以得到：

1. **更高的準確度**：把複雜問題拆成步驟，Claude 比較不會跳躍推論或做出可能導致錯誤的假設。
2. **更好的決策**：我們這些人類開發者可以審視 Claude 的推理過程，了解它是怎麼得出結論的，從而在除錯或改善提示詞時做出更明智的決定。
3. **降低風險**：在金融、法律或醫療等領域，了解建議背後的邏輯，對於評估潛在風險和責任非常關鍵。
4. **可問責與透明**：遇到稽核或審查時，你有一份清楚的「決策是怎麼做出來的」紀錄，這對治理和法規遵循非常重要。

### 壞的範例：進軍市場的策略

想像你是一家在美國很成功的軟體公司的執行長，正在考慮擴展到亞洲市場。如果沒有要求逐步分析，你的提問可能長這樣：

**User（使用者）：**
> 我們的軟體公司 AcmeFlow，旗下的專案管理平台在美國非常成功。我們正在考慮擴展到亞洲。這是個好主意嗎？請提供一份給董事會的報告。

<details>
<summary>📄 英文原文</summary>

```
Our software company, AcmeFlow, has seen great success in the U.S. with our project management platform. We're considering expanding into Asia. Is this a good move? Provide a report for the board.
```

</details>

這個提示詞太模糊了。Claude 可能會給一個籠統的回答，缺乏國際擴張這種關鍵商業決策所需要的深度和具體性。

### 好的範例：進軍市場的策略

現在，我們用「讓 Claude 思考」的技巧，引導出更徹底的分析。主要有兩種做法：

1. 在提示詞中**明確告訴 Claude「一步一步思考」**（記得附上一些額外的引導、指示或考量，幫助 Claude 判斷**該怎麼**思考）。Claude 就會在給出最終答案之前，先拆解它的思考過程。
2. 在產生答案之前，**提供 Claude 一個放置想法的地方**。可以考慮使用像 `<thinking>` 和 `<answer>` 這樣的 XML 標籤：指示 Claude 把思考過程放在 `<thinking>` 標籤裡，把最終答案放在 `<answer>` 標籤裡。Claude 就會在標籤裡完成思考過程，再給出最終答案。

**注意：在實際的應用中，我們會想要給 Claude 一些工具，讓它能取得最新的亞洲市場資訊、財經新聞等等。**

我們試著用這個策略，改寫上面那個「壞的」提示詞：

**User（使用者）：**
> 我們的軟體公司 AcmeFlow，旗下的專案管理平台在美國非常成功。我們正在考慮擴展到亞洲。我需要一份完整的分析，向董事會報告。
>
> 這是我們公司的資料：
> `<company_data>`
> `{{ACMEFLOW_DATA}}`
> `</company_data>`
>
> 這是亞洲科技產業的市場研究：
> `<market_research>`
> `{{ASIA_TECH_MARKET}}`
> `</market_research>`
>
> 請分析擴展到亞洲對 AcmeFlow 來說是不是一個好決定。在回答之前先把分析想清楚，考慮所有可能相關的因素，包括市場潛力、競爭、法規挑戰和財務預測，做出一份全面、完整的策略分析。每一個步驟，都請把你的思考過程寫在 `<thinking></thinking>` 標籤裡。分析完之後，在 `<recommendation></recommendation>` 標籤裡給董事會一個明確的建議。
>
> 記住，董事會需要一個有充分理由的論點才能做出明智的決定，所以請分析得徹底一點。

<details>
<summary>📄 英文原文</summary>

```
Our software company, AcmeFlow, has seen great success with our project management platform in the U.S. We're considering expanding into Asia. I need a comprehensive analysis to present to the board.

Here's our company data:
<company_data>
{{ACMEFLOW_DATA}}
</company_data>

Here's market research on the Asian tech sector:
<market_research>
{{ASIA_TECH_MARKET}}
</market_research>

Please analyze whether expanding into Asia is a good move for AcmeFlow. Think through your analysis before you answer, considering all factors around market potential, competition, regulatory challenges, and financial projections that might be relevant to creating a holistic and complete strategic analysis. For each step, provide your thought process within <thinking></thinking> tags. After your analysis, provide a clear recommendation for the board in <recommendation></recommendation> tags.

Remember, the board needs a well-reasoned argument to make an informed decision, so be thorough in your analysis.
```

</details>

下面是上面這個提示詞產生的範例輸出（中文翻譯）：

> `<thinking>`
> **步驟 1：分析市場潛力**
> - AcmeFlow 在美國 1.5 億的營收，顯示在成熟市場中有很強的產品市場契合度。
> - 亞洲科技產業成長快速，年成長率 12%，市場規模 5,000 億。這代表有很大的擴張潛力。
> - 高智慧型手機普及率（80%）和日益增加的數位轉型，顯示對 AcmeFlow 專案管理平台這類科技解決方案有強烈需求。
>
> **步驟 2：評估競爭**
> - 亞洲只有兩個主要的本地競爭者，合計市占率 30%。這留下 70% 的市場，對 AcmeFlow 是很大的機會。
> - 競爭者缺乏即時協作和 AI 驅動洞見這些關鍵功能，而這正是 AcmeFlow 的獨特賣點。這個差異化可能是重大優勢。
>
> **步驟 3：評估法規挑戰**
> - 亞洲的資料隱私法規多元且持續演變。中國和新加坡的法規很嚴格（類似 GDPR），印度和印尼則還在發展中。
> - AcmeFlow 已經符合 GDPR 和 SOC 2 是一個優勢，但我們需要投資在各地區特定的法規遵循上來降低風險。估計成本：30 萬～50 萬。
>
> **步驟 4：財務預測**
> - 進入市場的初期投資：250 萬（包含在地化、行銷、法律費用）
> - 預估第一年營收（保守）：2% 市占率 = 100 億 × 0.02 = 2 億
> - 預估成長率：前 3 年每年 20%，根據我們在美國的成長和亞洲的市場趨勢
> - 5 年預估營收：2 億（第 1 年）× 1.2⁴ ≈ 4.15 億（第 5 年）
> - 損益兩平分析：假設利潤率 30%，我們會在第一年內達到損益兩平。
> `</thinking>`
>
> `<recommendation>`
> 根據這份分析，我強烈建議 AcmeFlow 擴展到亞洲市場。潛在的回報遠遠超過風險。
>
> 重點：
> 1. 龐大的市場機會：5,000 億的市場，年成長 12%。
> 2. 競爭優勢：我們的即時和 AI 功能勝過本地競爭者。
> 3. 高投資報酬率：250 萬的初期投資，第一年可能帶來 2 億營收，且每年強勁成長。
> 4. 可控的風險：法規遵循成本雖然不小，但相對於營收潛力是可以承擔的。
>
> 市場已經成熟、我們的產品更優秀、財務數字也很吸引人。及早進入能讓我們在市場更飽和之前站穩腳步。我建議分階段推出，從我們市場研究資料最完整的新加坡和印度開始。
> `</recommendation>`

<details>
<summary>📄 英文原文</summary>

```
<thinking>
Step 1: Analyze market potential
- AcmeFlow's U.S. revenue of 150M shows strong product-market fit in a mature market.
- Asia's tech sector is growing rapidly, with a 12% YoY growth and a 500B market size. This indicates significant potential for expansion.
- High smartphone penetration (80%) and increasing digital transformation suggest a strong demand for tech solutions like AcmeFlow's project management platform.

Step 2: Assess competition
- Only two major local competitors in Asia with a combined 30% market share. This leaves 70% of the market open, a substantial opportunity for AcmeFlow.
- Competitors lack key features like real-time collaboration and AI-driven insights, which are AcmeFlow's USPs. This differentiation could be a significant advantage.

Step 3: Evaluate regulatory challenges
- Data privacy laws in Asia are diverse and evolving. In China and Singapore, laws are stringent (similar to GDPR), while in India and Indonesia, they're still developing.
- AcmeFlow's existing compliance with GDPR and SOC 2 is advantageous, but we'll need to invest in region-specific compliance to mitigate risks. Estimated cost: 300,000-500,000.

Step 4: Project financials
- Initial investment for market entry: 2.5M (includes localization, marketing, legal fees)
- Projected first-year revenue (conservative): 2% of market share = 10B * 0.02 = 200M
- Estimated growth rate: 20% YoY for first 3 years, based on our U.S. growth and Asia's market trend
- 5-year projected revenue: 200M (Y1) * 1.2^4 ≈ 415M (Y5)
- Break-even analysis: Assuming 30% profit margin, we'll break even within the first year.
</thinking>

<recommendation>
Based on the analysis, I strongly recommend that AcmeFlow expands into the Asian market. The potential rewards far outweigh the risks.

Key points:
1. Massive market opportunity: 500B market with rapid 12% YoY growth.
2. Competitive advantage: Our real-time and AI features outshine local competitors.
3. High ROI: Initial 2.5M investment could yield 200M in first year, with strong YoY growth.
4. Manageable risks: Compliance costs are significant but manageable given the revenue potential.

The market is ripe, our product is superior, and the financials are compelling. Early entry will allow us to establish a strong foothold before the market becomes more saturated. I recommend proceeding with a phased rollout, starting with Singapore and India where we have the strongest market research data.
</recommendation>
```

</details>

這個回答展示了「讓 Claude 思考」的威力：

1. **結構化的分析**：`<thinking>` 標籤裡有一步一步的分析，有邏輯地拆解了決策過程。這讓董事會可以跟著 Claude 的推理，評估每一個論點。這也讓我們這些開發者能夠洞察 Claude 的思考過程，必要時增補或修改提示詞。
2. **關鍵洞見**：Claude 強調了市場規模、競爭態勢、法規挑戰和財務預測等關鍵因素。這些洞見展現了對商業背景的深刻理解。
3. **明確的建議**：`<recommendation>` 標籤裡是一個簡潔、可執行的建議，並有分析中的重點作為支持。分階段推出的策略展現了策略思維，在企圖心和審慎之間取得平衡。`<recommendation>` 標籤也讓我們很容易擷取相關的「最終」資訊，拿到別的地方使用。

> 🧩 **白話小補充**：細心的讀者可能會發現，範例輸出的財務推算其實有點問題（例如前面說市場規模 5,000 億，計算時卻用 100 億；「第一年就損益兩平」也太樂觀）。這反而說明了「讓 Claude 寫出思考過程」的另一個好處：**錯誤會攤在陽光下**，人類可以檢查出來，而不是只看到一個漂亮的結論就照單全收。

使用「讓 Claude 思考」的技巧，我們把一個原本可能只有一句話的模糊回答，變成了一份完整、可以直接拿到董事會報告的分析。對國際擴張這種高風險的商業決策來說，這種程度的細節和清晰度非常寶貴。

### 重點整理

#### 什麼時候用這個技巧
* 複雜的推理任務
* 需要了解 Claude 的邏輯時（為了除錯）
* 為了好好引導 Claude 完成多步驟的問題解決

#### 它解決的問題
* 決策過程不透明
* 邏輯不一致
* 在複雜流程中跳過步驟

---

## 5. 給 Claude 一個角色

### 是什麼：

Claude 是一個非常能幹的助理，但有時候，如果能多一些「它在這段對話中應該扮演什麼角色」的資訊，它會表現得更好。指定一個角色給 Claude，可以讓它用特定的方式回應、提升準確度和表現，並讓它的語氣和態度符合想要的情境。這個技巧也叫做**角色提示**。

一種做法是直接在主要的使用者提示詞裡加上角色提示的文字，但**我們建議把角色資訊放在系統提示詞（`system_prompt`）裡**。請注意：**角色資訊是我們唯一建議放在系統提示詞裡的資訊類型。**

### 為什麼重要：

在正式上線的提示詞中，**一致性是關鍵**：Claude 的語氣、專業程度和角色資訊都應該保持一致。用系統提示詞做角色提示，能確保 Claude 在多次互動中維持一致的口吻和專業程度。

角色提示在下面這些情況特別有用：
- **高度技術性的任務**：如果你需要 Claude 執行和邏輯、數學或程式相關的複雜任務，指定一個適當的角色可以幫助它表現出色，即使沒有角色提示時它可能做得很吃力。
- **特定的溝通風格**：當你需要 Claude 的回答有特定的語氣或風格時，角色提示是達成目標的有效方法。
- **提升基本表現**：除非你受到 token 數量的嚴格限制，否則如果你想讓 Claude 的表現超越它的基本能力，幾乎沒有理由不使用角色提示。

### 壞的範例：回應產品危機

你的公司 AcmeEV 剛剛發現最新款電動車有一個嚴重的軟體錯誤，可能導致車輛意外加速。你的公關團隊需要起草一份公開聲明，但他們忙不過來。他們請 Claude 幫忙，卻沒有提供太多指引：

**User（使用者）：**
> 我們的新電動車有一個錯誤，可能會導致突然加速。我們需要馬上發一份公開聲明。你可以幫我們寫點東西嗎？這是個嚴重的問題，所以要確保聽起來還可以。

<details>
<summary>📄 英文原文</summary>

```
Our new EV has a bug that can cause sudden acceleration. We need a public statement ASAP. Can you write something for us? It's a serious issue, so make sure it sounds ok.
```

</details>

這個提示詞有問題，因為：
- 它沒有給 Claude 任何角色或背景，所以 Claude 可能無法掌握情況的嚴重性。
- 「確保聽起來還可以」很模糊。Claude 需要知道在這個關鍵的情境下，「還可以」是什麼意思。
- **沒有任何關於語氣、關鍵訊息或目標受眾的指引，可能導致回答不符合公司的危機溝通策略。**

### 好的範例：回應產品危機

現在，我們用角色提示來得到更適當的回答：

**System（系統提示詞）：**
> 你是 AcmeEV 的**首席溝通長（CCO）**，AcmeEV 是一家以創新和安全聞名的領先電動車製造商。你在危機溝通方面有 20 年的經驗，處理過從產品召回到執行長醜聞的各種問題。你的溝通風格**有同理心又有權威感**，永遠把公眾安全放在第一位，同時維護品牌的誠信。

**User（使用者）：**
> 我們在新款 Model E 上發現了一個嚴重的軟體錯誤，可能導致意外加速。這個問題影響了上一季售出車輛的 70%。我們的工程團隊正在處理，但修正可能需要長達兩週。請起草一份立即發布的公開聲明。
>
> `<crisis_communication_guidelines>`（危機溝通準則）
> 1. 迅速承認問題，並對受影響的人表達關心。
> 2. 清楚說明問題和可能的影響，避免技術術語。
> 3. 概述為確保安全已立即採取的行動。
> 4. 提供明確的解決時程，並定期更新。
> 5. 重申公司的價值（安全、創新）和對顧客的承諾。
> 6. 提供直接的溝通管道，讓大家反映疑慮。
> 7. 以展望未來的聲明作結，重建信任。
>
> 記住，在危機中，速度、透明和同理心是關鍵。你的每一個字都會被媒體、顧客和股東仔細檢視。目標是保護公眾安全、維護品牌聲譽，並為復原打好基礎。
> `</crisis_communication_guidelines>`
>
> 請依照下列步驟：
> 1. 檢視提供的資訊，找出關鍵事實（受影響的比例、修正所需時間）。
> 2. 依照我們的危機溝通準則起草聲明。使用在關心和自信之間取得平衡的語氣。
> 3. 加入一段執行長的引言，強調我們對安全的承諾。
>
> 把你的分析寫在 `<analysis></analysis>` 標籤裡，把最終的聲明寫在 `<statement></statement>` 標籤裡。

<details>
<summary>📄 英文原文</summary>

**System:**
```
You are the Chief Communications Officer (CCO) at AcmeEV, a leading electric vehicle manufacturer known for innovation and safety. You have 20 years of experience in crisis communications, having handled issues from product recalls to CEO scandals. Your communication style is empathetic yet authoritative, always prioritizing public safety while maintaining brand integrity.
```

**User:**
```
We've discovered a critical software bug in our new Model E that can cause unintended acceleration. The issue affects 70% of cars sold in the last quarter. Our engineering team is working on it, but the fix may take up to two weeks. Draft a public statement for immediate release.
<crisis_communication_guidelines>
1. Acknowledge the issue promptly and express concern for affected parties.
2. Clearly state the problem and its potential impact, avoiding technical jargon.
3. Outline immediate actions taken to ensure safety.
4. Provide a clear timeline for resolution and regular updates.
5. Reaffirm company values (safety, innovation) and commitment to customers.
6. Offer a direct line of communication for concerns.
7. Close with a forward-looking statement to rebuild trust.

Remember, in a crisis, speed, transparency, and empathy are key. Your words will be scrutinized by the media, customers, and shareholders alike. The goal is to protect public safety, maintain brand reputation, and set the stage for recovery.
</crisis_communication_guidelines>

Follow these steps:
1. Review the provided information and identify key facts (percentage affected, timeframe for fix).
2. Draft the statement following our crisis communication guidelines. Use a tone that balances concern with confidence.
3. Include a quote from the CEO that reinforces our commitment to safety.

Write your analysis within <analysis></analysis> tags, and your final statement within <statement></statement> tags.
```

</details>

> 🧩 **白話小補充**：注意這個好範例**不只**用了角色提示——它同時用了清楚的指示、XML 標籤（準則）、步驟（思考）和輸出格式。真實世界的提示詞，通常都是好幾種技巧一起用。

### 重點整理

#### 什麼時候用這個技巧
* 要設定特定的背景或觀點時
* 需要具備特定專業的回答時
* 要影響回答的語氣或風格時

#### 它解決的問題
* 回答不符合情境
* 語氣或風格不一致
* 回答沒有對應到特定的專業

---

## 6. 長文本提示

Claude 擴大的**上下文視窗（context window）**讓它能處理需要大量資料的複雜任務。當你在提示詞中把大量資訊（特別是 **3 萬個 token 以上**）和指示結合在一起時，很重要的一點是：組織提示詞時要**清楚地把輸入資料和指示分開**。我們建議用 XML 標籤把每一份文件包起來，讓 Claude 清楚知道輸入資料在哪裡結束、指示／範例／提示詞的其他部分從哪裡開始。

此外，**我們建議把長文件和背景資料放在提示詞的最前面**，指示和範例放在後面。如果文件放在詳細指示或使用者問題的**上方**，Claude 的表現通常會明顯比較好。

> 🧩 **白話小補充**：「上下文視窗」就是 Claude 一次能讀進去的文字量上限（以 token 計算）。可以想成 Claude 的「工作桌」大小：桌子越大，一次能攤開越多文件。

### 好的範例：分析市場趨勢

**User（使用者）：**
> 我們即將推出「AcmeAI」——一款 AI 驅動的 CRM，我需要一份完整的分析。請檢閱這些市場研究報告並提供洞見：
>
> `<reports>`
> `<report_1>`
> `{{GLOBAL_TECH_TRENDS_2023}}`（2023 全球科技趨勢）
> `</report_1>`
> `<report_2>`
> `{{CRM_MARKET_ANALYSIS}}`（CRM 市場分析）
> `</report_2>`
> `<report_3>`
> `{{COMPETITOR_LANDSCAPE}}`（競爭者概況）
> `</report_3>`
> `</reports>`
>
> 請產生一份詳細的報告，包含以下部分：
>
> 1. 執行摘要（100～150 字）：整合主要發現，以及它們對 AcmeAI 上市的意義。
> 2. 市場機會：
>    - 全球 CRM 市場規模和成長率
>    - CRM 中的 AI 採用率：現況和預測
>    - 各地區的市場潛力（著重北美、歐洲和亞太地區）
> 3. 競爭者分析：
>    - 前 3 大競爭者的市占率和成長率
>    - 他們的 AI 能力 vs. 我們的（使用比較表）
>    - 他們的產品中 AcmeAI 可以切入的缺口
> 4. 上市策略（時間軸）：
>    - 2024 年第三季：關鍵里程碑和行銷活動
>    - 2024 年第四季：銷售目標和合作夥伴目標
>    - 2025 年第一季：上市後檢討和產品路線圖
> 5. 風險評估：
>    - 著重 AI 相關因素的 SWOT 分析
>    - 前 3 大風險的因應策略
>
> 每個主要部分都用 `<section></section>` 標籤包起來，讓報告容易解析。

<details>
<summary>📄 英文原文</summary>

```
I need a comprehensive analysis for our upcoming launch of 'AcmeAI', an AI-powered CRM. Please review these market research reports and provide insights:

<reports>
<report_1>
{{GLOBAL_TECH_TRENDS_2023}}
</report_1>
<report_2>
{{CRM_MARKET_ANALYSIS}}
</report_2>
<report_3>
{{COMPETITOR_LANDSCAPE}}
</report_3>
</reports>

Generate a detailed report with the following sections:

1. Executive Summary (100-150 words): Synthesize the key findings and their implications for AcmeAI's launch.
2. Market Opportunity:
- Global CRM market size and growth rate
- AI adoption in CRM: current and projected
- Region-wise market potential (focus on North America, Europe, and Asia-Pacific)
3. Competitor Analysis:
- Top 3 competitors' market share and growth rates
- Their AI capabilities vs. ours (use a comparison table)
- Gaps in their offerings that AcmeAI can exploit
4. Launch Strategy (timeline view):
- Q3 2024: Key milestones and marketing initiatives
- Q4 2024: Sales targets and partnership goals
- Q1 2025: Post-launch review and product roadmap
5. Risk Assessment:
- SWOT analysis focusing on AI-specific factors
- Mitigation strategies for top 3 risks

Use <section></section> tags for each main section to make the report easy to parse.
```

</details>

> 🧩 **白話小補充**：SWOT 是常見的分析框架：Strengths（優勢）、Weaknesses（劣勢）、Opportunities（機會）、Threats（威脅）。

這個提示詞非常有效，因為：

1. **文件放在最前面**：長文件放在詳細的提示詞指示之前。
2. **結構化的資料**：每一份報告都用 XML 標籤（`<report_1>`、`<report_2>`、`<report_3>`）清楚地劃分，並放在一個更大的 `<reports>` 標籤裡，讓 Claude 很容易分辨和引用不同的資料來源。
3. **清楚的指示**：提示詞具體說明了 Claude 應該從每份報告中擷取什麼（市場規模、AI 採用率、競爭者分析），降低遺漏關鍵資料的機率。
4. **輸出用 XML 標籤**：`<section>` 標籤讓程式很容易解析 Claude 的回答，方便把這份輸出整合到其他業務流程或簡報中。

### 重點整理

#### 什麼時候用這個技巧
* 處理大量輸入資料時

#### 它解決的問題
* 難以處理又大又複雜的輸入

---

## 結論

這些技巧構成了一套強大的工具組，可以在各種任務上提升 Claude 的表現。只要用心運用，就能大幅提升 Claude 輸出的準確度、一致性和相關性。隨著你持續使用 Claude，你會逐漸培養出「在什麼情況下該用哪種技巧」的直覺。

我們鼓勵你把這些技巧應用在自己的專案中，並持續探索優化與 Claude 互動的新方法。AI 領域正在快速發展，提示詞工程的最佳做法也是一樣。

---

## 📌 重點整理（新手版）

| # | 技巧 | 一句話記住 |
|---|---|---|
| 0 | 提示詞產生器 | 解決「空白頁問題」的起點，產生後還要再修改 |
| 1 | 清楚、直接 | **永遠要用**：明確說出格式、長度、風格，不要假設 Claude 懂你的情境 |
| 2 | XML 標籤 | 把資料、指示、範例分開；也能規定輸出的結構 |
| 3 | 範例 | 正式上線的提示詞幾乎都該有；相關、多樣、3～5 個 |
| 4 | 讓 Claude 思考 | `<thinking>` 寫推理、`<answer>` 寫結論；更準確、可除錯、可稽核 |
| 5 | 角色 | 放在**系統提示詞**裡（這也是唯一建議放在系統提示詞的資訊） |
| 6 | 長文本 | 長文件放**最前面**、用 XML 標籤分開，指示和問題放後面 |

👉 下一課：[3-2 醫療提示詞實作演練](02_medical_prompt.md)
