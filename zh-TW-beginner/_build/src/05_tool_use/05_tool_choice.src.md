<!--meta {"orig": "tool_use/05_tool_choice.ipynb", "out": "05_tool_use/05_tool_choice"} -->
# 5-5 工具選擇（Tool choice）

> 📚 **第 5 單元：工具使用**｜第 5 課 / 共 6 課
> ⏱️ 預估時間：40 分鐘

## 🎯 這一課你會學到

- `tool_choice` 參數的三種設定：**`auto`**（自己決定）、**`any`**（一定要用某個工具，但可以自己挑）、**`tool`**（一定要用指定的工具）
- 每一種設定適合什麼情況
- 用 `auto` 時，**提示詞寫得好不好**影響很大

> 🔄 **2026 更新**：
> - 這一課原本使用 `claude-3-sonnet-20240229`，新手版換成 `claude-sonnet-4-6`（它支援全部三種 `tool_choice`）。
> - ⚠️ **最新一代的部分模型（例如 Opus 5.5、Sonnet 5.5、Fable 5.1 / 5.2）不支援 `{"type": "any"}` 和 `{"type": "tool", ...}`**，會回傳錯誤；在那些模型上只能用 `{"type": "auto"}`（或 `{"type": "none"}`，禁止使用工具），並在提示詞裡明確要求使用哪個工具。學完這一課的觀念之後，做自己的專案時請留意這一點。
> - 原課程的範例問題（2024 年的比賽）對新模型來說可能已經是「已知的過去」，所以 Claude 可能不會呼叫搜尋工具，這是正常的。

---

Claude API 支援一個叫做 **`tool_choice`** 的參數，讓你指定希望 Claude **怎麼**呼叫工具。在這份 notebook 中，我們會看看它是怎麼運作的，以及什麼時候該使用它。

使用 `tool_choice` 參數時，有三種可能的選項：

* **`auto`**：讓 Claude 自己決定要不要呼叫任何提供的工具。
* **`any`**：告訴 Claude 它**必須**使用其中一個提供的工具，但不強制是哪一個。
* **`tool`**：讓我們能強制 Claude **永遠**使用某個特定的工具。

這張圖說明了每個選項是怎麼運作的：

![三種 tool_choice 的比較圖](@orig/images/tool_choice.png)

> 🧩 **白話小補充：用「點餐」比喻**
> - `auto`：「想點什麼都可以，不點也行。」
> - `any`：「一定要點一樣東西，菜單上隨你挑。」
> - `tool`：「你一定要點這道菜。」

我們來詳細看看每個選項。先從匯入 Anthropic SDK 開始：

> 💡 **新手版補充**：原課程這一格沒有讀取 `.env`，如果你的 API 金鑰是存在 `.env` 檔裡，請先執行下面這格：

```python run
from dotenv import load_dotenv
load_dotenv()   # 從 .env 讀取 ANTHROPIC_API_KEY
```

{{cell 2}}

---

## Auto（自動）

把 `tool_choice` 設成 `auto`，讓模型自動決定要不要使用工具。**如果你完全不使用 `tool_choice` 參數，這就是使用工具時的預設行為。**

為了示範這一點，我們要提供 Claude 一個**假的網路搜尋工具**。我們會問 Claude 一些問題，其中有些需要呼叫網路搜尋工具，有些則是 Claude 應該能自己回答的。

我們先定義一個叫做 `web_search` 的工具。請注意：為了讓示範保持簡單，我們這裡**並沒有真的上網搜尋**。

{{cell 4}}

（`web_search` 函式只會印出「假裝在網路上搜尋 {topic}」。工具說明：「一個透過搜尋網路，取得某個主題最新資訊的工具」，參數 `topic` 是「要在網路上搜尋的主題」。）

接著，我們寫一個函式：接收一個 `user_query`（使用者問題），把它和 `web_search_tool` 一起傳給 Claude。

我們也把 `tool_choice` 設成 `auto`：

```python
tool_choice={"type": "auto"}
```

這是完整的函式：

{{cell 8}}

**逐行解說：**
- `from datetime import date`：匯入日期工具。
- 系統提示詞（翻譯）：「盡可能用你現有的知識回答問題。只在你**沒辦法有信心地回答**的問題上搜尋網路。今天的日期是 {今天日期}。如果你認為使用者的問題涉及**還沒發生的未來**的事情，就使用搜尋工具。」
  - `date.today().strftime("%B %d %Y")`：把今天的日期排成像「November 23 2026」的格式。告訴 Claude 今天幾號，它才能判斷哪些事是「最近的」。
- `tool_choice={"type": "auto"}`：讓 Claude 自己決定。
- `last_content_block = response.content[-1]`：看回應的最後一個區塊：
  - 如果是 `"text"`：Claude 沒有呼叫工具，印出它的回答。
  - 如果是 `"tool_use"`：Claude 想用工具，印出工具使用區塊。

我們先從一個 Claude 應該不需要工具就能回答的問題開始：

