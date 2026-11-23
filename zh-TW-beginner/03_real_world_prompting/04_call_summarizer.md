<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`04_call_summarizer.ipynb`](04_call_summarizer.ipynb)。

# 3-4 客服通話紀錄摘要器

> 📚 **第 3 單元：真實世界的提示詞**｜第 4 課 / 共 5 課
> ⏱️ 預估時間：60 分鐘

## 🎯 這一課你會學到

- 用上一課的「提示詞工程流程」，**一步一步**打造一個客服通話摘要提示詞
- 把很長的資料放在提示詞**最前面**、用 XML 標籤包起來
- 設計 **JSON 輸出格式**，並讓 Claude 先在 `<thinking>` 裡分析
- 找出並處理**邊緣情況**（打錯電話、斷線、聽不清楚、語言不通）
- 提供涵蓋**不同情況**的範例

> 🔄 **2026 更新**：這一課的程式碼原本使用 `claude-3-sonnet-20240229`，新手版換成 `claude-sonnet-4-6`。下面顯示的執行結果是原課程用舊模型跑出來的。

---

在這一課，我們要為一個很常見的客戶使用情境——**摘要**——撰寫一個複雜的提示詞。具體來說，我們要摘要很長的**客服通話逐字稿**。我們的目標是為了「客服績效指標」而摘要客服通話：我們想要完整客服通話的摘要，用來評估客服團隊的成效。這代表我們會**排除**那些有連線問題、語言障礙，以及其他會妨礙有效摘要的通話。

想像一下，我們在 Acme 公司上班，這是一家賣智慧家電的公司。公司每天要處理數百通客服電話，需要一種方法，快速把這些對話轉換成**有用的、結構化的資料**。

一些重要的考量包括：
* 通話可能簡短明快，也可能又長又複雜。
* 顧客打來的原因可能是任何事，從簡單的 Wi-Fi 連線問題到複雜的系統故障都有。
* 我們需要摘要有**特定的格式**，這樣之後才方便分析。
* 我們必須小心，**不要在摘要中包含任何顧客的個人資訊**。

為了幫助我們，我們會遵循之前介紹過的最佳做法：
* 用系統提示詞設定舞台。
* 組織提示詞的結構以達到最佳表現。
* 給出清楚的指示，定義你想要的輸出。
* 用 XML 標籤整理資訊。
* 處理特殊情況和邊緣情境。
* 提供範例引導模型。

---

## 了解資料

我們已經了解任務了，現在來看看要處理的資料。在這一課，我們會使用各式各樣**模擬**的 Acme 公司智慧家電客服團隊的通話逐字稿。這些逐字稿能幫助我們打造一個能處理不同情境的強健提示詞。

我們來看看可能會遇到的幾種通話逐字稿：

**一通簡短的通話**（顧客的智慧燈泡打不開，客服 Alex 教他斷電 5 秒再開來重設）：

```python
call1 = """
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How can I help you?
Customer: Hi, I can't turn on my smart light bulb.
Agent: I see. Have you tried resetting the bulb?
Customer: Oh, no. How do I do that?
Agent: Just turn the power off for 5 seconds, then back on. It should reset.
Customer: Ok, I'll try that. Thanks!
Agent: You're welcome. Call us back if you need further assistance.
"""
```

**一通中等長度、最後有解決的通話**（顧客的 SmartTherm 智慧溫控器設定 72 度但家裡熱很多，客服 Jamie 教他重新校正，請他一小時後再確認）：

```python
call2 = """
Agent: Acme Smart Home Support, this is Jamie. How may I assist you today?
Customer: Hi Jamie, my Acme SmartTherm isn't maintaining the temperature I set. It's set to 72 but the house is much warmer.
Agent: I'm sorry to hear that. Let's troubleshoot. Is your SmartTherm connected to Wi-Fi?
Customer: Yes, the Wi-Fi symbol is showing on the display.
Agent: Great. Let's recalibrate your SmartTherm. Press and hold the menu button for 5 seconds.
Customer: Okay, done. A new menu came up.
Agent: Perfect. Navigate to "Calibration" and press select. Adjust the temperature to match your room thermometer.
Customer: Alright, I've set it to 79 degrees to match.
Agent: Great. Press select to confirm. It will recalibrate, which may take a few minutes. Check back in an hour to see if it's fixed.
Customer: Okay, I'll do that. Thank you for your help, Jamie.
Agent: You're welcome! Is there anything else I can assist you with today?
Customer: No, that's all. Thanks again.
Agent: Thank you for choosing Acme Smart Home. Have a great day!
"""
```

**一通比較長、沒有解決的通話**（顧客的 SecureHome 保全系統半夜一直亂響，客服 Sarah 檢查了門窗和電池都正常，懷疑是感應器故障，最後把顧客轉給技術團隊做診斷）：

```python
call3 = """
Agent: Thank you for contacting Acme Smart Home Support. This is Sarah. How can I help you today?
Customer: Hi Sarah, I'm having trouble with my Acme SecureHome system. The alarm keeps going off randomly.
Agent: I'm sorry to hear that. Can you tell me when this started happening?
Customer: It started about two days ago. It's gone off three times now, always in the middle of the night.
Agent: I see. Are there any error messages on the control panel when this happens?
Customer: No, I didn't notice any. But I was pretty groggy each time.
Agent: Understood. Let's check a few things. First, can you confirm that all your doors and windows are closing properly?
Customer: Yes, I've checked all of them. They're fine.
Agent: Okay. Next, let's check the battery in your control panel. Can you tell me if the low battery indicator is on?
Customer: Give me a moment... No, the battery indicator looks normal.
Agent: Alright. It's possible that one of your sensors is malfunctioning. I'd like to run a diagnostic, but I'll need to transfer you to our technical team for that. Is that okay?
Customer: Yes, that's fine. I just want this fixed. It's really disruptive.
Agent: I completely understand. I'm going to transfer you now. They'll be able to run a full system diagnostic and hopefully resolve the issue for you.
Customer: Okay, thank you.
Agent: You're welcome. Thank you for your patience, and I hope you have a great rest of your day.
"""
```

這些例子展示了我們需要處理的各種通話和考量：
* 通話的長度差異非常大。
* 通話涉及各種支援問題（簡單的修正、裝置故障、複雜的問題）。
* 有些通話以解決收場，有些則仍然沒有解決。
* 有些通話需要後續追蹤。

在打造提示詞的過程中，我們要確保它能有效地摘要所有這些類型的通話，擷取關鍵資訊，並用一致、結構化的格式呈現。
在下一節，我們會開始一步一步打造提示詞，處理這些各式各樣的通話逐字稿。

---

## 提示詞的簡單版本

我們已經了解任務和要處理的資料類型了，現在開始打造提示詞。我們會從一個基本版本開始，再逐步修改，以處理通話摘要任務的複雜性。

我們先從這個非常簡單、只概述基本任務的提示詞開始：

```python
prompt = """
Summarize the following customer service call transcript. Focus on the main issue, how it was resolved, and any required follow-up.

{transcript}
"""
```

