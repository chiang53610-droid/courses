<!--meta {"orig": "real_world_prompting/02_medical_prompt.ipynb", "out": "03_real_world_prompting/02_medical_prompt"} -->
# 3-2 一個真實世界的提示詞：醫療病歷摘要

> 📚 **第 3 單元：真實世界的提示詞**｜第 2 課 / 共 5 課
> ⏱️ 預估時間：50 分鐘

## 🎯 這一課你會學到

- 從一個「很爛」的提示詞開始，**一步一步**用上一課的技巧把它改好
- 依序加入：系統提示詞（角色）→ XML 標籤包住資料 → 清楚的指示 → 範例 → 輸出用 XML 標籤
- 最後把輸出改成 **JSON**，讓程式可以直接拿來用

> 🔄 **2026 更新**：這一課的程式碼原本使用 `claude-3-sonnet-20240229`，新手版換成 `claude-sonnet-4-6`。下面顯示的執行結果是原課程用舊模型跑出來的。
>
> ⚠️ **免責聲明（新手版補充）**：這一課的病歷都是**虛構**的教學範例。用 AI 摘要真實病歷時，必須遵守個資與醫療法規，而且 AI 的摘要一定要經過醫療專業人員確認。

---

在上一課，我們討論了幾個關鍵的提示詞技巧，並看到了每個技巧單獨使用的例子。現在，我們來試著寫一個**大得多**、融合了剛剛介紹的多種技巧的提示詞。

## 我們的提示詞目標

這一課的重點是寫一個「**病歷摘要器**」提示詞：它會讀入很長的病歷，產生一份包含重要資訊的摘要，幫助醫師為即將到來的門診做準備。

每一份病患病歷大概長這樣（以下是中文翻譯，英文原文在下方）：

> **病患姓名：** Evelyn Thompson　**年齡：** 78
> **病歷：**
> - 1985：診斷出第二型糖尿病，開始服用 metformin（二甲雙胍）
> - 1992：出現高血壓，開立 lisinopril（賴諾普利）
> - 1998：因骨關節炎進行（右側）全髖關節置換術
> - 2000：診斷出甲狀腺功能低下，開始服用 levothyroxine（左旋甲狀腺素）
> - 2003：白內障手術（雙眼）
> - 2005：因心房顫動住院，開始服用 warfarin（抗凝血劑）
> - 2008：診斷出維生素 B12 缺乏，開始每月注射
> - 2010：因 A1C（糖化血色素）上升，增加 metformin 劑量
> - 2011：因短暫性腦缺血發作（TIA）住院，加上 aspirin（阿斯匹靈）
> - 2013：診斷出第二期乳癌，進行乳房腫瘤切除術和放射治療
> - 2014：開始服用 anastrozole，預防乳癌復發
> - 2015：出現第三期慢性腎臟病（CKD），調整 metformin
> - 2017：因骨關節炎進行（左側）全膝關節置換術
> - 2018：因肺炎住院，接受靜脈注射抗生素治療
> - 2019：發現輕度認知障礙，開始服用 donepezil（愛憶欣）
> - 2020：因頑固性高血壓，增加 lisinopril 劑量
> - 2021：反覆泌尿道感染，開立低劑量預防性抗生素
> - 2022：年度乳房攝影正常，但 eGFR（腎絲球過濾率）顯示腎功能惡化
> - 2023：行動能力下降，開始物理治療和居家照護員到府服務

<details>
<summary>📄 英文原文</summary>

```
Patient Name: Evelyn Thompson
Age: 78
Medical Record:

1985: Diagnosed with type 2 diabetes, started on metformin
1992: Developed hypertension, prescribed lisinopril
1998: Total hip replacement (right) due to osteoarthritis
2000: Diagnosed with hypothyroidism, started on levothyroxine
2003: Cataract surgery (both eyes)
2005: Admitted for atrial fibrillation, started on warfarin
2008: Vitamin B12 deficiency diagnosed, monthly injections started
2010: Increased metformin dose due to rising A1C levels
2011: Admitted for transient ischemic attack (TIA), added aspirin to regimen
2013: Diagnosed with stage 2 breast cancer, underwent lumpectomy and radiation
2014: Started on anastrozole for breast cancer recurrence prevention
2015: Developed chronic kidney disease (CKD) stage 3, metformin adjusted
2017: Total knee replacement (left) due to osteoarthritis
2018: Hospitalized for pneumonia, treated with IV antibiotics
2019: Mild cognitive impairment noted, started on donepezil
2020: Lisinopril dosage increased due to refractory hypertension
2021: Recurrent UTIs, prescribed low-dose prophylactic antibiotics
2022: Annual mammogram clear, but eGFR shows worsening kidney function
2023: Mobility declining, started physical therapy and home health aide visits
```