{{cell 10}}

（「天空是什麼顏色？」）

當我們問「天空是什麼顏色？」，Claude 沒有使用工具。我們來問一個 Claude 應該使用網路搜尋工具才能回答的問題：

{{cell 12}}

（「誰贏得了 2024 年邁阿密大獎賽（F1）？」）

當我們問「誰贏得了 2024 年邁阿密大獎賽？」，Claude 使用了網路搜尋工具！

我們再試幾個例子：

{{cells 14-15}}

（「誰贏得了 2022 年超級盃？」→ 不需要工具，直接回答洛杉磯公羊隊；「誰贏得了 2024 年超級盃？」→ 使用工具。）

### 提示詞很重要！

把 `tool_choice` 設成 `auto` 時，花時間寫一個詳細的提示詞是很重要的。Claude 常常會**太熱衷於呼叫工具**。寫一個詳細的提示詞，能幫助 Claude 判斷什麼時候該呼叫工具、什麼時候不該。在上面的例子中，我們在系統提示詞裡加入了具體的指示：

```python
system_prompt=f"""
    Answer as many questions as you can using your existing knowledge.  
    Only search the web for queries that you can not confidently answer.
    Today's date is {date.today().strftime("%B %d %Y")}
    If you think a user's question involves something in the future that hasn't happened yet, use the search tool.
"""
```

---

## 強制使用特定的工具

我們可以用 `tool_choice` 強制 Claude 使用某個特定的工具。在下面的例子中，我們定義了兩個簡單的工具：
* **`print_sentiment_scores`**：一個「騙」Claude 產生結構良好的 JSON 輸出（包含情緒分析資料）的工具。想了解更多這個方法，請參考 Anthropic Cookbook 中的[使用 Claude 和工具使用擷取結構化 JSON](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/extracting_structured_json.ipynb)。（也就是 [5-3 課](03_structured_outputs.md)教的技巧。）
* **`calculator`**：一個非常簡單的計算機工具，接收兩個數字並把它們相加。

{{cell 20}}

我們的目標是寫一個叫做 `analyze_tweet_sentiment` 的函式：接收一則推文，用 Claude 印出這則推文的基本情緒分析。最終我們會「強制」Claude 使用 `print_sentiment_scores` 工具，但我們先展示**沒有**強制使用工具時會發生什麼事。

在這個第一個「爛」版本的 `analyze_tweet_sentiment` 函式中，我們提供 Claude 兩個工具。為了比較，我們先把 `tool_choice` 設成 `auto`：

```python
tool_choice={"type": "auto"}
```

請注意，我們**刻意**沒有提供 Claude 寫得很好的提示詞，這樣比較容易看出「強制使用特定工具」的效果。

{{cell 24}}

（使用者訊息就直接是推文本身，沒有任何說明。）

我們來看看用這則推文呼叫函式會發生什麼事：`Holy cow, I just made the most incredible meal!`（天啊，我剛做出了史上最棒的一餐！）

{{cell 26}}

Claude 沒有呼叫我們的 `print_sentiment_scores` 工具，而是直接回應：
> "That's great to hear! I don't actually have the capability to assess sentiment from text, but it sounds like you're really excited and proud of the incredible meal you made
>（太棒了！我其實沒有評估文字情緒的能力，但聽起來你對你做出的那一餐感到非常興奮和自豪⋯⋯）

接著，想像有人發了這則推文：`I love my cats! I had four and just adopted 2 more! Guess how many I have now?`（我愛我的貓！我原本有四隻，剛剛又領養了 2 隻！猜猜我現在有幾隻？）

{{cell 28}}

Claude 想呼叫**計算機**工具：

> ToolUseBlock(id='toolu_staging_01RFker5oMQoY6jErz5prmZg', input={'num1': 4, 'num2': 2}, name='calculator', type='tool_use')

很明顯，目前的實作沒有做到我們想要的（主要是因為我們故意讓它失敗）。

所以，我們來更新 `tool_choice`，強制 Claude **永遠**使用 `print_sentiment_scores` 工具：

```python
tool_choice={"type": "tool", "name": "print_sentiment_scores"}
```

除了把 `type` 設成 `tool` 之外，我們還**必須**提供一個特定的工具名稱。

{{cell 33}}

現在，如果我們用之前同樣的提示詞問 Claude，它**一定**會呼叫 `print_sentiment_scores` 工具：

{{cell 35}}

Claude 呼叫了我們的 `print_sentiment_scores` 工具：

> ToolUseBlock(id='toolu_staging_01FMRQ9pZniZqFUGQwTcFU4N', input={'positive_score': 0.9, 'negative_score': 0.0, 'neutral_score': 0.1}, name='print_sentiment_scores', type='tool_use')

就算我們試著用一則「跟數學有關」的推文來誤導 Claude，它還是一定會呼叫 `print_sentiment_scores` 工具：

{{cell 37}}