（「摘要下面這份客服通話逐字稿。著重在主要問題、怎麼解決的，以及任何需要的後續追蹤。」）

這個基本的提示詞讓 Claude 大概知道我們要什麼，但它有幾個限制：

* 沒有指定想要的輸出格式，可能導致摘要不一致。
* 沒有提供如何處理不同情境的指引（例如問題沒有解決，或資訊不足）。
* 沒有設定長度或內容的限制，可能產生過長或過度詳細的摘要。
* 沒有指示 Claude 省略個人資訊，可能導致隱私問題。

話雖如此，我們還是先測試一下，看看它表現得怎麼樣：

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

def summarize_call(transcript):
    final_prompt = prompt.format(transcript=transcript)
    # Make the API call
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": final_prompt}
        ]
    )
    print(response.content[0].text)
```

```python
summarize_call(call1)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
Here is a summary of the customer service call transcript:

Main Issue:
The customer was unable to turn on their Acme smart light bulb.

Resolution:
The service agent instructed the customer to reset the bulb by turning the power off for 5 seconds and then back on. This should reset the bulb and allow it to turn on.

Follow-Up:
The agent told the customer to call back if they continued to have issues after trying the reset procedure. No other follow-up was mentioned.
```

```python
summarize_call(call2)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
Summary:

Main Issue: The customer's Acme SmartTherm thermostat was not maintaining the set temperature of 72°F, and the house was much warmer.

Resolution: The agent guided the customer through the process of recalibrating the SmartTherm thermostat. This involved accessing the "Calibration" menu, adjusting the temperature to match the customer's room thermometer (79°F in this case), and confirming the new setting. The recalibration process may take a few minutes to complete.

Follow-up Required: The customer was advised to check the thermostat in an hour to see if the issue was resolved after the recalibration process completed.
```

```python
summarize_call(call3)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
Here is a summary of the customer service call transcript:

Main Issue:
The customer was having an issue with their Acme SecureHome alarm system going off randomly in the middle of the night, even though all doors and windows were closed properly.

How It Was Resolved:
The customer service agent first had the customer check for any error messages on the control panel and confirm that the battery was not low. When those basic troubleshooting steps did not reveal the issue, the agent determined that one of the sensors may be malfunctioning and needed to transfer the customer to the technical support team for a full system diagnostic.

Required Follow-Up:
The technical support team needs to run a diagnostic on the customer's SecureHome system to identify which sensor(s) may be causing the false alarms and then repair or replace those components. The customer should be contacted again once the diagnostic is complete and the repair/replacement has been performed to ensure the random alarms have been resolved.
```

可以看到，雖然 Claude 確實提供了摘要，但格式並不方便有系統地分析。摘要可能太長或太短，也不一定每次都涵蓋我們在意的所有重點。

在接下來的步驟中，我們會開始在提示詞中加入更多結構和引導，解決這些限制。我們會看到每一項新增的內容，如何提升 Claude 摘要的品質和一致性。

記住，提示詞工程是一個反覆循環的過程。我們從簡單的開始，再逐步修改提示詞。

---

## 加入系統提示詞

最簡單的起點，就是一個能設定 Claude 整體背景和角色的系統提示詞，幫助在整個互動中引導它的行為。

我們從這個系統提示詞開始：

```python
system = """
You are an expert customer service analyst, skilled at extracting key information from call transcripts and summarizing them in a structured format.
Your task is to analyze customer service call transcripts and generate concise, accurate summaries while maintaining a professional tone.
"""
```

**翻譯**：「你是一位專業的客服分析師，擅長從通話逐字稿中擷取關鍵資訊，並用結構化的格式加以摘要。你的任務是分析客服通話逐字稿，產生簡潔、準確的摘要，同時保持專業的語氣。」

---

## 組織主要提示詞的結構

接下來，我們要開始寫主要的提示詞。我們會運用下面這些提示詞技巧：

- 把長文件（我們的逐字稿）放在**最上面**。
- 加入詳細的指示和輸出格式要求。
- 引入 XML 標籤，組織提示詞和輸出。
- 給 Claude 「**把想法說出來**」的空間。

因為這個提示詞可能會變得很長，我們會**分段**寫好各個部分，最後再組合起來。

### 輸入資料

使用像 Claude 這樣的大型語言模型時，把長文件（像我們的通話逐字稿）放在提示詞的開頭非常重要。這能確保 Claude 在收到具體的指示之前，就已經掌握所有必要的背景。我們也應該用 XML 標籤在提示詞中標示出逐字稿：

```python
prompt_pt1 = """
Analyze the following customer service call transcript and generate a JSON summary of the interaction:

<transcript>
[INSERT CALL TRANSCRIPT HERE]
</transcript>
"""
```

（「分析下面這份客服通話逐字稿，並產生這次互動的 JSON 摘要：」後面是 `<transcript>[INSERT CALL TRANSCRIPT HERE]</transcript>`。`[INSERT CALL TRANSCRIPT HERE]` 的意思是「在這裡插入通話逐字稿」，之後會用程式把它替換成真正的逐字稿。）

### 指示和輸出格式

在繼續之前，我們先好好想清楚：一個好的結構化輸出格式應該長什麼樣子。為了讓解析結果時輕鬆一點，請 Claude 用 **JSON** 回答通常是最簡單的。在這個例子中，好的 JSON 應該長什麼樣子？

我們的 JSON 輸出至少應該包含下面這些：
- 一個**狀態（status）**，表示 Claude 是否有足夠的資訊產生摘要。這個我們之後會再回來處理。目前，我們先假設所有摘要的狀態都是 `"COMPLETE"`，代表 Claude 可以產生摘要。
- 顧客問題的摘要
- 這通電話是否需要額外的後續追蹤
- 如果需要，後續行動的細節（回電給顧客等）
- 問題是怎麼解決的
- 對話中模糊或不清楚之處的清單

下面是一個建議的 JSON 結構範例：

```json
{
  "summary": {
    "customerIssue": "Brief description of the main problem or reason for the call",
    "resolution": "How the issue was addressed or resolved, if applicable",
    "followUpRequired": true/false,
    "followUpDetails": "Description of any necessary follow-up actions, or null if none required"
  },
  "status": "COMPLETE",
  "ambiguities": ["List of any unclear or vague points in the conversation, or an empty array if none"]
}
```

**各欄位的意思：**
| 欄位 | 意思 |
|---|---|
| `customerIssue` | 主要問題或來電原因的簡短描述 |
| `resolution` | 問題是怎麼處理或解決的（如果有的話） |
| `followUpRequired` | 是否需要後續追蹤（`true` 是／`false` 否） |
| `followUpDetails` | 需要的後續行動的描述；不需要的話就是 `null`（空值） |
| `status` | 狀態，目前固定是 `"COMPLETE"`（完成） |
| `ambiguities` | 對話中任何不清楚或模糊之處的清單；沒有的話就是空陣列 `[]` |

我們來建立提示詞的新段落，包含具體的指示，包括：
- 產生一份摘要，著重在主要問題、解決方式，以及任何需要的後續行動。
- 依照我們特定的標準化格式產生 JSON 輸出。
- 在摘要中**省略**特定的顧客資訊。
- 讓摘要的每個部分都保持簡短。

下面是一個提供輸出指示的嘗試，包含我們特定的 JSON 輸出格式：

```python
prompt_pt2 = """
Instructions:
1. Read the transcript carefully.
2. Analyze the transcript, focusing on the main issue, resolution, and any follow-up required.
3. Generate a JSON object summarizing the key aspects of the interaction according to the specified structure.

Important guidelines:
- Confidentiality: Omit all specific customer data like names, phone numbers, and email addresses.
- Character limit: Restrict each text field to a maximum of 100 characters.
- Maintain a professional tone in your summary.

Output format:
Generate a JSON object with the following structure:
<json>
{
  "summary": {
    "customerIssue": "Brief description of the main problem or reason for the call",
    "resolution": "How the issue was addressed or resolved, if applicable",
    "followUpRequired": true/false,
    "followUpDetails": "Description of any necessary follow-up actions, or null if none required"
  },
  "status": "COMPLETE",
  "ambiguities": ["List of any unclear or vague points in the conversation, or an empty array if none"]
}
</json>
"""
```

**翻譯**：
「指示：
1. 仔細閱讀逐字稿。
2. 分析逐字稿，著重在主要問題、解決方式和任何需要的後續追蹤。
3. 依照指定的結構，產生一個摘要這次互動重點的 JSON 物件。

重要準則：
- **保密**：省略所有特定的顧客資料，例如姓名、電話號碼和電子郵件地址。
- **字數限制**：每個文字欄位最多 100 個字元。
- 摘要要保持專業的語氣。

輸出格式：
產生一個具有下列結構的 JSON 物件：`<json>`（上面那個結構）`</json>`」

---

## 使用 XML 標籤，並給 Claude 思考的空間

接下來，我們要再運用兩個提示詞策略：**給 Claude 思考的空間**和**使用 XML 標籤**。
- 我們會請 Claude 先輸出包含它分析內容的 `<thinking>` 標籤。
- 接著，我們會請 Claude 把 JSON 輸出放在 `<json>` 標籤裡。

這是我們提示詞初稿的最後一段：

```python
prompt_pt3 = """
Before generating the JSON, please analyze the transcript in <thinking> tags. 
Include your identification of the main issue, resolution, follow-up requirements, and any ambiguities. 
Then, provide your JSON output in <json> tags.
"""
```

**翻譯**：「在產生 JSON 之前，請先在 `<thinking>` 標籤裡分析逐字稿。內容要包含你判斷的主要問題、解決方式、後續追蹤需求，以及任何模糊之處。然後，把你的 JSON 輸出放在 `<json>` 標籤裡。」

請 Claude 把分析放在 `<thinking>` 標籤裡，就是在促使它在寫出最終的 JSON 輸出之前，先拆解自己的思考過程。這能讓它用更徹底、更有結構的方式分析逐字稿。
`<thinking>` 區塊讓我們（以及可能的其他審查者或系統）看到 Claude 的推理過程。這種透明度對除錯和品質保證來說可能非常關鍵。

把分析（`<thinking>`）和結構化輸出（`<json>`）分開，能清楚地區分「Claude 對逐字稿的解讀」和「它排版好的摘要」。這在我們想把分析和 JSON 輸出分開審查時很有幫助；另外，把 JSON 內容單獨放在 `<json>` 標籤裡，也讓我們很容易解析最終的回答，擷取出我們要用的 JSON。

---

## 測試更新後的提示詞

這是完整版的提示詞，由我們目前寫好的各個段落組合而成：

```python
system = """
You are an expert customer service analyst, skilled at extracting key information from call transcripts and summarizing them in a structured format.
Your task is to analyze customer service call transcripts and generate concise, accurate summaries while maintaining a professional tone.
"""

