# 📖 名詞小辭典

> 整套課程會出現的專有名詞，用白話解釋。依照「主題」分類，每個名詞後面標註它主要出現在哪一課。
> 找不到想查的詞？用瀏覽器的「尋找」功能（`Ctrl + F` 或 `Command + F`）搜尋看看。

[回到課程首頁](README.md)

---

## 🤖 AI 與 Claude 基本概念

| 名詞 | 白話解釋 | 出現在 |
|---|---|---|
| **LLM（大型語言模型）** | 讀過超大量文字、很會「接話」的 AI 程式。Claude 就是一個 LLM。 | 0-2 |
| **Claude** | Anthropic 公司開發的 LLM。有 Haiku（小、快、便宜）、Sonnet（平衡）、Opus（最聰明）等型號。 | 0-2、1-3 |
| **模型（model）** | Claude 的不同「型號」，在程式裡用一串名稱指定，例如 `claude-haiku-4-5`。 | 1-3 |
| **提示詞（prompt）** | 你傳給 Claude 的文字：問題、指示、資料。 | 0-2 |
| **提示詞工程（prompt engineering）** | 研究「怎麼寫提示詞才能得到最好的回答」的方法，講究精確、可重複、持續測試改進。 | 第 2、3 單元 |
| **token（詞元）** | LLM 處理文字的最小單位，大約是一個英文單字的 3/4，或 1～2 個中文字。計費和長度限制都以 token 計算。 | 0-2、1-4 |
| **上下文視窗（context window）** | Claude 一次能讀進去的文字量上限（以 token 計）。 | 3-1 |
| **幻覺（hallucination）** | AI 一本正經地說出錯誤或編造的內容。 | 2-8 |
| **訓練資料截止日（training cutoff）** | 模型「學到的知識」的最後日期，之後發生的事它不知道。 | 5-2、5-4 |
| **基準測試（benchmark）** | AI 世界的標準化考試（例如 MMLU），用來比較模型的一般能力。 | 4-1 |
| **延遲（latency）** | 從送出問題到收到回答要等多久。 | 1-3 |
| **延伸思考（extended thinking）** | 新一代模型內建的功能：先在內部思考，再給出答案。 | 2-6、5-6 |

## 🔌 API 與程式相關

