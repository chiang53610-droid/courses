<!--meta {"orig": "prompt_evaluations/03_code_graded_evals/03_code_graded.ipynb", "out": "04_prompt_evaluations/03_code_graded"} -->
# 4-3 一個簡單的程式評分評估

> 📚 **第 4 單元：提示詞評估**｜第 3 課 / 共 9 課
> ⏱️ 預估時間：40 分鐘

## 🎯 這一課你會學到

- 用 Python 寫一個完整的**程式評分評估**：資料集 → 提示詞 → 收集輸出 → 評分 → 算出正確率
- 用評估分數**證明**提示詞的修改真的有效：66.7% → 75% → 100%
- 用正規表達式從 `<answer>` 標籤裡擷取答案再評分

> 🔄 **2026 更新**：原課程的 `MODEL_NAME = "claude-3-haiku-20240307"` 已換成 `"claude-haiku-4-5"`。新模型比較聰明，你跑出來的第一版分數可能就比 66.7% 高，這很正常——重點是學會「怎麼用分數來比較提示詞」的流程。

---

在這一課，我們先看一個非常簡單的程式評分評估範例，下一課再介紹比較貼近真實的提示詞。我們會依照這張圖描述的流程進行：

![以評估為核心的提示詞開發流程](@root/prompt_evaluations/images/process.png)

大致的步驟是：
1. 先定義我們的**評估測試集**
2. 寫出提示詞的第一次嘗試
3. 用評估流程執行它，**得到一個分數**
4. 根據評估結果**修改提示詞**
5. 用評估流程執行修改後的提示詞，希望得到更好的分數！

我們來試試照著這個流程走！

---

## 我們的輸入資料

我們要評分的評估，是請 Claude 正確判斷**一種動物有幾條腿**。在之後的課程中，我們會看到更複雜、更貼近真實的提示詞和評估，但這裡我們刻意保持簡單，專注在評估的流程本身。

第一步是寫出評估資料集，包含輸入和對應的標準答案。我們用這個簡單的「字典串列」，每個字典都有 `animal_statement`（動物描述）和 `golden_answer`（標準答案）兩個 key：

{{cell 2}}

**資料集翻譯：**
| # | 動物描述 | 標準答案 |
|---|---|---|
| 1 | 這種動物是人類。 | 2 |
| 2 | 這種動物是蛇。 | 0 |
| 3 | 這隻狐狸失去了一條腿，但後來神奇地長回了失去的那條腿，而且還多長了一條神祕的腿。 | 5 |
| 4 | 這種動物是狗。 | 4 |
| 5 | 這種動物是多了兩條腿的貓。 | 6 |
| 6 | 這種動物是大象。 | 4 |
| 7 | 這種動物是鳥。 | 2 |
| 8 | 這種動物是魚。 | 0 |
| 9 | 這種動物是多了兩條腿的蜘蛛 | 10 |
| 10 | 這種動物是章魚。 | 8 |
| 11 | 這種動物是一隻失去兩條腿、然後又長回三條腿的章魚。 | 9 |
| 12 | 這種動物是一隻有兩個頭、八條腿的神話生物。 | 8 |

注意，有些評估問題有點**刁鑽**，例如這一題：
> The fox lost a leg, but then magically grew back the leg he lost and a mysterious extra leg on top of that.
>（這隻狐狸失去了一條腿，但後來神奇地長回了失去的那條腿，而且還多長了一條神祕的腿。→ 4 - 1 + 1 + 1 = 5）

這一點等一下會很重要！

---

## 我們的初始提示詞

接著，我們定義初始的提示詞。下面的函式接收一則動物描述，回傳一個格式正確、包含我們第一次嘗試的提示詞的訊息串列：

{{cell 5}}

**提示詞翻譯**：「你會收到一則關於某種動物的描述，你的工作是判斷那種動物有幾條腿。這是動物描述：`<animal_statement>{animal_statement}</animal_statement>`。這種動物有幾條腿？請用一個數字回答。」

我們用 `eval_data` 資料集的第一筆快速測試一下：

{{cell 7}}

（`eval_data[0]['animal_statement']`：取出資料集第一筆（`[0]`）裡的 `'animal_statement'` 值，也就是「The animal is a human.」。）

接著，我們寫一個簡單的函式：接收一個訊息串列，把它送到 Anthropic API：

{{cell 9}}

我們用 `eval_data` 串列的第一筆來測試，它包含下面這則動物描述：
```
'The animal is a human.'
```