prompt = """
Analyze the following customer service call transcript and generate a JSON summary of the interaction:

<transcript>
[INSERT CALL TRANSCRIPT HERE]
</transcript>

Instructions:
1. Read the transcript carefully.
2. Analyze the transcript, focusing on the main issue, resolution, and any follow-up required.
3. Generate a JSON object summarizing the key aspects of the interaction according to the specified structure.

Important guidelines:
- Confidentiality: Omit all specific customer data like names, phone numbers, and email addresses.
- Character limit: Restrict each text field to a maximum of 100 characters.
- Maintain a professional tone in your summary.

Output format:
Generate a JSON object with the following structure:
<json>
{
  "summary": {
    "customerIssue": "Brief description of the main problem or reason for the call",
    "resolution": "How the issue was addressed or resolved, if applicable",
    "followUpRequired": true/false,
    "followUpDetails": "Description of any necessary follow-up actions, or null if none required"
  },
  "status": "COMPLETE",
  "ambiguities": ["List of any unclear or vague points in the conversation, or an empty array if none"]
}
</json>

Before generating the JSON, please analyze the transcript in <thinking> tags. 
Include your identification of the main issue, resolution, follow-up requirements, and any ambiguities. 
Then, provide your JSON output in <json> tags.
"""
```

這是一個可以用來測試提示詞的函式：

```python
def summarize_call_with_improved_prompt(transcript):
    final_prompt = prompt.replace("[INSERT CALL TRANSCRIPT HERE]", transcript)
    # Make the API call
    response = client.messages.create(
        model="claude-sonnet-4-6",
        system=system,
        max_tokens=4096,
        messages=[
            {"role": "user", "content": final_prompt}
        ]
    )
    print(response.content[0].text)
```

**逐行解說：**
- `prompt.replace("[INSERT CALL TRANSCRIPT HERE]", transcript)`：把佔位文字**替換**成真正的逐字稿。
  > 🧩 **為什麼這次不用 `.format()`？** 因為提示詞裡有 JSON 的大括號 `{ }`，用 `.format()` 會出錯（上一課提過）。改用 `.replace()`（取代文字）就沒有這個問題。
- `system=system`：加上系統提示詞。

我們用之前定義好的幾份通話逐字稿來測試這個提示詞：

```python
summarize_call_with_improved_prompt(call1)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
<thinking>
From the transcript, the main issue appears to be that the customer could not turn on their smart light bulb. The resolution provided by the agent was to reset the bulb by turning the power off for 5 seconds and then back on.

The agent did offer for the customer to call back if they needed further assistance, indicating potential follow-up may be required if the reset did not resolve the issue. However, no specific follow-up details were provided.

There do not seem to be any significant ambiguities in the conversation.
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Unable to turn on smart light bulb",
    "resolution": "Agent instructed customer to reset the bulb by turning power off for 5 seconds, then back on",
    "followUpRequired": true,
    "followUpDetails": "Customer was advised to call back if the reset did not resolve the issue"
  },
  "status": "COMPLETE",
  "ambiguities": []
}
</json>
```

```python
summarize_call_with_improved_prompt(call2)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
<thinking>
Main issue: The customer's Acme SmartTherm thermostat is not maintaining the set temperature of 72°F, and the house is much warmer.