</details>

我們的最終目標是產生**格式一致**的病歷摘要，幫助醫療人員為即將到來的門診做準備。每一份摘要都應該包含下面這些關鍵資訊：

* 病患姓名
* 病患年齡
* 主要診斷
* 病患被開立的藥物清單
* 近期的疑慮
* 醫療人員的待辦事項

上面那份病歷的範例輸出可能長這樣（中文翻譯）：

> **姓名：** Evelyn Thompson　**年齡：** 78
>
> **主要診斷：** 第二型糖尿病（1985）、高血壓（1992）、骨關節炎（1998 和 2017 年髖、膝關節置換）、甲狀腺功能低下（2000）、心房顫動（2005）、維生素 B12 缺乏（2008）、短暫性腦缺血發作（2011）、乳癌（2013）、第三期慢性腎臟病（2015）、肺炎（2018）、輕度認知障礙（2019）、反覆泌尿道感染（2021）
>
> **藥物：** metformin（糖尿病）、lisinopril（高血壓）、levothyroxine（甲狀腺功能低下）、warfarin（心房顫動）、aspirin（抗血小板）、anastrozole（預防乳癌復發）、donepezil（認知障礙）、低劑量預防性抗生素（反覆泌尿道感染）
>
> **其他治療：** 全髖關節置換（1998）、白內障手術（2003）、維生素 B12 注射（2008）、乳房腫瘤切除和放射治療（乳癌，2013）、全膝關節置換（2017）、物理治療和居家照護（2023）
>
> **近期疑慮：** 腎功能惡化（2022 年 eGFR 下降）、行動能力下降（2023）
>
> **待辦事項：** 監測腎功能並視需要調整藥物、持續物理治療和居家照護支援、評估認知退化並調整治療計畫、處理行動能力問題和跌倒風險、確保遵循建議的癌症篩檢

<details>
<summary>📄 英文原文</summary>

```
Name: Evelyn Thompson
Age: 78

Key Diagnoses:
- Type 2 Diabetes (1985)
- Hypertension (1992)
- Osteoarthritis (Hip and Knee Replacements in 1998 and 2017)
- Hypothyroidism (2000)
- Atrial Fibrillation (2005)
- Vitamin B12 Deficiency (2008)
- Transient Ischemic Attack (TIA) (2011)
- Breast Cancer (2013)
- Chronic Kidney Disease (CKD) Stage 3 (2015)
- Pneumonia (2018)
- Mild Cognitive Impairment (2019)
- Recurrent Urinary Tract Infections (UTIs) (2021)

Medications:
- Metformin (Diabetes)
- Lisinopril (Hypertension)
- Levothyroxine (Hypothyroidism)
- Warfarin (Atrial Fibrillation)
- Aspirin (Antiplatelet)
- Anastrozole (Breast Cancer Recurrence Prevention)
- Donepezil (Cognitive Impairment)
- Low-dose Prophylactic Antibiotics (Recurrent UTIs)

Other Treatments:
- Total Hip Replacement (1998)
- Cataract Surgery (2003)
- Vitamin B12 Injections (2008)
- Lumpectomy and Radiation (Breast Cancer, 2013)
- Total Knee Replacement (2017)
- Physical Therapy and Home Health Aide (2023)

Recent Concerns:
- Worsening Kidney Function (eGFR Decline in 2022)
- Declining Mobility (2023)

Action Items:
- Monitor Kidney Function and Adjust Medications as Needed
- Continue Physical Therapy and Home Health Support
- Evaluate for Cognitive Decline and Adjust Treatment Plan
- Address Mobility Issues and Fall Risk
- Ensure Adherence to Recommended Cancer Screening
```

