<!--meta {"orig": "prompt_evaluations/02_workbench_evals/02_workbench_evals.ipynb", "out": "04_prompt_evaluations/02_workbench_evals"} -->
# 4-2 用 Anthropic Workbench 做評估（人工評分）

> 📚 **第 4 單元：提示詞評估**｜第 2 課 / 共 9 課
> ⏱️ 預估時間：30 分鐘（這一課是在網頁上操作，沒有程式碼）

## 🎯 這一課你會學到

- 認識 Anthropic 的 **Workbench（工作台）**：一個在網頁上試寫提示詞的工具
- 在 Workbench 裡用**變數**、**加入多個測試案例**、**人工打分數**
- 修改提示詞後重新評估，並**並排比較**兩個版本

> 🔄 **2026 更新**：Anthropic Console（主控台）的網址和介面可能已經改版，按鈕的位置、名稱或外觀可能和下面的截圖不同，但「寫提示詞 → 填變數 → 多個測試案例 → 打分數 → 比較版本」的流程概念是一樣的。

---

這一課會示範怎麼用 **Anthropic Workbench** 執行你自己的**人工評分**評估。它是一個非常容易使用、視覺化的介面，可以快速製作提示詞原型並執行人工評分的評估。雖然我們一般建議正式上線的評估採用更能大規模進行的方法，但在轉向更嚴謹的程式評分或模型評分評估之前，Anthropic Workbench 是開始做人工評分評估的好地方。

在這一課，我們會看到怎麼用 Workbench 測試提示詞、執行簡單的評估，以及比較不同版本的提示詞。

---

## Anthropic Workbench