Resolution: The agent guided the customer through recalibrating the SmartTherm thermostat by:
1. Having the customer press and hold the menu button for 5 seconds.
2. Navigating to the "Calibration" menu and selecting it.
3. Adjusting the temperature to match the customer's room thermometer reading of 79°F.
4. Confirming the new calibration setting.

Follow-up required: Yes, the agent instructed the customer to check back in an hour to see if the recalibration resolved the temperature issue.

Ambiguities: None
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Thermostat not maintaining set temperature, causing house to be much warmer.",
    "resolution": "Agent guided customer through recalibrating the thermostat to match room temperature.",
    "followUpRequired": true,
    "followUpDetails": "Customer to check back in an hour to see if recalibration resolved the temperature issue."
  },
  "status": "COMPLETE",
  "ambiguities": []
}
</json>
```

```python
summarize_call_with_improved_prompt(call3)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
<thinking>
Main issue: The customer's Acme SecureHome system alarm is going off randomly in the middle of the night, even though doors and windows are closed properly.

Resolution: The agent suggests running a diagnostic on the system to identify potential sensor malfunctions. The customer is transferred to the technical team to perform the diagnostic and resolve the issue.

Follow-up required: Yes, the technical team needs to follow up with the customer to diagnose and fix the alarm system problem.

Ambiguities: None identified in the conversation.
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Customer's home security alarm system is going off randomly at night without apparent cause.",
    "resolution": "Agent suggests running a diagnostic to check for sensor malfunction and transfers customer to technical team.",
    "followUpRequired": true,
    "followUpDetails": "Technical team to diagnose and resolve the issue with the customer's alarm system."
  },
  "status": "COMPLETE",
  "ambiguities": []
}
</json>
```

這些回答看起來都很棒！我們再試一份**有點模稜兩可**的通話逐字稿，看看 JSON 結果是否會包含那些模糊之處：

```python
ambiguous_call = """
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How may I assist you today?
Customer: Hi Alex, I'm having an issue with my SmartLock. It's not working properly.
Agent: I'm sorry to hear that. Can you tell me more about what's happening with your SmartLock?
Customer: Well, sometimes it doesn't lock when I leave the house. I think it might be related to my phone, but I'm not sure.
Agent: I see. When you say it doesn't lock, do you mean it doesn't respond to the auto-lock feature, or are you trying to lock it manually through the app?
Customer: Uh, both, I think. Sometimes one works, sometimes the other. It's inconsistent.
Agent: Okay. And you mentioned it might be related to your phone. Have you noticed any pattern, like it works better when you're closer to the door?
Customer: Maybe? I haven't really paid attention to that.
Agent: Alright. Let's try to troubleshoot this. First, can you tell me what model of SmartLock you have?
Customer: I'm not sure. I bought it about six months ago, if that helps.
Agent: That's okay. Can you see a model number on the lock itself?
Customer: I'd have to go check. Can we just assume it's the latest model?
Agent: Well, knowing the exact model would help us troubleshoot more effectively. But let's continue with what we know. Have you tried resetting the lock recently?
Customer: I think so. Or maybe that was my SmartTherm. I've been having issues with that too.
Agent: I see. It sounds like we might need to do a full diagnostic on your SmartLock. Would you be comfortable if I walked you through that process now?
Customer: Actually, I have to run to an appointment. Can I call back later?
Agent: Of course. Before you go, is there a good contact number where our technical team can reach you for a more in-depth troubleshooting session?
Customer: Sure, you can reach me at 555... oh wait, that's my old number. Let me check my new one... You know what, I'll just call back when I have more time.
Agent: I understand. We're here 24/7 when you're ready to troubleshoot. Is there anything else I can help with before you go?
Customer: No, that's it. Thanks.
Agent: You're welcome. Thank you for choosing Acme Smart Home. Have a great day!
"""