| 名詞 | 白話解釋 | 出現在 |
|---|---|---|
| **API** | 程式和服務溝通的「點餐窗口」：照規定的格式送出請求，就能拿到回應。 | 0-2 |
| **API 金鑰（API key）** | 證明身分、用來計費的一串密碼。**絕對不能外流。** | 0-3、1-1 |
| **SDK** | 官方提供、幫你方便使用 API 的工具包。Anthropic 的 Python SDK 叫 `anthropic`。 | 0-2、1-1 |
| **客戶端（client）** | 用 SDK 建立的物件（`client = Anthropic()`），所有對 Claude 的請求都透過它送出。 | 1-1 |
| **請求（request）／回應（response）** | 你送給 API 的東西／API 回傳給你的東西。 | 0-2 |
| **Messages API** | Claude 目前主要的 API，用 `client.messages.create(...)` 呼叫。 | 1-2、2-1 |
| **`messages`** | 對話內容，是「裝著字典的串列」，每則訊息有 `role` 和 `content`。 | 1-2 |
| **`role`（角色）** | 訊息是誰說的：`"user"`（使用者）或 `"assistant"`（Claude）。 | 1-2 |
| **`content`（內容）** | 訊息的內容，可以是字串，或「內容區塊」的串列。 | 1-2、1-6 |
| **內容區塊（content block）** | 回應或訊息中的一塊內容，有不同類型：`text`（文字）、`image`（圖片）、`tool_use`（工具使用）、`tool_result`（工具結果）⋯⋯ | 1-2、1-6、5-2 |
| **系統提示詞（system prompt）** | 用 `system` 參數給 Claude 的背景設定，例如角色、語氣。 | 1-4、2-1 |
| **`max_tokens`** | Claude 的回答最多幾個 token，超過會被切斷。 | 1-4 |
| **`temperature`（溫度）** | 0～1，控制回答的隨機性。越低越穩定，越高越有創意。最新模型已不支援。 | 1-4 |
| **`stop_sequences`（停止序列）** | 指定一些字串，Claude 一寫出來就停下。 | 1-4 |
| **`stop_reason`** | Claude 停下來的原因：`end_turn`（說完了）、`max_tokens`（被切斷）、`stop_sequence`（碰到停止序列）、`tool_use`（想用工具）。 | 1-4、5-2 |
| **`usage`** | 回應中記錄 token 用量的資訊：`input_tokens`、`output_tokens`。 | 1-2 |
| **串流（streaming）** | Claude 一邊產生一邊傳送回答，不用等全部寫完。 | 1-5 |
| **TTFT（第一個 token 的等待時間）** | 從送出請求到收到第一個字的時間。串流可以大幅縮短 TTFT。 | 1-5 |
| **事件（event）／SSE** | 串流時伺服器一筆一筆推送過來的資料，例如 `content_block_delta`。 | 1-5 |
| **非同步（async）** | 一種讓程式在等待時可以先做別的事的寫法（`async`/`await`）。 | 1-5 |
| **base64** | 把圖片等二進位資料轉成一串英文字母和數字的方法，才能放進文字訊息裡傳送。 | 1-6 |
| **MIME 類型（media type）** | 檔案種類的標準寫法，例如 `image/png`、`image/jpeg`。 | 1-6 |
| **多模態（multimodal）** | 不只一種形式的資料，例如「文字 + 圖片」。 | 1-6 |
| **錯誤代碼 400／401／404／429／529** | 400：請求格式錯誤；401：金鑰錯誤；404：找不到（例如模型名稱錯誤）；429：太頻繁；529：伺服器太忙。 | 0-3 |

## ✍️ 提示詞技巧

| 名詞 | 白話解釋 | 出現在 |
|---|---|---|
| **XML 標籤** | 像 `<email>...</email>` 這樣成對的標籤，用來把資料、指示、範例分開，或規定輸出格式。名稱可以自己取。 | 2-4、2-5 |
| **提示詞範本（prompt template）** | 固定的指示骨架 + 用 `{變數}` 標示的空格，每次填入不同的資料。 | 2-4 |
| **角色提示（role prompting）** | 請 Claude 扮演某個角色（例如「你是資深律師」）。 | 2-3 |
| **prefill（預先填寫回答／幫 Claude 開口）** | 在最後一則 `assistant` 訊息先寫好開頭，Claude 會接著寫。最新模型已不支援。 | 1-2、2-5 |
| **思維鏈（chain of thought）／預先思考** | 請 Claude 先一步一步思考（寫在 `<thinking>` 裡）再回答，提升準確度。 | 2-6、3-1 |
| **少量範例提示（few-shot）** | 在提示詞裡給幾個範例，讓 Claude 照著做。zero-shot = 不給範例，one-shot = 1 個。 | 1-2、2-7 |
| **給退路（give Claude an out）** | 允許 Claude 說「我不知道」，減少幻覺。 | 2-8 |
| **串連提示詞（prompt chaining）** | 把上一次的回答放進下一次的提示詞，一步一步完成任務。 | 2-10.1 |
| **RAG（檢索增強生成）** | 先搜尋相關資料，再讓 Claude 根據資料回答。 | 2-10.3 |
| **embedding（嵌入向量）／向量資料庫** | 把文字轉成一串數字，意思相近的文字數字也相近；向量資料庫用來快速找出意思相近的資料。 | 2-10.3 |
| **邊緣情況（edge case）** | 不常見、極端或奇怪的輸入，最容易讓提示詞出錯。 | 3-3、3-4 |
| **拒絕句（objection phrase）** | 規定 Claude 在不該回答時一字不差使用的句子，例如「I'm sorry, I can't help with that.」 | 3-5 |
| **越獄（jailbreak）** | 用話術讓 AI 違反它的設定或規則。 | 3-5 |
| **正式上線（production）** | 真正給客戶、使用者使用的產品環境。 | 3-1 |
| **提示詞產生器（Prompt Generator）** | Anthropic Console 上幫你產生提示詞初稿的工具。 | 3-1 |

