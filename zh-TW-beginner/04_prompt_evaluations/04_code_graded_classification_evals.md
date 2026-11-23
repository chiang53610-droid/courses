<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`04_code_graded_classification_evals.ipynb`](04_code_graded_classification_evals.ipynb)。

# 4-4 程式評分評估：分類任務

> 📚 **第 4 單元：提示詞評估**｜第 4 課 / 共 9 課
> ⏱️ 預估時間：35 分鐘

## 🎯 這一課你會學到

- 從零寫一個**稍微複雜一點**的程式評分評估：顧客客訴分類
- 用 Python 的 **`set`（集合）** 比較答案，允許「多個分類、順序不同」也算對
- 加入分類說明和範例，把正確率從 85% 提升到 100%

> 🔄 **2026 更新**：原課程呼叫 `evaluate_prompt(..., model_name="claude-3-haiku-20240307")`，新手版已換成 `"claude-haiku-4-5"`。你自己跑的分數可能和原課程不同。

---

在這一課，我們要從零實作一個**稍微複雜一點**的程式評分評估，用來測試一個顧客客訴分類的提示詞。我們的目標是寫出一個能**穩定地**把顧客客訴分類到下列類別的提示詞：

* Software Bug（軟體錯誤）
* Hardware Malfunction（硬體故障）
* User Error（使用者操作錯誤）
* Feature Request（功能建議）
* Service Outage（服務中斷）

舉例來說，下面這則客訴：

> The website is completely down, I can't access any pages
>（網站完全掛了，我什麼頁面都打不開）

應該被分類為 `Service Outage`（服務中斷）。

在某些情況下，我們可能會允許**最多兩個**適用的分類，就像這個例子：

> I think I installed something incorrectly, and now my computer won't start at all
>（我覺得我裝錯了什麼東西，現在電腦完全開不了機）

它應該同時被分類為 `User Error`（使用者操作錯誤）和 `Hardware Malfunction`（硬體故障）。

---

## 評估資料集

我們先定義由輸入和標準答案組成的評估資料集。記住，一般來說我們希望評估資料集有大約 100 筆輸入，但為了讓這些課程保持簡單（而且執行起來又快又便宜），我們使用一個精簡過的資料集。

這個測試集由一個字典串列組成，每個字典都包含 `complaint`（客訴）和 `golden_answer`（標準答案）兩個 key：

```python
eval_data = [
    {
        "complaint": "The app crashes every time I try to upload a photo",
        "golden_answer": ["Software Bug"]
    },
    {
        "complaint": "My printer isn't recognized by my computer",
        "golden_answer": ["Hardware Malfunction"]
    },
    {
        "complaint": "I can't figure out how to change my password",
        "golden_answer": ["User Error"]
    },
    {
        "complaint": "The website is completely down, I can't access any pages",
        "golden_answer": ["Service Outage"]
    },
    {
        "complaint": "It would be great if the app had a dark mode option",
        "golden_answer": ["Feature Request"]
    },
    {
        "complaint": "The software keeps freezing when I try to save large files",
        "golden_answer": ["Software Bug"]
    },
    {
        "complaint": "My wireless mouse isn't working, even with new batteries",
        "golden_answer": ["Hardware Malfunction"]
    },
    {
        "complaint": "I accidentally deleted some important files, can you help me recover them?",
        "golden_answer": ["User Error"]
    },
    {
        "complaint": "None of your servers are responding, is there an outage?",
        "golden_answer": ["Service Outage"]
    },
    {
        "complaint": "Could you add a feature to export data in CSV format?",
        "golden_answer": ["Feature Request"]
    },
    {
        "complaint": "The app is crashing and my phone is overheating",
        "golden_answer": ["Software Bug", "Hardware Malfunction"]
    },
    {
        "complaint": "I can't remember my password!",
        "golden_answer": ["User Error"]
    },
    {
        "complaint": "The new update broke something and the app no longer works for me",
        "golden_answer": ["Software Bug"]
    },
    {
        "complaint": "I think I installed something incorrectly, now my computer won't start at all",
        "golden_answer": ["User Error", "Hardware Malfunction"]
    },
    {
        "complaint": "Your service is down, and I urgently need a feature to batch process files",
        "golden_answer": ["Service Outage", "Feature Request"]
    },
    {
        "complaint": "The graphics card is making weird noises",
        "golden_answer": ["Hardware Malfunction"]
    },
    {
        "complaint": "My keyboard just totally stopped working out of nowhere",
        "golden_answer": ["Hardware Malfunction"]
    },
    {
        "complaint": "Whenever I open your app, my phone gets really slow",
        "golden_answer": ["Software Bug"]
    },
    {
        "complaint": "Can you make the interface more user-friendly? I always get lost in the menus",
        "golden_answer": ["Feature Request", "User Error"]
    },
    {
        "complaint": "The cloud storage isn't syncing and I can't access my files from other devices",
        "golden_answer": ["Software Bug", "Service Outage"]
    }
]
```