summarize_call_with_improved_prompt(ambiguous_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
<thinking>
Main Issue: The customer is experiencing issues with their Acme SmartLock not consistently locking automatically or manually through the app.

Resolution: The agent attempted to troubleshoot by asking for the specific SmartLock model and suggesting a reset, but the customer had to leave before completing the troubleshooting process.

Follow-Up Required: Yes, the customer needs to call back to complete a full diagnostic and troubleshooting session with the technical team.

Ambiguities:
- The customer was unsure if the issue was related to their phone or not, suggesting a potential connectivity problem.
- The customer mentioned having issues with another Acme product (SmartTherm), but it's unclear if those issues are related to the SmartLock problem.
- The customer's contact number was not clearly provided, which could make follow-up more difficult.
</thinking>

<json>
{
  "summary": {
    "customerIssue": "SmartLock not consistently locking automatically or manually through the app.",
    "resolution": "Attempted troubleshooting but customer had to leave before completing the process.",
    "followUpRequired": true,
    "followUpDetails": "Customer needs to call back for full diagnostic and troubleshooting session with technical team."
  },
  "status": "COMPLETE",
  "ambiguities": [
    "Potential connectivity issue with customer's phone",
    "Unclear if issues with other Acme product are related",
    "Customer's contact number not clearly provided"
  ]
}
</json>
```

（這通電話：顧客的 SmartLock 智慧門鎖有時候鎖不上，但他說不清楚是自動上鎖還是用 App 手動上鎖有問題、不知道門鎖型號、不確定有沒有重設過（「或許那是我的 SmartTherm？」），最後說要去赴約，連聯絡電話都沒留就掛了。Claude 在 `ambiguities` 裡列出了這些不清楚的地方。）

太好了！一切看起來都如預期運作。

---

## 邊緣情況

到目前為止，我們試過的所有通話逐字稿，都是相對單純的客服通話。在真實世界中，我們預期也會遇到一些我們**可能不想摘要**的逐字稿，包括：

- 有連線問題的通話
- 有語言障礙的通話
- 逐字稿亂碼的通話
- 顧客不理性或情緒激動的通話

記住，我們摘要這些通話的目的，是**評估我們提供的客服成效**。如果把這些邊緣情況的通話也納入摘要，我們很可能會得到**失真的結果**。

我們來看看用目前的提示詞處理這些邊緣情況會發生什麼事。下面我們定義了一些新的通話逐字稿：

```python
wrong_number_call = """
Agent: Acme Smart Home Support, Lisa speaking. How can I help you?
Customer: Is this tech support?
Agent: Yes, this is technical support for Acme Smart Home devices. What can I help you with?
Customer: Sorry, wrong number.
Agent: No problem. Have a nice day.
"""

incomplete_call = """
Agent: Acme Smart Home Support, this is Sarah. How can I assist you today?
Customer: The thing isn't working.
Agent: I'm sorry to hear that. Could you please specify which device you're having trouble with?
Customer: You know, the usual one. Gotta go, bye.
Agent: Wait, I need more infor... [call disconnected]
"""

garbled_call = """
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How may I assist you today?
Customer: [garbled voice]
Agent: Hello? Are you there?
"""

language_barrier_call = """
Agent: Acme Smart Home Support, Sarah speaking. How can I help you today?
Customer: [Speaking in Spanish]
Agent: I apologize, but I don't speak Spanish. Do you speak English?
Customer: [Continues Spanish]
Agent: One moment please, I'll try to get a translator on the line...
"""

```

**四通邊緣情況的電話：**
- `wrong_number_call`（打錯電話）：「這是技術支援嗎？」「是的⋯⋯」「抱歉，打錯了。」
- `incomplete_call`（不完整）：「那個東西壞了。」「請問是哪個裝置？」「你知道的，平常那個。我得走了，掰。」〔通話中斷〕
- `garbled_call`（亂碼）：顧客的聲音〔模糊不清〕，客服：「喂？你還在嗎？」
- `language_barrier_call`（語言障礙）：顧客〔說西班牙文〕，客服不會說西班牙文，正在找翻譯⋯⋯

我們把這些邊緣情況的逐字稿丟給提示詞，看看會得到什麼結果：

```python
summarize_call_with_improved_prompt(wrong_number_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
<thinking>
Issue: The customer appears to have dialed the wrong number for technical support.
Resolution: Since it was a wrong number, there was no issue to resolve. The agent politely concluded the call.
Follow-up: No follow-up is required since it was a misdialed call.
Ambiguities: There are no apparent ambiguities in this brief conversation.
</thinking>

<json>
{
  "summary": {
    "customerIssue": "The customer dialed the wrong number for technical support",
    "resolution": "The agent concluded the call politely since it was a misdialed number",
    "followUpRequired": false,
    "followUpDetails": null
  },
  "status": "COMPLETE",
  "ambiguities": []
}
</json>
```

```python
summarize_call_with_improved_prompt(incomplete_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
<thinking>
In this transcript, the main issue is unclear as the customer does not provide sufficient details about the device they are having trouble with. The agent attempts to clarify the issue, but the customer disconnects the call before providing more information.

There is no resolution since the issue is not clearly identified. However, follow-up is required to gather more details from the customer about the specific device and the problem they are experiencing.

The key ambiguity is the lack of clarity about the device and the nature of the problem. The customer's vague statements ("the thing isn't working" and "the usual one") do not provide enough information for the agent to diagnose or resolve the issue.
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Customer reported an unspecified device was not working but did not provide further details.",
    "resolution": "No resolution was possible due to lack of information from the customer.",
    "followUpRequired": true,
    "followUpDetails": "Agent needs to contact the customer again to gather details about the specific device and issue."
  },
  "status": "COMPLETE",
  "ambiguities": ["The device the customer was referring to", "The nature of the problem with the device"]
}
</json>
```

```python
summarize_call_with_improved_prompt(garbled_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
<thinking>
From the transcript, it appears the customer called Acme Smart Home Support, but their voice was garbled, and the agent could not understand them. With this limited information, it is unclear what the main issue or reason for the call was. There was no resolution provided, and it is ambiguous whether follow-up is required since the issue itself is unknown. The key ambiguity is the lack of clear communication from the customer, preventing the agent from understanding the problem.
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Unclear due to garbled voice from the customer",
    "resolution": "No resolution provided since the issue could not be understood",
    "followUpRequired": true,
    "followUpDetails": "Agent should try to reconnect with the customer for clearer communication"
  },
  "status": "COMPLETE",
  "ambiguities": ["The customer's voice was garbled, preventing understanding of the issue"]
}
</json>
```

```python
summarize_call_with_improved_prompt(language_barrier_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
<thinking>
Main issue: The customer called and spoke in Spanish, but the agent could not understand Spanish.
Resolution: The agent tried to get a translator on the line to resolve the language barrier.
Follow-up required: Yes, the agent needs to connect with a Spanish translator to assist the customer.
Ambiguities: It is unclear why the customer called, as the reason for their call is not stated in the transcript.
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Customer spoke in a language the agent did not understand (Spanish).",
    "resolution": "Agent attempted to get a translator to resolve the language barrier.",
    "followUpRequired": true,
    "followUpDetails": "Agent needs to connect the customer with a Spanish translator."
  },
  "status": "COMPLETE",
  "ambiguities": ["Reason for the customer's call is not stated in the transcript."]
}
</json>
```

很遺憾，這些邊緣情況的逐字稿都得到了完整的摘要。下面是回答中一些有問題的部分：

>  "customerIssue": "Customer spoke in a language the agent did not understand (Spanish)."
>（顧客說的語言客服聽不懂〔西班牙文〕。）

> "customerIssue": "Unclear due to garbled voice from the customer"
>（因為顧客聲音模糊而不清楚。）

> "customerIssue": "The customer dialed the wrong number for technical support"
>（顧客打錯了技術支援的電話。）

記住，我們的目標是摘要客服通話，以了解客服團隊有多有效。這些邊緣情況的逐字稿產生了完整的摘要，在分析所有摘要時會造成問題（例如統計「問題解決率」時，這些根本不是真正的客服問題）。我們需要決定處理這些通話的策略。

---

## 進一步改善提示詞

就像剛剛看到的，我們的提示詞目前會為邊緣情況的逐字稿產生完整的摘要。我們想改變這個行為。處理這些邊緣情況有幾種選擇：

- 用某種方式**標記**它們，表示無法摘要，方便之後由人工審查。
- 把它們**另外分類**（例如「技術問題」、「語言障礙」等）。

為了簡單起見，我們選擇**標記**這些邊緣情況的通話，請模型輸出像這樣的 JSON：

```json
{
  "status": "INSUFFICIENT_DATA"
}
```

（`INSUFFICIENT_DATA` = 資料不足。）

為了做到這一點，我們需要用下面的方式更新提示詞：
- 加入說明「什麼時候要輸出 `INSUFFICIENT_DATA`」的指示
- 加入範例，展示可以摘要和不能摘要的逐字稿，以及它們對應的 JSON 輸出。

### 更新指示

我們在提示詞的指示部分寫一段新的內容，說明模型什麼時候應該輸出 `INSUFFICIENT_DATA` 的 JSON。

```python
# Just the new content.  We'll look at the entire prompt in a moment
new_instructions_addition = """
Insufficient data criteria:
   If either of these conditions are met:
   a) The transcript has fewer than 5 total exchanges, or
   b) The customer's issue is unclear
   c) The call is garbled, incomplete, or is hindered by a language barrier
   Then return ONLY the following JSON:
   {
     "status": "INSUFFICIENT_DATA"
   }
"""
```

**翻譯**（程式碼的註解說：「這只是新增的內容，等一下再看完整的提示詞」）：
「資料不足的判斷標準：
   如果符合下列任一條件：
   a) 逐字稿總共少於 5 次對話往來，或
   b) 顧客的問題不清楚
   c) 通話有亂碼、不完整，或因語言障礙而受阻
   那就**只**回傳下面這個 JSON：`{"status": "INSUFFICIENT_DATA"}`」

（原文寫「If either of these conditions（這兩個條件之一）」，但其實列了三個條件，意思是「任一條件」。）

### 加入範例

就像我們在這門課之前討論過的，在提示詞中加入範例幾乎總是好主意。在這個特定的使用情境中，範例能幫助 Claude 大致了解，對於可以摘要和不能摘要的通話逐字稿，我們各想要什麼樣的摘要。

下面是一組我們可以放進提示詞的範例：

<details>
<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>

```python
examples_for_prompt = """
<examples>
1. Complete interaction:
<transcript>
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How may I assist you today?
Customer: Hi Alex, my Acme SmartTherm isn't maintaining the temperature I set. It's set to 72 but the house is much warmer.
Agent: I'm sorry to hear that. Let's troubleshoot. Is your SmartTherm connected to Wi-Fi?
Customer: Yes, the Wi-Fi symbol is showing on the display.
Agent: Great. Let's recalibrate your SmartTherm. Press and hold the menu button for 5 seconds.
Customer: Okay, done. A new menu came up.
Agent: Perfect. Navigate to "Calibration" and press select. Adjust the temperature to match your room thermometer.
Customer: Alright, I've set it to 79 degrees to match.
Agent: Great. Press select to confirm. It will recalibrate, which may take a few minutes. Check back in an hour to see if it's fixed.
Customer: Okay, I'll do that. Thank you for your help, Alex.
Agent: You're welcome! Is there anything else I can assist you with today?
Customer: No, that's all. Thanks again.
Agent: Thank you for choosing Acme Smart Home. Have a great day!
</transcript>

<thinking>
Main issue: SmartTherm not maintaining set temperature
Resolution: Guided customer through recalibration process
Follow-up: Not required, but customer should check effectiveness after an hour
Ambiguities: None identified
</thinking>

<json>
{
  "summary": {
    "customerIssue": "SmartTherm not maintaining set temperature, showing higher than set 72 degrees",
    "resolution": "Guided customer through SmartTherm recalibration process",
    "followUpRequired": false,
    "followUpDetails": null
  },
  "status": "COMPLETE",
  "ambiguities": []
}
</json>

2. Interaction requiring follow-up:
<transcript>
Agent: Acme Smart Home Support, this is Jamie. How can I help you?
Customer: Hi, I just installed my new Acme SmartCam, but I can't get it to connect to my Wi-Fi.
Agent: I'd be happy to help. Are you using the Acme Smart Home app?
Customer: Yes, I have the app on my phone.
Agent: Great. Make sure your phone is connected to the 2.4GHz Wi-Fi network, not the 5GHz one.
Customer: Oh, I'm on the 5GHz network. Should I switch?
Agent: Yes, please switch to the 2.4GHz network. The SmartCam only works with 2.4GHz.
Customer: Okay, done. Now what?
Agent: Open the app, select 'Add Device', choose 'SmartCam', and follow the on-screen instructions.
Customer: It's asking for a password now.
Agent: Enter your Wi-Fi password and it should connect.
Customer: It's still not working. I keep getting an error message.
Agent: I see. In that case, I'd like to escalate this to our technical team. They'll contact you within 24 hours.
Customer: Okay, that sounds good. Thank you for trying to help.
Agent: You're welcome. Is there anything else you need assistance with?
Customer: No, that's all for now. Thanks again.
Agent: Thank you for choosing Acme Smart Home. Have a great day!
</transcript>

<thinking>
Main issue: Customer unable to connect new SmartCam to Wi-Fi
Resolution: Initial troubleshooting unsuccessful, issue escalated to technical team
Follow-up: Required, technical team to contact customer within 24 hours
Ambiguities: Specific error message customer is receiving not mentioned
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Unable to connect new SmartCam to Wi-Fi",
    "resolution": "Initial troubleshooting unsuccessful, issue escalated to technical team",
    "followUpRequired": true,
    "followUpDetails": "Technical team to contact customer within 24 hours for further assistance"
  },
  "status": "COMPLETE",
  "ambiguities": ["Specific error message customer is receiving not mentioned"]
}
</json>

3. Insufficient data:
<transcript>
Agent: Acme Smart Home Support, this is Sam. How may I assist you?
Customer: Hi, my smart lock isn't working.
Agent: I'm sorry to hear that. Can you tell me more about the issue?
Customer: It just doesn't work. I don't know what else to say.
Agent: Okay, when did you first notice the problem? And what model of Acme smart lock do you have?
Customer: I don't remember. Listen, I have to go. I'll call back later.
Agent: Alright, we're here 24/7 if you need further assistance. Have a good day.
</transcript>

<thinking>
This transcript has fewer than 5 exchanges and the customer's issue is unclear. The customer doesn't provide specific details about the problem with the smart lock or respond to the agent's questions. This interaction doesn't provide sufficient information for a complete summary.
</thinking>

<json>
{
  "status": "INSUFFICIENT_DATA"
}
</json>
</examples>
"""
```

</details>

**三個範例的內容：**
1. **完整的互動**（Complete interaction）：SmartTherm 溫控器溫度不準，客服引導重新校正 → `<thinking>` 分析 → JSON：`followUpRequired: false`、`ambiguities: []`。
2. **需要後續追蹤的互動**（Interaction requiring follow-up）：新買的 SmartCam 攝影機連不上 Wi-Fi，客服請顧客改用 2.4GHz 網路、重新加入裝置，還是出現錯誤訊息，最後轉給技術團隊、24 小時內聯絡 → JSON：`followUpRequired: true`、`followUpDetails: "技術團隊將在 24 小時內聯絡顧客提供進一步協助"`、`ambiguities: ["沒有提到顧客收到的具體錯誤訊息"]`。
3. **資料不足**（Insufficient data）：顧客只說「智慧門鎖壞了」「就是不能用，我不知道還能說什麼」「我不記得了，我得走了」 → `<thinking>`：「這份逐字稿少於 5 次往來，而且顧客的問題不清楚⋯⋯」→ JSON：`{"status": "INSUFFICIENT_DATA"}`。

注意，這些範例涵蓋了三種不同的情況：
* 一個**不需要**後續追蹤的完整互動
* 一個**需要**後續追蹤、而且有模糊之處的完整互動
* 一個資料不足、**無法摘要**的互動

提供範例給 Claude 時，**涵蓋各種不同的輸入／輸出組合**是很重要的。

---

## 我們的最終提示詞

我們把一開始的提示詞，和上一節新增的內容組合起來：
* 處理資料不足通話的指示
* 一組範例輸入和輸出

這是新的完整提示詞：

<details>
<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>

```python
system = """
You are an expert customer service analyst, skilled at extracting key information from call transcripts and summarizing them in a structured format.
Your task is to analyze customer service call transcripts and generate concise, accurate summaries while maintaining a professional tone.
"""

