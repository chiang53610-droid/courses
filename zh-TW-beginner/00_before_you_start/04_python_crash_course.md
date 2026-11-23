<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`04_python_crash_course.ipynb`](04_python_crash_course.ipynb)。

# 0-4 Python 速成：只學課程會用到的

> 🎯 **這一課你會學到：** 看懂整套課程程式碼所需要的 Python 基本功。我們**只教課程裡真的會出現的語法**，不多教。
>
> ⏱️ 預估時間：1～2 小時（建議打開 `.ipynb` 邊跑邊學）
>
> 💡 這一課**完全不需要 API 金鑰**，也不會花到錢，放心地跑、放心地改！

**目錄**
1. `print` 與註解
2. 變數
3. 字串（文字）——課程裡最重要的資料型態
4. 數字
5. 串列（list）
6. 字典（dict）
7. 把串列和字典組合起來——Claude 的訊息格式
8. 判斷：`if` / `elif` / `else`
9. 迴圈：`for` 與 `while`
10. 函式（function）
11. `import`：使用別人寫好的工具
12. 物件與「點」：看懂 `response.content[0].text`
13. JSON
14. 正規表達式 `re`：在文字裡找東西
15. 錯誤處理：`try` / `except`
16. 其他會看到的語法：`with`、串列生成式、`input()`、`async`、`%store`

---

## 1. `print` 與註解

`print()` 會把括號裡的東西顯示在畫面上。這是你最常用的指令。

```python
print("哈囉，世界！")
print("我正在學 Python")
```

`#` 後面的文字叫做**註解（comment）**，是寫給人看的筆記，Python 會**直接忽略**它。

```python
# 這一行是註解，不會被執行
print("這一行會被執行")  # 註解也可以寫在程式碼的後面
```

---

## 2. 變數

**變數**就像一個**貼了標籤的盒子**，可以把東西放進去，之後用標籤名稱拿出來。
用 `=` 把右邊的值放進左邊的盒子（`=` 在程式裡的意思是「放進去」，不是數學的「等於」）。

```python
name = "小明"        # 把文字 "小明" 放進叫 name 的盒子
age = 18            # 把數字 18 放進叫 age 的盒子
print(name)
print(age)

age = 19            # 盒子可以換新的東西進去
print(age)
```

> 💡 變數名稱慣例用**小寫英文 + 底線**，例如 `my_api_key`、`first_message`。全部大寫（例如 `MODEL_NAME`、`API_KEY`）通常代表「設定好就不會再改的值」。

---

## 3. 字串（文字）——課程裡最重要的資料型態

**字串（string）**就是一段文字。用**雙引號 `"..."` 或單引號 `'...'`** 包起來。
跟 Claude 溝通，送出去的提示詞和收回來的回答都是字串，所以這一節特別重要。

```python
greeting = "你好"
question = 'Claude 是什麼？'
print(greeting)
print(question)
```

### 3-1 多行字串：三個引號

提示詞常常很長、有很多行。用**三個引號 `"""..."""`** 就可以寫多行文字：

```python
prompt = """請幫我做以下事情：
1. 讀這篇文章
2. 寫一段摘要
3. 列出三個重點"""
print(prompt)
```

### 3-2 f-string：把變數塞進文字裡

在引號前面加一個 **`f`**，就可以在文字中用 **`{變數名稱}`** 把變數的值塞進去。
課程裡**超級常用**這個技巧來組合提示詞（例如把一篇文章塞進提示詞裡）。

```python
animal = "貓"
sound = "喵喵"
sentence = f"{animal}的叫聲是「{sound}」"
print(sentence)

# 多行 + f-string 一起用
email = "老闆你好，我明天要請假。"
prompt = f"""請把下面這封信改寫得更有禮貌：
<email>
{email}
</email>"""
print(prompt)
```

> 🧩 **白話小補充**：上面的 `<email>` 和 `</email>` 叫做 **XML 標籤**，只是普通的文字，用來把資料「框起來」，讓 Claude 知道哪裡到哪裡是信件內容。第 2 單元第 4 章會詳細教這個技巧。

### 3-3 字串的常見操作

```python
text = "  Hello Claude  "

print(text + "!!!")          # + 可以把字串接起來
print(len("你好"))            # len() 算出有幾個字 → 2
print(text.strip())          # .strip() 去掉頭尾的空白
print(text.lower())          # .lower() 全部變小寫
print(text.upper())          # .upper() 全部變大寫
print(text.replace("Hello", "Hi"))   # .replace(舊, 新) 取代文字
print("Claude" in text)      # in 檢查「有沒有包含」→ True（是）
print("a,b,c".split(","))    # .split(",") 用逗號切開 → ['a', 'b', 'c']
```

