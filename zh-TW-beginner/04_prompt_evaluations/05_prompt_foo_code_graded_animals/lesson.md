<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`lesson.ipynb`](lesson.ipynb)。

# 4-5 promptfoo 入門

> 📚 **第 4 單元：提示詞評估**｜第 5 課 / 共 9 課
> ⏱️ 預估時間：60 分鐘（第一次要安裝 Node.js，會比較久）

## 🎯 這一課你會學到

- 為什麼要用現成的評估工具，而不是自己從零寫
- 安裝並使用開源評估工具 **promptfoo**
- 設定 `promptfooconfig.yaml`：**providers（模型）**、**prompts（提示詞）**、**tests（測試）**
- 用 CSV 檔定義測試資料、用 `transform` 先處理輸出再評分
- 用網頁儀表板查看結果、一次比較多個模型

> 📁 **這一課的檔案都已經幫你準備好了！**
> 原課程說：「這一課所在的資料夾裡有相關的程式碼檔案，如果你想跟著執行評估，請下載整個資料夾。」
> 新手版已經把這些檔案放在**和這份講義同一個資料夾**裡（`zh-TW-beginner/04_prompt_evaluations/05_prompt_foo_code_graded_animals/`），而且**已經把模型名稱換成目前可用的模型**：
> - `promptfooconfig.yaml`：promptfoo 的設定檔
> - `prompts.py`：三個提示詞函式
> - `animal_legs_tests.csv`：測試資料
> - `transform.py`：轉換輸出的函式
>
> 下面的講義會一步一步帶你從零建立這些檔案，讓你了解每個檔案的作用。你可以照著自己建一次，也可以直接用準備好的檔案執行。

> 🔄 **2026 更新**：原課程的 `claude-3-haiku-20240307` 換成 `claude-haiku-4-5`，`claude-3-5-sonnet-20240620` 換成 `claude-sonnet-4-6`。講義中的 YAML 範例保留原課程的寫法，**實際執行請以資料夾裡已更新的檔案為準**。截圖是原課程用舊模型跑出來的，你的結果會不同。

---

