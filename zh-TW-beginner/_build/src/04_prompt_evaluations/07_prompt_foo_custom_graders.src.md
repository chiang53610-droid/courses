<!--meta {"orig": "prompt_evaluations/07_prompt_foo_custom_graders/lesson.ipynb", "out": "04_prompt_evaluations/07_prompt_foo_custom_graders/lesson"} -->
# 4-7 promptfoo：自訂程式評分器

> 📚 **第 4 單元：提示詞評估**｜第 7 課 / 共 9 課
> ⏱️ 預估時間：30 分鐘

## 🎯 這一課你會學到

- 把提示詞**直接寫在 YAML 檔裡**，用 `{{變數}}` 當佔位符
- 把測試案例**直接寫在 YAML 檔裡**（`tests:` + `vars:`）
- 用 Python 寫**自訂評分器** `get_assert(output, context)`，回傳「通過與否、分數、原因」

> 📁 **這一課的檔案已經準備好了**：和這份講義同一個資料夾裡有 `promptfooconfig.yaml` 和 `count.py`，模型已換成 `claude-haiku-4-5` 和 `claude-sonnet-4-6`。`cd` 到這個資料夾、設定好 `ANTHROPIC_API_KEY`，執行 `npx promptfoo@latest eval` 即可。
>
> 🔄 **2026 更新**：講義中的 YAML 範例保留原課程的舊模型名稱，實際執行請用資料夾裡已更新的檔案。截圖是原課程的結果。

---

**注意：這一課所在的資料夾裡有相關的程式碼檔案。如果你想跟著執行評估，請下載整個資料夾。**

到目前為止，我們已經看過怎麼使用 promptfoo 的一些內建評分器，例如 `exact-match`（完全比對）和 `contains-all`（全部包含）。這些功能通常很有用，但 promptfoo 也讓我們能**為更特定的評分任務撰寫自訂的評分邏輯**。

為了示範這一點，我們會使用一個非常簡單的提示詞範本：

> Write a short paragraph about {{topic}}. Make sure you mention {{topic}} exactly {{count}} times, no more or fewer.
>（寫一段關於 {{topic}} 的短文。確保你剛好提到 {{topic}} {{count}} 次，不多也不少。）

我們會在 `{{topic}}`（主題）和 `{{count}}`（次數）填入像 `"tweezers"`（鑷子）和 `7` 這樣的值，得到像這樣的提示詞：

> Write a short paragraph about tweezers. Make sure you mention tweezers exactly 7 times, no more or fewer.
>（寫一段關於鑷子的短文。確保你剛好提到鑷子 7 次，不多也不少。）

為了替這個輸出評分，我們需要寫一些自訂的邏輯，確認模型的輸出剛好提到「tweezers」7 次。

對於這個提示詞：

> Write a short paragraph about sheep. Make sure you mention sheep exactly 3 times, no more or fewer.
>（寫一段關於羊的短文。確保你剛好提到羊 3 次，不多也不少。）

我們需要寫評分邏輯，確保「sheep」這個字在模型的輸出中剛好出現 3 次。

> 🧩 **白話小補充**：內建的斷言（例如 `contains`）只能檢查「有沒有」，沒辦法檢查「剛好出現幾次」。遇到這種特殊需求，就需要**自己寫評分程式**。

---

## 初始化 promptfoo

一如往常，第一步是用這個指令初始化 promptfoo：

```bash
npx promptfoo@latest init
```

就像之前看到的，這會建立一個 `promptfooconfig.yaml` 檔案。我們可以把裡面原本的內容刪掉。

接著，我們設定供應商。把下面的內容加到 `promptfooconfig.yaml`：

```yaml
description: Count mentions

providers:
  - anthropic:messages:claude-3-haiku-20240307
  - anthropic:messages:claude-3-5-sonnet-20240620
```

這告訴 promptfoo：我們想同時用 Claude 3 Haiku 和 Claude 3.5 Sonnet 來執行評估。我們要比較它們在這個特定任務上表現得怎麼樣！

請確認你已經設定好 `ANTHROPIC_API_KEY` 環境變數。你可以在終端機執行這個指令來設定環境變數：

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

---

## 準備我們的提示詞

到目前為止，我們看到可以把提示詞寫成 Python 檔案裡的函式。這是我們推薦的做法，但 promptfoo 也提供好幾種其他指定提示詞的選擇。**最簡單的選擇，是把提示詞以文字的形式直接寫在 YAML 檔案裡。**

我們來試試這種「行內」的寫法。更新 `promptfooconfig.yaml` 檔案，加入下面的內容：