[Anthropic 的 Workbench](https://console.anthropic.com/workbench/) 是快速製作提示詞原型、執行人工評分評估的好地方。這是第一次打開 Workbench 時的樣子：

![空白的 Workbench](@root/prompt_evaluations/images/empty_workbench.png)

我們可以在左邊輸入提示詞。想像我們正在開發一個「**程式碼翻譯**」應用程式，想寫出最好的提示詞，用 Anthropic API 把任何程式語言的程式碼翻譯成 Python。這是提示詞的第一次嘗試：

```
You are a skilled programmer tasked with translating code from one programming language to Python. Your goal is to produce an accurate and idiomatic Python translation of the provided source code.

Here is the source code to translate:

<source_code>
{{SOURCE_CODE}}
</source_code>

The source code is written in the following language:

<source_language>
{{SOURCE_LANGUAGE}}
</source_language>

Please translate this code to Python
```

**翻譯**：「你是一位技術純熟的程式設計師，任務是把程式碼從一種程式語言翻譯成 Python。你的目標是為提供的原始程式碼，產生準確而且道地（符合 Python 慣用寫法）的 Python 翻譯。
這是要翻譯的原始程式碼：`<source_code>{{SOURCE_CODE}}</source_code>`
原始程式碼是用下面這種語言寫的：`<source_language>{{SOURCE_LANGUAGE}}</source_language>`
請把這段程式碼翻譯成 Python」

注意 `{{SOURCE_CODE}}`（原始程式碼）和 `{{SOURCE_LANGUAGE}}`（原始語言）這兩個**變數**，我們之後會把它們換成動態的值。

> 🧩 **白話小補充**：在 Workbench 裡，變數是用**兩層大括號** `{{變數名稱}}` 來表示的。這和第 2 單元在 Python 裡用 f-string 的 `{變數}` 是同樣的概念：先寫好範本，再填入不同的資料。

我們可以把這個提示詞貼到 Workbench 的左邊：

![貼上提示詞的 Workbench](@root/prompt_evaluations/images/workbench_with_prompt.png)

接著，點擊**變數按鈕**（`{ }`），為變數設定測試值：

![變數按鈕](@root/prompt_evaluations/images/variables_button.png)

這會打開一個對話框，請我們輸入 `{{SOURCE_CODE}}` 和 `{{SOURCE_LANGUAGE}}` 變數的值：

![輸入變數值的對話框](@root/prompt_evaluations/images/adding_variables.png)

接著，按下執行（Run），就能看到模型產生的輸出：

![第一次執行的輸出](@root/prompt_evaluations/images/first_output.png)

---

## Workbench 評估

一次用一組變數測試提示詞是個好的開始，但 Workbench 還**內建了一個評估工具**，幫助我們用多個輸入執行提示詞。要切換到評估畫面，點擊上方的「**Evaluate（評估）**」切換按鈕：

![Evaluate 按鈕](@root/prompt_evaluations/images/evaluate_button.png)

這會打開評估畫面，裡面已經預先填好了我們一開始的結果：

![評估畫面](@root/prompt_evaluations/images/evaluate1.png)

接著，我們可以按「**Add Row（新增一列）**」按鈕，加入一些新的測試案例。我們加入兩個新的測試案例：一段 Ruby 程式碼和一段 C# 程式碼：

![新增兩個測試案例](@root/prompt_evaluations/images/evaluate2.png)

接著，我們可以按每個測試案例旁邊個別的「Run（執行）」按鈕，或是按橘色的「**Run Remaining（執行剩下的）**」按鈕，一次執行所有還沒執行的測試案例：

![Run Remaining 按鈕](@root/prompt_evaluations/images/run_remaining.png)

我們按下 Run Remaining 按鈕，看看模型的回答。這是我們得到的結果：

![三個測試案例的結果](@root/prompt_evaluations/images/evaluate3.png)

---

## 人工評分

現在是時候仔細看看模型的輸出，並給它們打分數了。在最右邊那一欄，我們可以為每個輸出打一個分數：

![打分數的欄位](@root/prompt_evaluations/images/score.png)

我們來仔細看看其中幾個輸出。

### JavaScript 測試案例的結果

這是 JavaScript 翻譯測試案例的結果：

```
Here's the Python translation of the provided JavaScript code:

chicken_count = 99


In Python:
1. We don't use the `const` keyword to declare constants. By convention, constants in Python are typically written in all uppercase, but this isn't enforced by the language.
2. We don't need to use any keyword (like `let` or `var` in JavaScript) to declare variables.
3. The variable name uses snake_case, which is already consistent with Python naming conventions.

If you want to emphasize that this is intended to be a constant (i.e., a value that shouldn't be changed), you could use the all-uppercase convention:


CHICKEN_COUNT = 99


Both versions are valid Python code, with the uppercase version signaling to other developers that this value is intended to be constant.
```

（翻譯大意：「這是提供的 JavaScript 程式碼的 Python 翻譯：`chicken_count = 99`。在 Python 中：1. 我們不用 `const` 關鍵字宣告常數，依照慣例常數通常全部大寫，但語言本身不強制。2. 宣告變數不需要任何關鍵字（像 JavaScript 的 `let` 或 `var`）。3. 變數名稱使用 snake_case（小寫加底線），已經符合 Python 的命名慣例。如果你想強調這是一個常數（不應該被改變的值），可以用全部大寫的慣例：`CHICKEN_COUNT = 99`。兩個版本都是有效的 Python 程式碼，大寫版本是在向其他開發者表示這個值是常數。」——**一行程式碼，配了一大段解釋**。）

### Ruby 測試案例的結果

這是 Ruby 翻譯測試案例的結果：

```
Certainly! Here's the Python translation of the provided Ruby code:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1

    def introduce(self):
        print(f"Hello, I'm {self.name} and I'm {self.age} years old.")

    @classmethod
    def create_family(cls, members):
        return [cls(name, age) for name, age in members]

# Create a family
family = Person.create_family([
    ["Alice", 35],
    ["Bob", 40],
    ["Charlie", 12]
])

# Introduce family members
for person in family:
    person.introduce()

# Celebrate Charlie's birthday
charlie = next(person for person in family if person.name == "Charlie")
charlie.birthday()
charlie.introduce()


Here are the key changes and explanations:

1. In Python, we don't need to explicitly declare attribute readers. The attributes are accessible by default.

2. The `initialize` method in Ruby becomes `__init__` in Python.

3. The `birthday!` method is renamed to `birthday` in Python, as the exclamation mark is not typically used in Python method names.

4. The `self.` prefix is used explicitly in Python method definitions and when accessing instance attributes.

5. String interpolation uses f-strings in Python (e.g., `f"Hello, I'm {self.name}"`).

6. The `create_family` class method is defined using the `@classmethod` decorator in Python.

7. List comprehension is used instead of `map` for creating the family members.

8. The `each` method with `&:introduce` is replaced by a simple `for` loop in Python.

9. The `find` method is replaced with `next()` and a generator expression to find Charlie.

This Python code maintains the functionality of the original Ruby code while adhering to Python's syntax and conventions.
```

（翻譯大意：開頭「當然！這是提供的 Ruby 程式碼的 Python 翻譯：」→ 一段定義 `Person` 類別、建立家庭成員、自我介紹、幫 Charlie 過生日的 Python 程式碼 → 後面又列了 9 點「主要修改和說明」（例如 Ruby 的 `initialize` 在 Python 變成 `__init__`、驚嘆號通常不用在 Python 方法名稱裡、用 f-string 做字串插值、用 `@classmethod` 裝飾器⋯⋯）→ 最後一句總結。）

### 替提示詞打分數

目前所有的輸出在翻譯程式碼上都做得還不錯，但有幾個關鍵問題：

* 我們不需要「Certainly! Here's the Python translation of the provided Ruby code.（當然！這是提供的 Ruby 程式碼的 Python 翻譯。）」這種**煩人的開場白**。它們只是在浪費輸出 token！
* 目前的格式**很難用程式解析**。我們要怎麼寫程式，把翻譯好的 Python 程式碼單獨擷取出來？
* 我們不需要輸出最後那一長串**解釋**。在我們的使用情境中，我們只要翻譯好的程式碼。

我們來替這些輸出打分數。我們給每個輸出都打 **3 分（滿分 5 分）**。

---

## 更新提示詞

下一步是修改提示詞，然後再執行一次評估！我們來更新提示詞，反映前面找到的問題。

```
You are a skilled programmer tasked with translating code from one programming language to Python. Your goal is to produce an accurate and idiomatic Python translation of the provided source code.

Here is the source code to translate:

<source_code>
{{SOURCE_CODE}}
</source_code>

The source code is written in the following language:

<source_language>
{{SOURCE_LANGUAGE}}
</source_language>

Please translate this code to Python.
Format your response as follows:

<python_code>
Your Python translation here
</python_code>

Only output the <python_code> tags without any other text content
```

**新增的部分翻譯**：「請把你的回答排成下面這樣的格式：`<python_code>` 你的 Python 翻譯放在這裡 `</python_code>`。**只輸出 `<python_code>` 標籤，不要有任何其他文字內容。**」

如果我們切換回「Prompt（提示詞）」畫面，就能在介面上更新提示詞：

![更新後的提示詞](@root/prompt_evaluations/images/updated_prompt.png)

綠色標示的文字就是我們新增到提示詞裡的內容。

接著，按橘色的「Run」按鈕測試新的提示詞。這是新的結果：

![新提示詞的回答](@root/prompt_evaluations/images/updated_response.png)

這正是我們想要的！回答裡沒有開場白，也沒有長長的程式碼解釋。

---

## 重新執行評估

接著，切換回評估畫面：

![第二版提示詞的評估畫面](@root/prompt_evaluations/images/evaluate4.png)

注意左上角顯示「**v2**」，表示這是提示詞的第二個版本。我們按「Run Remaining」，看看其他測試案例的輸出：

![第二版的所有結果](@root/prompt_evaluations/images/evaluate5.png)

新的輸出看起來很棒！它們全都跳過了開場白和解釋文字，只包含裝著翻譯好的 Python 程式碼的 `<python_code>` 標籤。我們把它們全部標記為 **5/5 分**！

![全部打 5 分](@root/prompt_evaluations/images/evaluate6.png)

---

## 比較結果

我們已經試過兩個不同的提示詞了，現在可以把結果並排比較。點擊右上角的「**+ Add Comparison（新增比較）**」按鈕，選擇提示詞的前一個版本（v1），和 v2 的結果做比較。這會把兩個提示詞的模型輸出和人工評分並排顯示：

![v1 和 v2 並排比較](@root/prompt_evaluations/images/comparison.png)

很明顯，我們可以看到 v2 提示詞在我們的特定使用情境中效果好很多！

Workbench 和它的評估工具，是快速製作提示詞原型、並排比較結果的好地方。在轉向更穩健的解決方案之前，它是開始評估之旅的理想環境。在接下來的課程中，我們會看到怎麼自動化更大規模的程式評分和模型評分評估。

---

## 📌 重點整理

- **Workbench** 是 Anthropic Console 上的網頁工具，不用寫程式就能試提示詞。
- 用 `{{變數}}` 寫提示詞範本 → 用 `{ }` 按鈕填變數 → 切到 **Evaluate** 畫面 → **Add Row** 加測試案例 → **Run Remaining** 一次執行 → 在右欄**人工打分數**。
- 修改提示詞後，版本會自動變成 v2；用 **+ Add Comparison** 並排比較新舊版本。
- 這一課的提示詞改進：要求「只輸出 `<python_code>` 標籤」，去掉開場白和解釋 → 分數從 3/5 提升到 5/5。
- Workbench 適合**起步**；大規模的評估需要用程式自動化（下一課開始）。

👉 下一課：[4-3 寫簡單的程式評分評估](03_code_graded.md)
