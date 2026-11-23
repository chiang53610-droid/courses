<!--meta {"orig": "tool_use/04_complete_workflow.ipynb", "out": "05_tool_use/04_complete_workflow"} -->
# 5-4 完整的工具使用流程

> 📚 **第 5 單元：工具使用**｜第 4 課 / 共 6 課
> ⏱️ 預估時間：60 分鐘

## 🎯 這一課你會學到

* 了解**完整的**工具使用流程（4 個步驟全部走完）
* 寫出結構正確的 **`tool_result`** 訊息，把工具結果回傳給 Claude
* 實作一個會使用工具（搜尋維基百科）的聊天機器人

> 🔄 **2026 更新**：
> - 這一課原本使用 `claude-3-sonnet-20240229`，新手版換成 `claude-sonnet-4-6`。
> - 這一課的範例問題（2024 年名人賽冠軍、2024 年 F1 澳洲站、電影《挑戰者》）在 2024 年是「Claude 不知道的新資訊」，所以需要查維基百科。但新模型的訓練資料比較新，**很可能已經知道這些答案**，就不會呼叫工具了。如果想看到 Claude 使用工具，可以改問比較新的事件（例如「今年的⋯⋯是誰？」），或是在提示詞中要求它「請先查維基百科確認」。
> - 需要 `wikipedia` 套件：`%pip install wikipedia`。

---

在這一課，我們要實作之前介紹過的「完整」4 步驟工具使用流程。到目前為止，我們看過 Claude 使用工具，但我們還沒有送出**包含工具結果的後續請求**給 Claude。這裡複習一下完整的 4 步驟流程：

1. **提供 Claude 工具和使用者提示詞**：（API 請求）
    * 定義你想讓 Claude 使用的一組工具，包括它們的名稱、描述和輸入格式。
    * 提供一個可能需要用到其中一個或多個工具才能回答的使用者提示詞，例如「我用 500 美元可以買幾股通用汽車？」

2. **Claude 使用工具**：（API 回應）
    * Claude 評估使用者的提示詞，判斷可用的工具中有沒有能幫上使用者問題或任務的。如果有，它也會決定要用哪個（哪些）工具、輸入什麼。
    * Claude 輸出一個格式正確的工具使用請求。
    * API 回應的 `stop_reason` 會是 `tool_use`，表示 Claude 想使用一個外部工具。

3. **擷取工具輸入、執行程式碼、回傳結果**：（API 請求）
    * 在客戶端，你要從 Claude 的工具使用請求中擷取出工具名稱和輸入。
    * 在客戶端執行真正的工具程式碼。
    * 繼續這段對話，送出一則包含 `tool_result` 內容區塊的新使用者訊息，把結果回傳給 Claude。

4. **Claude 使用工具結果組織回答**：（API 回應）
    * 收到工具結果之後，Claude 會用這些資訊，針對原本的使用者提示詞組織出最終的回答。

在這一課，我們會完整走過整個流程。

這是整個流程的概覽圖：

![工具使用流程概覽](@orig/images/tool_use_flow.png)

這是說明我們的程式會怎麼運作的圖：

![維基百科搜尋工具的運作圖](@orig/images/wikipedia_diagram.png)

下面是一些真實的對話，展示我們希望達成的最終結果：

> **使用者**：截至 2024 年，克里斯多福·諾蘭和班·史提勒誰拿過比較多座奧斯卡？

> *Claude 想取得克里斯多福·諾蘭的文章*（工具使用）

> *Claude 想取得班·史提勒的文章*（工具使用）

> **Claude**：截至 2024 年，電影導演克里斯多福·諾蘭以 2023 年的電影《奧本海默》贏得了 2 座奧斯卡獎（最佳導演和最佳影片）。另一方面，演員兼喜劇演員班·史提勒到目前為止的職業生涯中還沒有贏過奧斯卡，雖然他贏過艾美獎和 MTV 電影獎等其他獎項。所以直接回答問題：截至 2024 年，克里斯多福·諾蘭贏得的奧斯卡（2 座）比一座都沒有的班·史提勒多。

另一個例子：

> **使用者：** 誰贏得了 2024 年名人賽（Masters Tournament，高爾夫四大賽之一）？

> *Claude 想取得「2024 年名人賽」的文章*（工具使用）

> **Claude：** 史考帝·薛弗勒贏得了 2024 年名人賽，這是他第二次在名人賽奪冠。他以 4 桿的差距領先亞軍路德維格·奧柏格，而奧柏格是第一次參加名人賽。