```yaml
description: Count mentions
prompts:
  - >-
    Write a short paragraph about {{topic}}. Make sure you mention {{topic}} exactly {{count}} times, no more or fewer. Only use lower case letters in your output.
providers:
  - anthropic:messages:claude-3-haiku-20240307
  - anthropic:messages:claude-3-5-sonnet-20240620
```

注意 `prompts` 欄位，它直接在 YAML 檔案裡包含了我們的文字提示詞。（最後多了一句「Only use lower case letters in your output.（輸出只能使用小寫字母。）」，方便等一下計算次數。）注意 `{{topic}}` 和 `{{count}}` 這兩個變數，它們使用**兩層大括號**。這些提示詞使用的是 **Nunjucks 範本語法**，等一下會很重要！

> 🧩 **白話小補充**：
> - YAML 裡的 `>-` 代表「下面縮排的多行文字，合併成一段文字」，適合寫很長的提示詞。
> - **Nunjucks** 是一種範本語言，`{{變數}}` 會被替換成實際的值。這和 Python 的 f-string `{變數}` 概念一樣，只是寫法是兩層大括號。

---

## 撰寫測試案例

在之前的課程中，我們把測試案例和評分邏輯寫在 CSV 檔案裡。就像之前討論過的，promptfoo 非常有彈性，提供多種指定測試的方式。

我們可以把測試案例**直接寫在 YAML 設定檔裡**。把 `promptfooconfig.yaml` 檔案更新成這樣：

```yaml
description: Count mentions
prompts:
  - >-
    Write a short paragraph about {{topic}}. Make sure you mention {{topic}} exactly {{count}} times, no more or fewer. Only use lower case letters in your output.
providers:
  - anthropic:messages:claude-3-haiku-20240307
  - anthropic:messages:claude-3-5-sonnet-20240620
tests:
  - vars:
      topic: sheep
      count: 3
  - vars:
      topic: fowl
      count: 2
  - vars:
      topic: gallows
      count: 4
  - vars:
      topic: tweezers
      count: 7
  - vars:
      topic: jeans
      count: 6
```

在最下面，我們定義了 5 個測試案例，每個都有自己的 `topic` 和 `count` 值（羊 3 次、家禽 2 次、絞刑台 4 次、鑷子 7 次、牛仔褲 6 次）。promptfoo 會自動執行每個測試，替換提示詞範本裡的 `{{topic}}` 和 `{{count}}`。

> 🧩 **白話小補充**：`tests:` 底下每個 `- vars:` 就是一個測試案例；`vars`（variables，變數）裡寫的就是要填進提示詞的值。

我們還沒有任何評分邏輯，但我們仍然可以執行評估，確認變數有正確地被加進去。

要執行評估，我們用之前看過的同一個指令：

```bash
npx promptfoo@latest eval
```

這是我們得到的輸出：

![還沒有評分邏輯時的評估結果](@orig/images/initial_eval_output.png)

如果我們放大其中一列，可以看到模型的輸出大致上看起來不錯。在這個例子中，`{{topic}}` 被設定成「sheep」，而對應的模型輸出都是關於羊的段落！

![其中一列（羊）的輸出](@orig/images/single_row.png)

現在我們只需要實作自訂的評分邏輯，測試輸出提到主題的次數是否正確！

---

## 加入自訂的評分函式

promptfoo 讓我們可以定義自己的 **Python 評分函式**。在這個特定的例子中，我們想定義一個函式，確保模型的輸出提到特定主題的次數是正確的。我們先建立一個叫做 `count.py` 的新 Python 檔案。在這個檔案裡，加入下面這個函式：

```py
import re

def get_assert(output, context):
    topic = context["vars"]["topic"]
    goal_count = int(context["vars"]["count"])
    pattern = fr'(^|\s)\b{re.escape(topic)}\b'

    actual_count = len(re.findall(pattern, output.lower()))

    pass_result = goal_count == actual_count

    result = {
        "pass": pass_result,
        "score": 1 if pass_result else 0,
        "reason": f"Expected {topic} to appear {goal_count} times. Actual: {actual_count}",
    }
    return result
```

我們來談談上面這段程式碼在做什麼。promptfoo 會自動在我們的檔案裡尋找一個叫做 **`get_assert`** 的函式。它會傳給這個函式兩個參數：

- 某個模型的**輸出（output）**
- **`context`（情境）字典**，裡面包含產生這個輸出的變數和提示詞

promptfoo 預期我們的函式回傳下面其中一種：
- 一個布林值（bool，通過／失敗）
- 一個浮點數（float，分數）
- 一個 **GradingResult（評分結果）字典**

我們選擇回傳 GradingResult 字典，它必須包含下面這些屬性：

- `pass_`：布林值（通過與否）
- `score`：浮點數（分數）
- `reason`：一段文字說明（原因）

（原課程這裡寫成 `pass_`，但程式碼裡實際用的 key 是 `"pass"`，以程式碼為準。）

