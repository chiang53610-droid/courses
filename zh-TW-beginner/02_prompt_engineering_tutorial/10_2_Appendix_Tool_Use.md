<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`10_2_Appendix_Tool_Use.ipynb`](10_2_Appendix_Tool_Use.ipynb)。

# 附錄 10.2：工具使用（Tool Use）

> 📚 **第 2 單元：提示詞工程互動教學**｜附錄 2 / 共 3 篇（超越標準提示詞）
> ⏱️ 預估時間：50 分鐘

- [課程](#課程)
- [練習](#練習)
- [範例遊樂場](#範例遊樂場)

## 🎯 這一章你會學到

- 「工具使用（tool use）」又叫「函式呼叫（function calling）」，其實就是**替換 + 串連提示詞**的組合
- Claude 並不會真的去執行工具，而是**說出它想呼叫哪個工具、用什麼參數**，由**你的程式**去執行，再把結果交回給 Claude
- 用「系統提示詞 + 控制邏輯」實作一個計算機工具

> 🔄 **2026 更新（重要）**：這篇附錄教的是**早期用 XML 標籤（`<function_calls>`）在提示詞裡實作工具使用**的方法。現在 Claude API 已經有**內建的工具使用功能**（用 `tools` 參數定義工具，Claude 會回傳 `tool_use` 內容區塊），更穩定、更好用——本套課程的<strong>第 5 單元「工具使用」</strong>會完整教那個新方法。
> 這篇附錄仍然很值得讀，因為它讓你看清楚工具使用「底層的原理」。程式碼裡原本用的 `claude-3-sonnet-20240229` 已換成 `claude-sonnet-4-6`。

## 準備工作

執行下面這個準備格，載入你的 API 金鑰，並建立 `get_completion` 輔助函式。

```python
%pip install "anthropic<1"

# Import python's built-in regular expression library
import re
import anthropic

# Retrieve the API_KEY variable from the IPython store
%store -r API_KEY

client = anthropic.Anthropic(api_key=API_KEY)

# Rewrittten to call Claude 3 Sonnet, which is generally better at tool use, and include stop_sequences
def get_completion(messages, system_prompt="", prefill="",stop_sequences=None):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        temperature=0.0,
        system=system_prompt,
        messages=messages,
        stop_sequences=stop_sequences
    )
    return message.content[0].text
```

**這一版的 `get_completion` 有什麼不同？**
- 程式碼的註解說：「改寫成呼叫 Claude 3 Sonnet（它通常比較擅長工具使用），並加入 `stop_sequences`」。新手版換成了 `claude-sonnet-4-6`。
- 注意這一版**沒有**讀取 `MODEL_NAME`，模型名稱直接寫在函式裡。
- 新增 `stop_sequences=None` 參數：預設不使用停止序列。

---

## 課程

工具使用（又叫函式呼叫）乍看之下觀念可能很複雜，但其實非常簡單！實作工具使用所需要的技能你**全都已經會了**，它其實就是「**替換**」和「**串連提示詞**」的組合。

在之前的替換練習中，我們是把**文字**替換進提示詞。在工具使用中，我們則是把**工具或函式的結果**替換進提示詞。Claude 沒辦法真的去呼叫或存取工具和函式。取而代之的是，我們讓 Claude：
1. 輸出它想呼叫的**工具名稱和參數**
2. 在工具被呼叫的期間，**停止**繼續產生回答
3. 然後我們把**工具的結果**附加上去，再次呼叫 Claude

> 🧩 **白話小補充：用「打電話叫外送」來比喻**
> Claude 就像一個坐在辦公室、不能出門的助理。它不能自己去買東西，但它可以**寫一張紙條**：「請幫我去 7-11 買一瓶水（工具名稱：買東西；參數：店家=7-11、商品=水）」。
> 你（程式）看到紙條，就跑去買回來，把水和收據（工具結果）交給它，它就能繼續完成工作。

函式呼叫很有用，因為它能**擴充 Claude 的能力**，讓 Claude 能處理更複雜、多步驟的任務。
你可以提供給 Claude 的函式例子：
- 計算機
- 字數計算器
- SQL 資料庫查詢和資料擷取
- 天氣 API

要讓 Claude 使用工具，需要結合下面兩個元素：

1. **一個系統提示詞**：向 Claude 解釋「工具使用」的概念，並詳細列出它可以使用的工具清單
2. **控制邏輯**：用來安排和執行 Claude 的工具使用請求（也就是你寫的程式）

### 工具使用的發展藍圖

*這一課教的是我們目前的工具使用格式。不過，我們在不久的將來會更新和改進工具使用的功能，包括：*
* *更精簡的函式定義和呼叫格式*
* *更穩健的錯誤處理，涵蓋更多邊緣情況*
* *和 API 其他部分更緊密的整合*
* *更好的可靠性和效能，特別是在比較複雜的工具使用任務上*

（🔄 這些改進後來都實現了，就是第 5 單元會教的內建工具使用功能。）

### 範例

要讓 Claude 能使用工具，我們從系統提示詞開始。在這個特別的工具使用系統提示詞裡，我們會告訴 Claude：
* 工具使用的基本前提，以及它包含哪些事
* Claude 可以怎麼呼叫和使用它被賦予的工具
* 在這個特定情境中，它可以使用的工具的詳細清單

下面是系統提示詞的第一部分，向 Claude 解釋工具使用。這部分的系統提示詞在所有「請 Claude 使用工具」的情況下都可以通用。我們給 Claude 的工具呼叫結構（`<function_calls> [...] </function_calls>`）是 Claude 受過專門訓練去使用的結構，所以建議你照著用。

```python
system_prompt_tools_general_explanation = """You have access to a set of functions you can use to answer the user's question. This includes access to a
sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external
resources, except by invoking the below functions.

You can invoke one or more functions by writing a "<function_calls>" block like the following as part of your
reply to the user:
<function_calls>
<invoke name="$FUNCTION_NAME">
<antml:parameter name="$PARAMETER_NAME">$PARAMETER_VALUE</parameter>
...
</invoke>
<nvoke name="$FUNCTION_NAME2">
...
</invoke>
</function_calls>

String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that
spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular
expressions.

The output and/or any errors will appear in a subsequent "<function_results>" block, and remain there as part of
your reply to the user.
You may then continue composing the rest of your reply to the user, respond to any errors, or make further function
calls as appropriate.
If a "<function_results>" does NOT appear after your function calls, then they are likely malformatted and not
recognized as a call."""
```

**這段系統提示詞的意思（翻譯）：**
> 你可以使用一組函式來回答使用者的問題，這包括使用一個沙盒（隔離的）運算環境。除了呼叫下面這些函式之外，你目前**沒有**能力檢查檔案或和外部資源互動。
>
> 你可以在回覆使用者時，寫一個像下面這樣的 `<function_calls>` 區塊，來呼叫一個或多個函式：（接著是格式範例：`<invoke name="函式名稱">` 裡面放 `<parameter name="參數名稱">參數值</parameter>`）
>
> 字串和單一數值的參數照原樣寫，串列和物件則用 JSON 格式。注意字串值裡的空白不會被刪掉。輸出不需要是有效的 XML，它會用正規表達式來解析。
>
> 輸出和／或任何錯誤會出現在接下來的 `<function_results>` 區塊裡，並保留在那裡，作為你回覆使用者的一部分。接著你可以繼續寫完給使用者的回覆、回應任何錯誤，或視情況再呼叫其他函式。
> 如果你的函式呼叫後面**沒有**出現 `<function_results>`，那它們很可能格式錯誤，沒有被辨識為呼叫。

（原文中的 `<nvoke name=...>` 少了一個 i，是原作者的筆誤，不影響效果。）

下面是系統提示詞的第二部分，定義 Claude 在這個特定情境中可以使用的工具。在這個例子中，我們要給 Claude 一個**計算機工具**，它需要三個參數：兩個運算元和一個運算子。

然後我們把系統提示詞的兩個部分組合起來。

```python
system_prompt_tools_specific_tools = """Here are the functions available in JSONSchema format:
<tools>
<tool_description>
<tool_name>calculator</tool_name>
<description>
Calculator function for doing basic arithmetic.
Supports addition, subtraction, multiplication
</description>
<parameters>
<parameter>
<name>first_operand</name>
<type>int</type>
<description>First operand (before the operator)</description>
</parameter>
<parameter>
<name>second_operand</name>
<type>int</type>
<description>Second operand (after the operator)</description>
</parameter>
<parameter>
<name>operator</name>
<type>str</type>
<description>The operation to perform. Must be either +, -, *, or /</description>
</parameter>
</parameters>
</tool_description>
</tools>
"""

system_prompt = system_prompt_tools_general_explanation + system_prompt_tools_specific_tools
```

**工具定義的意思：**
- `<tool_name>calculator</tool_name>`：工具名稱是「計算機」。
- `<description>`：「用來做基本算術的計算機函式，支援加法、減法、乘法。」
- 三個參數：
  - `first_operand`（第一個運算元，整數）：運算符號前面的數字
  - `second_operand`（第二個運算元，整數）：運算符號後面的數字
  - `operator`（運算子，字串）：要做的運算，必須是 `+`、`-`、`*` 或 `/` 其中之一
- 最後一行 `system_prompt = ... + ...`：把兩部分接起來。

現在我們可以問 Claude 一個需要用到 `calculator` 工具的問題。我們會把 `</function_calls>` 放進 `stop_sequences`，用來偵測 Claude **是否**以及**何時**呼叫了函式。

```python
multiplication_message = {
    "role": "user",
    "content": "Multiply 1,984,135 by 9,343,116"
}

stop_sequences = ["</function_calls>"]

# Get Claude's response
function_calling_response = get_completion([multiplication_message], system_prompt=system_prompt, stop_sequences=stop_sequences)
print(function_calling_response)
```

**逐行解說：**
- `multiplication_message`：使用者的訊息——「把 1,984,135 乘以 9,343,116」（這種大數字乘法 LLM 很容易算錯，所以適合交給計算機）。
- `stop_sequences = ["</function_calls>"]`：Claude 一寫完函式呼叫就停下來，等我們去執行工具。
- 印出的結果應該會是一段 `<function_calls><invoke name="calculator">...` 的文字。

現在，我們可以從 Claude 的函式呼叫中**擷取出參數**，並**代替 Claude 真的去執行函式**。

首先，我們定義函式的程式碼。

```python
def do_pairwise_arithmetic(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        return num1 / num2
    else:
        return "Error: Operation not supported."
```

（一個簡單的函式：根據 `operation` 是 `+`、`-`、`*`、`/`，回傳兩個數字的運算結果；其他符號就回傳錯誤訊息。）

接著，我們從 Claude 的函式呼叫回應中擷取參數。如果所有參數都存在，就執行計算機工具。

```python
def find_parameter(message, parameter_name):
    parameter_start_string = f"name=\"{parameter_name}\">"
    start = message.index(parameter_start_string)
    if start == -1:
        return None
    if start > 0:
        start = start + len(parameter_start_string)
        end = start
        while message[end] != "<":
            end += 1
    return message[start:end]

first_operand = find_parameter(function_calling_response, "first_operand")
second_operand = find_parameter(function_calling_response, "second_operand")
operator = find_parameter(function_calling_response, "operator")

if first_operand and second_operand and operator:
    result = do_pairwise_arithmetic(int(first_operand), int(second_operand), operator)
    print("---------------- RESULT ----------------")
    print(f"{result:,}")
```

**逐行解說：**
- `def find_parameter(message, parameter_name):`：一個小函式，在 Claude 的回應裡找出某個參數的值。
  - `parameter_start_string = f"name=\"{parameter_name}\">"`：要找的字串，例如 `name="first_operand">`。
  - `message.index(...)`：找到這個字串在回應中的位置。（⚠️ 小提醒：如果找不到，`.index()` 其實會直接**出錯**，而不是回傳 -1，所以下一行的檢查不太會發揮作用。這是原課程程式碼的小瑕疵，不影響正常情況下的執行。）
  - 然後從那個位置往後一個字元一個字元地讀，讀到 `<` 為止，中間的文字就是參數值。
- 下面三行分別擷取三個參數。
- `if first_operand and second_operand and operator:`：三個參數都找到了，才執行計算。
- `int(first_operand)`：擷取出來的是**文字**，要用 `int()` 轉成**整數**才能計算。
- `print(f"{result:,}")`：`:,` 會在數字中加上千分位逗號，例如 `18,538,003,464,660`。

現在我們有結果了，接著要把這個結果**正確地排版**，這樣把它傳回給 Claude 時，Claude 才知道這個結果是哪個工具產生的。Claude 受過訓練、能辨認的固定格式如下：
```
<function_results>
<result>
<tool_name>{TOOL_NAME}</tool_name>
<stdout>
{TOOL_RESULT}
</stdout>
</result>
</function_results>
```

（`stdout` 是「standard output，標準輸出」的縮寫，也就是「程式的輸出結果」。）

執行下面這格，把上面的工具結果排成這個格式。

```python
def construct_successful_function_run_injection_prompt(invoke_results):
    constructed_prompt = (
        "<function_results>\n"
        + '\n'.join(
            f"<result>\n<tool_name>{res['tool_name']}</tool_name>\n<stdout>\n{res['tool_result']}\n</stdout>\n</result>"
            for res in invoke_results
        ) + "\n</function_results>"
    )

    return constructed_prompt

formatted_results = [{
    'tool_name': 'do_pairwise_arithmetic',
    'tool_result': result
}]
function_results = construct_successful_function_run_injection_prompt(formatted_results)
print(function_results)
```

**逐行解說：**
- `construct_successful_function_run_injection_prompt(invoke_results)`：函式名稱很長，意思是「為成功執行的函式，建立要注入（放回）提示詞的內容」。
- 它接收一個串列，裡面每個字典都有 `tool_name` 和 `tool_result`，然後組出上面那種 `<function_results>` 格式的文字。
- `'\n'.join(...)`：如果有多個結果，用換行把它們接起來。

現在我們只要把這個結果**附加到之前的同一串訊息後面**，傳回給 Claude，就大功告成了！

```python
full_first_response = function_calling_response + "</function_calls>"

# Construct the full conversation
messages = [multiplication_message,
{
    "role": "assistant",
    "content": full_first_response
},
{
    "role": "user",
    "content": function_results
}]
   
# Print Claude's response
final_response = get_completion(messages, system_prompt=system_prompt, stop_sequences=stop_sequences)
print("------------- FINAL RESULT -------------")
print(final_response)
```

**逐行解說：**
- `full_first_response = function_calling_response + "</function_calls>"`：因為 `</function_calls>` 是停止序列，**不會**出現在 Claude 的回應裡，所以要自己把它補回去，讓對話紀錄完整。
- `messages` 有三則：
  1. user：「把 1,984,135 乘以 9,343,116」
  2. assistant：Claude 的函式呼叫（補完整的）
  3. user：工具的結果（`<function_results>...`）
- Claude 收到結果後，就會用這個正確的數字回答使用者。

恭喜你完整跑完一整個工具使用的流程！

那如果我們問 Claude 一個**完全不需要**用到這個工具的問題呢？

```python
non_multiplication_message = {
    "role": "user",
    "content": "Tell me the capital of France."
}

stop_sequences = ["</function_calls>"]

# Get Claude's response
function_calling_response = get_completion([non_multiplication_message], system_prompt=system_prompt, stop_sequences=stop_sequences)
print(function_calling_response)
```

（「告訴我法國的首都。」）

成功了！可以看到，Claude 知道在不需要的時候**不要**呼叫函式。

如果你想在不改動上面任何內容的情況下試玩課程中的提示詞，可以捲到這份 notebook 的最下面，前往[**範例遊樂場**](#範例遊樂場)。

---

## 練習
- [練習 10.2.1 - SQL](#練習-1021---sql)

### 練習 10.2.1 - SQL

在這個練習中，你要寫一個工具使用的提示詞，用來查詢和寫入「世界上最小的『資料庫』」。下面是初始化好的資料庫，其實它只是一個字典。

```python
db = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ],
    "products": [
        {"id": 1, "name": "Widget", "price": 9.99},
        {"id": 2, "name": "Gadget", "price": 14.99},
        {"id": 3, "name": "Doohickey", "price": 19.99}
    ]
}
```

（資料庫裡有兩張「表」：`users`（使用者：Alice、Bob、Charlie）和 `products`（商品：Widget、Gadget、Doohickey，各有價格）。）

下面是讀取和寫入資料庫的函式程式碼。

```python
def get_user(user_id):
    for user in db["users"]:
        if user["id"] == user_id:
            return user
    return None

def get_product(product_id):
    for product in db["products"]:
        if product["id"] == product_id:
            return product
    return None

def add_user(name, email):
    user_id = len(db["users"]) + 1
    user = {"id": user_id, "name": name, "email": email}
    db["users"].append(user)
    return user

def add_product(name, price):
    product_id = len(db["products"]) + 1
    product = {"id": product_id, "name": name, "price": price}
    db["products"].append(product)
    return product
```

**四個函式：**
- `get_user(user_id)`：用 ID 找使用者，找不到回傳 `None`。
- `get_product(product_id)`：用 ID 找商品。
- `add_user(name, email)`：新增使用者（ID 自動設為目前人數 + 1）。
- `add_product(name, price)`：新增商品。

要解這個練習，先定義一個像上面 `system_prompt_tools_specific_tools` 那樣的系統提示詞。記得包含**每個工具的名稱和描述**，以及**每個函式的每個參數的名稱、型別和描述**。我們在下面幫你準備了一些起始架構。

```python
system_prompt_tools_specific_tools_sql = """
"""

system_prompt = system_prompt_tools_general_explanation + system_prompt_tools_specific_tools_sql
```

> 💡 **提示**：照著上面計算機工具的 `<tools><tool_description>...</tool_description></tools>` 格式，為 `get_user`、`get_product`、`add_user`、`add_product` 各寫一段描述。

準備好之後，可以用下面的範例測試你的工具定義系統提示詞。執行下面這格就好！

```python
examples = [
    "Add a user to the database named Deborah.",
    "Add a product to the database named Thingo",
    "Tell me the name of User 2",
    "Tell me the name of Product 3"
]

for example in examples:
    message = {
        "role": "user",
        "content": example
    }

    # Get & print Claude's response
    function_calling_response = get_completion([message], system_prompt=system_prompt, stop_sequences=stop_sequences)
    print(example, "\n----------\n\n", function_calling_response, "\n*********\n*********\n*********\n\n")
```

（四個測試問題：「新增一位叫 Deborah 的使用者到資料庫。」「新增一個叫 Thingo 的商品到資料庫。」「告訴我使用者 2 的名字。」「告訴我商品 3 的名字。」）

如果你寫對了，函式呼叫的訊息應該會正確地呼叫 `add_user`、`add_product`、`get_user` 和 `get_product` 函式。

**額外加分題**：多加幾個程式碼格，寫出解析參數的程式碼。然後用 Claude 給你的參數真的呼叫這些函式，看看呼叫之後「資料庫」的狀態。

❓ 如果你想看一個可能的參考答案，執行下面這格！

```python
from hints import exercise_10_2_1_solution; print(exercise_10_2_1_solution)
```

### 恭喜！

恭喜你學會了工具使用和函式呼叫！如果你想學更多關於搜尋和 RAG 的內容，請前往最後一篇附錄。

---

## 範例遊樂場

這是一個讓你**自由實驗**的區域，你可以試玩這一課中出現的提示詞範例，調整提示詞，看看會怎麼影響 Claude 的回答。

```python
system_prompt_tools_general_explanation = """You have access to a set of functions you can use to answer the user's question. This includes access to a
sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external
resources, except by invoking the below functions.

You can invoke one or more functions by writing a "<function_calls>" block like the following as part of your
reply to the user:
<function_calls>
<invoke name="$FUNCTION_NAME">
<antml:parameter name="$PARAMETER_NAME">$PARAMETER_VALUE</parameter>
...
</invoke>
<nvoke name="$FUNCTION_NAME2">
...
</invoke>
</function_calls>

String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that
spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular
expressions.

The output and/or any errors will appear in a subsequent "<function_results>" block, and remain there as part of
your reply to the user.
You may then continue composing the rest of your reply to the user, respond to any errors, or make further function
calls as appropriate.
If a "<function_results>" does NOT appear after your function calls, then they are likely malformatted and not
recognized as a call."""
```

```python
system_prompt_tools_specific_tools = """Here are the functions available in JSONSchema format:
<tools>
<tool_description>
<tool_name>calculator</tool_name>
<description>
Calculator function for doing basic arithmetic.
Supports addition, subtraction, multiplication
</description>
<parameters>
<parameter>
<name>first_operand</name>
<type>int</type>
<description>First operand (before the operator)</description>
</parameter>
<parameter>
<name>second_operand</name>
<type>int</type>
<description>Second operand (after the operator)</description>
</parameter>
<parameter>
<name>operator</name>
<type>str</type>
<description>The operation to perform. Must be either +, -, *, or /</description>
</parameter>
</parameters>
</tool_description>
</tools>
"""

system_prompt = system_prompt_tools_general_explanation + system_prompt_tools_specific_tools
```

```python
multiplication_message = {
    "role": "user",
    "content": "Multiply 1,984,135 by 9,343,116"
}

stop_sequences = ["</function_calls>"]

# Get Claude's response
function_calling_response = get_completion([multiplication_message], system_prompt=system_prompt, stop_sequences=stop_sequences)
print(function_calling_response)
```

```python
def do_pairwise_arithmetic(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        return num1 / num2
    else:
        return "Error: Operation not supported."
```

```python
def find_parameter(message, parameter_name):
    parameter_start_string = f"name=\"{parameter_name}\">"
    start = message.index(parameter_start_string)
    if start == -1:
        return None
    if start > 0:
        start = start + len(parameter_start_string)
        end = start
        while message[end] != "<":
            end += 1
    return message[start:end]

first_operand = find_parameter(function_calling_response, "first_operand")
second_operand = find_parameter(function_calling_response, "second_operand")
operator = find_parameter(function_calling_response, "operator")

if first_operand and second_operand and operator:
    result = do_pairwise_arithmetic(int(first_operand), int(second_operand), operator)
    print("---------------- RESULT ----------------")
    print(f"{result:,}")
```

```python
def construct_successful_function_run_injection_prompt(invoke_results):
    constructed_prompt = (
        "<function_results>\n"
        + '\n'.join(
            f"<result>\n<tool_name>{res['tool_name']}</tool_name>\n<stdout>\n{res['tool_result']}\n</stdout>\n</result>"
            for res in invoke_results
        ) + "\n</function_results>"
    )

    return constructed_prompt

formatted_results = [{
    'tool_name': 'do_pairwise_arithmetic',
    'tool_result': result
}]
function_results = construct_successful_function_run_injection_prompt(formatted_results)
print(function_results)
```

```python
full_first_response = function_calling_response + "</function_calls>"

# Construct the full conversation
messages = [multiplication_message,
{
    "role": "assistant",
    "content": full_first_response
},
{
    "role": "user",
    "content": function_results
}]
   
# Print Claude's response
final_response = get_completion(messages, system_prompt=system_prompt, stop_sequences=stop_sequences)
print("------------- FINAL RESULT -------------")
print(final_response)
```

```python
non_multiplication_message = {
    "role": "user",
    "content": "Tell me the capital of France."
}

stop_sequences = ["</function_calls>"]

# Get Claude's response
function_calling_response = get_completion([non_multiplication_message], system_prompt=system_prompt, stop_sequences=stop_sequences)
print(function_calling_response)
```

---

## 📌 重點整理

- **工具使用 = 替換 + 串連提示詞**：Claude 說出「想用哪個工具、參數是什麼」→ 你的程式執行工具 → 把結果放回對話 → Claude 繼續回答。
- Claude **不會真的執行**工具，執行的永遠是你的程式。
- 舊方法的兩個元素：**系統提示詞**（解釋工具使用 + 工具清單）和**控制邏輯**（偵測呼叫、擷取參數、執行、回傳結果）。
- 用 `stop_sequences=["</function_calls>"]` 讓 Claude 寫完呼叫就停下來。
- Claude 會判斷什麼時候**需要**、什麼時候**不需要**使用工具。
- 🔄 現在有內建的工具使用 API，請到 **第 5 單元** 學習新方法。

👉 下一篇：[附錄 10.3：搜尋與檢索](10_3_Appendix_Search_and_Retrieval.md)