### 3-4 特殊字元 `\n`

在字串裡，`\n` 代表「換行」：

```python
print("第一行\n第二行")
```

---

## 4. 數字

Python 的數字有**整數**（`int`，例如 `3`）和**小數**（`float`，例如 `0.5`）。

```python
a = 10
b = 3
print(a + b)    # 加 → 13
print(a - b)    # 減 → 7
print(a * b)    # 乘 → 30
print(a / b)    # 除 → 3.333...
print(a // b)   # 整數除法（只要商）→ 3
print(round(3.14159, 2))  # 四捨五入到小數第 2 位 → 3.14
```

課程裡的 `max_tokens=1000`、`temperature=0.5` 就是用數字設定參數。

---

## 5. 串列（list）

**串列**是一個**有順序的清單**，用**中括號 `[ ]`** 包起來，裡面的東西用逗號分開。

```python
fruits = ["蘋果", "香蕉", "橘子"]
print(fruits)
print(len(fruits))      # 有幾個 → 3
```

### 5-1 用「編號」拿出裡面的東西

⚠️ **程式的編號是從 0 開始數的！** 第一個是 `[0]`，第二個是 `[1]`⋯⋯

```python
fruits = ["蘋果", "香蕉", "橘子"]
print(fruits[0])    # 第一個 → 蘋果
print(fruits[1])    # 第二個 → 香蕉
print(fruits[-1])   # 負數代表從後面數，-1 是最後一個 → 橘子
```

> 🧩 這就是為什麼課程裡會一直看到 `content[0]`——意思是「拿 content 這個串列的**第一個**東西」。

### 5-2 加入新東西

```python
fruits = ["蘋果", "香蕉"]
fruits.append("西瓜")    # .append() 加到最後面
print(fruits)
```

> 🧩 在第 1 單元，我們會用 `.append()` 把新的對話訊息加進對話紀錄裡，做出一個聊天機器人。

---

## 6. 字典（dict）

**字典**用來存放「**名稱：值**」這樣成對的資料，用**大括號 `{ }`** 包起來。
就像真的字典：用「單字」（叫做 **key／鍵**）查到「解釋」（叫做 **value／值**）。

```python
student = {
    "name": "小華",
    "age": 20,
    "school": "台灣大學"
}
print(student["name"])   # 用 key 拿出值 → 小華
print(student["age"])    # → 20

student["age"] = 21          # 修改
student["major"] = "資工系"   # 新增
print(student)
```

---

## 7. 把串列和字典組合起來——Claude 的訊息格式

這一節是**整套課程最重要的 Python 觀念**！
跟 Claude 對話時，我們送出的「訊息」就是**一個串列，裡面裝著好幾個字典**：

```python
messages = [
    {"role": "user", "content": "你好，你叫什麼名字？"},
    {"role": "assistant", "content": "你好！我是 Claude。"},
    {"role": "user", "content": "你會做什麼？"}
]

print(len(messages))              # 共有 3 則訊息
print(messages[0])                # 第 1 則訊息（一個字典）
print(messages[0]["role"])        # 第 1 則訊息的角色 → user
print(messages[1]["content"])     # 第 2 則訊息的內容 → 你好！我是 Claude。
```

**怎麼讀 `messages[1]["content"]`？** 從左到右一層一層拆開：
1. `messages` → 整個串列
2. `messages[1]` → 串列裡的第 2 個東西（一個字典）
3. `messages[1]["content"]` → 那個字典裡 `"content"` 對應的值

```python
# 加入新的一則訊息
messages.append({"role": "assistant", "content": "我可以幫你寫作、翻譯、寫程式⋯⋯"})
print(len(messages))   # 變成 4 則
```

---

## 8. 判斷：`if` / `elif` / `else`

讓程式「看情況做不同的事」。

```python
score = 75

if score >= 90:
    print("優秀")
elif score >= 60:      # elif = else if，「不然的話，如果⋯⋯」
    print("及格")
else:                  # 以上都不是
    print("不及格")
```

⚠️ **Python 用「縮排」（每行前面的空白，通常是 4 個空格）來表示「哪些程式碼屬於這個 if」**。縮排錯了程式就會出錯，這是 Python 的特色。

### 常用的比較符號