</details>

下面是一個包含 5 份病歷的 Python 串列，我們會用它來測試我們的提示詞：

{{cell 4}}

（5 位虛構病患：78 歲的 Evelyn Thompson、42 歲的 Marcus Reyes（心理健康相關病史）、8 歲的 Lily Chen（先天性心臟病）、25 歲的 Jason Tran（運動傷害和心理健康）、36 歲的 Amira Khan（紅斑性狼瘡）。）

我們先看其中一份，確認串列沒問題：

{{cell 6}}

> 🧩 **白話小補充**：輸出裡的 `\n` 代表換行。因為 notebook 直接顯示「字串本身」，所以換行會顯示成 `\n`；如果用 `print()` 印出來，就會真的換行。

---

## 一開始的「爛」提示詞

我們先從一個非常簡單的提示詞開始，請 Claude 幫我們產生摘要。一個非常簡單的第一次嘗試可能長這樣：

> 我有這份病患病歷。你可以幫我做個摘要嗎？
>
> {病歷放在這裡}
>
> 我需要在病患明天門診之前快速看一下。

我們把它整理成一個具體的提示詞，可以動態地插入病歷：

{{cell 8}}

接著，我們寫一個簡單的函式：接收一份病歷，把它插入提示詞，然後請 Claude 產生摘要：

{{cell 10}}

**逐行解說：**
- `initial_prompt.format(record=patient_record)`：把病歷填進提示詞範本裡的 `{record}`。
- `client.messages.create(...)`：送出請求（這裡沒有系統提示詞）。
- 印出分隔線和 Claude 的回答。

我們用 `patient_records` 串列裡全部 5 份病歷試試看：

{{cells 12-16}}

仔細看看 Claude 產生的這些摘要，它們**五花八門**！有些摘要只是一長段文字，有些則拆成條列式清單。每份摘要的實際內容差異也非常大。摘要的內容不算太差，但**格式、長度和摘要資料的類型都不一致**，很難讓程式拿來使用。我們來改善它吧！

---

## 改善提示詞

就像我們在上一課學到的，有一套明確的提示詞技巧可以幫助我們得到更好、更一致的結果，包括：

* 加入清楚的**系統提示詞**，設定助理的背景和角色，例如醫療專業人員或醫療資料分析師
* 用 **XML 標籤**（例如 `<patient_record>`）組織輸入資料，清楚表示提示詞的哪一部分是輸入資料
* 提供**清楚、具體的指示**，說明摘要應該著重什麼，例如診斷、藥物和近期的健康疑慮
* **指定**摘要想要的**格式**，例如條列式，或有特定段落的結構化格式
* 加入一個格式良好的摘要**範例**，引導助理的回答
* 用某種**輸出用的 XML 標籤**組織輸出，讓使用者能快速找到相關資訊

**在接下來的課程中，我們會討論一種具體、細膩的提示詞工程方法，以及怎麼挑選提示詞技巧。在這一課，我們先用「散彈槍」的方法，一次把所有技巧都用上。**

### 加入系統提示詞

我們一個一個來處理這些建議。首先，定義一個系統提示詞，設定助理的背景和角色。根據我們的經驗，**這是唯一應該放在系統提示詞裡的資訊**。

在我們的使用情境中，系統提示詞應該告訴 Claude：它的角色是一位擅長把冗長的病史轉換成簡潔摘要的醫療專業人員。

這是其中一種寫法：

{{cell 20}}

**系統提示詞翻譯**：「你是一位經驗非常豐富的醫療專業人員，專長是把複雜的病史轉換成簡潔、可據以行動的摘要。你的角色是分析病患病歷、找出關鍵資訊，並用清楚、結構化的格式呈現，協助診斷和治療計畫。對於需要在門診前快速掌握病患病史的忙碌醫療人員來說，你的摘要非常寶貴。」

### 組織輸入資料

使用 Claude 時，最重要的提示詞技巧之一，就是**用 XML 標籤清楚地標示輸入資料**。在我們目前的提示詞中，是這樣提供病史作為主要輸入的：

> 我有這份病患病歷。你可以幫我做個摘要嗎？
>
> {病歷放在這裡}
>
> 我需要在病患明天門診之前快速看一下。

