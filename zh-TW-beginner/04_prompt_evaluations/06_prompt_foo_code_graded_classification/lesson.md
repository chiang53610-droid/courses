<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`lesson.ipynb`](lesson.ipynb)。

# 4-6 promptfoo：分類評估

> 📚 **第 4 單元：提示詞評估**｜第 6 課 / 共 9 課
> ⏱️ 預估時間：30 分鐘

## 🎯 這一課你會學到

- 把 [4-4 課](../04_code_graded_classification_evals.md) 的客訴分類評估，移植到 promptfoo 上
- 認識 promptfoo **內建的斷言（assertions）**：`contains-all`、`icontains`、`regex`⋯⋯
- 在 CSV 的 `__expected` 欄位裡使用 `contains-all:分類1,分類2`

> 📁 **這一課的檔案已經準備好了**：和這份講義同一個資料夾裡有 `promptfooconfig.yaml`、`prompts.py`、`dataset.csv`，模型已換成 `claude-haiku-4-5`。用終端機 `cd` 到這個資料夾，設定好 `ANTHROPIC_API_KEY`，執行 `npx promptfoo@latest eval` 就能跑。（安裝 Node.js、設定金鑰的方法請見 [4-5 課](../05_prompt_foo_code_graded_animals/lesson.md#-新手版補充開始之前先安裝-nodejs)。）
>
> 🔄 **2026 更新**：講義中的 YAML 範例保留原課程的模型名稱 `claude-3-haiku-20240307`（已停用），實際執行請用資料夾裡已更新的檔案。

---

**注意：這一課所在的資料夾裡有相關的程式碼檔案。如果你想跟著執行評估，請下載整個資料夾。**

在之前的一課中，我們評估了把顧客客訴分類的提示詞，例如：

> Whenever I open your app, my phone gets really slow
>（每次我打開你們的 App，我的手機就變得超慢）

和

> I can't figure out how to change my password
>（我不知道怎麼改密碼）

分到五個不同的類別：
- Software Bug（軟體錯誤）
- Hardware Malfunction（硬體故障）
- User Error（使用者操作錯誤）
- Service Outage（服務中斷）
- Feature Request（功能建議）

在這一課，我們要把這個提示詞評估移植到 promptfoo 上，讓批次執行和比較結果變得更容易。

---

## 初始化 promptfoo

第一步是用這個指令初始化 promptfoo：

```bash
npx promptfoo@latest init
```

就像上一課看到的，這會建立一個 `promptfooconfig.yaml` 檔案。我們可以把裡面原本的內容刪掉。

接著，我們設定供應商。把下面的內容加到 `promptfooconfig.yaml`：

```yaml
description: "Complaint Classification Eval"
  
providers:
  - "anthropic:messages:claude-3-haiku-20240307"
```

我們用 Claude 3 Haiku 來節省 API 費用，因為在這一課中我們會執行這個評估好幾次。

**請確認你已經設定好 `ANTHROPIC_API_KEY` 環境變數。你可以在終端機執行這個指令來設定環境變數：**

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

（Windows 的寫法請見 [4-5 課](../05_prompt_foo_code_graded_animals/lesson.md#設定供應商模型)。）

---

## 準備我們的提示詞

接著，我們要收集提示詞，並確保 promptfoo 知道它們。我們會遵循上一課看到的同樣模式：

- 每個提示詞都寫成一個 Python 函式。
- 每個提示詞函式都回傳一個提示詞字串。
- 所有的提示詞函式都放在一個 `prompts.py` 檔案裡。

建立一個叫做 `prompts.py` 的新檔案，把下面的提示詞函式加進去。這兩個提示詞，就是我們在原本的客訴分類課程中寫的那兩個：

```py
def basic_prompt(complaint):
    return f"""
    Classify the following customer complaint into one or more of these categories: 
    Software Bug, Hardware Malfunction, User Error, Feature Request, or Service Outage.
    Only respond with the classification.

    Complaint: {complaint}

    Classification:
    """

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

（兩個提示詞的中文說明請見 [4-4 課](../04_code_graded_classification_evals.md#改善後的提示詞)。）

接著，我們要告訴 promptfoo 我們想使用這兩個提示詞。更新 `promptfooconfig.yaml` 檔案：

```yaml
description: "Complaint Classification Eval"

prompts:
  - prompts.py:basic_prompt
  - prompts.py:improved_prompt
  
providers:
  - "anthropic:messages:claude-3-haiku-20240307"
```

---

## 準備評估測試集

最後一步，是把評估資料集整理成 promptfoo 好用的形式。提醒一下，這是之前那一課原本的 `eval_data` Python 串列：

```py
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

就像上一課一樣，我們要把資料集轉成一個 CSV 檔案。主要的差別在於：我們的評估邏輯**不再是單純的完全比對**了。為了替這個評估評分，我們希望 promptfoo 確認每一個模型輸出都**包含**正確的分類。

舉例來說，對於資料集中的這一列：

```py
{
    "complaint": "The cloud storage isn't syncing and I can't access my files from other devices",
    "golden_answer": ["Software Bug", "Service Outage"]
}
```

我們會寫一個提示詞，接收這則輸入的 `complaint`：

>The cloud storage isn't syncing and I can't access my files from other devices
>（雲端儲存沒有同步，我從其他裝置都打不開我的檔案）

對於上面這個例子，我們需要 promptfoo 確認模型的回答**同時包含**「Software Bug」和「Service Outage」。我們不能用完全比對——萬一模型把兩個分類的順序對調了呢？幸好，promptfoo 內建了一堆我們可以利用的**斷言（assertions）**。這些斷言包括：

* `contains`：輸出包含某個子字串
* `contains-all`：輸出包含清單中的**所有**子字串
* `contains-any`：輸出包含清單中的**任何一個**子字串
* `contains-json`：輸出包含有效的 JSON（可以選擇用 JSON schema 驗證）
* `contains-sql`：輸出包含有效的 SQL
* `contains-xml`：輸出包含有效的 XML
* `equals`：輸出完全相同
* `icontains`：輸出包含某個子字串，**不分大小寫**
* `icontains-all`：輸出包含清單中的所有子字串，不分大小寫
* `icontains-any`：輸出包含清單中的任何一個子字串，不分大小寫
* `regex`：輸出符合正規表達式
* 還有很多其他的

[點這裡查看完整的內建指標清單。](https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic/)

> 🧩 **白話小補充：什麼是「斷言（assertion）」？** 就是「檢查規則」——「我斷定輸出應該要怎樣怎樣」，符合就通過、不符合就失敗。開頭的 `i` 代表 **i**nsensitive（大小寫不敏感），例如 `icontains` 會把 "software bug" 和 "Software Bug" 視為一樣。

在我們的使用情境中，我們會用 `contains-all` 來確保每個輸出都包含所有適當的分類標籤。

載入和組織 promptfoo 評估資料集的一種方式，是使用 CSV。就像之前看到的，我們可以提供一個叫做 `__expected` 的特殊 CSV 欄位名稱，來指定評分邏輯。在這個欄位裡，我們可以使用上面任何一個內建的斷言，包括 `contains-all`。

建立一個叫做 `dataset.csv` 的新檔案，把下面的內容貼進去：

```csv
complaint,__expected
The app crashes every time I try to upload a photo,contains-all:Software Bug
My printer isn't recognized by my computer,contains-all:Hardware Malfunction
I can't figure out how to change my password,contains-all:User Error
The website is completely down I can't access any pages,contains-all:Service Outage
It would be great if the app had a dark mode option,contains-all:Feature Request
The software keeps freezing when I try to save large files,contains-all:Software Bug
My wireless mouse isn't working even with new batteries,contains-all:Hardware Malfunction
I accidentally deleted some important files can you help me recover them?,contains-all:User Error
None of your servers are responding is there an outage?,contains-all:Service Outage
Could you add a feature to export data in CSV format?,contains-all:Feature Request
"The app is crashing and my phone is overheating","contains-all:Software Bug,Hardware Malfunction"
I can't remember my password!,contains-all:User Error
The new update broke something and the app no longer works for me,contains-all:Software Bug
"I think I installed something incorrectly now my computer won't start at all","contains-all:User Error,Hardware Malfunction"
"Your service is down and I urgently need a feature to batch process files","contains-all:Service Outage,Feature Request"
The graphics card is making weird noises,contains-all:Hardware Malfunction
My keyboard just totally stopped working out of nowhere,contains-all:Hardware Malfunction
Whenever I open your app my phone gets really slow,contains-all:Software Bug
Can you make the interface more user-friendly? I always get lost in the menus,"contains-all:Feature Request,User Error"
The cloud storage isn't syncing and I can't access my files from other devices,"contains-all:Software Bug,Service Outage"
```

我們的 CSV 有兩個欄位：
- `complaint`：實際輸入的客訴
- `__expected`：一個 `contains-all` 斷言

看看其中一列，例如這一列：

> "Your service is down and I urgently need a feature to batch process files","contains-all:Service Outage,Feature Request"

資料集的這一列指定：給定輸入「Your service is down and I urgently need a feature to batch process files（你們的服務掛了，而且我急需一個批次處理檔案的功能）」時，我們希望 promptfoo 檢查模型的輸出，確保它**同時包含**「Service Outage」和「Feature Request」。

> 🧩 **白話小補充：CSV 裡的引號和逗號**
> - `contains-all:` 後面用逗號隔開多個要檢查的字：`contains-all:Service Outage,Feature Request`。
> - 但 CSV 本身也是用逗號分隔欄位！所以當一個欄位的內容**裡面有逗號**時，要用雙引號 `"..."` 把整個欄位包起來，CSV 才不會把它切錯。
> - 你可能也注意到了，原課程把客訴文字裡的逗號拿掉了（例如 `The website is completely down I can't access any pages`），這也是為了避免和 CSV 的分隔逗號混淆。

這裡的最後一步，是更新 `promptfooconfig.yaml` 檔案，加入我們剛剛寫好的測試。檔案現在應該長這樣：

```yaml
description: "Complaint Classification Eval"

prompts:
  - prompts.py:basic_prompt
  - prompts.py:improved_prompt
  
providers:
  - "anthropic:messages:claude-3-haiku-20240307"

tests: dataset.csv

```

---

## 執行評估

要執行評估，我們用之前看過的同一個指令：

```bash
npx promptfoo@latest eval
```

這是我們第一次執行上面這個評估時得到的輸出：

![分類評估在終端機的結果](../../../prompt_evaluations/06_prompt_foo_code_graded_classification/images/eval_output.png)

很明顯，包含範例的改善版提示詞，表現比最初的基本版提示詞好。範例幫助模型理解：在哪些情況下，我們可能希望輸出被指定多個分類：

![其中一列的輸出比較](../../../prompt_evaluations/06_prompt_foo_code_graded_classification/images/output_row.png)

一如往常，我們也可以用這個指令，打開互動式的網頁版評估結果：

```bash
npx promptfoo@latest view
```

![分類評估的網頁儀表板](../../../prompt_evaluations/06_prompt_foo_code_graded_classification/images/web_view.png)

我們可以看到，`basic_prompt` 答對了 **80%**，而 `improved_prompt` 拿到了 **100%**。

**一如往常，請記得我們使用的是小型的教學資料集，並不能代表真實世界的評估。我們一律建議評估資料集至少要有 100 列。**

接下來，我們要看看怎麼在 promptfoo 裡撰寫自訂的評分邏輯！

---

## 📌 重點整理

- 移植到 promptfoo 的步驟：`init` → 設定 `providers` → 把提示詞寫成 `prompts.py` 裡的函式 → 把資料集轉成 CSV → `tests: dataset.csv` → `eval` → `view`。
- **內建斷言**可以直接寫在 CSV 的 `__expected` 欄位：`contains-all:A,B`（全部都要有）、`contains-any`（有一個就好）、`icontains`（不分大小寫）、`equals`（完全相同）、`regex`（正規表達式）⋯⋯
- 多分類用 `contains-all`，不在乎順序。
- CSV 欄位內容有逗號時，要用雙引號包起來。

👉 下一課：[4-7 用 promptfoo 自訂評分器](../07_prompt_foo_custom_graders/lesson.md)