如果我們問 Claude 一個**不需要**使用工具就能回答的問題，它應該直接回答，不使用我們的維基百科搜尋工具：

> **使用者：** 誰贏得了 2021 年名人賽？

> **Claude：** 松山英樹贏得了 2021 年名人賽，成為第一位贏得高爾夫大滿貫賽的日本男子選手。他以 278 桿（低於標準桿 10 桿）的成績，在奧古斯塔國家高爾夫俱樂部穿上綠夾克。

<details>
<summary>📄 上面三段對話的英文原文</summary>

> **User**: As of 2024 who has more oscars, Christopher Nolan or Ben Stiller?
> *Claude wants to get an article for Christopher Nolan* (tool use)
> *Claude wants to get an article for Ben Stiller* (tool use)
> **Claude**: As of 2024, filmmaker Christopher Nolan has won 2 Academy Awards for Best Director and Best Picture for his 2023 film Oppenheimer. On the other hand, actor and comedian Ben Stiller has not won any Oscars in his career so far, although he has won other awards like Emmys and MTV Movie Awards. So to directly answer the question, as of 2024, Christopher Nolan has won more Oscars (2) than Ben Stiller, who has not won any.

> **User:** Who won the 2024 Masters Tournament?
> *Claude wants to get an article for 2024 Masters Tournament*  (tool use)
> **Claude:** Scottie Scheffler won the 2024 Masters Tournament, his second Masters victory. He finished four strokes ahead of runner-up Ludvig Åberg, who was making his debut at the Masters.

> **User:** Who won the 2021 Masters?
> **Claude:** Hideki Matsuyama won the 2021 Masters Tournament, becoming the first Japanese man to win a major golf championship. He finished with a score of 278 (-10) to claim the green jacket at Augusta National Golf Club.

</details>

這是整個過程結束時，`messages` 串列的樣子：

![流程結束時 messages 串列的樣子](@orig/images/messages_diagram.png)

這一課**最主要的新主題**，是在回應 Claude 的 `tool_use` 訊息時，怎麼正確地排版我們的 `tool_result` 使用者訊息。

---

## 建立完整的流程

### 1. 定義維基百科搜尋函式

在和 Claude 做任何事之前，我們先寫一個簡單的函式來搜尋維基百科。下面的函式使用 `wikipedia` 套件，根據搜尋詞搜尋相符的維基百科頁面。為了簡單起見，我們取第一個回傳的頁面標題，再用它取得對應的頁面內容。

注意：這個簡單的函式**假設**我們一定找得到維基百科文章。為了保持簡短，這個函式沒有任何錯誤處理——在真實世界中這可不是好主意！

> 💡 還沒安裝 `wikipedia` 套件的話，先執行下面這格：

```python run
%pip install wikipedia
```

{{cell 5}}

**逐行解說：**
- `wikipedia.search(search_term)`：搜尋，回傳一串可能的頁面標題。
- `results[0]`：取第一個。
- `wikipedia.page(first_result, auto_suggest=False)`：取得那個頁面（`auto_suggest=False` 代表不要自動「猜」別的標題）。
- `return page.content`：回傳整篇文章的文字。

{{cells 6-7}}

（分別取得「超人」和「千黛亞（Zendaya）」的文章，`article[:500]` 只印出前 500 個字元預覽，因為文章非常長。）

### 2. 撰寫工具定義

接著，我們需要用正確的 JSON Schema 格式定義工具。這是一個非常簡單的工具定義，因為函式只需要一個參數：搜尋詞字串。

{{cell 9}}

（工具名稱 `get_article`，說明「一個取得最新維基百科文章的工具」，只有一個必填的 `search_term`（用標題尋找維基百科文章的搜尋詞）。）

### 3. 提供 Claude 工具和使用者提示詞

接著，我們告訴 Claude 它可以使用維基百科搜尋工具，並問它一個我們知道它**沒有工具就答不出來**的問題，例如「誰贏得了 2024 年名人賽？」

{{cell 11}}

### 4. Claude 使用工具（API 回應）

我們來看看拿回來的回應。Claude 想使用我們的工具！

{{cell 13}}

Claude 的回應包含 **2 個區塊**：

* 一個 **TextBlock（文字區塊）**，文字是「好的，讓我用可用的工具，試著在維基百科上找到 2024 年名人賽冠軍是誰的資訊：」

```
TextBlock(text='Okay, let me use the available tool to try and find information on who won the 2024 Masters Tournament:', type='text')
```