| 符號 | 意思 |
|---|---|
| `==` | 等於（注意是**兩個**等號；一個等號是「放進變數」） |
| `!=` | 不等於 |
| `>`、`<`、`>=`、`<=` | 大於、小於、大於等於、小於等於 |
| `and`、`or`、`not` | 而且、或者、不是 |

```python
answer = "Yes"
print(answer == "Yes")    # True
print(answer != "No")     # True
print(answer == "Yes" and len(answer) == 3)   # True
```

`True`（真/是）和 `False`（假/否）叫做**布林值（boolean）**。課程的練習題常常會用 `True`/`False` 判斷你的答案對不對。

另外，`None` 代表「什麼都沒有」：

```python
result = None
if result is None:
    print("目前沒有結果")
```

---

## 9. 迴圈：`for` 與 `while`

### 9-1 `for`：對清單裡的每一個東西做同樣的事

```python
animals = ["貓", "狗", "兔子"]
for animal in animals:          # 每一輪，animal 會依序變成清單裡的每一個東西
    print(f"我喜歡{animal}")
```

```python
# range(3) 會產生 0, 1, 2 三個數字
for i in range(3):
    print(f"這是第 {i} 次")
```

> 🧩 課程裡常用 `for` 迴圈「對很多筆資料，一筆一筆請 Claude 處理」，例如一次分類很多封信。

### 9-2 `while`：只要條件成立就一直重複

```python
count = 0
while count < 3:
    print(f"count = {count}")
    count = count + 1     # 每次加 1，不然會無限重複下去！
```

`while True:` 代表「永遠重複」，通常搭配 `break`（跳出迴圈）一起用。第 1 單元的聊天機器人就是這樣寫的：

```python
n = 0
while True:
    n = n + 1
    if n == 3:
        print("到 3 了，跳出！")
        break
    print(n)
```

---

## 10. 函式（function）

**函式**是「**把一段常用的程式碼包起來，取個名字**」，以後只要叫名字就能重複使用。
就像一台果汁機：放進材料（**參數**），按下按鈕，就會吐出果汁（**回傳值**）。

```python
def make_greeting(name):          # def = 定義函式；name 是參數（要放進來的材料）
    message = f"你好，{name}！"
    return message                # return = 把結果「交回去」

result = make_greeting("小美")    # 呼叫函式，把 "小美" 放進去
print(result)
print(make_greeting("阿強"))
```

### 10-1 參數可以有預設值

```python
def ask(question, polite=True):     # polite 沒給的話，預設是 True
    if polite:
        return f"請問，{question}"
    return question

print(ask("今天天氣如何？"))              # 用預設值
print(ask("今天天氣如何？", polite=False)) # 指定參數名稱來設定
```

> 🧩 課程裡會一直看到這種寫法：
> ```python
> def get_completion(prompt, system_prompt=""):
>     message = client.messages.create(...)
>     return message.content[0].text
> ```
> 意思是：「定義一個叫 `get_completion` 的函式，給它一段提示詞，它會去問 Claude，然後把 Claude 的回答交回來。」把這些步驟包成函式，以後只要寫 `get_completion("你的問題")` 就好，不用每次都寫一大串。

### 10-2 呼叫函式時「指名道姓」傳參數

呼叫函式時，可以用 `參數名稱=值` 的方式傳入，這叫**關鍵字參數**。課程裡呼叫 Claude 就是這樣寫的：

```python
client.messages.create(
    model="claude-haiku-4-5",   # 參數名稱 model，值是 "claude-haiku-4-5"
    max_tokens=1000,            # 參數名稱 max_tokens，值是 1000
    messages=[...]              # 參數名稱 messages，值是一個串列
)
```

---

## 11. `import`：使用別人寫好的工具

Python 有很多現成的工具（**模組/套件**），用 `import` 把它們拿出來用。

```python
import random                   # 拿出整個 random 工具箱
print(random.randint(1, 6))     # 用「工具箱.工具」的方式使用：擲骰子

from datetime import date       # 只從 datetime 工具箱拿出 date 這一個工具
print(date.today())             # 今天的日期
```

課程裡最常見的幾行：

```python
from anthropic import Anthropic   # 從 anthropic 套件拿出 Anthropic（用來建立客戶端）
from dotenv import load_dotenv    # 從 dotenv 套件拿出 load_dotenv（讀取 .env 檔）
import os                         # 作業系統工具（讀取環境變數）
import json                       # 處理 JSON 格式
import re                         # 正規表達式（在文字裡搜尋）
```

---

## 12. 物件與「點」：看懂 `response.content[0].text`