一個能帶來大幅改善的簡單修改，就是用 XML 標籤把輸入資料包起來。我們用 `<patient_record>` 標籤更新提示詞：

{{cell 22}}

（程式碼裡的註解「Improved Prompt (still a work in progress!)」意思是「改良版提示詞（還在進行中！）」。）

### 提供清楚的指示

使用 Claude 時，提供清楚、直接的指示是得到最好結果的關鍵。就像我們第一次教人做某項任務一樣，我們越是直截了當地解釋我們到底想要什麼，Claude 的回答就會越好、越準確。

在一開始的「爛」提示詞中，我們的指示是：

> 我有這份病患病歷。你可以幫我做個摘要嗎？

這實在模糊得可憐！我們需要想出一套清楚、具體的指示。我們到底希望摘要長什麼樣子？

假設我們希望摘要包含下面這幾類不同的資訊：

* 病患姓名
* 病患年齡
* 主要診斷清單
* 病患被開立的藥物清單
* 非藥物治療的清單（物理治療、CBT 等）
* 近期疑慮清單
* 給醫師的重要待辦事項清單

同樣重要的是，要具體說明我們想要的**確切輸出格式**，所以我們會明確要求 Claude 使用「**條列式清單**」，而不只是籠統的「清單」。

這是更新後的提示詞：

{{cell 24}}

**新增的指示翻譯**：「我需要你幫忙替我們的醫師團隊摘要病患病歷。我們明天有一連串的回診，醫師需要快速、有洞見的摘要來做準備。每份摘要都應該**依照這個順序**包含下列元素：
- 病患姓名
- 病患年齡
- 依時間順序排列的主要診斷條列清單
- 病患被開立的藥物條列清單
- 其他治療的條列清單：像 CBT 或物理治療這類非藥物治療
- 簡短的近期疑慮條列清單
- 關鍵待辦事項的條列清單，幫助醫師為即將到來的病患回診做準備」

> 🧩 **白話小補充**：CBT（Cognitive Behavioral Therapy）是「認知行為治療」，一種常見的心理治療。

### 加入範例

範例是提升 Claude 表現、引導它產生想要的輸出**最強大的工具之一**。只要在提示詞中提供幾個精心設計的範例，就能大幅提升 Claude 回答的準確度、一致性和品質。這個技巧對於非常講究細節、需要結構化輸出或遵守特定格式的任務特別有效。

目前，我們的提示詞完全沒有範例。為了簡短起見，我們只加入一個範例，不過**通常最好至少有兩個**。

我們會根據下面這份病史，做出範例的輸入和輸出（病患 Ethan Blackwood，55 歲。病史重點：2010 年輕度高血壓 → 2012 年失業後憂鬱症，服用 sertraline 並接受 CBT → 2015 年早期椎間盤退化，物理治療 → 2016 年開始服用 lisinopril → 2018 年胃食道逆流，服用 omeprazole → 2019 年阻塞型睡眠呼吸中止症，使用 CPAP 呼吸器 → 2020 年疫情期間焦慮增加，恢復 CBT → 2021 年半月板輕微撕裂 → 2022 年糖尿病前期 → 2023 年 PSA（攝護腺特異抗原）升高但切片排除癌症，接受膝關節鏡手術 → 2024 年膝蓋術後恢復良好、糖尿病前期改善、心臟超音波顯示輕度左心室肥大，開始服用低劑量 ACE 抑制劑保護心臟）：