## 📏 評估（Evals）

| 名詞 | 白話解釋 | 出現在 |
|---|---|---|
| **評估（evaluation，eval）** | 用一組考題和標準答案，替「提示詞 + 模型」打分數。 | 第 4 單元 |
| **標準答案（golden answer）** | 正確或理想的回答，作為比較基準。 | 4-1 |
| **基準分數（baseline）** | 第一版提示詞的分數，之後修改要跟它比。 | 4-1、4-3 |
| **退步（regression）** | 修改後，原本正常的情況反而變差了。 | 4-1 |
| **人工評分** | 由人依照評分準則打分數。最準但最慢最貴。 | 4-1、4-2 |
| **程式評分（code-graded）** | 用程式比對答案（完全比對、關鍵字、正規表達式）。快、便宜、一致。 | 4-1、4-3 |
| **模型評分（model-graded／LLM as a judge）** | 請另一個 LLM 依照評分準則打分數。 | 4-1、4-8 |
| **評分準則（rubric）** | 描述「怎樣算好、怎樣算不好」的標準。 | 4-8、4-9 |
| **完全比對（exact match）** | 輸出和標準答案一字不差才算對。 | 4-3 |
| **Workbench** | Anthropic Console 上試寫提示詞、做人工評估的網頁工具。 | 4-2 |
| **promptfoo** | 開源的提示詞評估工具，用 `npx promptfoo@latest eval` 執行。 | 4-5～4-9 |
| **provider（供應商）** | promptfoo 裡指的是「要用哪個模型」，例如 `anthropic:messages:claude-haiku-4-5`。 | 4-5 |
| **斷言（assertion）** | promptfoo 的檢查規則，例如 `contains-all`、`icontains`、`llm-rubric`。 | 4-6 |
| **transform（轉換）** | promptfoo 在評分前先處理輸出的函式，例如擷取 `<answer>` 裡的內容。 | 4-5 |
| **`get_assert`** | promptfoo 自訂評分器的函式名稱，回傳通過與否、分數、原因。 | 4-7、4-9 |
| **YAML** | 一種用縮排寫設定檔的格式（promptfoo 的 `promptfooconfig.yaml`）。 | 4-5 |
| **CSV** | 用逗號分隔欄位的簡單表格檔案。 | 4-5 |
| **Node.js／npx** | 執行 JavaScript 工具的環境；`npx` 可以直接下載並執行工具（例如 promptfoo）。 | 4-5 |

## 🛠 工具使用（Tool use）

| 名詞 | 白話解釋 | 出現在 |
|---|---|---|
| **工具使用（tool use）／函式呼叫（function calling）** | 讓 Claude 「請你的程式」幫忙做事（查資料、計算⋯⋯）。Claude 只說要用什麼工具，真正執行的是你的程式。 | 第 5 單元 |
| **工具定義（tool definition）** | 告訴 Claude 有哪些工具：`name`（名稱）、`description`（說明）、`input_schema`（輸入格式）。 | 5-2 |
| **JSON Schema** | 描述 JSON 資料結構的規格：有哪些欄位、什麼型別、哪些必填。 | 5-2 |
| **`enum`（列舉）** | 限定只能填清單中的其中一個值，像下拉式選單。 | 5-2 |
| **`tool_use` 區塊** | Claude 想使用工具時回傳的內容區塊，包含 `id`、`name`、`input`。 | 5-2 |
| **`tool_result` 區塊** | 你把工具結果回傳給 Claude 的內容區塊，包含 `tool_use_id`、`content`、`is_error`。 | 5-4 |
| **`tool_choice`** | 控制 Claude 怎麼使用工具：`auto`（自己決定）、`any`（一定要用某個）、`tool`（一定要用指定的）。 | 5-3、5-5 |
| **結構化輸出（structured outputs）** | 讓 Claude 的回答保證符合指定 JSON 結構的功能（也可以用工具定義來達成）。 | 5-3 |
| **實體擷取（entity extraction）** | 從文字中找出人名、組織、地點等具體事物並分類。 | 5-3 |