即使我們已經強制 Claude 呼叫 `print_sentiment_scores` 工具，我們還是應該用一些基本的提示詞工程，給 Claude 更好的任務背景：

{{cell 39}}

（提示詞改成：「分析下面這則推文的情緒：`<tweet>{query}</tweet>`」。）

> ⚠️ **小提醒**：這個「加上更好提示詞」的版本裡，原課程把 `tool_choice` 寫成了 `{"type": "auto"}`。依照上下文，作者的意思應該是**同時**使用強制工具 `{"type": "tool", "name": "print_sentiment_scores"}` 和更好的提示詞。你可以自己改成強制工具的版本試試看。

---

## Any（任一）

`tool_choice` 的最後一個選項是 **`any`**，它讓我們告訴 Claude：「**你必須呼叫一個工具，但你可以選擇是哪一個。**」想像我們要用 Claude 做一個**簡訊（SMS）聊天機器人**。這個聊天機器人唯一能真正和使用者「溝通」的方式，就是透過簡訊。

在下面的例子中，我們做了一個非常簡單的簡訊助理，它可以使用兩個工具：
* **`send_text_to_user`**：傳一則簡訊給使用者。
* **`get_customer_info`**：根據使用者名稱查詢顧客資料。

我們的想法是打造一個**一定會呼叫其中一個工具、永遠不會用非工具方式回應**的聊天機器人。在所有情況下，Claude 都應該要嘛試著傳簡訊回覆，要嘛呼叫 `get_customer_info` 取得更多顧客資訊。為了確保這一點，我們把 `tool_choice` 設成 `any`：

```python
tool_choice={"type": "any"}
```

{{cell 43}}

**逐行解說：**
- `send_text_to_user(text)`：傳簡訊給使用者（註解說：為了簡單起見，我們只是把簡訊印出來）。
- `get_customer_info(username)`：回傳一個假的顧客資料（使用者名稱、email、三筆購買紀錄：滑鼠、螢幕保護貼、USB 充電線）。
- 兩個工具的定義。`get_customer_info` 的說明特別寫了：「根據顧客的使用者名稱取得顧客資訊。回應包含 email、使用者名稱和過去的購買紀錄。**只在使用者提供了他的使用者名稱之後，才呼叫這個工具。**」
- 系統提示詞（翻譯）：「你和使用者的所有溝通都是透過簡訊進行的。只在你有足夠的資訊可以準確呼叫工具時才呼叫工具。在使用者提供他的使用者名稱之前，不要呼叫 get_customer_info 工具。這很重要。如果你不知道使用者的使用者名稱，就直接問使用者。」
- `sms_chatbot(user_message)`：
  - `tool_choice={"type": "any"}`：一定要用一個工具。
  - 如果 Claude 想用 `send_text_to_user`，就「傳簡訊」（印出來）；如果想用 `get_customer_info`，就印出查到的資料。
  - 如果 `stop_reason` 不是 `tool_use`，印出「沒有呼叫工具。這不應該發生！」

我們從簡單的開始：

{{cell 45}}

（「嘿！你好嗎？」→ Claude 用 `send_text_to_user` 回覆：「哈囉！我很好，謝謝關心。今天有什麼可以幫你的嗎？」）

Claude 用呼叫 `send_text_to_user` 工具的方式回應。

接著，我們問 Claude 一個比較難一點的問題：

{{cell 47}}

（「我需要幫忙查一筆訂單」）

Claude 想傳一則簡訊，請使用者提供他的使用者名稱。

現在，我們來看看提供使用者名稱給 Claude 時會發生什麼事：

{{cell 49}}

（「我需要幫忙查一筆訂單。我的使用者名稱是 jenny76」）

Claude 呼叫了 `get_customer_info` 工具，正如我們所希望的！

就算我們傳給 Claude 一則亂碼訊息，它還是會呼叫我們的其中一個工具：

{{cell 51}}

（Claude 傳簡訊：「恐怕我沒聽懂你的問題。可以請你換個方式說明你需要什麼幫助嗎？」）

---

## 📌 重點整理

| `tool_choice` | 寫法 | 意思 | 適合的情況 |
|---|---|---|---|
| `auto`（預設） | `{"type": "auto"}` | Claude 自己決定要不要用工具 | 一般聊天機器人；要搭配**寫得好的提示詞**，避免亂用工具 |
| `any` | `{"type": "any"}` | 一定要用工具，但可以自己挑哪一個 | 所有回覆都必須透過工具送出（例如簡訊機器人） |
| `tool` | `{"type": "tool", "name": "工具名稱"}` | 一定要用指定的工具 | 強制取得結構化輸出（例如情緒分析 JSON） |

- 即使強制使用工具，仍然建議寫好提示詞，給 Claude 清楚的任務背景。
- 🔄 最新的部分模型只支援 `auto`（和 `none`），強制用法要改成提示詞或結構化輸出。

👉 下一課：[5-6 打造有多個工具的聊天機器人](06_chatbot_with_multiple_tools.md)