* 一個 **ToolUseBlock（工具使用區塊）**，用 `search_term`「2024 Masters Tournament」呼叫我們的 `get_article` 工具

```
ToolUseBlock(id='toolu_01MbstBxD654o9hE2RGNdtSr', input={'search_term': '2024 Masters Tournament'}, name='get_article', type='tool_use')]
```

### 5. 擷取工具輸入、執行程式碼、回傳結果（API 請求）

既然 Claude 已經回應說它想使用一個工具，現在是時候由我們真正執行背後的功能，**並且**把對應的維基百科頁面內容回傳給 Claude 了。

**我們需要特別注意，確保有更新我們的 `messages` 串列。**

我們先更新 `messages` 串列，加入 Claude 最新的回應：

{{cell 17}}

> 🧩 **白話小補充**：注意這裡是把 **`response.content`（整個內容區塊串列）** 當作 assistant 訊息的 `content`，而不只是文字。因為等一下回傳工具結果時，API 需要看到 Claude 當初的 `tool_use` 區塊（包含它的 `id`）。

{{cell 18}}

接著，我們擷取 Claude 想使用的特定工具和參數：

{{cell 20}}

（程式碼的註解說：「這是一種簡單、但**脆弱**的取得工具使用資訊的方法：我們只是取 Claude 回應的最後一個區塊。」`[-1]` 就是最後一個。）

接著，我們確認 Claude 呼叫的是我們預期的 `get_article` 工具。我們把 Claude 想出的 `search_term` 傳給前面寫的 `get_article` 函式。

{{cell 22}}

我們已經執行了 Claude 想要我們呼叫的函式，現在是時候把維基百科的頁面資料回傳給 Claude 了。

我們知道，當 Claude 想使用工具時，它會回應一個 `stop_reason` 為 `tool_use` 的 API 回應，裡面有一個或多個 `tool_use` 內容區塊，包含：
* **`id`**：這個工具使用區塊的唯一識別碼。之後會用它來**配對**工具結果。
* **`name`**：正在使用的工具名稱。
* **`input`**：一個物件，包含要傳給工具的輸入，符合工具的 `input_schema`。

執行完背後的工具函式之後，我們也需要用一個特定的格式回應 Claude。具體來說，要繼續這段對話，我們需要送出一則**角色為 `user`** 的新訊息，裡面有一個**類型為 `tool_result`** 的內容區塊，並包含下面這些資訊：
* **`tool_use_id`**：這個結果所對應的工具使用請求的 `id`。
* **`content`**：工具的結果，可以是一個字串（例如 `"content": "15 degrees"`），或是巢狀內容區塊的串列（例如 `"content": [{"type": "text", "text": "15 degrees"}]`）。
* **`is_error`**（選填）：如果工具執行時發生錯誤，就設為 `true`。

下面是一則格式正確的 `tool_result` 訊息的樣子：

```python
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "The result of actually calling the tool goes here"
    }
  ]
}
```

（`"content"` 的意思是「真正呼叫工具得到的結果放在這裡」。原課程把這段放成程式碼格，執行它只會顯示這個字典，沒有其他作用，新手版改成只顯示。）

> 🧩 **白話小補充：為什麼工具結果是用 `user` 角色？** 因為從 Claude 的角度來看，對話只有兩方：它自己（assistant）和「外面的世界」（user）。工具的結果是從外面送進來的，所以用 `user` 角色。而 `tool_use_id` 就像「取件編號」，讓 Claude 知道這份結果是回覆它哪一次的工具請求。

我們現在就為維基百科搜尋的例子這樣做。我們需要組出一則結構正確的工具回應訊息，把維基百科的搜尋結果回傳給 Claude：

{{cell 26}}

{{cell 27}}

（註解：「注意那很長的維基百科文章內容！」）

接著，我們需要把 `tool_response` 訊息加進 messages 串列：

{{cell 29}}

我們的 `messages` 串列現在長這樣：

* **User（使用者）**：誰贏得了 2024 年名人賽？
* **Assistant（Claude）**：我想用 `search_term`「2024 Masters Tournament」使用 `get_article` 工具
* **User（使用者）**：這是工具的結果，包含你要的維基百科文章

下面這張圖說明了這一點。

![messages 串列的三則訊息](@orig/images/wiki_messages.png)

注意，一開始的 `id` 和我們後續使用者訊息中的 `tool_use_id` 是**一樣的**。

### 6. Claude 使用工具結果組織回答（API 回應）