prompt = """
Analyze the following customer service call transcript and generate a JSON summary of the interaction:

<transcript>
[INSERT CALL TRANSCRIPT HERE]
</transcript>

Instructions:
<instructions>
1. Read the transcript carefully.
2. Analyze the transcript, focusing on the main issue, resolution, and any follow-up required.
3. Generate a JSON object summarizing the key aspects of the interaction according to the specified structure.

Important guidelines:
- Confidentiality: Omit all specific customer data like names, phone numbers, and email addresses.
- Character limit: Restrict each text field to a maximum of 100 characters.
- Maintain a professional tone in your summary.

Output format:
Generate a JSON object with the following structure:
<json>
{
  "summary": {
    "customerIssue": "Brief description of the main problem or reason for the call",
    "resolution": "How the issue was addressed or resolved, if applicable",
    "followUpRequired": true/false,
    "followUpDetails": "Description of any necessary follow-up actions, or null if none required"
  },
  "status": "COMPLETE",
  "ambiguities": ["List of any unclear or vague points in the conversation, or an empty array if none"]
}
</json>

Insufficient data criteria:
   If any of these conditions are met:
   a) The transcript has fewer than 5 total exchanges
   b) The customer's issue is unclear
   c) The call is garbled, incomplete, or is hindered by a language barrier
   Then return ONLY the following JSON:
   {
     "status": "INSUFFICIENT_DATA"
   }

Examples: 
<examples>
1. Complete interaction:
<transcript>
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How may I assist you today?
Customer: Hi Alex, my Acme SmartTherm isn't maintaining the temperature I set. It's set to 72 but the house is much warmer.
Agent: I'm sorry to hear that. Let's troubleshoot. Is your SmartTherm connected to Wi-Fi?
Customer: Yes, the Wi-Fi symbol is showing on the display.
Agent: Great. Let's recalibrate your SmartTherm. Press and hold the menu button for 5 seconds.
Customer: Okay, done. A new menu came up.
Agent: Perfect. Navigate to "Calibration" and press select. Adjust the temperature to match your room thermometer.
Customer: Alright, I've set it to 79 degrees to match.
Agent: Great. Press select to confirm. It will recalibrate, which may take a few minutes. Check back in an hour to see if it's fixed.
Customer: Okay, I'll do that. Thank you for your help, Alex.
Agent: You're welcome! Is there anything else I can assist you with today?
Customer: No, that's all. Thanks again.
Agent: Thank you for choosing Acme Smart Home. Have a great day!
</transcript>

<thinking>
Main issue: SmartTherm not maintaining set temperature
Resolution: Guided customer through recalibration process
Follow-up: Not required, but customer should check effectiveness after an hour
Ambiguities: None identified
</thinking>

<json>
{
  "summary": {
    "customerIssue": "SmartTherm not maintaining set temperature, showing higher than set 72 degrees",
    "resolution": "Guided customer through SmartTherm recalibration process",
    "followUpRequired": false,
    "followUpDetails": null
  },
  "status": "COMPLETE",
  "ambiguities": []
}
</json>

2. Interaction requiring follow-up:
<transcript>
Agent: Acme Smart Home Support, this is Jamie. How can I help you?
Customer: Hi, I just installed my new Acme SmartCam, but I can't get it to connect to my Wi-Fi.
Agent: I'd be happy to help. Are you using the Acme Smart Home app?
Customer: Yes, I have the app on my phone.
Agent: Great. Make sure your phone is connected to the 2.4GHz Wi-Fi network, not the 5GHz one.
Customer: Oh, I'm on the 5GHz network. Should I switch?
Agent: Yes, please switch to the 2.4GHz network. The SmartCam only works with 2.4GHz.
Customer: Okay, done. Now what?
Agent: Open the app, select 'Add Device', choose 'SmartCam', and follow the on-screen instructions.
Customer: It's asking for a password now.
Agent: Enter your Wi-Fi password and it should connect.
Customer: It's still not working. I keep getting an error message.
Agent: I see. In that case, I'd like to escalate this to our technical team. They'll contact you within 24 hours.
Customer: Okay, that sounds good. Thank you for trying to help.
Agent: You're welcome. Is there anything else you need assistance with?
Customer: No, that's all for now. Thanks again.
Agent: Thank you for choosing Acme Smart Home. Have a great day!
</transcript>

<thinking>
Main issue: Customer unable to connect new SmartCam to Wi-Fi
Resolution: Initial troubleshooting unsuccessful, issue escalated to technical team
Follow-up: Required, technical team to contact customer within 24 hours
Ambiguities: Specific error message customer is receiving not mentioned
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Unable to connect new SmartCam to Wi-Fi",
    "resolution": "Initial troubleshooting unsuccessful, issue escalated to technical team",
    "followUpRequired": true,
    "followUpDetails": "Technical team to contact customer within 24 hours for further assistance"
  },
  "status": "COMPLETE",
  "ambiguities": ["Specific error message customer is receiving not mentioned"]
}
</json>

3. Insufficient data:
<transcript>
Agent: Acme Smart Home Support, this is Sam. How may I assist you?
Customer: Hi, my smart lock isn't working.
Agent: I'm sorry to hear that. Can you tell me more about the issue?
Customer: It just doesn't work. I don't know what else to say.
Agent: Okay, when did you first notice the problem? And what model of Acme smart lock do you have?
Customer: I don't remember. Listen, I have to go. I'll call back later.
Agent: Alright, we're here 24/7 if you need further assistance. Have a good day.
</transcript>

<thinking>
This transcript has fewer than 5 exchanges and the customer's issue is unclear. The customer doesn't provide specific details about the problem with the smart lock or respond to the agent's questions. This interaction doesn't provide sufficient information for a complete summary.
</thinking>

<json>
{
  "status": "INSUFFICIENT_DATA"
}
</json>
</examples>
</instructions>

Before generating the JSON, please analyze the transcript in <thinking> tags. 
Include your identification of the main issue, resolution, follow-up requirements, and any ambiguities. 
Then, provide your JSON output in <json> tags.
"""
```

</details>

上面的提示詞相當長，但大致的結構如下：
- **系統提示詞**設定模型的背景、角色和語氣。
- **主要提示詞**包含下面這些：
    - 通話逐字稿
    - 一組指示（放在 `<instructions>` 標籤裡），包含：
        - 一般指示
        - 準則
        - 輸出格式要求
        - 處理邊緣情況通話的細節
        - 範例
    - 輸出時要使用哪些 XML 標籤的說明

下面這份摘要可以幫助你視覺化提示詞的流程：

```txt
Analyze the following customer service call transcript and generate a JSON summary of the interaction:

<transcript>
[INSERT CALL TRANSCRIPT HERE]
</transcript>

<instructions>
- General instructions and guidelines
- Output JSON format description
- Insufficient data (edge-case) criteria
<examples>
varied example inputs and outputs
</examples>
</instructions>

Before generating the JSON, please analyze the transcript in <thinking> tags. 
Include your identification of the main issue, resolution, follow-up requirements, and any ambiguities. 
Then, provide your JSON output in <json> tags.

```

（中文對照：分析通話逐字稿並產生 JSON 摘要 → `<transcript>` 逐字稿 → `<instructions>`：一般指示和準則、JSON 輸出格式說明、資料不足（邊緣情況）的判斷標準、`<examples>` 各種範例 → 最後提醒：先在 `<thinking>` 分析，再把 JSON 放在 `<json>` 裡。）

我們用一個新的函式來測試最終的提示詞。注意這個函式會**擷取** `<json>` 標籤裡的 JSON 摘要內容：

```python
import re

def summarize_call_with_final_prompt(transcript):
    final_prompt = prompt.replace("[INSERT CALL TRANSCRIPT HERE]", transcript)
    # Make the API call
    response = client.messages.create(
        model="claude-sonnet-4-6",
        system=system,
        max_tokens=4096,
        messages=[
            {"role": "user", "content": final_prompt}
        ]
    )
    
    # Extract content between <json> tags
    json_content = re.search(r'<json>(.*?)</json>', response.content[0].text, re.DOTALL)
    
    if json_content:
        print(json_content.group(1).strip())
    else:
        print("No JSON content found in the response.")
