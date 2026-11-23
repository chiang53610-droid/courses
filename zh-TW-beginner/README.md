# Anthropic 官方課程・新手白話版（繁體中文）

> 給**程式新手**的完整中文版：用白話解釋每一個觀念，**完整保留**原課程的所有內容，並補上新手需要的背景知識。
> 原始英文課程：本 repository 根目錄的 5 門課（由 Anthropic 製作）。

---

## 🚀 第一次來？從這裡開始

1. 先讀 **[0-1 這套課程怎麼用？](00_before_you_start/01_how_to_use_this_course.md)**（5 分鐘）
2. 照著 **[0-3 準備你的電腦](00_before_you_start/03_setup_your_computer.md)** 安裝環境、申請 API 金鑰
3. 然後**照順序**一課一課往下學 👇

每一課都有兩個檔案，內容完全相同：
- **`.md`**：直接在 GitHub 網頁上**閱讀**（手機也可以）
- **`.ipynb`**：用 VS Code 或 Jupyter 打開，可以**動手執行**程式碼

遇到看不懂的名詞 → 查 **[名詞小辭典](GLOSSARY.md)**。

---

## 📚 完整目錄

### 0. 開始之前（新手先修）

> 原課程沒有這個單元，是新手版補充的。原課程假設你已經會 Python，這裡幫你補上。

| 課 | 內容 | 時間 |
|---|---|---|
| [0-1 這套課程怎麼用？](00_before_you_start/01_how_to_use_this_course.md) | 學習路線、每課的結構、遇到問題怎麼辦 | 5 分 |
| [0-2 什麼是 API？什麼是大型語言模型？](00_before_you_start/02_what_is_an_api.md) | LLM、API、API 金鑰、SDK、提示詞、token | 15 分 |
| [0-3 準備你的電腦](00_before_you_start/03_setup_your_computer.md) | 安裝 Python、VS Code/Jupyter、套件、API 金鑰、**2026 模型更新說明**、常見錯誤 | 30～60 分 |
| [0-4 Python 速成](00_before_you_start/04_python_crash_course.md) | 只教課程會用到的 Python：字串、串列、字典、函式、JSON、正規表達式⋯⋯ | 1～2 小時 |

### 1. Claude API 基礎

> 原課程：`anthropic_api_fundamentals/`｜學會用 Python 程式和 Claude 對話。

| 課 | 內容 |
|---|---|
| [1-1 開始使用](01_api_fundamentals/01_getting_started.md) | 安裝 SDK、取得 API 金鑰、送出第一個請求 |
| [1-2 訊息格式](01_api_fundamentals/02_messages_format.md) | `messages` 格式、回應物件、prefill、少量範例、聊天機器人 |
| [1-3 模型](01_api_fundamentals/03_models.md) | 比較各模型的速度、能力、成本；**2026 年模型一覽** |
| [1-4 模型參數](01_api_fundamentals/04_parameters.md) | `max_tokens`、`stop_sequences`、`temperature`、`system` |
| [1-5 串流](01_api_fundamentals/05_Streaming.md) | 一邊產生一邊顯示、串流事件、TTFT、串流小幫手 |
| [1-6 視覺（傳圖片）](01_api_fundamentals/06_vision.md) | 傳送圖片、base64、多張圖片、網路圖片、看圖提示技巧 |

### 2. 提示詞工程互動教學

> 原課程：`prompt_engineering_interactive_tutorial/`｜學會寫出讓 Claude 回答得又好又準的提示詞。每章都有<strong>練習（自動批改）</strong>和**範例遊樂場**。