我們已經看過怎麼從零寫自己的評估了，這樣做雖然有效，但有點麻煩。比較實際的做法，通常是利用**專門為評估設計的工具**。現在有很多評估工具和函式庫可以用（而且一直有新的推出！），包括：
- [promptfoo](https://github.com/promptfoo/promptfoo)
- [Vellum](https://www.vellum.ai/#playground)
- [Scale Evaluation](https://scale.com/evaluation/model-developers)
- [Prompt Layer](https://promptlayer.com/)
- [Chain Forge](https://github.com/ianarawjo/ChainForge)
- 還有很多其他的！

其中一個**開源、好用**的選擇是 **promptfoo**。promptfoo 提供一個精簡、開箱即用的解決方案，能大幅減少全面測試提示詞所需的時間和精力。它提供簡單、現成的基礎設施，支援批次測試、版本控制和效能分析，讓開發者能把更多心力放在改進提示詞上，而不是建立和維護測試框架。它讓我們能輕鬆地在多個提示詞、模型和供應商之間執行評估，也提供工具讓我們輕鬆地視覺化、比較評估結果。比起自己從零寫評估邏輯，promptfoo 和其他評估工具是很大的進步！

執行評估之後，promptfoo 會產生一個像下面這張圖的儀表板：

![promptfoo 的評估結果儀表板](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/prompt_foo.png)

我們開始吧！

---

## 我們的第一個 promptfoo 評估

接下來的幾堂課，會著重在用 promptfoo 撰寫評估。在這第一課，我們會學習用一種簡單的方法，用 promptfoo 評估幾課前的「這種動物有幾條腿？」提示詞。這是一個非常簡單的提示詞和評估。我們的重點在於**實際使用 promptfoo 執行評估的工具和流程**。

提醒一下，在那一課我們用的是這個小小的評估資料集：

```py
eval_data = [
    {"animal_statement": "The animal is a human.", "golden_answer": "2"},
    {"animal_statement": "The animal is a snake.", "golden_answer": "0"},
    {"animal_statement": "The fox lost a leg, but then magically grew back the leg he lost and a mysterious extra leg on top of that.", "golden_answer": "5"},
    {"animal_statement": "The animal is a dog.", "golden_answer": "4"},
    {"animal_statement": "The animal is a cat with two extra legs.", "golden_answer": "6"},
    {"animal_statement": "The animal is an elephant.", "golden_answer": "4"},
    {"animal_statement": "The animal is a bird.", "golden_answer": "2"},
    {"animal_statement": "The animal is a fish.", "golden_answer": "0"},
    {"animal_statement": "The animal is a spider with two extra legs", "golden_answer": "10"},
    {"animal_statement": "The animal is an octopus.", "golden_answer": "8"},
    {"animal_statement": "The animal is an octopus that lost two legs and then regrew three legs.", "golden_answer": "9"},
    {"animal_statement": "The animal is a two-headed, eight-legged mythical creature.", "golden_answer": "8"},
]
```

（中文翻譯請見 [4-3 課](../03_code_graded.md#我們的輸入資料)。）

在那一課，我們寫了三個不同的提示詞，在我們陽春的評估函式下，正確率一個比一個高。在這一課，我們會把評估資料集和提示詞移植到 promptfoo 上，看看執行和比較它們的輸出有多簡單。

---

## 🧩 新手版補充：開始之前，先安裝 Node.js

promptfoo 是用 JavaScript 寫的工具，要用 **`npx`** 指令來執行，而 `npx` 是 **Node.js** 附帶的工具。所以要先安裝 Node.js：

1. 到 <https://nodejs.org/> 下載「**LTS**（長期支援）」版本並安裝（一路按「下一步」即可）。
2. 安裝完後**重新打開**終端機，輸入下面兩行確認安裝成功（會顯示版本號碼）：
   ```bash
   node --version
   npx --version
   ```

另外，promptfoo 會呼叫 Python 來執行我們寫的 `prompts.py` 和 `transform.py`，所以電腦裡也要有 Python（你在 [0-3](../../00_before_you_start/03_setup_your_computer.md) 已經裝好了）。

> 🧩 **什麼是終端機裡的「目前資料夾」？** 在終端機裡執行 promptfoo 時，它會在「目前所在的資料夾」裡尋找 `promptfooconfig.yaml`。所以要先用 `cd` 指令移動到正確的資料夾，例如：
> ```bash
> cd 你放課程的路徑/courses/zh-TW-beginner/04_prompt_evaluations/05_prompt_foo_code_graded_animals
> ```
> （小技巧：在 VS Code 裡，對資料夾按右鍵 →「在整合式終端機中開啟」，就會自動 `cd` 到那個資料夾。）

---

## 安裝 promptfoo

使用 promptfoo 的第一步，是透過命令列安裝它。移動到你要寫評估程式碼的資料夾，執行下面這個指令：

```bash
npx promptfoo@latest init
```

這會在目前的資料夾建立一個 `promptfooconfig.yaml` 檔案。**所有的魔法都發生在這個檔案裡。** 我們會在裡面設定下面這些東西：
- 我們想在評估中使用的**供應商（providers）**（要用哪些 Anthropic API 模型）
- 我們想評估的**提示詞（prompts）**
- 我們想執行的**測試（tests）**

> 🧩 **白話小補充**：
> - `npx promptfoo@latest init`：意思是「用最新版（`@latest`）的 promptfoo，執行 `init`（初始化）」。`npx` 會自動下載 promptfoo，不用另外安裝。第一次執行時可能會問你要不要安裝，輸入 `y` 再按 Enter。
> - **YAML** 是一種寫設定檔的格式，用「縮排」和「`名稱: 值`」來表示結構，比 JSON 更好讀。注意**縮排要用空格，不能用 Tab**。
>
> 💡 如果你直接使用新手版準備好的資料夾，**不需要**執行 `init`（設定檔已經有了）。

---

## 設定供應商（模型）

接著，我們可以設定 promptfoo 使用我們想用來執行評估的 Anthropic API 模型。做法是在 `promptfooconfig.yaml` 檔案裡指定一個 `providers` 欄位，並把它設定成一個或多個 Anthropic 模型。promptfoo 用一種特定的格式來指定模型名稱。目前支援的 Anthropic 模型字串有：

- `anthropic:messages:claude-3-5-sonnet-20240620`
- `anthropic:messages:claude-3-haiku-20240307`
- `anthropic:messages:claude-3-sonnet-20240229`
- `anthropic:messages:claude-3-opus-20240229`
- `anthropic:messages:claude-2.0`
- `anthropic:messages:claude-2.1`
- `anthropic:messages:claude-instant-1.2`

> 🔄 **2026 更新**：上面這些都是 2024 年的模型，現在**全部已停用**。格式一樣是 `anthropic:messages:模型名稱`，例如 `anthropic:messages:claude-haiku-4-5`、`anthropic:messages:claude-sonnet-4-6`、`anthropic:messages:claude-opus-4-6`。

這次的評估我們先用 Haiku。把 `promptfooconfig.yaml` 檔案原本的內容刪掉，換成這樣：

```yaml
description: "Animal Legs Eval"
  
providers:
  - "anthropic:messages:claude-3-haiku-20240307"
```

（新手版請寫成 `- "anthropic:messages:claude-haiku-4-5"`。）

每個部分的作用如下：

- `description`（描述）是一個選填的標籤，描述我們在評估什麼任務。
- `providers`（供應商）告訴 promptfoo 我們想用 Haiku 來做這次評估。我們可以指定多個模型，在之後的課程會看到。

promptfoo 在執行評估時，會尋找一個叫做 `ANTHROPIC_API_KEY` 的**環境變數**。你可以在命令列執行下面這個指令來設定環境變數：

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

> 🧩 **新手版補充：不同作業系統的寫法**（把 `your_api_key_here` 換成你的金鑰）
> | 系統 | 指令 |
> |---|---|
> | Mac / Linux | `export ANTHROPIC_API_KEY=your_api_key_here` |
> | Windows PowerShell | `$env:ANTHROPIC_API_KEY="your_api_key_here"` |
> | Windows 命令提示字元（cmd） | `set ANTHROPIC_API_KEY=your_api_key_here` |
>
> ⚠️ 這樣設定只在**這個終端機視窗**有效，關掉視窗就要重新設定。另外，promptfoo 通常也會自動讀取「目前資料夾」裡的 `.env` 檔，你也可以在這個資料夾裡放一份 `.env`（內容跟 [0-3 步驟 6](../../00_before_you_start/03_setup_your_computer.md#步驟-6把-api-金鑰安全地存起來env-檔) 一樣）。

---

## 指定我們的提示詞

下一步是告訴 promptfoo 我們想評估哪些提示詞。做法有很多種，包括：
- 直接把提示詞以文字寫在 YAML 檔案裡
- 從 JSON 檔案載入提示詞
- 從文字檔載入提示詞
- 從另一個 YAML 檔案載入提示詞
- 從 Python 檔案載入提示詞

我們比較喜歡把所有相關的提示詞放在**一個 Python 檔案**裡，每個提示詞寫成一個回傳提示詞字串的函式。在之後的課程中，我們會看到其他的做法。你會在整門課中看到，promptfoo 非常有彈性！

建立一個叫做 `prompts.py` 的 Python 檔案，把下面這些提示詞函式放進去：

```py
def simple_prompt(animal_statement):
    return f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? Please respond with a number"""

def better_prompt(animal_statement):
    return f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? Please only respond with a single digit like 2 or 9"""
```

（`simple_prompt` 最後是「請用一個數字回答」；`better_prompt` 最後是「請只用一個數字回答，例如 2 或 9」。）

注意，每個函式都接收一個 `animal_statement` 參數，把它插入提示詞，然後回傳最終的提示詞字串。

下一步是告訴 promptfoo 設定檔，我們想從剛剛建立的 `prompts.py` 檔案載入提示詞。做法是更新 `promptfooconfig.yaml` 檔案，加入這段程式碼：

```yaml
description: "Animal Legs Eval"

prompts:
  - prompts.py:simple_prompt
  - prompts.py:better_prompt
  
providers:
  - "anthropic:messages:claude-3-haiku-20240307"
```

注意，我們為加入 `prompts.py` 檔案的每個提示詞函式各加了一行。我們告訴 promptfoo：我們想評估兩個提示詞——`simple_prompt` 和 `better_prompt`，它們都「住在」`prompts.py` 檔案裡。

（`prompts.py:simple_prompt` 的意思是「`prompts.py` 這個檔案裡的 `simple_prompt` 函式」。）

---

## 設定我們的測試

下一步是告訴 promptfoo，我們想用特定的提示詞和供應商執行哪些測試。promptfoo 提供很多種定義測試的方式，但我們先從最常見的一種開始：**在 CSV 檔案裡指定測試**。

我們會建立一個新的 CSV 檔案，叫做 `dataset.csv`，把測試輸入寫在裡面。

promptfoo 讓我們可以直接在 CSV 檔案裡定義評估邏輯。在接下來的課程中，我們會看到一些 promptfoo 內建的測試斷言（assertion），但在這個評估中，我們只需要檢查模型的輸出和預期的腿數是否**完全相同**。

為了做到這一點，我們會在 CSV 裡寫兩個欄位標題：
- `animal_statement`：放輸入的動物描述，例如「The animal is an elephant」
- `__expected`：放預期的正確輸出（注意 `__expected` 前面是**兩個底線**）。這是 promptfoo 特有的語法。

> 🧩 **白話小補充：CSV 是什麼？** CSV（Comma-Separated Values，逗號分隔值）是一種很簡單的表格檔案，每一行是一列資料，欄位之間用逗號隔開。可以用 Excel 或記事本打開。第一行是**欄位名稱**。
> - 欄位名稱 `animal_statement` 會自動對應到提示詞函式的參數 `animal_statement`。
> - `__expected` 是 promptfoo 的特殊欄位，裡面放「預期答案」。只寫一個值（例如 `"2"`）時，代表輸出要**完全等於**這個值。

建立一個 `dataset.csv` 檔案，加入下面的內容：

```csv
animal_statement,__expected
"The animal is a human.","2"
"The animal is a snake.","0"
"The fox lost a leg, but then magically grew back the leg he lost and a mysterious extra leg on top of that.","5"
"The animal is a dog.","4"
"The animal is a cat with two extra legs.","6"
"The animal is an elephant.","4"
"The animal is a bird.","2"
"The animal is a fish.","0"
"The animal is a spider with two extra legs","10"
"The animal is an octopus.","8"
"The animal is an octopus that lost two legs and then regrew three legs.","9"
"The animal is a two-headed, eight-legged mythical creature.","8"
```

最後，我們告訴 promptfoo 應該從我們的 `dataset.csv` 檔案載入測試。做法是更新 `promptfooconfig.yaml` 檔案，加入這段程式碼：

```yaml
description: "Animal Legs Eval"

prompts:
  - prompts.py:simple_prompt
  - prompts.py:better_prompt
  
providers:
  - "anthropic:messages:claude-3-haiku-20240307"

tests: animal_legs_tests.csv
```

> ⚠️ **注意檔名**：原課程前面說要建立 `dataset.csv`，但設定檔裡寫的卻是 `animal_legs_tests.csv`（實際提供的檔案也叫 `animal_legs_tests.csv`）。**設定檔裡的檔名要和實際的 CSV 檔名一致**。新手版資料夾裡用的是 `animal_legs_tests.csv`。

---

## 執行我們的評估

我們已經指定了供應商、提示詞和測試，現在是執行評估的時候了！

在終端機執行下面這個指令：

```bash
npx promptfoo@latest eval
```

這會開始評估流程。對於每個提示詞，promptfoo 會：
- 從 CSV 檔案取出每一則 `animal_statement`
- 組出包含這則 `animal_statement` 的完整提示詞
- 用這個提示詞送出一個請求到 Anthropic API
- 檢查輸出是否符合 CSV 檔案裡的預期輸出

評估完成後，promptfoo 會在終端機顯示結果。

下面是執行上面兩個提示詞時，promptfoo 輸出的範例：

![promptfoo 在終端機顯示的評估結果](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/eval_output1.png)

上面的截圖只包含前四列，但評估其實在全部十二筆輸入上都執行了。
- **左邊那一欄**顯示特定的 `animal_statement`
- **中間那一欄**顯示 `simple_prompt` 的輸出和分數，它似乎每一個測試案例都失敗了！
- **右邊那一欄**顯示 `better_prompt` 的輸出和分數，除了邏輯比較複雜的那幾題以外，大部分的測試案例都成功了。

---

## 查看評估結果

promptfoo 讓我們可以很輕鬆地啟動一個儀表板，在瀏覽器裡視覺化、檢視評估結果。執行完上面的評估之後，試著在終端機執行這個指令：

```bash
npx promptfoo@latest view
```

它會問你要不要啟動一個伺服器（輸入 `y`），然後在瀏覽器裡打開一個儀表板。

![promptfoo 的網頁儀表板](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/eval_view1.png)

> 💡 看完之後，回到終端機按 `Ctrl + C` 就可以關掉這個伺服器。

最相關的摘要資訊在最上面：

![儀表板上方的摘要資訊](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/eval_results1.png)

我們也可以深入查看特定的結果，了解它們為什麼失敗。我們來看看其中一個 `simple_prompt` 的結果（中間那一欄）。這個提示詞的每一列都被標記為失敗。到底發生了什麼事？

點擊格子裡的**放大鏡按鈕**，可以看到更多資訊：

![格子上的工具列（放大鏡按鈕）](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/toolbar.png)

這會打開一個視窗，裡面有輸出和評分的具體細節：

![輸出和評分的細節](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/details.png)

我們可以清楚地看到，`simple_prompt` 得到了正確答案 0，但輸出裡包含了一堆額外的、不需要的解釋文字，導致它沒有通過評估。

如果我們仔細看最右邊那一欄——也就是 `better_prompt` 提示詞的結果——我們得到的回答好很多，全部都是像 `5` 或 `0` 這樣的單一數字。它似乎在那些比較複雜、需要更多推理才能回答的 `animal_statement` 上失敗了，例如：

> The fox lost a leg, but then magically grew back the leg he lost and a mysterious extra leg on top of that.

---

## 加入第三個提示詞

回想一下之前程式評分評估那一課，我們最後是在提示詞中加入一些**思維鏈推理**，才得到最好的結果。我們來加入改進過的第三個提示詞，它包含思維鏈，看看它在「比較刁鑽」的問題上表現如何！

把下面這個提示詞函式加到 `prompts.py`：

```py
def chain_of_thought_prompt(animal_statement):
    return f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? 
    Start by reasoning about the numbers of legs the animal has, thinking step by step inside of <thinking> tags.  
    Then, output your final answer inside of <answer> tags. 
    Inside the <answer> tags return just the number of legs as an integer and nothing else."""
```

接著，更新 `promptfooconfig.yaml` 檔案，加入我們的新提示詞：

```yaml
description: "Animal Legs Eval"

prompts:
  - prompts.py:simple_prompt
  - prompts.py:better_prompt
  - prompts.py:chain_of_thought_prompt
  
providers:
  - "anthropic:messages:claude-3-haiku-20240307"

tests: animal_legs_tests.csv
```

在執行這個評估之前，我們必須先解決一個問題：我們新的 `chain_of_thought_prompt` 會在輸出中回應 `<thinking>` 和 `<answer>` 標籤。要真正評估模型用這個提示詞的表現，我們需要擷取出模型放在 `<answer>` 標籤裡的數字答案，再拿它和預期的值比較。

promptfoo 讓我們可以定義自訂的「**轉換（transforms）**」，在做實際的比較邏輯之前，先處理一下模型的輸出。為此，我們會寫一個簡單的 Python 函式，從 `<answer>` 標籤中間擷取出答案。

建立一個叫做 `transform.py` 的新檔案，加入下面的程式碼：

```py
def get_transform(output, context):
    if "<thinking>" in output:
        try:
            return output.split("<answer>")[1].split("</answer>")[0].strip()
        except Exception as e:
            print(f"Error in get_transform: {e}")
            return output
    return output
```

這個叫做 `get_transform` 的函式，預期會收到一個模型的輸出（`context` 參數我們會在之後的課程介紹）。接著，我們可以在回傳之前，把模型的輸出轉換成任何我們想要的樣子。在這個例子中，我們做兩件事的其中一件：

- 如果輸出包含 `<thinking>` 標籤，我們就知道它是思維鏈提示詞的輸出。我們從 `<answer>` 標籤中間擷取出數字，把它當作新的輸出回傳。
- 否則就回傳原本的輸出（給其他沒有使用思維鏈的提示詞用）

> 🧩 **白話小補充：看懂 `output.split("<answer>")[1].split("</answer>")[0].strip()`**
> 假設 `output` 是 `"<thinking>...</thinking><answer>5</answer>"`：
> 1. `.split("<answer>")` 用 `<answer>` 切開 → `["<thinking>...</thinking>", "5</answer>"]`
> 2. `[1]` 取第二段 → `"5</answer>"`
> 3. `.split("</answer>")` 再用 `</answer>` 切開 → `["5", ""]`
> 4. `[0]` 取第一段 → `"5"`
> 5. `.strip()` 去掉前後空白 → `"5"`
>
> 如果找不到 `<answer>`，第 2 步的 `[1]` 會出錯，所以用 `try`/`except` 包起來，出錯就回傳原本的輸出。

最後一步是告訴 promptfoo 我們想使用這個轉換函式。把 `promptfooconfig.yaml` 檔案更新成這樣：

```yaml
description: "Animal Legs Eval"

prompts:
  - prompts.py:simple_prompt
  - prompts.py:better_prompt
  - prompts.py:chain_of_thought_prompt
  
providers:
  - "anthropic:messages:claude-3-haiku-20240307"

tests: animal_legs_tests.csv

defaultTest:
  options:
    transform: file://transform.py
```

最後那一段告訴 promptfoo：**在所有測試上**都套用 `transform.py` 裡的轉換函式。在預設情況下，promptfoo 會在 `transform.py` 檔案裡尋找一個叫做 `get_transform` 的函式。

（`defaultTest` = 「每個測試的預設設定」；`file://transform.py` = 「使用 `transform.py` 這個檔案」。）

現在，我們可以再用這個指令執行一次評估：

```bash
npx promptfoo@latest eval
```

我們會看到類似下面的輸出，現在有 4 欄了：

![三個提示詞的評估結果](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/three_prompt_eval.png)

我們可以再次用這個指令在瀏覽器裡查看結果：

```bash
npx promptfoo@latest view
```

我們會看到一個像這樣的網頁：

![三個提示詞的網頁儀表板](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/final_view.png)

我們可以清楚地看到，包含思維鏈的提示詞**答對了 100% 的問題**！

---

## 比較模型

promptfoo 一個很棒的功能，是可以很輕鬆地用不同的模型執行評估。我們做了一些提示詞工程，才讓一個提示詞在使用 Haiku 時拿到 100% 的分數，但我們來看看，如果決定換成一個能力更強的模型，例如 Claude 3.5 Sonnet，會發生什麼事。

我們只要更新 `promptfooconfig.yaml` 檔案，加入第二個供應商（符合有效的 Anthropic 供應商字串格式）就好。把 `promptfooconfig.yaml` 更新成包含兩個供應商：

```yaml
description: "Animal Legs Eval"

prompts:
  - prompts.py:simple_prompt
  - prompts.py:better_prompt
  - prompts.py:chain_of_thought_prompt
  
providers:
  - anthropic:messages:claude-3-haiku-20240307
  - anthropic:messages:claude-3-5-sonnet-20240620

tests: animal_legs_tests.csv

defaultTest:
  options:
    transform: file://transform.py
```

（新手版資料夾裡的設定檔就是這個最終版本，模型已換成 `claude-haiku-4-5` 和 `claude-sonnet-4-6`。）

然後，我們可以用和之前一樣的指令再執行一次評估：

```bash
npx promptfoo@latest eval
```

當我們查看網頁版儀表板時，會看到一些有趣的結果！

![兩個模型的評估結果](../../../prompt_evaluations/05_prompt_foo_code_graded_animals/images/multi_model_eval_view.png)

只在 YAML 檔案加了一行，我們就能在兩個模型上執行整套評估。前三個輸出欄是 Claude 3 Haiku 的輸出，最後三欄是 Claude 3.5 Sonnet 的輸出。看起來，Claude 3.5 Sonnet 就算用 `simple_prompt`（在 Claude 3 Haiku 上得到 0%）也能 100% 通過我們的評估。

這種資訊非常寶貴：不只是哪個提示詞表現最好，還有**對於特定任務，哪一種「模型 + 提示詞」組合表現最好**。

**附註：** 如果你好奇為什麼 Claude 3.5 Sonnet 在思維鏈提示詞上沒有拿到 100%，這裡是解釋！它在「The animal is an octopus.（這種動物是章魚。）」這一題答錯了。在它的 `<thinking>` 標籤裡，Claude 3.5 Sonnet 推理說：章魚其實沒有「腿」，它的附肢通常被稱為「**手臂（arms）**」，而從來不被稱為「腿（legs）」。**換成一個「更聰明」的模型，思維鏈提示詞的表現反而稍微變差了，因為模型「太聰明了」。** 如果我們想確保在所有模型上都有好的表現，可以修改提示詞，更具體地說明什麼才算是「腿」。

這一課只是我們第一次接觸 promptfoo。在接下來的課程中，我們會學習怎麼處理更複雜的程式評分邏輯、定義我們自己的自訂評分器，以及執行模型評分的評估。

---

## 📌 重點整理

- **promptfoo** 是開源的評估工具：用 `npx promptfoo@latest eval` 執行評估，`npx promptfoo@latest view` 打開網頁儀表板。（需要先安裝 Node.js，並設定 `ANTHROPIC_API_KEY`。）
- `promptfooconfig.yaml` 的三大區塊：
  | 區塊 | 作用 | 這一課的寫法 |
  |---|---|---|
  | `providers` | 用哪些模型 | `anthropic:messages:模型名稱`，可以列好幾個來比較 |
  | `prompts` | 評估哪些提示詞 | `prompts.py:函式名稱` |
  | `tests` | 測試資料 | CSV 檔；`__expected` 欄放預期答案（完全比對） |
- `defaultTest.options.transform: file://transform.py`：評分前先用 `get_transform()` 處理輸出（例如擷取 `<answer>`）。
- 加一行 provider 就能比較不同模型；更聰明的模型不一定在每個提示詞上都更好（章魚的「腿」vs.「手臂」）。

👉 下一課：[4-6 用 promptfoo 寫分類評估](../06_prompt_foo_code_graded_classification/lesson.md)