```

**逐行解說：**
- `re.search(r'<json>(.*?)</json>', response.content[0].text, re.DOTALL)`：在 Claude 的回答中找出 `<json>` 和 `</json>` 中間的內容（`<thinking>` 的部分就不要了）。
- `if json_content:`：有找到的話，印出 `.group(1)`（括號圈起來的部分），`.strip()` 去掉頭尾空白。
- 沒找到的話，印出「回答中找不到 JSON 內容」。

我們用一些現有的通話變數來測試看看：

```python
summarize_call_with_final_prompt(call1)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
{
  "summary": {
    "customerIssue": "Unable to turn on smart light bulb",
    "resolution": "Agent guided customer to reset the bulb by cycling power off and on",
    "followUpRequired": false,
    "followUpDetails": null
  },
  "status": "COMPLETE",
  "ambiguities": []
}
```

```python
summarize_call_with_final_prompt(call3)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
{
  "summary": {
    "customerIssue": "Acme SecureHome alarm system going off randomly multiple times at night without apparent cause",
    "resolution": "Initial troubleshooting steps taken, but issue unresolved. Customer transferred to technical team for diagnostics",
    "followUpRequired": true,
    "followUpDetails": "Technical team to diagnose and resolve issue with alarm system"
  },
  "status": "COMPLETE",
  "ambiguities": []
}
```

我們來試試那份應該產生「`ambiguities` 陣列不是空的」摘要的通話逐字稿：

```python
summarize_call_with_final_prompt(ambiguous_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
{
  "summary": {
    "customerIssue": "SmartLock not reliably locking automatically or through app, behavior is inconsistent",
    "resolution": "Troubleshooting attempted but incomplete due to lack of model details, customer had to leave",
    "followUpRequired": true,
    "followUpDetails": "Customer to call back for further troubleshooting of SmartLock issue when available"
  },
  "status": "COMPLETE",
  "ambiguities": [
    "Unclear if related SmartTherm issue mentioned",
    "SmartLock model not identified",
    "Customer's contact number not confirmed"
  ]
}
```

現在來試試一些我們**不想**摘要的邊緣情況：

```python
summarize_call_with_final_prompt(garbled_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
{
  "status": "INSUFFICIENT_DATA"
}
```

```python
summarize_call_with_final_prompt(language_barrier_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
{
  "status": "INSUFFICIENT_DATA"
}
```

```python
summarize_call_with_final_prompt(incomplete_call)
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
{
  "status": "INSUFFICIENT_DATA"
}
```

太好了！我們得到的正是想要的輸出！我們再推得更遠一點試試：

```python
summarize_call_with_final_prompt("blah blah blah")
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
{
  "status": "INSUFFICIENT_DATA"
}
```

```python
summarize_call_with_final_prompt("")
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
{
  "status": "INSUFFICIENT_DATA"
}
```

（輸入「blah blah blah」（廢話連篇）和空字串，也都正確地回傳了 `INSUFFICIENT_DATA`。）

太棒了，這個提示詞處理了我們所有的邊緣情況！

---

## 總結

在這一課，我們走過了為客服通話逐字稿摘要開發一個複雜提示詞的過程。我們來回顧一下用到的提示詞技巧：

* **系統提示詞**：用系統提示詞設定 Claude 的整體背景和角色。
* **結構化的輸入**：用 XML 標籤把通話逐字稿放在提示詞的開頭。
* **清楚的指示**：詳細說明要著重什麼、以及如何組織輸出。
* **輸出格式**：指定摘要的 JSON 結構，確保結果一致、容易解析。
* **處理邊緣情況**：加入辨識資料不足通話的判斷標準。
* **範例**：加入多樣化的範例，說明不同情境下想要的輸出。
* **把想法說出來**：請 Claude 在給出最終 JSON 輸出之前，先在 `<thinking>` 標籤裡展示它的分析。

運用這些技巧，我們打造了一個強健的提示詞，能為各式各樣的客服通話逐字稿產生結構化的摘要，同時妥善處理邊緣情況。這個做法也能應用在通話摘要以外的許多其他複雜提示詞情境。

**重要提醒：** 雖然我們開發了一個看起來能妥善處理測試案例的精緻提示詞，但很重要的是要了解：**這個提示詞還沒有達到可以正式上線的程度**。我們做出來的是一個很有希望的起點，但在能可靠地用在真實世界之前，它還需要大量的測試和評估。我們目前「用眼睛看」的評估，只根據一小組範例。這並不能代表真實客服通話的多樣性和常常無法預測的本質。為了確保提示詞的有效性和可靠性，我們需要實施一套包含**量化指標**的完整評估流程。**穩健、以資料為依據的評估，是把「有希望的原型」變成「可靠的、正式上線等級的解決方案」的關鍵。**

> 🧩 **白話小補充**：「怎麼做量化評估」就是<strong>第 4 單元「提示詞評估」</strong>的主題！

---

## 📌 重點整理

- 先寫**簡單版** → 測試 → 發現格式不一致 → 逐步加入：系統提示詞、逐字稿放最前面並用 `<transcript>` 包住、清楚的指示（含保密與字數限制）、JSON 格式、`<thinking>` + `<json>`。
- **找出邊緣情況**（打錯電話、斷線、亂碼、語言不通），決定處理策略（這裡選擇標記為 `INSUFFICIENT_DATA`），寫成明確的判斷標準。
- **範例要涵蓋不同情況**：不需追蹤的、需要追蹤且有模糊之處的、資料不足的。
- 提示詞裡有 JSON 大括號時，用 `.replace()` 代替 `.format()` 插入資料。
- 用正規表達式擷取 `<json>` 裡的內容。
- 「用眼睛看」的測試不夠，正式上線前需要**量化評估**。

👉 下一課：[3-5 客服機器人提示詞實作演練](05_customer_support_ai.md)