```
Patient Name: Ethan Blackwood
Age: 55
Medical Record:

2010: Annual check-up, mild hypertension noted
  - Started on lifestyle modifications (diet, exercise)
2012: Diagnosed with moderate depression following job loss
  - Started on sertraline and cognitive-behavioral therapy (CBT)
2014: New job, reported improved mood
  - Continued sertraline, reduced CBT sessions
2015: Mild back pain, diagnosed with early degenerative disc disease
  - Physical therapy and over-the-counter NSAIDs prescribed
2016: Hypertension worsened, started on lisinopril
2017: Routine colonoscopy showed benign polyps, removed during procedure
2018: Developed persistent cough, chest X-ray clear
  - Diagnosed with Gastroesophageal Reflux Disease (GERD)
  - Started on omeprazole
2019: Diagnosed with obstructive sleep apnea (OSA)
  - Started CPAP therapy, reported improved energy levels
2020: COVID-19 pandemic, worked from home
  - Reported increased anxiety, CBT sessions resumed (telehealth)
  - COVID-19 vaccination (Moderna, both doses)
2021: Mild knee pain, MRI showed minor meniscus tear
  - Arthroscopic surgery recommended, patient opted for conservative management
2022: Annual check-up showed pre-diabetes (A1C: 6.1%)
  - Intensified lifestyle modifications, referred to nutritionist
- Discontinued omeprazole due to resolved GERD symptoms
2023: Blood tests showed elevated PSA (Prostate-Specific Antigen)
  - Prostate biopsy performed, results negative for cancer
- Knee pain worsened, agreed to arthroscopic surgery
2024: Post-op knee recovery: good, continuing physical therapy
  - A1C levels improved (5.8%), pre-diabetes resolved
  - Stress test normal, but mild LVH on echocardiogram
  - Started on low-dose ACE inhibitor for cardioprotection
```

根據這個範例輸入，一份遵守我們提示詞規則、結構良好的輸出可能長這樣：

```
Name: Ethan Blackwood
Age: 55  

Key Diagnoses:
- Hypertension (2010)
- Depression (2012)
- Degenerative Disc Disease (2015) 
- Gastroesophageal Reflux Disease (GERD) (2018)
- Obstructive Sleep Apnea (OSA) (2019)
- Pre-diabetes (2022)
- Meniscus Tear (2021)
- Left Ventricular Hypertrophy (LVH) (2024)

Medications: 
- Sertraline (depression)
- Lisinopril (hypertension)
- Omeprazole (GERD) - discontinued in 2022
- Low-dose ACE inhibitor (cardioprotection - 2024)

Other Treatments:
- Cognitive Behavioral Therapy (CBT) (depression)
- Physical therapy (back pain, post-op knee recovery)
- CPAP therapy (OSA)
- Arthroscopic knee surgery (2023)

Recent Concerns:
- Worsening knee pain
- Elevated PSA (2023) 
- Left ventricular hypertrophy on echocardiogram (2024)

Action Items:  
- Follow up on post-op knee recovery and physical therapy  
- Monitor PSA levels and prostate health
- Optimize blood pressure and hypertension management
- Assess need for further cardiac workup after LVH finding

```

**範例輸出翻譯**：
- **主要診斷**：高血壓（2010）、憂鬱症（2012）、椎間盤退化（2015）、胃食道逆流（2018）、阻塞型睡眠呼吸中止症（2019）、糖尿病前期（2022）、半月板撕裂（2021）、左心室肥大（2024）
- **藥物**：sertraline（憂鬱症）、lisinopril（高血壓）、omeprazole（胃食道逆流，2022 年停藥）、低劑量 ACE 抑制劑（保護心臟，2024）
- **其他治療**：認知行為治療（憂鬱症）、物理治療（背痛、膝蓋術後恢復）、CPAP 治療（睡眠呼吸中止）、膝關節鏡手術（2023）
- **近期疑慮**：膝蓋疼痛惡化、PSA 升高（2023）、心臟超音波顯示左心室肥大（2024）
- **待辦事項**：追蹤膝蓋術後恢復和物理治療、監測 PSA 數值和攝護腺健康、優化血壓和高血壓的控制、評估發現左心室肥大後是否需要進一步心臟檢查

我們來更新提示詞，加入這個範例輸入和輸出。為了讓 Claude 看得更清楚，我們會確保把範例包在 `<example>` 標籤裡：

{{cell 27}}

**這一版新增了什麼？**「這是我們希望摘要排版的範例：」接著是 `<example>` 標籤，裡面有 `<patient_record>`（Ethan 的病歷）和「Your output:（你的輸出：）」加上標準摘要。最後是：「現在，請用同樣的格式摘要下面這份病患病歷：」以及 `<patient_record>{record}</patient_record>`。

### 輸出的 XML 結構