| 章 | 內容 | 程度 |
|---|---|---|
| [第 0 課 使用說明（含單元介紹）](02_prompt_engineering_tutorial/00_Tutorial_How-To.md) | 設定 API 金鑰、`get_completion` 小幫手 | — |
| [第 1 章 提示詞的基本結構](02_prompt_engineering_tutorial/01_Basic_Prompt_Structure.md) | Messages API、系統提示詞 | 初級 |
| [第 2 章 清楚、直接](02_prompt_engineering_tutorial/02_Being_Clear_and_Direct.md) | 黃金法則：朋友看不懂，Claude 也看不懂 | 初級 |
| [第 3 章 指定角色](02_prompt_engineering_tutorial/03_Assigning_Roles_Role_Prompting.md) | 角色提示 | 初級 |
| [第 4 章 把資料和指示分開](02_prompt_engineering_tutorial/04_Separating_Data_and_Instructions.md) | 提示詞範本、XML 標籤 | 中級 |
| [第 5 章 格式化輸出 & 幫 Claude 開口](02_prompt_engineering_tutorial/05_Formatting_Output_and_Speaking_for_Claude.md) | XML/JSON 輸出、prefill | 中級 |
| [第 6 章 預先思考](02_prompt_engineering_tutorial/06_Precognition_Thinking_Step_by_Step.md) | 一步一步想、思考要說出來 | 中級 |
| [第 7 章 使用範例](02_prompt_engineering_tutorial/07_Using_Examples_Few-Shot_Prompting.md) | few-shot 少量範例提示 | 中級 |
| [第 8 章 避免幻覺](02_prompt_engineering_tutorial/08_Avoiding_Hallucinations.md) | 給退路、先找證據 | 進階 |
| [第 9 章 從零打造複雜提示詞](02_prompt_engineering_tutorial/09_Complex_Prompts_from_Scratch.md) | 10 個元素、職涯教練、法律、財務、程式教學 | 進階 |
| [附錄 10.1 串連提示詞](02_prompt_engineering_tutorial/10_1_Appendix_Chaining_Prompts.md) | 把回答接到下一個提示詞 | 附錄 |
| [附錄 10.2 工具使用（舊方法）](02_prompt_engineering_tutorial/10_2_Appendix_Tool_Use.md) | 用 XML 實作函式呼叫的原理 | 附錄 |
| [附錄 10.3 搜尋與檢索](02_prompt_engineering_tutorial/10_3_Appendix_Search_and_Retrieval.md) | RAG 入門 | 附錄 |
| [附錄 10.4 實證效能評估（加碼）](02_prompt_engineering_tutorial/10_4_Appendix_Empirical_Performance_Evaluations.md) | 程式／人工／模型評分（原本只在 Bedrock 版） | 附錄 |
| [關於 Amazon Bedrock 版本](02_prompt_engineering_tutorial/bedrock_version_notes.md) | Bedrock 版和本版的差異 | 說明 |

提示與參考答案（中文）：[`02_prompt_engineering_tutorial/hints.py`](02_prompt_engineering_tutorial/hints.py)

### 3. 真實世界的提示詞

> 原課程：`real_world_prompting/`｜把技巧組合起來，寫出正式產品等級的長提示詞。

| 課 | 內容 |
|---|---|
| [3-1 必備提示詞技巧總複習](03_real_world_prompting/01_prompting_recap.md) | 提示詞產生器、清楚直接、XML、範例、思考、角色、長文本 |
| [3-2 醫療病歷摘要](03_real_world_prompting/02_medical_prompt.md) | 從爛提示詞一步步改好、JSON 輸出 |
| [3-3 提示詞工程的流程](03_real_world_prompting/03_prompt_engineering.md) | 生命週期：建立 → 測試 → 選技巧 → 改進 → 循環 |
| [3-4 客服通話摘要器](03_real_world_prompting/04_call_summarizer.md) | 邊緣情況處理、`INSUFFICIENT_DATA` |
| [3-5 客服聊天機器人](03_real_world_prompting/05_customer_support_ai.md) | 拒絕句、`<thinking>` vs `<final_answer>` |

### 4. 提示詞評估

> 原課程：`prompt_evaluations/`｜學會「打分數」，客觀判斷提示詞有沒有變好。第 5～9 課使用評估工具 **promptfoo**，需要的檔案都放在各課的資料夾裡，可以直接執行。

| 課 | 內容 |
|---|---|
| [4-1 評估入門](04_prompt_evaluations/01_intro_to_evals.md) | 基準測試 vs. 客戶評估、評估的組成、三種評分方法 |
| [4-2 用 Workbench 做人工評分](04_prompt_evaluations/02_workbench_evals.md) | 網頁工具：變數、多個測試案例、比較版本 |
| [4-3 簡單的程式評分評估](04_prompt_evaluations/03_code_graded.md) | 完全比對、66.7% → 100% |
| [4-4 分類評估](04_prompt_evaluations/04_code_graded_classification_evals.md) | 用 `set` 比對多個分類 |
| [4-5 promptfoo 入門](04_prompt_evaluations/05_prompt_foo_code_graded_animals/lesson.md) | 安裝、providers/prompts/tests、transform、比較模型 |
| [4-6 promptfoo 分類評估](04_prompt_evaluations/06_prompt_foo_code_graded_classification/lesson.md) | 內建斷言 `contains-all` |
| [4-7 promptfoo 自訂評分器](04_prompt_evaluations/07_prompt_foo_custom_graders/lesson.md) | 用 Python 寫 `get_assert` |
| [4-8 promptfoo 模型評分](04_prompt_evaluations/08_prompt_foo_model_graded/lesson.md) | `llm-rubric`：LLM 當評審 |
| [4-9 自訂模型評分](04_prompt_evaluations/09_custom_model_graded_prompt_foo/lesson.md) | 多標準評分提示詞、平均分數門檻 |