最後，我們用更新後的 `messages` 串列，送出一個新的請求給 Claude：

{{cell 32}}

{{cell 33}}

Claude 現在有了回答最初問題所需的資訊，並回應：

> 'Based on the Wikipedia article summary, it appears that Scottie Scheffler won the 2024 Masters Tournament. He shot a final round...'
>（「根據維基百科文章的摘要，看起來是史考帝·薛弗勒贏得了 2024 年名人賽。他在最後一輪打出⋯⋯」）

我們現在已經完成了流程的全部 4 個步驟！

---

## 改善程式碼

最起碼，我們大概會想把上面所有的程式碼放進一個**可以重複使用的函式**，這樣才能多試幾次：

{{cell 37}}

**逐行解說（重點）：**
- 第一次呼叫 Claude（帶上工具）。
- `if(response.stop_reason == "tool_use"):`：如果 Claude 想用工具：
  - 取出最後一個區塊（工具使用）的 `name` 和 `input`。
  - 把 Claude 的回應加進 messages（註解：「把 Claude 的工具使用呼叫加進 messages」）。
  - 如果是 `get_article`：取得維基百科文章（註解：「取得維基百科文章內容」）、組出 `tool_result` 訊息（註解：「建立我們的 tool_result 訊息」）、加進 messages、**再呼叫一次 Claude**（註解：「回應 Claude」），印出最終答案。
- `else:`：Claude 沒有呼叫工具，直接印出它的回答。

{{cells 38-39}}

（「誰贏得了 2024 年 F1 澳洲大獎賽」、「誰主演電影《挑戰者》？」——原課程的輸出顯示「Claude want to」、「Final Answer」，和程式碼裡的文字略有不同，是更早版本的程式碼跑出來的，不影響理解。）

{{cell 40}}

（註解：「我們來試一個 Claude **不需要**我們的工具就能回答的例子：」——「誰寫了《少年 Pi 的奇幻漂流》這本書？」）

注意，Claude 在回答最後這個問題時呼叫了我們的維基百科工具，**即使 Claude 早就知道答案了**。《少年 Pi 的奇幻漂流》是 2001 年出版的，遠早於 Claude 的訓練資料截止日！

---

## 改善我們的提示詞

就像我們在之前的課程看到的，有時候 Claude **太熱衷於使用工具**了。一個簡單的修正方法是透過系統提示詞。

我們可以加入一個像這樣的系統提示詞：

{{cell 44}}

**翻譯**：「使用者會問你一個問題。如果回答這個問題需要你**沒有受過訓練的資料**，你可以使用 get_article 工具，取得一篇關於這個主題的最新維基百科文章內容。如果你不需要取得更多資訊就能回答這個問題，就請直接回答。**只在需要時呼叫工具。**」

我們來更新函式，使用這個新的系統提示詞：

{{cell 46}}

（和之前的函式一樣，只是兩次呼叫 Claude 都多了 `system=system_prompt`。）

我們來問同樣的問題：

{{cell 48}}

成功了！Claude 在不需要的時候沒有使用我們的工具。我們來確認它在回答**需要**最新知識的問題時，仍然能正常運作：

{{cell 50}}

（「誰為電影《挑戰者》寫了配樂？」→ 查了維基百科，回答是 Trent Reznor 和 Atticus Ross。）

兩種情況都如預期運作！現在我們來讓 Claude 的回答**簡潔一點**。Claude 解釋它是**怎麼**得出正確答案的很好，但有點太囉嗦了。我們來做一點基本的提示詞工程修正它。

我們試試這樣：

{{cell 52}}

（「回答下面這個問題 `<question>誰寫了電影《可憐的東西》？</question>`。當你能回答這個問題時，**盡量讓答案越短越好，並用 `<answer>` 標籤包起來**。」）

這是使用新提示詞更新後的函式：

{{cell 54}}

{{cells 55-56}}

（「誰為電影《挑戰者》寫了配樂？」→ `<answer>電影《挑戰者》的配樂是由 Trent Reznor 和 Atticus Ross 創作的。</answer>`；「章魚有幾條腿？」→ 不用工具，`<answer>章魚有 8 條腿。</answer>`）

好多了！Claude 現在回答時，不會附上一堆額外的「思考」和它怎麼得出答案的解釋了。

---

## ✏️ 練習

你能更新這段程式碼，讓它符合下面這些要求嗎：