在 Python 裡，很多東西是**物件（object）**。物件身上有**屬性**（資料）和**方法**（功能），都用**「點 `.`」**來取用。

- `"hello".upper()` → 對字串物件使用 `upper` 這個方法
- `client.messages.create(...)` → 使用 `client` 物件裡 `messages` 的 `create` 方法

Claude 回傳的回應（response）也是一個物件。我們用下面的程式「模擬」一個長得很像的物件，來練習怎麼拆開它：

```python
from types import SimpleNamespace   # 一個可以隨手做出「有屬性的物件」的小工具

# 模擬一個 Claude 的回應（真正的回應就長得很像這樣）
response = SimpleNamespace(
    id="msg_123",
    model="claude-haiku-4-5",
    role="assistant",
    stop_reason="end_turn",
    content=[                                   # content 是一個串列
        SimpleNamespace(type="text", text="你好！我是 Claude，很高興認識你。")
    ],
    usage=SimpleNamespace(input_tokens=12, output_tokens=20),
)

print(response.role)                  # → assistant
print(response.content)               # 一個串列，裡面有一個「內容區塊」
print(response.content[0])            # 串列的第一個內容區塊
print(response.content[0].text)       # 那個內容區塊的文字 ← 這就是 Claude 的回答！
print(response.usage.output_tokens)   # 回答用了幾個 token
```

**怎麼讀 `response.content[0].text`？**
1. `response` → 整個回應物件
2. `response.content` → 回應裡的「內容」，是一個**串列**
3. `response.content[0]` → 串列裡的**第一個**內容區塊
4. `response.content[0].text` → 那個區塊裡的**文字**

> 🧩 為什麼 content 是串列，不直接是文字？因為 Claude 的回答可能包含好幾塊不同類型的內容（例如文字＋「我想使用某個工具」）。第 5 單元「工具使用」會看到這種情況。

---

## 13. JSON

**JSON** 是一種「用文字表示資料」的通用格式，長得幾乎和 Python 的字典/串列一模一樣。
程式之間交換資料時很常用它。課程裡會請 Claude 用 JSON 格式回答，方便程式讀取。

```python
import json

data = {"name": "小明", "hobbies": ["籃球", "畫畫"]}

# 字典 → JSON 文字
text = json.dumps(data, ensure_ascii=False)   # ensure_ascii=False 讓中文正常顯示
print(text)
print(type(text))     # <class 'str'>，它是字串

# JSON 文字 → 字典
back = json.loads('{"score": 95, "passed": true}')
print(back["score"])  # 95
print(type(back))     # <class 'dict'>，它是字典
```

---

## 14. 正規表達式 `re`：在文字裡找東西

**正規表達式（regular expression，簡稱 regex）** 是一種「描述文字長什麼樣子」的規則，用來在一大段文字裡搜尋。
課程裡主要拿它來做兩件事：**檢查 Claude 的回答有沒有某些字**（練習題的自動批改），以及**從 XML 標籤中間把內容拿出來**。

```python
import re

answer = "The answer is Yes, I think."

# re.search(要找的規則, 在哪段文字裡找) → 找到會回傳一個「找到了」的物件，找不到回傳 None
print(re.search("Yes", answer))          # 找到了
print(re.search("No", answer))           # None（找不到）
print(bool(re.search("Yes", answer)))    # 轉成 True/False → True
```

```python
# 從 XML 標籤中間拿出內容
reply = "這是我的想法⋯⋯<answer>台北</answer>"
match = re.search(r"<answer>(.*?)</answer>", reply)
print(match.group(1))   # 小括號 ( ) 圈起來的部分 → 台北
```

**規則小抄**（看得懂就好，不用背）：

| 寫法 | 意思 |
|---|---|
| `.` | 任意一個字元 |
| `*` | 前一個東西重複 0 次以上 |
| `.*?` | 任意文字，但「越短越好」 |
| `( )` | 把這部分圈起來，之後可以用 `.group(1)` 拿出來 |
| `^` / `$` | 開頭 / 結尾 |
| `\d` | 一個數字 |
| `r"..."` | 字串前面加 `r`，代表裡面的反斜線 `\` 不要特別處理（寫 regex 時的好習慣） |

`re.findall` 會找出**所有**符合的部分：

```python
import re
text = "<item>蘋果</item><item>香蕉</item>"
print(re.findall(r"<item>(.*?)</item>", text))   # → ['蘋果', '香蕉']
```

---

## 15. 錯誤處理：`try` / `except`

程式出錯時，正常來說會整個停下來。用 `try` / `except` 可以「**試試看，出錯的話改做別的事**」。

```python
try:
    number = int("abc")      # 想把 "abc" 轉成數字，一定會出錯