### 5. 工具使用

> 原課程：`tool_use/`｜讓 Claude 呼叫你寫的程式（計算機、資料庫、維基百科⋯⋯）。

| 課 | 內容 |
|---|---|
| [5-1 工具使用概觀](05_tool_use/01_tool_use_overview.md) | 什麼是工具使用、4 個步驟 |
| [5-2 你的第一個簡單工具](05_tool_use/02_your_first_simple_tool.md) | 計算機工具、工具定義、JSON Schema |
| [5-3 用工具強制輸出 JSON](05_tool_use/03_structured_outputs.md) | 情緒分析、實體擷取、`tool_choice` |
| [5-4 完整的工具使用流程](05_tool_use/04_complete_workflow.md) | `tool_result`、維基百科搜尋 |
| [5-5 工具選擇](05_tool_use/05_tool_choice.md) | `auto` / `any` / `tool` |
| [5-6 多個工具的聊天機器人](05_tool_use/06_chatbot_with_multiple_tools.md) | 假資料庫、客服機器人、`<reply>` |

---

## 🔄 2026 年重要說明（請務必讀）

原課程製作於 2024 年，使用的 **Claude 3 系列模型現在已全部停用**。為了讓你**不用改任何程式碼就能跑完整套課程**，新手版做了這些調整：

| 項目 | 原課程 | 新手版 |
|---|---|---|
| Claude 3 Haiku | `claude-3-haiku-20240307` | `claude-haiku-4-5` |
| Claude 3 / 3.5 Sonnet | `claude-3-sonnet-20240229`、`claude-3-5-sonnet-20240620` | `claude-sonnet-4-6` |
| Claude 3 Opus | `claude-3-opus-20240229` | `claude-opus-4-6` |
| Python SDK | `pip install anthropic`（最新版） | `pip install "anthropic<1"`（0.x 版） |

- 選這些模型和 SDK 版本，是因為它們仍支援原課程用到的 **`temperature` 參數**和 <strong>prefill（預先填寫回答）</strong>技巧，而且預設不會先「思考」，回應格式和原課程一致。有幾個地方因為模型限制做了個別調整，會在該課說明。
- 每課顯示的「**原課程執行結果**」是用舊模型跑出來的，**你自己跑的結果一定會不同**，這是正常的。
- 學完課程、做自己的專案時，建議改用最新的模型（例如 `claude-opus-5-5`、`claude-sonnet-5-5`、`claude-haiku-5-5`）和最新版 SDK，並留意它們不支援 prefill 和 `temperature`、部分不支援強制 `tool_choice`。詳見 [0-3 的說明](00_before_you_start/03_setup_your_computer.md#-2026-更新為什麼模型名稱和原課程不一樣)。

---

## 📝 這個版本做了什麼？

- **完整翻譯**：原課程的每一段說明、每一個範例、每一題練習都翻譯成白話繁體中文。英文提示詞保留原文（因為練習的自動批改是檢查英文字），並附上中文翻譯。
- **保留原始程式碼和執行結果**：程式碼格直接從原課程複製，只把停用的模型名稱換掉；長篇的英文範例文件也完整保留。
- **新手補充**（用 🧩、💡、⚠️、🔄、📌 等標記，和原課程內容區分）：
  - 每課開頭的「🎯 這一課你會學到」、結尾的「📌 重點整理」
  - 看起來嚇人的程式碼都有「**逐行解說**」
  - 生活化的比喻、名詞解釋、常見錯誤提醒
  - 原課程沒有提供答案的練習，補上參考答案（收在可以展開的區塊裡）
  - 原課程的小錯誤（錯字、程式碼小瑕疵）會在旁邊註明
- **新增「0. 開始之前」單元**和<strong>[名詞小辭典](GLOSSARY.md)</strong>。

---

## 🛠 給維護者

所有課程都是從 [`_build/src/`](_build/src) 裡的原稿自動產生的，請不要直接修改 `.md` 和 `.ipynb`。建置方式請見 [`_build/README.md`](_build/README.md)。

---

原始課程內容版權屬於 Anthropic，依原 repository 的 [授權條款](../LICENSE) 使用。