**資料集裡有 20 則客訴**，大部分只有一個分類，最後幾筆刻意設計成有**兩個分類**，例如：
- 「你們的服務掛了，而且我急需一個批次處理檔案的功能」→ 服務中斷 + 功能建議
- 「可以把介面做得更好用嗎？我在選單裡總是迷路」→ 功能建議 + 使用者操作錯誤
- 「雲端儲存沒有同步，我從其他裝置都打不開我的檔案」→ 軟體錯誤 + 服務中斷

---

## 初始提示詞

我們從一個基本的提示詞開始，衡量它的表現。下面這個產生提示詞的函式接收一則 `complaint`，回傳一個提示詞字串：

```python
def basic_prompt(complaint):
    return f"""
    Classify the following customer complaint into one or more of these categories: 
    Software Bug, Hardware Malfunction, User Error, Feature Request, or Service Outage.
    Only respond with the matching category or categories and nothing else.

    Complaint: {complaint}

    Classification:
    """
```

**翻譯**：「把下面這則顧客客訴分類到一個或多個類別：Software Bug、Hardware Malfunction、User Error、Feature Request 或 Service Outage。只回答符合的類別，其他什麼都不要。客訴：{complaint} 分類：」

---

## 收集輸出

接著，我們來寫評估提示詞的邏輯。這個邏輯比上一課的「數腿」範例複雜一點：

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

