<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
# 0-2 什麼是 API？什麼是大型語言模型？

> 🎯 **讀完這一頁，你會知道：** API、大型語言模型（LLM）、提示詞（prompt）、token、SDK、API 金鑰這些詞到底是什麼意思。這些是整套課程最常出現的名詞，先把它們搞懂，後面會輕鬆很多。

---

## 1. 大型語言模型（LLM）是什麼？

**大型語言模型**（Large Language Model，簡稱 **LLM**）是一種讀過超大量文字的 AI 程式。
它最擅長的事情是：**看了前面的文字，猜出接下來最適合的文字。**

把這件事做到極致，它就能：回答問題、寫文章、翻譯、寫程式、摘要、分類⋯⋯

**Claude** 就是 Anthropic 公司做的大型語言模型。Claude 有好幾個「型號」（模型），就像手機有不同等級：

| 型號家族 | 特色（比喻） |
|---|---|
| **Haiku** | 小而快、最便宜。像「機車」：靈活、省油。 |
| **Sonnet** | 速度和聰明度平衡。像「轎車」。 |
| **Opus** | 最聰明但比較慢、比較貴。像「大卡車」：載得多但耗油。 |

> 🧩 **白話小補充**：Haiku（俳句）、Sonnet（十四行詩）、Opus（大型作品）都是文學作品的長度名稱，越後面越長、越大。

---

## 2. API 是什麼？

**API**（Application Programming Interface，應用程式介面）可以想成**餐廳的點餐窗口**：

- 你（程式）不需要知道廚房（Claude 的伺服器）裡面怎麼煮菜。
- 你只要照**規定的格式**填好點餐單（**請求 request**），交給窗口。
- 窗口就會把做好的菜（**回應 response**）交給你。

```
你的 Python 程式  ──(請求：我想問 Claude 一個問題)──▶  Anthropic 的伺服器（Claude 在這裡）
你的 Python 程式  ◀──(回應：Claude 的回答)──────────  Anthropic 的伺服器
```

「**Claude API**」就是 Anthropic 開放給大家、讓程式可以傳訊息給 Claude 的那個窗口。

---

## 3. API 金鑰（API Key）是什麼？

點餐窗口不會讓陌生人隨便點餐——它要知道「這筆帳要算誰的」。
**API 金鑰**就是一長串像密碼一樣的文字（例如 `sk-ant-api03-...`），每次請求都要附上，證明「是我在用，帳單請寄給我」。

> ⚠️ **注意**：API 金鑰 = 你的信用卡。**絕對不要**貼到網路上、傳給別人、或上傳到 GitHub。別人拿到就可以用你的錢呼叫 Claude。

---

## 4. SDK 是什麼？

你可以自己手動照格式寫「點餐單」傳給 API，但很麻煩。
**SDK**（Software Development Kit，軟體開發工具包）就是官方幫你包裝好的「點餐小幫手」。

Anthropic 提供的 Python SDK 套件名稱叫做 **`anthropic`**。裝好之後，只要幾行程式就能跟 Claude 對話：

```python
from anthropic import Anthropic   # 把點餐小幫手拿出來
client = Anthropic()               # 建立一個「客戶端」（會自動帶上你的 API 金鑰）
response = client.messages.create( # 送出點餐單
    model="claude-haiku-4-5",      # 要哪一個模型
    max_tokens=1000,               # 回答最長多少
    messages=[{"role": "user", "content": "你好！"}]  # 你要說的話
)
print(response.content[0].text)    # 把 Claude 的回答印出來
```

現在看不懂沒關係，第 1 單元第 1 課就會一步一步教。

---

## 5. 提示詞（Prompt）是什麼？

**提示詞（prompt）**就是你傳給 Claude 的文字——你的問題、指令、資料。
同樣的問題，**換個問法**，Claude 的回答品質可能差很多。
研究「怎麼寫提示詞才能得到最好的回答」，就叫做**提示詞工程（prompt engineering）**。這是第 2、3 單元的主題。

---

## 6. Token 是什麼？

LLM 不是一個字一個字讀文字的，而是把文字切成一小塊一小塊，每一塊叫做一個 **token**（可以翻成「詞元」）。

- 英文裡，一個 token 大約是 3～4 個字母，大概是 3/4 個英文單字。
- 中文裡，一個中文字通常是 1～2 個 token。

**為什麼要在意 token？**
1. **計費**：API 是用 token 數量算錢的（你送進去的 token + Claude 回答的 token）。
2. **長度限制**：每次請求能處理的 token 數量有上限。
3. **`max_tokens` 參數**：你可以規定 Claude 的回答最多幾個 token，超過就會被切斷。

---

## 7. 「回合」與「角色」

跟 Claude 的對話是由一則一則**訊息**組成的，每則訊息有一個**角色（role）**：

- **`user`（使用者）**：你說的話。
- **`assistant`（助理）**：Claude 說的話。

另外還有一個特別的 **`system`（系統提示詞）**，用來給 Claude「背景設定」，例如「你是一位很有耐心的數學老師」。

這些在第 1 單元第 2 課會詳細教。

---

## 8. 整套課程會用到的工具一覽

| 工具 | 是什麼 | 在哪裡會用到 |
|---|---|---|
| **Python** | 一種程式語言，語法接近英文，很適合新手 | 全部 |
| **Jupyter Notebook**（`.ipynb`） | 一種「可以邊寫說明、邊執行程式」的筆記本 | 全部 |
| **`anthropic` 套件** | 官方 Python SDK | 全部 |
| **`python-dotenv` 套件** | 從 `.env` 檔案讀取 API 金鑰 | 第 1 單元起 |
| **Anthropic Console**（主控台） | Anthropic 的網站後台，可以申請 API 金鑰、試用提示詞 | 第 1、3、4 單元 |
| **Node.js / npx / promptfoo** | 一個用來「自動評估提示詞」的工具 | 第 4 單元第 5 課以後 |

---

## 📌 重點整理

- **LLM** = 讀過大量文字、很會「接話」的 AI。**Claude** 是其中一個。
- **API** = 程式跟 Claude 溝通的「點餐窗口」；**SDK**（`anthropic` 套件）= 幫你填點餐單的小幫手。
- **API 金鑰** = 證明身分 + 計費用的密碼，**不能外流**。
- **提示詞** = 你傳給 Claude 的文字；**token** = 文字切成的小塊，用來計費和限制長度。
- 訊息有 `user`（你）和 `assistant`（Claude）兩種角色，還有 `system` 系統提示詞。

👉 下一課：[0-3 準備你的電腦](03_setup_your_computer.md)