在上面的函式中，我們從 `context` 參數取出主題和次數，然後用正規表達式計算主題在輸出中出現的次數，最後回傳 `result`。

> 🧩 **逐行解說 `count.py`：**
> - `topic = context["vars"]["topic"]`：從 context 拿出這個測試案例的主題（例如 `"sheep"`）。
> - `goal_count = int(context["vars"]["count"])`：拿出要求的次數，轉成整數。
> - `pattern = fr'(^|\s)\b{re.escape(topic)}\b'`：建立正規表達式。
>   - 字串前面的 `fr` = `f`（可以塞變數）+ `r`（反斜線不特別處理）。
>   - `re.escape(topic)`：把主題裡可能有特殊意義的符號「跳脫」，當成普通文字。
>   - `\b`：「單字的邊界」，確保 `sheep` 不會被算到 `sheepdog` 裡。
>   - `(^|\s)`：前面是「開頭」或「空白」。
> - `re.findall(pattern, output.lower())`：找出所有符合的地方（先轉小寫），`len(...)` 算出有幾個。
> - `pass_result = goal_count == actual_count`：次數剛好相等才通過。
> - `"score": 1 if pass_result else 0`：通過得 1 分，否則 0 分（這是 Python 的「三元運算式」：`A if 條件 else B`）。
> - `"reason"`：「預期 {topic} 出現 {goal_count} 次。實際：{actual_count} 次」。

我們已經定義好評分器了，現在要告訴 promptfoo。更新 `promptfooconfig.yaml` 檔案：

```yaml
description: Count mentions
prompts:
  - >-
    Write a short paragraph about {{topic}}. Make sure you mention {{topic}} exactly {{count}} times, no more or fewer. Only use lower case letters in your output.
providers:
  - anthropic:messages:claude-3-haiku-20240307
  - anthropic:messages:claude-3-5-sonnet-20240620
defaultTest:
  assert:
    - type: python
      value: file://count.py
tests:
  - vars:
      topic: sheep
      count: 3
  - vars:
      topic: fowl
      count: 2
  - vars:
      topic: gallows
      count: 4
  - vars:
      topic: tweezers
      count: 7
  - vars:
      topic: jeans
      count: 6
```

`defaultTest` 告訴 promptfoo：對於它執行的每一個測試，我們都想使用 `count.py` 檔案裡定義的 Python 評分器。

（`assert:` 底下的 `type: python` 代表「用 Python 程式評分」，`value: file://count.py` 代表「程式在 `count.py` 這個檔案裡」。）

---

## 執行評估

要執行評估，我們用之前看過的同一個指令：

```bash
npx promptfoo@latest eval
```

這是我們執行評估後得到的輸出：

![加入自訂評分器後的評估結果](@orig/images/final_eval.png)

執行這個指令來啟動網頁介面：

```bash
npx promptfoo@latest view
```

![網頁儀表板](@orig/images/final_view.png)

我們可以看到，在這個任務上，Claude 3.5 Sonnet 拿到 **100%**，而 Claude 3 Haiku 只拿到 **20%**。要確認結果，可以點擊放大鏡圖示，查看完整的輸入提示詞和對應的輸出。

這是 Claude 3 Haiku 錯誤的輸出：

![Claude 3 Haiku 在「鑷子」題的錯誤輸出](@orig/images/tweezers_haiku_closeup.png)

這是 Claude 3.5 Sonnet 正確的輸出：

![Claude 3.5 Sonnet 在「鑷子」題的正確輸出](@orig/images/tweezers_sonnet_closeup.png)

這個特定的評估有點傻，但它的目的是示範**定義自訂 Python 評分邏輯**的流程。結合 promptfoo 內建的斷言和自訂的評分函式，我們幾乎可以寫出任何程式評分的評估。

在下一課，我們會學習 promptfoo 中的**模型評分**評估。

---

## 📌 重點整理

- 提示詞可以**直接寫在 YAML** 裡：`prompts: - >- 提示詞文字 {{變數}}`。
- 測試案例可以**直接寫在 YAML** 裡：`tests: - vars: {topic: sheep, count: 3}`。
- **自訂評分器**：在 Python 檔裡寫 `get_assert(output, context)`：
  - `output`：模型的輸出
  - `context["vars"]`：這個測試案例的變數
  - 回傳 `True/False`、分數，或 `{"pass": ..., "score": ..., "reason": ...}`
- 在設定檔用 `defaultTest: assert: - type: python, value: file://count.py` 套用到所有測試。
- 內建斷言 + 自訂評分器 = 幾乎可以寫出任何程式評分的評估。

👉 下一課：[4-8 用 promptfoo 做模型評分](../08_prompt_foo_model_graded/lesson.md)