def get_model_response(prompt, model_name):
    response = client.messages.create(
        model=model_name,
        max_tokens=200,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.content[0].text

def calculate_accuracy(eval_data, model_responses):
    correct_predictions = 0
    total_predictions = len(eval_data)
    
    for item, response in zip(eval_data, model_responses):
        golden_set = set(category.lower() for category in item["golden_answer"])
        prediction_set = set(category.strip().lower() for category in response.split(','))
        
        if golden_set == prediction_set:
            correct_predictions += 1
    
    return correct_predictions / total_predictions

def evaluate_prompt(prompt_func, eval_data, model_name):
    print(f"Evaluating with model: {model_name}")
    model_responses = [get_model_response(prompt_func(item['complaint']), model_name) for item in eval_data]
    accuracy = calculate_accuracy(eval_data, model_responses)
    
    print(f"Accuracy: {accuracy:.2%}")
    
    for item, response in zip(eval_data, model_responses):
        print(f"\nComplaint: {item['complaint']}")
        print(f"Golden Answer: {item['golden_answer']}")
        print(f"Model Response: {response}")
    return accuracy
```

**逐行解說：**
- `get_model_response(prompt, model_name)`：問 Claude，回傳文字（這次把模型名稱也當成參數，方便換模型比較）。
- `calculate_accuracy(eval_data, model_responses)`：計算正確率。
  - `golden_set = set(category.lower() for category in item["golden_answer"])`：把標準答案的每個分類轉成小寫，放進一個**集合（set）**。
  - `prediction_set = set(category.strip().lower() for category in response.split(','))`：把 Claude 的回答用逗號 `,` 切開（例如 `"Software Bug, Service Outage"` → `["Software Bug", " Service Outage"]`），每一段去掉前後空白、轉小寫，放進集合。
  - `if golden_set == prediction_set:`：兩個集合**內容一樣**就算對。
- `evaluate_prompt(prompt_func, eval_data, model_name)`：整個評估流程——對每一筆客訴產生提示詞、問 Claude、算正確率、印出結果。
  - 注意 `prompt_func` 是**一個函式**！我們可以把「產生提示詞的函式」當作參數傳進去，這樣同一套評估程式就能測試不同的提示詞。
  - `f"{accuracy:.2%}"`：`.2%` 會把 0.85 顯示成 `85.00%`。

> 🧩 **白話小補充：為什麼用 `set`（集合）？**
> 集合有兩個特性：**沒有順序**、**不會重複**。所以：
> ```python
> set(["software bug", "service outage"]) == set(["service outage", "software bug"])  # True！
> ```
> 這樣 Claude 不管先寫哪個分類，只要分類對了就算正確。如果用一般的字串比對，順序不同就會被判錯。

`evaluate_prompt` 函式做了下面這些事：

1. 把每一筆輸入傳進我們的「提示詞產生函式」，再用 `get_model_response` 函式把產生的提示詞送給模型執行，一邊產生一邊收集回答。
2. 把模型輸出的答案和資料集裡的標準答案比較，計算正確率。為了做到這一點，它會呼叫 `calculate_accuracy` 函式。
3. `calculate_accuracy` 函式使用 `set`，檢查模型的每一個輸出中是否有適當的分類類別。記住，這**不是**像上一課「數腿」評估那樣的完全比對評估。
4. `calculate_accuracy` 回傳正確率分數
5. `evaluate_prompt` 印出最終結果

**注意：和上一課用完全字串比對評分不同，我們這次的評分邏輯使用 `set` 來檢查模型輸出中是否出現特定的值。**

我們用初始的 `basic_prompt` 測試看看：

```python
evaluate_prompt(basic_prompt, eval_data, model_name="claude-haiku-4-5")
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
Evaluating with model: claude-3-haiku-20240307
Accuracy: 85.00%

Complaint: The app crashes every time I try to upload a photo
Golden Answer: ['Software Bug']
Model Response: Software Bug

Complaint: My printer isn't recognized by my computer
Golden Answer: ['Hardware Malfunction']
Model Response: Hardware Malfunction

Complaint: I can't figure out how to change my password
Golden Answer: ['User Error']
Model Response: User Error

Complaint: The website is completely down, I can't access any pages
Golden Answer: ['Service Outage']
Model Response: Service Outage

Complaint: It would be great if the app had a dark mode option
Golden Answer: ['Feature Request']
Model Response: Feature Request

Complaint: The software keeps freezing when I try to save large files
Golden Answer: ['Software Bug']
Model Response: Software Bug

Complaint: My wireless mouse isn't working, even with new batteries
Golden Answer: ['Hardware Malfunction']
Model Response: Hardware Malfunction

Complaint: I accidentally deleted some important files, can you help me recover them?
Golden Answer: ['User Error']
Model Response: User Error

Complaint: None of your servers are responding, is there an outage?
Golden Answer: ['Service Outage']
Model Response: Service Outage

Complaint: Could you add a feature to export data in CSV format?
Golden Answer: ['Feature Request']
Model Response: Feature Request

Complaint: The app is crashing and my phone is overheating
Golden Answer: ['Software Bug', 'Hardware Malfunction']
Model Response: Hardware Malfunction
Software Bug

Complaint: I can't remember my password!
Golden Answer: ['User Error']
Model Response: User Error

Complaint: The new update broke something and the app no longer works for me
Golden Answer: ['Software Bug']
Model Response: Software Bug

Complaint: I think I installed something incorrectly, now my computer won't start at all
Golden Answer: ['User Error', 'Hardware Malfunction']
Model Response: User Error, Hardware Malfunction

Complaint: Your service is down, and I urgently need a feature to batch process files
Golden Answer: ['Service Outage', 'Feature Request']
Model Response: Feature Request, Service Outage

Complaint: The graphics card is making weird noises
Golden Answer: ['Hardware Malfunction']
Model Response: Hardware Malfunction

Complaint: My keyboard just totally stopped working out of nowhere
Golden Answer: ['Hardware Malfunction']
Model Response: Hardware Malfunction

Complaint: Whenever I open your app, my phone gets really slow
Golden Answer: ['Software Bug']
Model Response: Hardware Malfunction

Complaint: Can you make the interface more user-friendly? I always get lost in the menus
Golden Answer: ['Feature Request', 'User Error']
Model Response: Feature Request

Complaint: The cloud storage isn't syncing and I can't access my files from other devices
Golden Answer: ['Software Bug', 'Service Outage']
Model Response: Software Bug, Service Outage
0.85
```

---

## 改善後的提示詞

我們的初始提示詞得到了 85% 的正確率。我們來修改提示詞並重新執行評估，希望能得到更好的分數。

下面這個提示詞加入了**各類別的詳細說明**，以及 **9 組範例輸入／輸出**：

```python
def improved_prompt(complaint):
    return f"""
    You are an AI assistant specializing in customer support issue classification. Your task is to analyze customer complaints and categorize them into one or more of the following categories:

    1. Software Bug: Issues related to software not functioning as intended.
    2. Hardware Malfunction: Problems with physical devices or components.
    3. User Error: Difficulties arising from user misunderstanding or misuse.
    4. Feature Request: Suggestions for new functionalities or improvements.
    5. Service Outage: System-wide issues affecting service availability.

    Important Guidelines:
    - A complaint may fall into multiple categories. If so, list all that apply but try to prioritize picking a single category when possible.

    Examples:
    1. Complaint: "The app crashes when I try to save my progress."
    Classification: Software Bug

    2. Complaint: "My keyboard isn't working after I spilled coffee on it."
    Classification: Hardware Malfunction

    3. Complaint: "I can't find the login button on your website."
    Classification: User Error

    4. Complaint: "It would be great if your app had a dark mode."
    Classification: Feature Request

    5. Complaint: "None of your services are loading for me or my colleagues."
    Classification: Service Outage

    6. Complaint "Complaint: The app breaks every time I try to change my profile picture"
    Classification: Software Bug

    7. Complaint "The app is acting buggy on my phone and it seems like your website is down, so I'm completely stuck!"
    Classification: Software Bug, Service Outage

    8. Complaint: "Your software makes my computer super laggy and awful, I hate it!"
    Classification: Software Bug

    9. Complaint: "Your dumb app always breaks when I try to do anything with images."
    Classification: 'Software Bug'

    Now, please classify the following customer complaint:

    <complaint>{complaint}</complaint>

    Only respond with the appropriate categories and nothing else.
    Classification:
    """
```

**改善後提示詞的重點翻譯：**
- **角色**：「你是一個專門分類客服問題的 AI 助理。你的任務是分析顧客客訴，並把它們分類到下列一個或多個類別：」
- **類別說明**：
  1. 軟體錯誤：和軟體沒有照預期運作有關的問題。
  2. 硬體故障：實體裝置或零件的問題。
  3. 使用者操作錯誤：因為使用者誤解或誤用而產生的困難。
  4. 功能建議：對新功能或改進的建議。
  5. 服務中斷：影響服務可用性的全系統問題。
- **重要準則**：「一則客訴可能屬於多個類別。如果是這樣，就列出所有適用的類別，但**盡可能優先只選一個類別**。」
- **9 個範例**：例如「我把咖啡灑在鍵盤上之後它就不能用了」→ 硬體故障；「我在你們網站上找不到登入按鈕」→ 使用者操作錯誤；「App 在我手機上怪怪的，而且你們網站好像也掛了，我完全卡住了！」→ 軟體錯誤, 服務中斷⋯⋯
- **最後**：「現在，請分類下面這則顧客客訴：`<complaint>{complaint}</complaint>` 只回答適當的類別，其他什麼都不要。分類：」

我們用改善後的提示詞執行評估：

```python
evaluate_prompt(improved_prompt, eval_data, model_name="claude-haiku-4-5")
```

**▶ 原課程執行結果（你自己跑的時候，Claude 的回答文字會不一樣，這是正常的）：**

```text
Evaluating with model: claude-3-haiku-20240307
Accuracy: 100.00%

Complaint: The app crashes every time I try to upload a photo
Golden Answer: ['Software Bug']
Model Response: Software Bug

Complaint: My printer isn't recognized by my computer
Golden Answer: ['Hardware Malfunction']
Model Response: Hardware Malfunction

Complaint: I can't figure out how to change my password
Golden Answer: ['User Error']
Model Response: User Error

Complaint: The website is completely down, I can't access any pages
Golden Answer: ['Service Outage']
Model Response: Service Outage

Complaint: It would be great if the app had a dark mode option
Golden Answer: ['Feature Request']
Model Response: Feature Request

Complaint: The software keeps freezing when I try to save large files
Golden Answer: ['Software Bug']
Model Response: Software Bug

Complaint: My wireless mouse isn't working, even with new batteries
Golden Answer: ['Hardware Malfunction']
Model Response: Hardware Malfunction

Complaint: I accidentally deleted some important files, can you help me recover them?
Golden Answer: ['User Error']
Model Response: User Error

Complaint: None of your servers are responding, is there an outage?
Golden Answer: ['Service Outage']
Model Response: Service Outage

Complaint: Could you add a feature to export data in CSV format?
Golden Answer: ['Feature Request']
Model Response: Feature Request

Complaint: The app is crashing and my phone is overheating
Golden Answer: ['Software Bug', 'Hardware Malfunction']
Model Response: Software Bug, Hardware Malfunction

Complaint: I can't remember my password!
Golden Answer: ['User Error']
Model Response: User Error

Complaint: The new update broke something and the app no longer works for me
Golden Answer: ['Software Bug']
Model Response: Software Bug

Complaint: I think I installed something incorrectly, now my computer won't start at all
Golden Answer: ['User Error', 'Hardware Malfunction']
Model Response: Hardware Malfunction, User Error

Complaint: Your service is down, and I urgently need a feature to batch process files
Golden Answer: ['Service Outage', 'Feature Request']
Model Response: Service Outage, Feature Request

Complaint: The graphics card is making weird noises
Golden Answer: ['Hardware Malfunction']
Model Response: Hardware Malfunction

Complaint: My keyboard just totally stopped working out of nowhere
Golden Answer: ['Hardware Malfunction']
Model Response: Hardware Malfunction

Complaint: Whenever I open your app, my phone gets really slow
Golden Answer: ['Software Bug']
Model Response: Software Bug

Complaint: Can you make the interface more user-friendly? I always get lost in the menus
Golden Answer: ['Feature Request', 'User Error']
Model Response: User Error, Feature Request

Complaint: The cloud storage isn't syncing and I can't access my files from other devices
Golden Answer: ['Software Bug', 'Service Outage']
Model Response: Software Bug, Service Outage
1.0
```

改善後的新提示詞得到了 **100%** 的正確率！

再一次，我們遵循了這張圖描述的標準「提示詞 + 評估」循環：

![以評估為核心的提示詞開發流程](../../prompt_evaluations/images/process.png)

**請記住，這是一個非常簡單的評估，使用的是非常小的資料集。這一課的目的是說明程式評分評估的一般流程，並不是要當作正式上線規模評估的標準範例！**

這個方法行得通，但從零寫出所有評估邏輯有點費工，而且很難把結果並排比較。如果我們使用一個工具，能產生排版漂亮、有圖表的結果，而且能輕鬆地在多個模型上執行評估呢？下一課我們就會看到這樣的工具！接下來，我們要介紹一個評估框架，讓你能輕鬆寫出可重複、可擴展、適合正式上線使用情境的評估。

---

## 📌 重點整理

- 分類任務的評估：**資料集**（客訴 + 標準答案串列）→ **提示詞函式** → **收集輸出** → **評分** → **正確率**。
- 用 **`set`** 比較答案：不在乎順序、不在乎大小寫（先 `.lower()`），可以處理「多個正確分類」。
- 把「提示詞函式」當成參數傳給 `evaluate_prompt`，同一套評估程式就能比較不同的提示詞。
- 這一課的改善：加入**角色、類別說明、準則、9 個範例、XML 標籤** → 85% 提升到 100%。
- 自己寫評估邏輯很費工、難比較 → 下一課介紹評估工具 **promptfoo**。

👉 下一課：[4-5 用 promptfoo 做評估：入門](05_prompt_foo_code_graded_animals/lesson.md)