一個常見的提示詞策略，是**請 Claude 在回答中使用 XML 標籤**。這樣一來，即使 Claude 決定加上「好的，這是你要的摘要！」之類的開場白，或補充其他內容，我們最終也能比較容易擷取出真正在意的內容。

在這個例子中，讓 Claude 把病歷摘要產生在 `<summary>` 標籤裡可能是合理的做法。一個簡單的實作方式，就是更新我們的範例，讓 Claude 看到我們想要的格式。

目前，提示詞的範例部分長這樣：

```
Here's an example of how we'd like the summaries formatted:

<example>
<patient_record>
Patient Name: Ethan Blackwood
Age: 55
Medical Record:

2010: Annual check-up, mild hypertension noted
  - Started on lifestyle modifications (diet, exercise)
medical record truncated to keep the text short here...
</patient_record>

Your output: 

Name: Ethan Blackwood
Age: 55  

Key Diagnoses:
- Hypertension (2010)
summary truncated to keep the text short here...
</example>
```

（「medical record truncated to keep the text short here...」和「summary truncated...」的意思是「為了讓這裡的文字短一點，病歷／摘要省略了⋯⋯」，只是說明用的，實際的提示詞裡是完整內容。）

只要一個簡單的修改，就能告訴 Claude 應該把輸出包在 `<summary>` 標籤裡：

```
Here's an example of how we'd like the summaries formatted:

<example>
<patient_record>
Patient Name: Ethan Blackwood
Age: 55
Medical Record:

2010: Annual check-up, mild hypertension noted
  - Started on lifestyle modifications (diet, exercise)
medical record truncated to keep the text short here...
</patient_record>

<summary>
Name: Ethan Blackwood
Age: 55  

Key Diagnoses:
- Hypertension (2010)
summary truncated to keep the text short here...
</summary>
</example>
```

（差別在於：把「Your output:」換成了 `<summary>` 和 `</summary>` 標籤，把範例摘要包起來。）

我們來更新提示詞的範例部分，反映這個修改：

{{cell 29}}

### 提示詞修改的重點回顧

在試用新的提示詞之前，我們先來看看做了哪些修改：

* 加入清楚的**系統提示詞**，設定背景並給 Claude 一個明確的角色。
* 用 **XML 標籤**（在我們的例子中是 `<patient_record>`）組織輸入資料，清楚表示提示詞的哪一部分是輸入資料。
* 提供**清楚、具體的指示**，說明摘要應該著重什麼，例如診斷、藥物和近期的健康疑慮。
* **指定**摘要想要的**格式**。
* 加入一個**範例**輸入和對應的、格式良好的摘要，引導 Claude 的回答。
* 請 Claude 把摘要產生在 **`<summary>` 標籤**裡。

---

## 測試新的提示詞

我們用新的 `system` 和 `updated_prompt`，搭配 `patient_records` 串列裡同樣的 5 份病歷試試看：

{{cell 32}}

**和之前的函式有什麼不同？** 用的是新的 `updated_prompt`（程式碼註解：「use our rewritten prompt!」用我們改寫的提示詞！），並加上了 `system=system`（「add in our system prompt!」加入我們的系統提示詞！）。

{{cells 33-37}}

效果很好！每一份輸出都遵守了我們指定的規則和格式。
往上捲回去，看看我們一開始的提示詞讓 Claude 產生了什麼樣的輸出，再和現在這些格式一致的新輸出比較一下！

---

## 換個方式：JSON！

我們也許對目前這個提示詞產生的文字摘要已經很滿意了，但很多時候，我們會想要特定的、**更容易讓程式處理**的結構化回答。最常見的做法就是使用 **JSON**。

**注意：「強制」得到 JSON 回答最簡單的方法，是透過 Claude 的工具使用功能，[我們在工具使用課程的另一堂課中會介紹](../05_tool_use/03_structured_outputs.md)。這裡的示範重點，是展示「修改提示詞」能帶來的影響。**

要讓目前的提示詞產生 JSON 回答，我們需要做幾個修改：
* 明確告訴 Claude 我們要 JSON 結果，並具體說明 JSON 輸出應該包含什麼。
* 把範例摘要改成 JSON 輸出。

{{cell 40}}