except ValueError:
    print("這不是數字喔！")

print("程式繼續執行")
```

---

## 16. 其他會看到的語法

### 16-1 `with`：用完自動收拾

`with` 會在區塊結束時自動幫你「收尾」（例如關閉檔案、結束連線）。課程裡讀檔案和「串流」會用到：

```python
# 寫一個小檔案，再讀回來
with open("test_file.txt", "w", encoding="utf-8") as f:   # "w" = 寫入模式
    f.write("這是測試文字")

with open("test_file.txt", "r", encoding="utf-8") as f:   # "r" = 讀取模式
    content = f.read()
print(content)

import os
os.remove("test_file.txt")   # 刪掉測試檔案
```

### 16-2 串列生成式（list comprehension）

一行就做出一個新串列的簡寫：

```python
numbers = [1, 2, 3, 4]
doubled = [n * 2 for n in numbers]       # 「對 numbers 裡每個 n，算 n*2」
print(doubled)                           # [2, 4, 6, 8]

# 等同於：
doubled2 = []
for n in numbers:
    doubled2.append(n * 2)
print(doubled2)
```

### 16-3 `input()`：讓使用者打字輸入

`input("提示文字")` 會停下來等你打字，按 Enter 後把你打的字變成字串。聊天機器人的練習會用到。

```python
name = input("請輸入你的名字：")
print(f"你好，{name}")
```

（這格不設定成自動執行，因為它會停下來等你輸入。你可以自己複製到程式碼格裡試試。）

### 16-4 `async` / `await`

在「串流」那一課，你會看到 `async def` 和 `await`。這是「**非同步**」寫法：讓程式在等待網路回應時可以先做別的事。新手**只要知道它是一種特殊寫法、照抄就能跑**就好，不需要深入了解。

### 16-5 `%store`（notebook 專用）

第 2 單元會看到 `%store API_KEY` 和 `%store -r API_KEY`。
這是 Jupyter 的「**魔法指令**」，用來**在不同 notebook 之間傳遞變數**：
- `%store API_KEY`：把 `API_KEY` 這個變數存起來
- `%store -r API_KEY`：在另一個 notebook 裡把它讀回來（`-r` = read）

---

## ✏️ 小練習

試著自己寫寫看（答案在下面，先自己想再看）：

1. 建立一個變數 `topic = "貓咪"`，用 f-string 組出提示詞：`請寫一首關於貓咪的短詩`，並印出來。
2. 建立一個 `messages` 串列，裡面有一則 `role` 是 `"user"`、`content` 是 `"你好"` 的訊息。然後用 `.append()` 加入一則 `assistant` 的回覆，最後印出第二則訊息的 `content`。
3. 寫一個函式 `is_yes(text)`：如果 `text` 裡面有 `"Yes"` 就回傳 `True`，否則回傳 `False`。

```python
# 在這裡寫你的答案

```

<details>
<summary>👀 點這裡看參考答案</summary>

```python
# 1
topic = "貓咪"
prompt = f"請寫一首關於{topic}的短詩"
print(prompt)

# 2
messages = [{"role": "user", "content": "你好"}]
messages.append({"role": "assistant", "content": "你好！有什麼可以幫你的嗎？"})
print(messages[1]["content"])

# 3
def is_yes(text):
    return "Yes" in text

print(is_yes("Yes, I agree"))  # True
print(is_yes("No way"))        # False
```

</details>

---

## 📌 重點整理

- **字串**是課程的主角：多行用 `"""..."""`，塞變數用 **f-string** `f"...{變數}..."`。
- **串列** `[ ]` 用編號拿東西，**從 0 開始**；**字典** `{ }` 用 key 拿東西。
- Claude 的訊息格式 = **串列裡裝字典**：`[{"role": "user", "content": "..."}]`。
- **函式** `def` 把常用步驟包起來，`return` 交回結果。
- `response.content[0].text` = 回應 → 內容串列 → 第一塊 → 文字。
- `re.search` 用來在文字裡找東西；`json` 用來處理 JSON 格式。
- notebook 要**從上往下**執行；看不懂的語法隨時回來這一課查。

🎉 **新手先修單元完成！** 👉 下一步：[第 1 單元：Claude API 基礎 — 1-1 開始使用](../01_api_fundamentals/01_getting_started.md)