{{cell 11}}

我們得到 `2` 這個回答，用眼睛看是通過的！人類一般有兩條腿。下一步是用 `eval_data` 集合裡全部 12 筆資料，建立並執行一個完整的評估。

---

## 撰寫評估邏輯

我們先把 `eval_data` 串列裡的每一筆輸入和提示詞範本組合起來，把組合好的「完整」提示詞送給模型，並收集我們拿回來的所有輸出：

{{cell 14}}

> 🧩 **白話小補充：看懂這一行**
> ```python
> outputs = [get_completion(build_input_prompt(question['animal_statement'])) for question in eval_data]
> ```
> 這是「串列生成式」（[0-4 第 16-2 節](../00_before_you_start/04_python_crash_course.md#16-2-串列生成式list-comprehension)），從右往左讀：
> 1. `for question in eval_data`：對資料集裡的每一筆資料（取名叫 `question`）
> 2. `question['animal_statement']`：取出動物描述
> 3. `build_input_prompt(...)`：組成提示詞
> 4. `get_completion(...)`：問 Claude
> 5. 把 12 個答案收集成一個串列 `outputs`

我們快速看一下拿回了什麼：

{{cell 16}}

我們已經可以看出提示詞需要改善了，因為有些答案**不是單純的數字**！我們把結果和對應的標準答案並排，仔細看看：

{{cell 18}}

（`zip(outputs, eval_data)` 把「第 1 個輸出和第 1 筆資料」、「第 2 個輸出和第 2 筆資料」⋯⋯一對一配對起來。）

這個資料集夠小，我們可以很容易地瀏覽結果、找出有問題的回答，但我們還是**有系統地**替結果評分吧：

{{cell 20}}

**逐行解說：**
- `grade_completion(output, golden_answer)`：評分函式，**完全相同**（`==`）才算對。這叫做「完全比對（exact match）」評分。
- `grades = [...]`：對每一組（輸出, 資料）評分，得到一串 `True`/`False`。
- `sum(grades)/len(grades)*100`：`True` 的數量 ÷ 總數 × 100 = 正確率（%）。

我們有了一個**基準分數**！在這個例子中，我們的初始提示詞得到了 **66.6%** 的正確率。瀏覽上面的結果之後，目前的輸出看起來有兩個明顯的問題：

### 問題 1：輸出格式的問題

我們的目標是寫出一個能產生**數字輸出**的提示詞。有些輸出不是數字：

```
Animal Statement: The animal is a bird.
Golden Answer: 2
Output: Based on the provided animal statement, "The animal is a bird.", the animal has 2 legs.
```

（輸出是「根據提供的動物描述『這種動物是鳥』，這種動物有 2 條腿。」——答案其實對，但因為不是只有「2」，完全比對就判錯了。）

我們可以透過提示詞來修正這個問題！

### 問題 2：答案錯誤

（原課程這裡的標題寫成「Problem 1」，應該是「Problem 2」。）

另外，有些答案完全錯了：

```
Animal Statement: The animal is an octopus that lost two legs and then regrew three legs.
Golden Answer: 9
Output: 5
```

和

```
Animal Statement: The animal is a spider with two extra legs
Golden Answer: 10
Output: 8
```

這些輸入有點「刁鑽」，似乎讓模型遇到了一些困難。我們也會試著透過提示詞修正這個問題！

---

## 第二次嘗試

我們的初始提示詞已經有了某種程度的基準表現，現在來試著改善提示詞，看看評估分數會不會提升。我們先處理「模型有時候會輸出額外的文字，而不是只回答一個數字」的問題。這是第二個產生提示詞的函式：

{{cell 23}}

提示詞的關鍵新增，是這一行：

> Respond only with a numeric digit, like 2 or 6, and nothing else.
>（只用一個數字回答，例如 2 或 6，其他什麼都不要。）

我們用這個新的提示詞測試每一筆輸入：

{{cell 26}}

快速看一下輸出：

{{cell 28}}

我們現在得到的**全部都是數字**輸出了！我們仔細看看結果：

{{cell 30}}

實際的數字答案還是有明顯的問題，例如這一題：

```
Animal Statement: The animal is a spider with two extra legs
Golden Answer: 10
Output: 8
```

在處理這個問題之前，我們先拿到一個正式的分數，看看表現（希望）提升了多少：

{{cell 32}}

我們的分數提升了一點（**75%**）！**注意：這個資料集很小，所以這些結果參考就好。**

---

## 第三次嘗試

接下來，我們來處理錯誤輸出中的**邏輯問題**，例如：

```
Animal Statement: The fox lost a leg, but then magically grew back the leg he lost and a mysterious extra leg on top of that.
Golden Answer: 5
Output: 6
```

我們可以在這裡運用的一個技巧是**思維鏈提示**：給 Claude 具體的指示，請它在最終產生答案之前，先推理出它的回答。**現在我們已經有評估了，就可以測試思維鏈提示到底有沒有幫助！**

我們來寫一個新的提示詞，請模型在 `<thinking>` 標籤裡「把想法說出來」。這會讓我們的程式邏輯稍微複雜一點，因為我們需要一個方便的方法來擷取模型的最終答案。我們會指示模型也把最終答案放在 `<answer>` 標籤裡，這樣我們就能輕鬆擷取出「最終」的數字答案：

{{cell 35}}

**新增的指示翻譯**：「一開始先推理這種動物有幾條腿，在 `<thinking>` 標籤裡一步一步思考。然後，把你的最終答案放在 `<answer>` 標籤裡。在 `<answer>` 標籤裡只回傳腿的數量（整數），其他什麼都不要。」

我們用這個新版本的提示詞收集輸出：

{{cell 37}}

我們來看看一些輸出：

{{cell 39}}

這是我們得到的回答類型的一個例子：

```
Animal Statement: The fox lost a leg, but then magically grew back the leg he lost and a mysterious extra leg on top of that.
Golden Answer: 5
Output: Here is my step-by-step reasoning:
<thinking>
1. The initial statement says the fox lost a leg.
2. But then the fox "magically grew back the leg he lost and a mysterious extra leg on top of that."
3. This means the fox originally had 4 legs, lost 1 leg, and then grew back the lost leg plus an extra leg, for a total of 5 legs.
</thinking>
<answer>5</answer>
```

（`<thinking>` 的翻譯：「1. 一開始的描述說狐狸失去了一條腿。2. 但後來狐狸『神奇地長回了失去的那條腿，而且還多長了一條神祕的腿』。3. 這代表狐狸原本有 4 條腿，失去 1 條，然後長回失去的那條再加上一條額外的腿，總共 5 條腿。」）

至少在這個例子中，邏輯看起來改善了。現在我們需要專注在讓這個提示詞「**可以被評分**」。在評分之前，我們需要擷取出 `answer` 標籤中間的數字。

這是一個擷取兩個 `<answer>` 標籤中間文字的函式：

{{cell 41}}

**逐行解說：**
- `pattern = r'<answer>(.*?)</answer>'`：正規表達式，找出 `<answer>` 和 `</answer>` 中間的內容（括號圈起來的部分）。
- `re.search(pattern, text)`：在文字裡搜尋。
- 找到就回傳 `.group(1)`（括號裡的內容），找不到就回傳 `None`。

接著，我們從最新一批的輸出中擷取答案：

{{cells 43-44}}

接著，我們拿到分數，看看在提示詞裡加入思維鏈有沒有帶來差別！

{{cell 46}}

我們把分數提升到了 **100%**！

我們的評估讓我們有信心：對提示詞做的修改，確實帶來了更好的輸出。這是一個使用「完全比對」評分的簡單例子，下一課我們會看一個稍微複雜一點的例子。

---

## 📌 重點整理

- 程式評分評估的基本架構：
  1. **資料集**：`eval_data = [{"輸入": ..., "golden_answer": ...}, ...]`
  2. **提示詞函式**：`build_input_prompt(輸入)` → 訊息串列
  3. **收集輸出**：`outputs = [get_completion(...) for ... in eval_data]`
  4. **評分函式**：`grade_completion(output, golden_answer)`（這裡是完全比對 `==`）
  5. **算分數**：`sum(grades) / len(grades) * 100`
- 有了分數，就能**客觀比較**提示詞：
  - v1（請用數字回答）：66.7%
  - v2（只用一個數字回答，其他什麼都不要）：75%
  - v3（先在 `<thinking>` 推理，答案放在 `<answer>`）：100%
- 使用思維鏈時，用正規表達式**擷取 `<answer>` 裡的答案**再評分。
- 資料集很小時，分數僅供參考；正式評估建議至少 100 筆。

👉 下一課：[4-4 寫一個分類評估](04_code_graded_classification_evals.md)