**這一格做了什麼？**
- 系統提示詞不變（註解：「Unchanged System Prompt」）。
- `updated_json_prompt`：提示詞改成「請用下列結構的 JSON 格式提供這些摘要」，並寫出 JSON 的結構：`name`（姓名）、`age`（年齡，整數）、`key_diagnoses`（主要診斷：每個包含 `diagnosis` 診斷名稱和 `year` 年份）、`medications`（藥物：`name` 名稱和 `purpose` 用途）、`other_treatments`（其他治療）、`recent_concerns`（近期疑慮）、`action_items`（待辦事項）。範例也改成 JSON 格式，最後要求「把你的 JSON 摘要輸出在 `<summary>` 標籤裡」。
- `medical_record_input_prompt`：把「病歷輸入」這一段**拆成另一個變數**。程式碼的註解解釋了原因：「把這部分拆成獨立的變數，之後比較容易使用 `format` 方法（上面提示詞裡 JSON 的大括號會讓 `format` 出問題）」。

> 🧩 **白話小補充：為什麼 JSON 的大括號會讓 `format` 出問題？** `.format()` 會把字串裡**所有**的 `{...}` 都當成「要替換的空格」。JSON 裡到處都是 `{` 和 `}`，`.format()` 就會搞混而出錯。所以作者把「有 `{record}` 要替換的部分」和「有 JSON 大括號的部分」分開，最後再用 `+` 接起來。

我們用下面這個函式測試看看：

{{cell 42}}

{{cell 43}}

太好了，我們得到想要的 JSON 了！
為了示範新的 JSON 回答有多好用，我們來寫一個函式：替一批病患產生摘要，然後輸出某位醫師在一天的門診中可能需要的所有「待辦事項」：

{{cell 45}}

**逐行解說：**
- `generate_summary_with_json_prompt(patient_record)`：和之前一樣，只是改成 `return`（回傳）文字，而不是印出來。
- `extract_json_from_summary_tags(summary_string)`：用正規表達式找出 `<summary>` 和 `</summary>` 中間的內容（`\s*` 代表「任意數量的空白」，`re.DOTALL` 讓 `.` 也能比對換行）。找不到就印出提示並回傳 `None`。
- `extract_action_items(model_response)`：
  - `json.loads(summary)`：把 JSON 文字轉成 Python 字典（[0-4 第 13 節](../00_before_you_start/04_python_crash_course.md#13-json)）。
  - `summary_data.get('action_items', [])`：取出待辦事項；`.get(key, 預設值)` 的好處是找不到 key 時不會出錯，而是回傳預設值（這裡是空串列）。
  - `enumerate(action_items, 1)`：從 1 開始編號。
  - `try` / `except json.JSONDecodeError`：如果 JSON 格式有錯，印出提示而不是讓程式當掉（[0-4 第 15 節](../00_before_you_start/04_python_crash_course.md#15-錯誤處理try--except)）。
- `generate_daily_action_items(patient_records)`：對每份病歷產生摘要，並印出待辦事項。

{{cell 46}}

> 🔄 **2026 更新**：現在 Claude API 有「**結構化輸出（structured outputs）**」功能，可以保證回答一定符合你指定的 JSON 結構，比只靠提示詞更可靠。第 5 單元的 [5-3 用工具強制輸出 JSON](../05_tool_use/03_structured_outputs.md) 會介紹用工具達成這件事的方法。

---

## 📌 重點整理

- 一開始的「爛」提示詞產生的摘要**格式、長度、內容都不一致**，程式很難使用。
- 改善步驟（散彈槍法，一次全用）：
  1. **系統提示詞**：給角色（醫療專業人員）
  2. **XML 標籤包住資料**：`<patient_record>`
  3. **清楚的指示**：要哪些項目、什麼順序、條列式
  4. **範例**：用 `<example>` 包住一組「病歷 → 標準摘要」
  5. **輸出 XML 標籤**：`<summary>`，方便擷取
- 改成 **JSON 輸出**後，程式可以用 `json.loads()` 直接處理（例如彙整所有待辦事項）。
- 小技巧：提示詞裡有 JSON 大括號時，把需要 `.format()` 替換的部分拆開。

👉 下一課：[3-3 提示詞工程的流程](03_prompt_engineering.md)
