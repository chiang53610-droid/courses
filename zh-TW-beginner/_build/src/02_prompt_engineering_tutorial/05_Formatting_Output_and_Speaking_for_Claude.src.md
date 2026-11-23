<!--meta {"orig": "prompt_engineering_interactive_tutorial/Anthropic 1P/05_Formatting_Output_and_Speaking_for_Claude.ipynb", "out": "02_prompt_engineering_tutorial/05_Formatting_Output_and_Speaking_for_Claude"} -->
# 第 5 章：格式化輸出 & 幫 Claude 開口（Formatting Output and Speaking for Claude）

> 📚 **第 2 單元：提示詞工程互動教學**｜第 5 章 / 共 9 章（中級）
> ⏱️ 預估時間：40 分鐘

- [課程](#課程)
- [練習](#練習)
- [範例遊樂場](#範例遊樂場)

## 🎯 這一章你會學到

- 請 Claude 用 **XML 標籤**、**JSON** 等格式輸出，方便程式擷取
- **幫 Claude 開口（prefill，預先填寫回答）**：在 `assistant` 回合先寫好開頭，讓 Claude 接著寫
- 加碼：用 `stop_sequences` 在結束標籤出現時停止，省錢又省時間

> 🔄 **2026 更新**：本章大量使用 prefill 技巧。新手版使用的 `claude-haiku-4-5` 支援 prefill，可以照常練習。但請記得：**最新一代的模型（例如 Haiku 5.5、Sonnet 4.6 以後、Opus 4.6 以後）已經不支援 prefill**，在那些模型上要改用「在提示詞裡明確要求格式」或「結構化輸出（structured outputs）」功能來達到同樣的效果。prefill 背後的觀念——「引導 Claude 從特定的格式開始寫」——仍然非常值得學。

## 準備工作

執行下面這個準備格，載入你的 API 金鑰，並建立 `get_completion` 輔助函式。

{{cell 1}}

**這一版的 `get_completion` 有什麼不同？**
- 多了一個參數 `prefill=""`（程式碼裡的註解說：「新增了一個用來預先填寫文字的參數，預設值是空字串」）。
- `messages` 裡現在有**兩則**訊息：
  1. `{"role": "user", "content": prompt}`：你的提示詞。
  2. `{"role": "assistant", "content": prefill}`：**你幫 Claude 預先寫好的開頭**。Claude 會從這裡**接著寫下去**。
- 如果 `prefill` 是空字串，就等於沒有預先填寫，Claude 會從頭開始回答。

---

## 課程

**Claude 可以用非常多種方式格式化它的輸出。** 你只需要開口要求它這樣做就好！

其中一種方式，是用 **XML 標籤**把回答和其他多餘的文字分開。你已經學過，可以用 XML 標籤讓你的提示詞對 Claude 來說更清楚、更容易解析。其實，你也可以請 Claude **用 XML 標籤讓它的輸出更清楚**，讓人更容易理解。

### 範例

還記得我們在第 2 章，靠著「請 Claude 完全跳過開場白」解決的「詩的開場白問題」嗎？其實我們也可以用**請 Claude 把詩放在 XML 標籤裡**的方式，達到類似的效果。

{{cell 4}}

（「請寫一首關於 {ANIMAL}（兔子）的俳句。把它放在 `<haiku>` 標籤裡。」）

為什麼要這樣做？因為輸出放在 **XML 標籤裡，使用者只要寫一個簡短的程式，擷取 XML 標籤中間的內容，就能穩定地拿到「這首詩，而且只有這首詩」**。

> 🧩 **白話小補充：怎麼擷取標籤中間的內容？** 用 [0-4 第 14 節](../00_before_you_start/04_python_crash_course.md#14-正規表達式-re在文字裡找東西) 學過的正規表達式：
> ```python
> import re
> poem = re.search(r"<haiku>(.*?)</haiku>", response, re.DOTALL).group(1)
> ```
> （`re.DOTALL` 讓 `.` 也能比對換行，因為詩有好幾行。）

這個技巧的進階版，是**把第一個 XML 標籤放在 `assistant` 回合裡**。當你在 `assistant` 回合放入文字時，基本上就是在告訴 Claude：「你已經說了這些話，請從這裡接著說下去」。這個技巧叫做「**幫 Claude 開口（speaking for Claude）**」或「**預先填寫 Claude 的回答（prefilling Claude's response）**」。

下面我們用第一個 `<haiku>` XML 標籤來示範。注意看 Claude 是怎麼**直接從我們停下來的地方接著寫**的。

{{cell 6}}

**逐行解說：**
- `PREFILL = "<haiku>"`：我們幫 Claude 先寫好 `<haiku>`。
- 程式印出「USER TURN（使用者回合）」和「ASSISTANT TURN（助理回合）」的內容，讓你看清楚送了什麼給 Claude。
- `get_completion(PROMPT, prefill=PREFILL)`：把 prefill 傳進去。
- Claude 的回答會**直接從詩的第一句開始**（因為 `<haiku>` 已經「說過了」），而且通常會以 `</haiku>` 結尾。

> 🧩 **白話小補充：prefill 就像幫人起頭**。你跟朋友說：「我們來接龍，我先說：『從前從前，有一隻⋯⋯』」，朋友就會接著說下去，而且故事一定是從「有一隻⋯⋯」開始。
> ⚠️ 注意：Claude 回傳的內容**不包含**你 prefill 的部分（`<haiku>` 不會出現在回答裡），需要的話要自己接回去。

Claude 也很擅長使用其他的輸出格式，特別是 **`JSON`**。如果你想強制 Claude 輸出 JSON（不是百分之百保證，但很接近），也可以在 Claude 的回答裡預先填寫一個左大括號 `{`。

{{cell 8}}

（「請寫一首關於貓的俳句。用 JSON 格式，key 分別是 "first_line"（第一句）、"second_line"（第二句）和 "third_line"（第三句）。」prefill 是 `{`。）

> 🧩 **小提醒**：字串裡的 `\"` 代表「一個雙引號字元」。因為整個字串是用雙引號包起來的，裡面要放雙引號就要在前面加 `\`（跳脫字元）。

下面是一個**在同一個提示詞裡使用多個輸入變數，而且還指定輸出格式——全部都用 XML 標籤完成**的範例。

{{cell 10}}

**逐行解說：**
- `EMAIL`：信件內容——「嗨 Zack，只是想問一下你負責寫的那個提示詞進度如何。」
- `ADJECTIVE = "olde english"`：要把信改成「古英文風格」。
- 提示詞：「嘿 Claude。這是一封信：<email>{EMAIL}</email>。請把這封信改得更 {ADJECTIVE}。把新版本寫在 <{ADJECTIVE}_email> XML 標籤裡。」——注意標籤名稱本身也用了變數，會變成 `<olde english_email>`。
- `PREFILL = f"<{ADJECTIVE}_email>"`：prefill 也用 f-string，跟提示詞裡的標籤一致。

#### 加碼課程

如果你是透過 API 呼叫 Claude，可以把**結束的 XML 標籤**傳給 `stop_sequences` 參數，讓 Claude 一寫出你想要的標籤就停止產生文字。這樣可以省錢，也能縮短「收到最後一個 token 的時間」，因為在 Claude 已經給你想要的答案之後，就不會再有它的結語了。

> 🧩 **舉例**：prefill 寫 `<haiku>`，再設定 `stop_sequences=["</haiku>"]`，Claude 寫完詩就會立刻停下，不會再補一句「希望你喜歡這首詩！」。（`stop_sequences` 在 [1-4 課](../01_api_fundamentals/04_parameters.md#stop-sequences停止序列) 學過。）

如果你想在不改動上面任何內容的情況下試玩課程中的提示詞，可以捲到這份 notebook 的最下面，前往[**範例遊樂場**](#範例遊樂場)。

---

## 練習
- [練習 5.1 - 柯瑞是史上最強](#練習-51---柯瑞是史上最強)
- [練習 5.2 - 兩首俳句](#練習-52---兩首俳句)
- [練習 5.3 - 兩首俳句，兩種動物](#練習-53---兩首俳句兩種動物)

### 練習 5.1 - 柯瑞是史上最強

被迫做出選擇時，Claude 選了麥可·喬丹作為史上最偉大的籃球員。我們能讓 Claude 選別人嗎？

修改 `PREFILL` 變數，**逼 Claude 詳細論證「史上最偉大的籃球員是史蒂芬·柯瑞（Stephen Curry）」**。除了 `PREFILL` 以外，盡量不要改其他東西，因為這個練習的重點就在 prefill。

{{cell 14}}

**題目**：「史上最偉大的籃球員是誰？請選一位特定的球員。」
**批改程式在做什麼？** 檢查回答裡有沒有 `Warrior`（柯瑞效力的「金州勇士隊」Golden State Warriors）。

❓ 如果你需要提示，執行下面這格！

{{cell 16}}

### 練習 5.2 - 兩首俳句

用 XML 標籤修改下面的 `PROMPT`，讓 Claude 針對這種動物寫**兩首**俳句，而不是只寫一首。要清楚地看出一首詩在哪裡結束、另一首在哪裡開始。

{{cell 18}}

**批改程式在做什麼？** 回答裡要有 `cat` 和 `<haiku>`，而且總行數要**超過 5 行**（`text.count("\n") + 1` 是計算行數的方法：換行符號的數量 + 1）。

> 💡 小提醒：因為 prefill 的 `<haiku>` 不會出現在回答裡，所以回答裡至少要有**第二個** `<haiku>` 標籤（也就是第二首詩的開始），批改才會通過。

❓ 如果你需要提示，執行下面這格！

{{cell 20}}

### 練習 5.3 - 兩首俳句，兩種動物

修改下面的 `PROMPT`，讓 **Claude 針對兩種不同的動物各寫一首俳句**。用 `{ANIMAL1}` 代表第一個要替換的變數，用 `{ANIMAL2}` 代表第二個要替換的變數。

{{cell 22}}

**批改程式在做什麼？** 回答裡要有 `tail`（尾巴）、`cat`（貓）和 `<haiku>`。（狗的俳句裡很可能會提到「搖尾巴」，所以會出現 tail。）

❓ 如果你需要提示，執行下面這格！

{{cell 24}}

### 恭喜！

如果你已經解完到目前為止所有的練習，就可以前往下一章了。祝你寫提示詞愉快！

---

## 範例遊樂場

這是一個讓你**自由實驗**的區域，你可以試玩這一課中出現的提示詞範例，調整提示詞，看看會怎麼影響 Claude 的回答。

{{cells 27-30}}

---

## 📌 重點整理

- 想要什麼格式，就**直接要求**：「放在 `<haiku>` 標籤裡」、「用 JSON 格式，key 是⋯⋯」。
- 輸出放在 XML 標籤裡，程式就能用正規表達式**穩定地擷取**需要的部分。
- **Prefill（幫 Claude 開口）**：在最後一則 `assistant` 訊息先寫好開頭（例如 `<haiku>`、`{`、`Stephen Curry is the best because`），Claude 會**接著寫**，可以強力引導格式和內容。prefill 的文字不會出現在回答裡。
- 加碼：把結束標籤（例如 `</haiku>`）設為 `stop_sequences`，省掉多餘的結語。
- 🔄 最新模型不支援 prefill，要改用明確的格式指示或結構化輸出。

👉 下一章：[第 6 章：預先思考（一步一步想）](06_Precognition_Thinking_Step_by_Step.md)