* Claude 可能沒辦法從我們回傳的**第一篇**維基百科頁面得到足夠的資訊。我們還沒處理這種情況。想像我們問 Claude「克里斯多福·諾蘭有幾座奧斯卡？他的奧斯卡數量有比班·史提勒的艾美獎數量多嗎？」Claude 需要搜尋克里斯多福·諾蘭的維基百科頁面**和**班·史提勒的頁面，很可能是一個接一個搜尋。我們的程式碼目前不允許這樣，所以我們來加入這個功能！**提示：用迴圈！**
* 從 Claude 目前回應的 `<answer></answer>` 標籤中**擷取出答案**，這樣你只印出真正的答案內容。
* 你能把它變成一個完整的**命令列聊天機器人**，持續請使用者輸入問題，然後一次又一次地回答，直到使用者結束程式嗎？輸出可能會像這樣：

這是一段範例對話的截圖：

![練習：命令列聊天機器人的範例對話](@orig/images/exercise_conversation.png)

```python run
# 在這裡寫你的答案

```

<details>
<summary>👀 點這裡看參考答案（新手版補充，原課程沒有提供答案）</summary>

```python
import re

def answer_question_with_loop(question):
    system_prompt = """
    You will be asked a question by the user.
    If answering the question requires data you were not trained on, you can use the get_article tool to get the contents of a recent wikipedia article about the topic.
    If you can answer the question without needing to get more information, please do so.
    Only call the tool when needed.
    """
    prompt = f"""
    Answer the following question <question>{question}</question>
    When you can answer the question, keep your answer as short as possible and enclose it in <answer> tags
    """
    messages = [{"role": "user", "content": prompt}]

    while True:   # 一直重複，直到 Claude 不再需要工具
        response = client.messages.create(
            model="claude-sonnet-4-6",
            system=system_prompt,
            messages=messages,
            max_tokens=1000,
            tools=[article_search_tool],
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            break   # Claude 已經可以回答了，跳出迴圈

        # Claude 可能一次要求好幾個工具呼叫，全部處理，並把結果放在「同一則」user 訊息裡
        tool_results = []
        for block in response.content:
            if block.type == "tool_use" and block.name == "get_article":
                search_term = block.input["search_term"]
                print(f"Claude 想查維基百科：{search_term}")
                try:
                    content = get_article(search_term)
                    tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": content})
                except Exception as e:
                    tool_results.append({"type": "tool_result", "tool_use_id": block.id,
                                         "content": f"Error: {e}", "is_error": True})
        messages.append({"role": "user", "content": tool_results})

    # 取出最後回答裡的文字，再擷取 <answer> 標籤中的內容
    final_text = "".join(block.text for block in response.content if block.type == "text")
    match = re.search(r"<answer>(.*?)</answer>", final_text, re.DOTALL)
    return match.group(1).strip() if match else final_text

# 命令列聊天機器人
while True:
    user_question = input("你的問題（輸入 quit 結束）：")
    if user_question.lower() == "quit":
        print("掰掰！")
        break
    print("Claude：", answer_question_with_loop(user_question))
```

**重點說明：**
- 用 `while True` 迴圈：只要 `stop_reason` 還是 `"tool_use"`，就執行工具、回傳結果、再問一次 Claude。
- 每一輪都把 Claude 的回應和工具結果加進 `messages`，對話紀錄才完整。
- 如果 Claude 一次要求多個工具呼叫，所有 `tool_result` 要放在**同一則** user 訊息裡回傳。
- 工具出錯時，回傳 `"is_error": True` 讓 Claude 知道，而不是讓程式當掉。

</details>

---

## 📌 重點整理

- 完整流程的關鍵是**維護好 `messages` 串列**：
  1. `{"role": "user", "content": 問題}`
  2. `{"role": "assistant", "content": response.content}` ← 整個內容區塊串列（含 `tool_use`）
  3. `{"role": "user", "content": [{"type": "tool_result", "tool_use_id": ..., "content": 結果}]}`
  4. 再呼叫一次 Claude → 得到最終回答
- `tool_result` 三個欄位：`tool_use_id`（**一定要和 `tool_use` 的 `id` 相同**）、`content`（結果，字串或內容區塊串列）、`is_error`（選填）。
- 用系統提示詞「只在需要時呼叫工具」，避免 Claude 不必要地使用工具。
- 用 `<answer>` 標籤 + 「答案越短越好」讓回答簡潔。
- 如果 Claude 可能需要多次使用工具，就用**迴圈**一直處理，直到 `stop_reason` 不是 `"tool_use"`。

👉 下一課：[5-5 工具選擇（tool choice）](05_tool_choice.md)