## 🐍 Python 與工具

| 名詞 | 白話解釋 | 出現在 |
|---|---|---|
| **Python** | 一種語法接近英文的程式語言，整套課程都用它。 | 0-3、0-4 |
| **Jupyter Notebook（`.ipynb`）** | 可以邊寫說明邊執行程式的筆記本，一格一格執行。 | 0-3 |
| **核心（kernel）** | 實際執行 notebook 程式碼的 Python 環境。亂掉時可以「重新啟動核心」。 | 0-3 |
| **終端機（terminal）** | 用打字指揮電腦的視窗。 | 0-3 |
| **套件（package）** | 別人寫好、可以直接拿來用的程式工具，用 `pip install` 安裝。 | 0-3 |
| **環境變數** | 電腦或程式身上帶著的設定值，例如 `ANTHROPIC_API_KEY`。 | 1-1 |
| **`.env` 檔** | 存放環境變數（例如 API 金鑰）的檔案，用 `python-dotenv` 讀取。 | 0-3、1-1 |
| **變數** | 貼了標籤的盒子，用 `=` 把值放進去。 | 0-4 |
| **字串（str）** | 一段文字。多行用 `"""..."""`。 | 0-4 |
| **f-string** | 在字串前加 `f`，用 `{變數}` 把變數塞進文字。 | 0-4 |
| **串列（list）** | 有順序的清單 `[ ]`，編號從 0 開始。 | 0-4 |
| **字典（dict）** | 「key: value」成對的資料 `{ }`。 | 0-4 |
| **集合（set）** | 沒有順序、不重複的一組資料，比較時不在乎順序。 | 4-4 |
| **函式（function）** | 用 `def` 把一段程式包起來，用 `return` 回傳結果。 | 0-4 |
| **類別（class）／物件（object）／方法（method）** | 類別是設計圖，物件是照設計圖做出來的東西，方法是物件身上的函式。 | 0-4、5-6 |
| **JSON** | 用文字表示資料的通用格式，長得很像 Python 的字典和串列。`json.dumps()`／`json.loads()` 互相轉換。 | 0-4 |
| **正規表達式（regex，`re`）** | 描述文字長什麼樣子的規則，用來搜尋、擷取文字。 | 0-4 |
| **`try` / `except`** | 試著執行，出錯時改做別的事，避免程式當掉。 | 0-4 |
| **串列生成式（list comprehension）** | 一行就做出新串列的簡寫：`[x*2 for x in 清單]`。 | 0-4 |
| **`%pip`／`%store`（魔法指令）** | Jupyter 專用指令：`%pip` 安裝套件；`%store` 在不同 notebook 之間傳遞變數。 | 0-4、2-0 |

## 🏢 平台與服務

| 名詞 | 白話解釋 | 出現在 |
|---|---|---|
| **Anthropic Console（主控台）** | Anthropic 的網站後台：申請 API 金鑰、儲值、Workbench、提示詞產生器。 | 0-3、4-2 |
| **Amazon Bedrock** | AWS（亞馬遜雲端）提供的服務，可以透過 AWS 帳號使用 Claude。 | 2 單元 Bedrock 說明 |
| **Google Vertex AI** | Google Cloud 提供的服務，也可以使用 Claude。 | 3-1 |
| **GitHub** | 存放和分享程式碼的網站。 | 0-3 |

---

[回到課程首頁](README.md)
