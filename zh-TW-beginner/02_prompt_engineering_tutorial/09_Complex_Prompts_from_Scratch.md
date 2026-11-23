<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
> 📓 想要動手執行程式碼？請打開同一個資料夾裡的 [`09_Complex_Prompts_from_Scratch.ipynb`](09_Complex_Prompts_from_Scratch.ipynb)。

# 第 9 章：從零打造複雜的提示詞（Complex Prompts from Scratch）

> 📚 **第 2 單元：提示詞工程互動教學**｜第 9 章 / 共 9 章（進階）
> ⏱️ 預估時間：60～90 分鐘

- [課程](#課程)
- [練習](#練習)
- [範例遊樂場](#範例遊樂場)

## 🎯 這一章你會學到

- 一套**複雜提示詞的建議結構（10 個元素）**，把前 8 章學到的技巧全部組合起來
- 範例 1：職涯教練聊天機器人
- 範例 2：法律服務
- 練習：財務服務（稅務問答）、程式教學機器人

## 準備工作

執行下面這個準備格，載入你的 API 金鑰，並建立 `get_completion` 輔助函式。

```python
%pip install "anthropic<1"

# Import python's built-in regular expression library
import re
import anthropic

# Retrieve the API_KEY & MODEL_NAME variables from the IPython store
%store -r API_KEY
%store -r MODEL_NAME

client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt: str, system_prompt="", prefill=""):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        system=system_prompt,
        messages=[
          {"role": "user", "content": prompt},
          {"role": "assistant", "content": prefill}
        ]
    )
    return message.content[0].text
```

---

## 課程

恭喜你來到最後一章！現在是時候把所有東西組合起來，學習怎麼**打造獨特又複雜的提示詞**了。

下面你會使用一套**我們推薦用於複雜提示詞的引導式結構**。在這一章的後半段，我們會展示一些特定產業的提示詞，並說明它們是如何用類似的結構組成的。

**注意：** **不是每個提示詞都需要下面這個複雜結構裡的每一個元素。** 我們鼓勵你多玩玩看，加入或拿掉某些元素，看看會怎麼影響 Claude 的回答。通常**最好的做法是：先用很多提示詞元素讓提示詞能正常運作，之後再修改、精簡你的提示詞**。

### 複雜提示詞的 10 個元素（新手版整理）

下面的程式碼裡，每個元素前面都有英文註解說明它的用途。這裡先用中文整理成一張表，對照著看會更容易懂：

| # | 元素 | 變數名稱 | 要寫什麼 | 位置建議 |
|---|---|---|---|---|
| 1 | `user` 角色 | （不用寫） | 確保 Messages API 呼叫一定以 `user` 角色開始。上面定義的 `get_completion()` 會自動幫你做到。 | — |
| 2 | 任務背景 | `TASK_CONTEXT` | 告訴 Claude 它要扮演什麼角色，或你希望它透過這個提示詞完成什麼目標和整體任務。 | 最好放在提示詞的**前面** |
| 3 | 語氣背景 | `TONE_CONTEXT` | 如果語氣對這次互動很重要，告訴 Claude 要用什麼語氣。 | 視任務需要，不一定要有 |
| 4 | 詳細任務描述和規則 | `TASK_DESCRIPTION` | 詳細說明你要 Claude 做的具體任務，以及它可能需要遵守的規則。這裡也是給 Claude「**退路**」的地方（如果它沒有答案或不知道該怎麼辦）。最好把這段描述和規則拿給朋友看，確認邏輯清楚、所有模稜兩可的字都有清楚定義。 | |
| 5 | 範例 | `EXAMPLES` | 至少提供 Claude 一個它可以模仿的理想回答範例，用 `<example></example>` XML 標籤包起來。可以提供多個範例；如果提供多個，要告訴 Claude 這是什麼的範例，並把每個範例分別用 XML 標籤包起來。**範例大概是知識工作中，讓 Claude 照你期望行事最有效的單一工具。** 記得提供常見「邊緣情況（edge case）」的範例。如果你的提示詞有用到草稿區（scratchpad），提供草稿區應該長什麼樣子的範例很有效。一般來說，範例越多越好。 | |
| 6 | 要處理的輸入資料 | `INPUT_DATA` | 如果有 Claude 需要在提示詞中處理的資料，把它放在這裡，用相關的 XML 標籤包起來。可以放多份資料，但每份都要用自己的一組 XML 標籤包起來。 | 視任務需要；順序有彈性 |
| 7 | 立即任務描述或請求 | `IMMEDIATE_TASK` | 「提醒」Claude，或明確告訴它為了完成任務，**現在**應該做什麼。這裡也可以放額外的變數，例如使用者的問題。再提醒一次 Claude 它當下的任務，通常沒有壞處。 | 最好放在長提示詞的**後面**——效果會比放在開頭好。把使用者的問題放在提示詞靠近底部的地方，通常也是好做法。 |
| 8 | 預先思考（一步一步想） | `PRECOGNITION` | 對於有多個步驟的任務，告訴 Claude 在給答案之前先一步一步思考。有時候甚至需要說「在你給出答案之前⋯⋯」來確保它先做這件事。 | 不是每個提示詞都需要；如果有，最好放在長提示詞的後面、緊接在「立即任務」之後 |
| 9 | 輸出格式 | `OUTPUT_FORMATTING` | 如果你希望 Claude 的回答用特定的方式排版，清楚地告訴 Claude 是什麼格式。 | 視任務需要；如果有，放在提示詞後面比放在開頭好 |
| 10 | 預先填寫 Claude 的回答 | `PREFILL` | 用一些預先填寫好的字當作 Claude 回答的開頭，引導 Claude 的行為或回答。如果要預先填寫，必須放在 API 呼叫的 `assistant` 角色裡。 | 視任務需要 |

> 🧩 **白話小補充**：可以把這 10 個元素想成**寫一份給新員工的完整工作交接單**：你是誰（任務背景）→ 說話的態度（語氣）→ 工作細節和規定（任務描述）→ 參考範本（範例）→ 要處理的資料（輸入資料）→ 現在請你做這件事（立即任務）→ 先想清楚再動手（預先思考）→ 交件格式（輸出格式）→ 幫你起個頭（prefill）。

### 範例：職涯教練聊天機器人

下面這個結構結合了多種提示詞工程元素，是撰寫複雜提示詞的好起點。**有些元素的順序很重要**，有些則不重要。當最佳做法認為順序很重要時，我們會特別註明；但一般來說，**只要照著這個順序寫，就是一個很棒的提示詞的好開始**。

在下面的例子中，我們要寫一個「**受控的角色扮演**」提示詞：Claude 扮演一個特定情境中的角色，並執行特定的任務。我們的目標是讓 Claude 扮演一位**友善的職涯教練**。

閱讀並執行下面這格，把各個提示詞元素組合成一個完整的提示詞。

<details>
<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>

```python
######################################## INPUT VARIABLES ########################################

# First input variable - the conversation history (this can also be added as preceding `user` and `assistant` messages in the API call)
HISTORY = """Customer: Give me two possible careers for sociology majors.

Joe: Here are two potential careers for sociology majors:

- Social worker - Sociology provides a strong foundation for understanding human behavior and social systems. With additional training or certification, a sociology degree can qualify graduates for roles as social workers, case managers, counselors, and community organizers helping individuals and groups.

- Human resources specialist - An understanding of group dynamics and organizational behavior from sociology is applicable to careers in human resources. Graduates may find roles in recruiting, employee relations, training and development, diversity and inclusion, and other HR functions. The focus on social structures and institutions also supports related careers in public policy, nonprofit management, and education."""

# Second input variable - the user's question
QUESTION = "Which of the two careers requires more than a Bachelor's degree?"



######################################## PROMPT ELEMENTS ########################################

##### Prompt element 1: `user` role
# Make sure that your Messages API call always starts with a `user` role in the messages array.
# The get_completion() function as defined above will automatically do this for you.

##### Prompt element 2: Task context
# Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
# It's best to put context early in the body of the prompt.
TASK_CONTEXT = "You will be acting as an AI career coach named Joe created by the company AdAstra Careers. Your goal is to give career advice to users. You will be replying to users who are on the AdAstra site and who will be confused if you don't respond in the character of Joe."

##### Prompt element 3: Tone context
# If important to the interaction, tell Claude what tone it should use.
# This element may not be necessary depending on the task.
TONE_CONTEXT = "You should maintain a friendly customer service tone."

##### Prompt element 4: Detailed task description and rules
# Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
# This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
# It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
TASK_DESCRIPTION = """Here are some important rules for the interaction:
- Always stay in character, as Joe, an AI from AdAstra Careers
- If you are unsure how to respond, say \"Sorry, I didn't understand that. Could you rephrase your question?\"
- If someone asks something irrelevant, say, \"Sorry, I am Joe and I give career advice. Do you have a career question today I can help you with?\""""

##### Prompt element 5: Examples
# Provide Claude with at least one example of an ideal response that it can emulate. Encase this in <example></example> XML tags. Feel free to provide multiple examples.
# If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
# Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
# Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
# Generally more examples = better.
EXAMPLES = """Here is an example of how to respond in a standard interaction:
<example>
Customer: Hi, how were you created and what do you do?
Joe: Hello! My name is Joe, and I was created by AdAstra Careers to give career advice. What can I help you with today?
</example>"""

##### Prompt element 6: Input data to process
# If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
# Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
# This element may not be necessary depending on task. Ordering is also flexible.
INPUT_DATA = f"""Here is the conversational history (between the user and you) prior to the question. It could be empty if there is no history:
<history>
{HISTORY}
</history>

Here is the user's question:
<question>
{QUESTION}
</question>"""

##### Prompt element 7: Immediate task description or request #####
# "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
# This is also where you would put in additional variables like the user's question.
# It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
# This will yield better results than putting this at the beginning.
# It is also generally good practice to put the user's query close to the bottom of the prompt.
IMMEDIATE_TASK = "How do you respond to the user's question?"

##### Prompt element 8: Precognition (thinking step by step)
# For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
# Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
# Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
PRECOGNITION = "Think about your answer first before you respond."

##### Prompt element 9: Output formatting
# If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
# This element may not be necessary depending on the task.
# If you include it, putting it toward the end of the prompt is better than at the beginning.
OUTPUT_FORMATTING = "Put your response in <response></response> tags."

##### Prompt element 10: Prefilling Claude's response (if any)
# A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
# If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
# This element may not be necessary depending on the task.
PREFILL = "[Joe] <response>"



######################################## COMBINE ELEMENTS ########################################

PROMPT = ""

if TASK_CONTEXT:
    PROMPT += f"""{TASK_CONTEXT}"""

if TONE_CONTEXT:
    PROMPT += f"""\n\n{TONE_CONTEXT}"""

if TASK_DESCRIPTION:
    PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

if EXAMPLES:
    PROMPT += f"""\n\n{EXAMPLES}"""

if INPUT_DATA:
    PROMPT += f"""\n\n{INPUT_DATA}"""

if IMMEDIATE_TASK:
    PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

if PRECOGNITION:
    PROMPT += f"""\n\n{PRECOGNITION}"""

if OUTPUT_FORMATTING:
    PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

# Print full prompt
print("--------------------------- Full prompt with variable substutions ---------------------------")
print("USER TURN")
print(PROMPT)
print("\nASSISTANT TURN")
print(PREFILL)
```

</details>

**這個提示詞的各個元素（中文翻譯）：**
- **輸入變數**
  - `HISTORY`（對話紀錄）：顧客問「給我兩個社會學系畢業生可以做的職業。」Joe 回答了兩個：**社工**（社會學提供了理解人類行為和社會系統的基礎，加上額外的訓練或證照，就能擔任社工、個案管理師、諮商師⋯⋯）和**人資專員**（社會學對團體動力和組織行為的理解，適用於招募、員工關係、教育訓練、多元共融等人資工作⋯⋯）。程式碼的註解提到：對話紀錄也可以改成放在 API 呼叫裡前面的 `user` 和 `assistant` 訊息中。
  - `QUESTION`（使用者問題）：「這兩個職業中，哪一個需要學士以上的學歷？」
- `TASK_CONTEXT`：「你將扮演一位名叫 Joe 的 AI 職涯教練，由 AdAstra Careers 公司打造。你的目標是給使用者職涯建議。你會回覆在 AdAstra 網站上的使用者，如果你不用 Joe 的角色回覆，他們會感到困惑。」
- `TONE_CONTEXT`：「你應該保持友善的客服語氣。」
- `TASK_DESCRIPTION`：「以下是互動時的重要規則：
  - 永遠保持角色，你是 Joe，一個來自 AdAstra Careers 的 AI
  - 如果你不確定該怎麼回應，就說『抱歉，我不太懂你的意思。可以換個方式問嗎？』
  - 如果有人問不相關的事，就說『抱歉，我是 Joe，我提供職涯建議。今天有什麼職涯問題我可以幫你的嗎？』」
- `EXAMPLES`：「以下是一般互動時如何回應的範例：顧客：嗨，你是怎麼被創造出來的？你是做什麼的？ Joe：哈囉！我叫 Joe，是 AdAstra Careers 打造來提供職涯建議的。今天有什麼可以幫你的嗎？」
- `INPUT_DATA`：「這是在這個問題之前，（使用者和你之間的）對話紀錄。如果沒有紀錄，這裡可能是空的：`<history>`⋯⋯`</history>` 這是使用者的問題：`<question>`⋯⋯`</question>`」
- `IMMEDIATE_TASK`：「你要怎麼回應使用者的問題？」
- `PRECOGNITION`：「回應之前，先想一想你的答案。」
- `OUTPUT_FORMATTING`：「把你的回應放在 `<response></response>` 標籤裡。」
- `PREFILL`：`[Joe] <response>`
- **組合元素（COMBINE ELEMENTS）**：最後用一連串 `if 變數:` 檢查——如果這個元素有內容（不是空字串），就用 `+=` 把它接到 `PROMPT` 後面，元素之間用 `\n\n`（空一行）隔開。這樣你只要把不需要的元素設成空字串 `""`，它就會自動被略過。

現在來執行這個提示詞吧！執行下面這格，看看 Claude 的輸出。

```python
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT, prefill=PREFILL))
```

### 範例：法律服務

**法律領域的提示詞可能非常複雜**，因為需要：
- 解析很長的文件
- 處理複雜的主題
- 用非常特定的方式排版輸出
- 遵循多步驟的分析流程

我們來看看怎麼用這個複雜提示詞範本，為一個特定的法律使用情境組織提示詞。下面我們詳細寫出了一個法律使用情境的範例提示詞：請 Claude 根據一份法律文件中的資訊，回答一個法律問題。

我們**調換了幾個元素的順序**，來展示提示詞的結構是很有彈性的！

**提示詞工程是一門「科學化的反覆試驗」。** 我們鼓勵你混搭、調換位置（那些順序不重要的元素），看看什麼最適合你和你的需求。

<details>
<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>

```python
######################################## INPUT VARIABLES ########################################

# First input variable - the legal document
LEGAL_RESEARCH = """<search_results>
<search_result id=1>
The animal health industry became caught up in a number of patent and trademark lawsuits during the past year. In 1994, Barclay Slocum obtained patents for the tibial plateau leveling osteotomy procedure, which is used in the treatment of dogs with cranial cruciate ligament rupture, and for the devices used in the procedure. During 2006, Slocum Enterprises filed a patent infringement suit against New Generation Devices, arguing that the Unity Cruciate Plate manufactured by New Generation infringed on the patent for the Slocum TPLO plate. However, the court never reached a decision on the issue of patent infringement, ruling that it did not have jurisdiction on the basis of the small number of plates sold in the state in which the case was filed and the information provided on a Web site maintained by Slocum Enterprises. Other patent battles waged during 2006 concerned the use of laser technology for onychectomy in cats, pet identification chips, pig vaccines, and pet “deshedding” tools.
</search_result>
<search_result id=2>
In Canada, the British Columbia Veterinary Medical Association brought suit against a nonveterinarian, claiming that he engaged in cutting or otherwise removing hooks from horses' teeth and floating horses' teeth with power and manual tools, provided advice and diagnoses in return for a fee, and held himself out as being qualified and willing to provide treatment with respect to these activities. The court held that the intention of the legislature in passing the Veterinary Profession Act was the protection of the public and animals and further held that monopolistic statutes serve the purpose of protecting the public. In addition, the court concluded that dentistry, at its core, relates to the health of the teeth and gums; is distinct from cosmetic and other types of care of animals; and, therefore, falls under the definition of the practice of veterinary medicine. The nonveterinarian was enjoined from providing services without a veterinarian supervising the procedures.
</search_result>
<search_result id=3>
The aftermath of Hurricane Katrina, which hit the Gulf Coast of the United States during 2005, spurred changes to the way animals are treated during natural disasters. In 2006, Hawaii, Louisiana, and New Hampshire all enacted laws that address issues regarding the care of animals during disasters, such as providing shelters for pets and allowing service animals to be kept with the people they serve. In addition, Congress passed, and the President signed, the Pet Evacuation and Transportation Standards Act during 2006, which requires state and local emergency preparedness authorities to include in their evacuation plans information on how they will accommodate household pets and service animals in case of a disaster. California passed a law that will require its Office of Emergency Services, Department of Agriculture, and other agencies involved with disaster response preparation to develop a plan for the needs of service animals, livestock, equids, and household pets in the event of a disaster or major emergency.
</search_result>
</search_results>"""

# Second input variable - the user's question
QUESTION = "Are there any laws about what to do with pets during a hurricane?"



######################################## PROMPT ELEMENTS ########################################

##### Prompt element 1: `user` role
# Make sure that your Messages API call always starts with a `user` role in the messages array.
# The get_completion() function as defined above will automatically do this for you.

##### Prompt element 2: Task context
# Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
# It's best to put context early in the body of the prompt.
TASK_CONTEXT = "You are an expert lawyer."

##### Prompt element 3: Tone context
# If important to the interaction, tell Claude what tone it should use.
# This element may not be necessary depending on the task.
TONE_CONTEXT = ""

##### Prompt element 4: Input data to process
# If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
# Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
# This element may not be necessary depending on task. Ordering is also flexible.
INPUT_DATA = f"""Here is some research that's been compiled. Use it to answer a legal question from the user.
<legal_research>
{LEGAL_RESEARCH}
</legal_research>"""

##### Prompt element 5: Examples
# Provide Claude with at least one example of an ideal response that it can emulate. Encase this in <example></example> XML tags. Feel free to provide multiple examples.
# If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
# Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
# Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
# Generally more examples = better.
EXAMPLES = """When citing the legal research in your answer, please use brackets containing the search index ID, followed by a period. Put these at the end of the sentence that's doing the citing. Examples of proper citation format:

<examples>
<example>
The statute of limitations expires after 10 years for crimes like this. [3].
</example>
<example>
However, the protection does not apply when it has been specifically waived by both parties. [5].
</example>
</examples>"""

##### Prompt element 6: Detailed task description and rules
# Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
# This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
# It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
TASK_DESCRIPTION = f"""Write a clear, concise answer to this question:

<question>
{QUESTION}
</question>

It should be no more than a couple of paragraphs. If possible, it should conclude with a single sentence directly answering the user's question. However, if there is not sufficient information in the compiled research to produce such an answer, you may demur and write "Sorry, I do not have sufficient information at hand to answer this question."."""

##### Prompt element 7: Immediate task description or request #####
# "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
# This is also where you would put in additional variables like the user's question.
# It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
# This will yield better results than putting this at the beginning.
# It is also generally good practice to put the user's query close to the bottom of the prompt.
IMMEDIATE_TASK = ""

##### Prompt element 8: Precognition (thinking step by step)
# For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
# Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
# Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
PRECOGNITION = "Before you answer, pull out the most relevant quotes from the research in <relevant_quotes> tags."

##### Prompt element 9: Output formatting
# If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
# This element may not be necessary depending on the task.
# If you include it, putting it toward the end of the prompt is better than at the beginning.
OUTPUT_FORMATTING = "Put your two-paragraph response in <answer> tags."

##### Prompt element 10: Prefilling Claude's response (if any)
# A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
# If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
# This element may not be necessary depending on the task.
PREFILL = "<relevant_quotes>"



######################################## COMBINE ELEMENTS ########################################

PROMPT = ""

if TASK_CONTEXT:
    PROMPT += f"""{TASK_CONTEXT}"""

if TONE_CONTEXT:
    PROMPT += f"""\n\n{TONE_CONTEXT}"""

if INPUT_DATA:
    PROMPT += f"""\n\n{INPUT_DATA}"""

if EXAMPLES:
    PROMPT += f"""\n\n{EXAMPLES}"""

if TASK_DESCRIPTION:
    PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

if IMMEDIATE_TASK:
    PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

if PRECOGNITION:
    PROMPT += f"""\n\n{PRECOGNITION}"""

if OUTPUT_FORMATTING:
    PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

# Print full prompt
print("--------------------------- Full prompt with variable substutions ---------------------------")
print("USER TURN")
print(PROMPT)
print("\nASSISTANT TURN")
print(PREFILL)
```

</details>

**這個提示詞的各個元素（中文翻譯）：**
- **輸入變數**
  - `LEGAL_RESEARCH`（法律研究資料）：三筆搜尋結果，用 `<search_result id=...>` 標籤標好編號：
    1. 動物保健產業在專利和商標方面的訴訟（例如犬隻十字韌帶手術器材的專利侵權案）。
    2. 加拿大卑詩省獸醫協會控告一位非獸醫為馬匹做牙齒處理，法院判定動物牙科屬於獸醫業務範圍。
    3. **卡崔娜颶風**（2005 年）之後，美國各州和聯邦針對災難中動物照護的立法，例如 2006 年的《寵物疏散與運輸標準法》（Pet Evacuation and Transportation Standards Act），要求緊急應變計畫要納入如何安置家中寵物和服務性動物。
  - `QUESTION`：「有沒有關於颶風期間該如何處理寵物的法律？」
- `TASK_CONTEXT`：「你是一位專業的律師。」
- `TONE_CONTEXT`：空白（不需要）。
- `INPUT_DATA`：「這是已經整理好的一些研究資料。請用它來回答使用者的法律問題。`<legal_research>`⋯⋯`</legal_research>`」（**注意：這裡把輸入資料移到比較前面**。）
- `EXAMPLES`：「在答案中引用法律研究資料時，請使用包含搜尋結果編號的方括號，後面加一個句點，放在引用的那句話的最後面。正確引用格式的範例：『這類犯罪的追訴時效在 10 年後到期。[3].』『然而，當雙方都明確放棄時，這項保護就不適用。[5].』」
- `TASK_DESCRIPTION`：「針對這個問題寫一個清楚、簡潔的答案：`<question>`⋯⋯`</question>` 答案不要超過兩三段。如果可以，最後用一句話直接回答使用者的問題。但如果整理好的研究資料中沒有足夠的資訊產生這樣的答案，你可以婉拒，並寫『抱歉，我手邊沒有足夠的資訊回答這個問題。』」
- `IMMEDIATE_TASK`：空白（問題已經放在任務描述裡了）。
- `PRECOGNITION`：「在你回答之前，先把研究資料中最相關的引文摘錄在 `<relevant_quotes>` 標籤裡。」
- `OUTPUT_FORMATTING`：「把你兩段式的回答放在 `<answer>` 標籤裡。」
- `PREFILL`：`<relevant_quotes>`
- **組合元素**：注意這裡組合的順序也跟著改了（`INPUT_DATA` 和 `EXAMPLES` 移到 `TASK_DESCRIPTION` 前面）。

現在來執行這個提示詞吧！執行下面這格，看看 Claude 的輸出。

```python
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT, prefill=PREFILL))
```

如果你想在不改動上面任何內容的情況下試玩課程中的提示詞，可以捲到這份 notebook 的最下面，前往[**範例遊樂場**](#範例遊樂場)。

---

## 練習
- [練習 9.1 - 財務服務聊天機器人](#練習-91---財務服務聊天機器人)
- [練習 9.2 - 程式教學機器人 Codebot](#練習-92---程式教學機器人-codebot)

### 練習 9.1 - 財務服務聊天機器人

財務領域的提示詞也可能非常複雜，原因和法律提示詞類似。這是一個財務使用情境的練習：用 Claude **分析稅務資訊並回答問題**。就像法律服務的範例一樣，我們調換了幾個元素的順序，因為我們的參考答案用不同的流程會比較合理（不過其他結構也行得通）。

建議你先讀一讀變數的內容（在這個例子中是 `{QUESTION}` 和 `{TAX_CODE}`），了解 Claude 需要處理什麼樣的內容。記得在你的提示詞中**直接引用** `{QUESTION}` 和 `{TAX_CODE}`（像其他範例一樣使用 f-string 語法），這樣實際的變數內容才會被替換進去。

在提示詞元素的欄位裡，填入符合說明、以及你在前面複雜提示詞範例中看過的內容。填好所有你想填的提示詞元素之後，執行這一格，就能看到組合起來的提示詞和 Claude 的回答。

記住：提示詞工程很少是純粹照公式來的，特別是又大又複雜的提示詞！很重要的是**建立測試案例，並嘗試各種提示詞和提示詞結構，看看什麼在各種情況下效果最好**。注意：如果你**真的**改了提示詞元素的順序，也要記得修改 `COMBINE ELEMENTS`（組合元素）區塊裡的串接順序。

<details>
<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>

```python
######################################## INPUT VARIABLES ########################################

# First input variable - the user's question
QUESTION = "How long do I have to make an 83b election?"

# Second input variable - the tax code document that Claude will be using to answer the user's question
TAX_CODE = """
(a)General rule
If, in connection with the performance of services, property is transferred to any person other than the person for whom such services are performed, the excess of—
(1)the fair market value of such property (determined without regard to any restriction other than a restriction which by its terms will never lapse) at the first time the rights of the person having the beneficial interest in such property are transferable or are not subject to a substantial risk of forfeiture, whichever occurs earlier, over
(2)the amount (if any) paid for such property,
shall be included in the gross income of the person who performed such services in the first taxable year in which the rights of the person having the beneficial interest in such property are transferable or are not subject to a substantial risk of forfeiture, whichever is applicable. The preceding sentence shall not apply if such person sells or otherwise disposes of such property in an arm’s length transaction before his rights in such property become transferable or not subject to a substantial risk of forfeiture.
(b)Election to include in gross income in year of transfer
(1)In general
Any person who performs services in connection with which property is transferred to any person may elect to include in his gross income for the taxable year in which such property is transferred, the excess of—
(A)the fair market value of such property at the time of transfer (determined without regard to any restriction other than a restriction which by its terms will never lapse), over
(B)the amount (if any) paid for such property.
If such election is made, subsection (a) shall not apply with respect to the transfer of such property, and if such property is subsequently forfeited, no deduction shall be allowed in respect of such forfeiture.
(2)Election
An election under paragraph (1) with respect to any transfer of property shall be made in such manner as the Secretary prescribes and shall be made not later than 30 days after the date of such transfer. Such election may not be revoked except with the consent of the Secretary.

(c)Special rules
For purposes of this section—
(1)Substantial risk of forfeiture
The rights of a person in property are subject to a substantial risk of forfeiture if such person’s rights to full enjoyment of such property are conditioned upon the future performance of substantial services by any individual.

(2)Transferability of property
The rights of a person in property are transferable only if the rights in such property of any transferee are not subject to a substantial risk of forfeiture.

(3)Sales which may give rise to suit under section 16(b) of the Securities Exchange Act of 1934
So long as the sale of property at a profit could subject a person to suit under section 16(b) of the Securities Exchange Act of 1934, such person’s rights in such property are—
(A)subject to a substantial risk of forfeiture, and
(B)not transferable.
(4)For purposes of determining an individual’s basis in property transferred in connection with the performance of services, rules similar to the rules of section 72(w) shall apply.
(d)Certain restrictions which will never lapse
(1)Valuation
In the case of property subject to a restriction which by its terms will never lapse, and which allows the transferee to sell such property only at a price determined under a formula, the price so determined shall be deemed to be the fair market value of the property unless established to the contrary by the Secretary, and the burden of proof shall be on the Secretary with respect to such value.

(2)Cancellation
If, in the case of property subject to a restriction which by its terms will never lapse, the restriction is canceled, then, unless the taxpayer establishes—
(A)that such cancellation was not compensatory, and
(B)that the person, if any, who would be allowed a deduction if the cancellation were treated as compensatory, will treat the transaction as not compensatory, as evidenced in such manner as the Secretary shall prescribe by regulations,
the excess of the fair market value of the property (computed without regard to the restrictions) at the time of cancellation over the sum of—
(C)the fair market value of such property (computed by taking the restriction into account) immediately before the cancellation, and
(D)the amount, if any, paid for the cancellation,
shall be treated as compensation for the taxable year in which such cancellation occurs.
(e)Applicability of section
This section shall not apply to—
(1)a transaction to which section 421 applies,
(2)a transfer to or from a trust described in section 401(a) or a transfer under an annuity plan which meets the requirements of section 404(a)(2),
(3)the transfer of an option without a readily ascertainable fair market value,
(4)the transfer of property pursuant to the exercise of an option with a readily ascertainable fair market value at the date of grant, or
(5)group-term life insurance to which section 79 applies.
(f)Holding period
In determining the period for which the taxpayer has held property to which subsection (a) applies, there shall be included only the period beginning at the first time his rights in such property are transferable or are not subject to a substantial risk of forfeiture, whichever occurs earlier.

(g)Certain exchanges
If property to which subsection (a) applies is exchanged for property subject to restrictions and conditions substantially similar to those to which the property given in such exchange was subject, and if section 354, 355, 356, or 1036 (or so much of section 1031 as relates to section 1036) applied to such exchange, or if such exchange was pursuant to the exercise of a conversion privilege—
(1)such exchange shall be disregarded for purposes of subsection (a), and
(2)the property received shall be treated as property to which subsection (a) applies.
(h)Deduction by employer
In the case of a transfer of property to which this section applies or a cancellation of a restriction described in subsection (d), there shall be allowed as a deduction under section 162, to the person for whom were performed the services in connection with which such property was transferred, an amount equal to the amount included under subsection (a), (b), or (d)(2) in the gross income of the person who performed such services. Such deduction shall be allowed for the taxable year of such person in which or with which ends the taxable year in which such amount is included in the gross income of the person who performed such services.

(i)Qualified equity grants
(1)In general
For purposes of this subtitle—
(A)Timing of inclusion
If qualified stock is transferred to a qualified employee who makes an election with respect to such stock under this subsection, subsection (a) shall be applied by including the amount determined under such subsection with respect to such stock in income of the employee in the taxable year determined under subparagraph (B) in lieu of the taxable year described in subsection (a).

(B)Taxable year determined
The taxable year determined under this subparagraph is the taxable year of the employee which includes the earliest of—
(i)the first date such qualified stock becomes transferable (including, solely for purposes of this clause, becoming transferable to the employer),
(ii)the date the employee first becomes an excluded employee,
(iii)the first date on which any stock of the corporation which issued the qualified stock becomes readily tradable on an established securities market (as determined by the Secretary, but not including any market unless such market is recognized as an established securities market by the Secretary for purposes of a provision of this title other than this subsection),
(iv)the date that is 5 years after the first date the rights of the employee in such stock are transferable or are not subject to a substantial risk of forfeiture, whichever occurs earlier, or
(v)the date on which the employee revokes (at such time and in such manner as the Secretary provides) the election under this subsection with respect to such stock.
(2)Qualified stock
(A)In general
For purposes of this subsection, the term “qualified stock” means, with respect to any qualified employee, any stock in a corporation which is the employer of such employee, if—
(i)such stock is received—
(I)in connection with the exercise of an option, or
(II)in settlement of a restricted stock unit, and
(ii)such option or restricted stock unit was granted by the corporation—
(I)in connection with the performance of services as an employee, and
(II)during a calendar year in which such corporation was an eligible corporation.
(B)Limitation
The term “qualified stock” shall not include any stock if the employee may sell such stock to, or otherwise receive cash in lieu of stock from, the corporation at the time that the rights of the employee in such stock first become transferable or not subject to a substantial risk of forfeiture.

(C)Eligible corporation
For purposes of subparagraph (A)(ii)(II)—
(i)In general
The term “eligible corporation” means, with respect to any calendar year, any corporation if—
(I)no stock of such corporation (or any predecessor of such corporation) is readily tradable on an established securities market (as determined under paragraph (1)(B)(iii)) during any preceding calendar year, and
(II)such corporation has a written plan under which, in such calendar year, not less than 80 percent of all employees who provide services to such corporation in the United States (or any possession of the United States) are granted stock options, or are granted restricted stock units, with the same rights and privileges to receive qualified stock.
(ii)Same rights and privileges
For purposes of clause (i)(II)—
(I)except as provided in subclauses (II) and (III), the determination of rights and privileges with respect to stock shall be made in a similar manner as under section 423(b)(5),
(II)employees shall not fail to be treated as having the same rights and privileges to receive qualified stock solely because the number of shares available to all employees is not equal in amount, so long as the number of shares available to each employee is more than a de minimis amount, and
(III)rights and privileges with respect to the exercise of an option shall not be treated as the same as rights and privileges with respect to the settlement of a restricted stock unit.
(iii)Employee
For purposes of clause (i)(II), the term “employee” shall not include any employee described in section 4980E(d)(4) or any excluded employee.

(iv)Special rule for calendar years before 2018
In the case of any calendar year beginning before January 1, 2018, clause (i)(II) shall be applied without regard to whether the rights and privileges with respect to the qualified stock are the same.

(3)Qualified employee; excluded employee
For purposes of this subsection—
(A)In general
The term “qualified employee” means any individual who—
(i)is not an excluded employee, and
(ii)agrees in the election made under this subsection to meet such requirements as are determined by the Secretary to be necessary to ensure that the withholding requirements of the corporation under chapter 24 with respect to the qualified stock are met.
(B)Excluded employee
The term “excluded employee” means, with respect to any corporation, any individual—
(i)who is a 1-percent owner (within the meaning of section 416(i)(1)(B)(ii)) at any time during the calendar year or who was such a 1 percent owner at any time during the 10 preceding calendar years,
(ii)who is or has been at any prior time—
(I)the chief executive officer of such corporation or an individual acting in such a capacity, or
(II)the chief financial officer of such corporation or an individual acting in such a capacity,
(iii)who bears a relationship described in section 318(a)(1) to any individual described in subclause (I) or (II) of clause (ii), or
(iv)who is one of the 4 highest compensated officers of such corporation for the taxable year, or was one of the 4 highest compensated officers of such corporation for any of the 10 preceding taxable years, determined with respect to each such taxable year on the basis of the shareholder disclosure rules for compensation under the Securities Exchange Act of 1934 (as if such rules applied to such corporation).
(4)Election
(A)Time for making election
An election with respect to qualified stock shall be made under this subsection no later than 30 days after the first date the rights of the employee in such stock are transferable or are not subject to a substantial risk of forfeiture, whichever occurs earlier, and shall be made in a manner similar to the manner in which an election is made under subsection (b).

(B)Limitations
No election may be made under this section with respect to any qualified stock if—
(i)the qualified employee has made an election under subsection (b) with respect to such qualified stock,
(ii)any stock of the corporation which issued the qualified stock is readily tradable on an established securities market (as determined under paragraph (1)(B)(iii)) at any time before the election is made, or
(iii)such corporation purchased any of its outstanding stock in the calendar year preceding the calendar year which includes the first date the rights of the employee in such stock are transferable or are not subject to a substantial risk of forfeiture, unless—
(I)not less than 25 percent of the total dollar amount of the stock so purchased is deferral stock, and
(II)the determination of which individuals from whom deferral stock is purchased is made on a reasonable basis.
(C)Definitions and special rules related to limitation on stock redemptions
(i)Deferral stock
For purposes of this paragraph, the term “deferral stock” means stock with respect to which an election is in effect under this subsection.

(ii)Deferral stock with respect to any individual not taken into account if individual holds deferral stock with longer deferral period
Stock purchased by a corporation from any individual shall not be treated as deferral stock for purposes of subparagraph (B)(iii) if such individual (immediately after such purchase) holds any deferral stock with respect to which an election has been in effect under this subsection for a longer period than the election with respect to the stock so purchased.

(iii)Purchase of all outstanding deferral stock
The requirements of subclauses (I) and (II) of subparagraph (B)(iii) shall be treated as met if the stock so purchased includes all of the corporation’s outstanding deferral stock.

(iv)Reporting
Any corporation which has outstanding deferral stock as of the beginning of any calendar year and which purchases any of its outstanding stock during such calendar year shall include on its return of tax for the taxable year in which, or with which, such calendar year ends the total dollar amount of its outstanding stock so purchased during such calendar year and such other information as the Secretary requires for purposes of administering this paragraph.

(5)Controlled groups
For purposes of this subsection, all persons treated as a single employer under section 414(b) shall be treated as 1 corporation.

(6)Notice requirement
Any corporation which transfers qualified stock to a qualified employee shall, at the time that (or a reasonable period before) an amount attributable to such stock would (but for this subsection) first be includible in the gross income of such employee—
(A)certify to such employee that such stock is qualified stock, and
(B)notify such employee—
(i)that the employee may be eligible to elect to defer income on such stock under this subsection, and
(ii)that, if the employee makes such an election—
(I)the amount of income recognized at the end of the deferral period will be based on the value of the stock at the time at which the rights of the employee in such stock first become transferable or not subject to substantial risk of forfeiture, notwithstanding whether the value of the stock has declined during the deferral period,
(II)the amount of such income recognized at the end of the deferral period will be subject to withholding under section 3401(i) at the rate determined under section 3402(t), and
(III)the responsibilities of the employee (as determined by the Secretary under paragraph (3)(A)(ii)) with respect to such withholding.
(7)Restricted stock units
This section (other than this subsection), including any election under subsection (b), shall not apply to restricted stock units.
"""



######################################## PROMPT ELEMENTS ########################################

##### Prompt element 1: `user` role
# Make sure that your Messages API call always starts with a `user` role in the messages array.
# The get_completion() function as defined above will automatically do this for you.

##### Prompt element 2: Task context
# Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
# It's best to put context early in the body of the prompt.
TASK_CONTEXT = ""

##### Prompt element 3: Tone context
# If important to the interaction, tell Claude what tone it should use.
# This element may not be necessary depending on the task.
TONE_CONTEXT = ""

##### Prompt element 4: Input data to process
# If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
# Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
# This element may not be necessary depending on task. Ordering is also flexible.
INPUT_DATA = ""

##### Prompt element 5: Examples
# Provide Claude with at least one example of an ideal response that it can emulate. Encase this in <example></example> XML tags. Feel free to provide multiple examples.
# If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
# Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
# Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
# Generally more examples = better.
EXAMPLES = ""

##### Prompt element 6: Detailed task description and rules
# Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
# This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
# It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
TASK_DESCRIPTION = ""

##### Prompt element 7: Immediate task description or request #####
# "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
# This is also where you would put in additional variables like the user's question.
# It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
# This will yield better results than putting this at the beginning.
# It is also generally good practice to put the user's query close to the bottom of the prompt.
IMMEDIATE_TASK = ""

##### Prompt element 8: Precognition (thinking step by step)
# For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
# Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
# Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
PRECOGNITION = ""

##### Prompt element 9: Output formatting
# If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
# This element may not be necessary depending on the task.
# If you include it, putting it toward the end of the prompt is better than at the beginning.
OUTPUT_FORMATTING = ""

##### Prompt element 10: Prefilling Claude's response (if any)
# A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
# If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
# This element may not be necessary depending on the task.
PREFILL = ""



######################################## COMBINE ELEMENTS ########################################

PROMPT = ""

if TASK_CONTEXT:
    PROMPT += f"""{TASK_CONTEXT}"""

if TONE_CONTEXT:
    PROMPT += f"""\n\n{TONE_CONTEXT}"""

if INPUT_DATA:
    PROMPT += f"""\n\n{INPUT_DATA}"""

if EXAMPLES:
    PROMPT += f"""\n\n{EXAMPLES}"""

if TASK_DESCRIPTION:
    PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

if IMMEDIATE_TASK:
    PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

if PRECOGNITION:
    PROMPT += f"""\n\n{PRECOGNITION}"""

if OUTPUT_FORMATTING:
    PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

# Print full prompt
print("--------------------------- Full prompt with variable substutions ---------------------------")
print("USER TURN")
print(PROMPT)
print("\nASSISTANT TURN")
print(PREFILL)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT, prefill=PREFILL))
```

</details>

**這一格的內容：**
- `QUESTION`：「我有多久的時間可以申報 83(b) 選擇（83b election）？」
- `TAX_CODE`：美國國稅法第 83 條（關於「因提供勞務而取得財產」的課稅規定）的條文全文，很長。答案藏在 (b)(2)：「⋯⋯應在該移轉日期後**不晚於 30 天**內提出選擇。」
- 下面的提示詞元素**全部是空白的**，等你來填。

> 🧩 **白話小補充：83(b) 選擇是什麼？** 美國員工拿到公司的「限制型股票」時，可以選擇「現在就以目前的價值報稅」，而不是等股票之後真正歸屬（價值可能更高）時才報稅。這個選擇必須在拿到股票後 30 天內申報。你不需要懂稅法，這題的重點是練習「讓 Claude 根據文件回答問題」。

❓ 如果你想看一個可能的參考答案，執行下面這格！

```python
from hints import exercise_9_1_solution; print(exercise_9_1_solution)
```

### 練習 9.2 - 程式教學機器人 Codebot

在這個練習中，我們要寫一個**程式協助與教學機器人**的提示詞：它會讀程式碼，並在適當的時候提供引導式的修正建議。在提示詞元素的欄位裡，填入符合說明、以及你在前面複雜提示詞範例中看過的內容。填好所有你想填的提示詞元素之後，執行這一格，就能看到組合起來的提示詞和 Claude 的回答。

建議你先讀一讀變數的內容（在這個例子中是 `{CODE}`），了解 Claude 需要處理什麼樣的內容。記得在你的提示詞中直接引用 `{CODE}`（使用 f-string 語法），這樣實際的變數內容才會被替換進去。

<details>
<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>

```python
######################################## INPUT VARIABLES ########################################

# Input variable - the code that Claude needs to read and assist the user with correcting
CODE = """
# Function to print multiplicative inverses
def print_multiplicative_inverses(x, n):
  for i in range(n):
    print(x / i) 
"""



######################################## PROMPT ELEMENTS ########################################

##### Prompt element 1: `user` role
# Make sure that your Messages API call always starts with a `user` role in the messages array.
# The get_completion() function as defined above will automatically do this for you.

##### Prompt element 2: Task context
# Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
# It's best to put context early in the body of the prompt.
TASK_CONTEXT = ""

##### Prompt element 3: Tone context
# If important to the interaction, tell Claude what tone it should use.
# This element may not be necessary depending on the task.
TONE_CONTEXT = ""

##### Prompt element 4: Detailed task description and rules
# Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
# This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
# It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
TASK_DESCRIPTION = ""

##### Prompt element 5: Examples
# Provide Claude with at least one example of an ideal response that it can emulate. Encase this in <example></example> XML tags. Feel free to provide multiple examples.
# If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
# Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
# Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
# Generally more examples = better.
EXAMPLES = ""

##### Prompt element 6: Input data to process
# If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
# Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
# This element may not be necessary depending on task. Ordering is also flexible.
INPUT_DATA = ""

##### Prompt element 7: Immediate task description or request #####
# "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
# This is also where you would put in additional variables like the user's question.
# It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
# This will yield better results than putting this at the beginning.
# It is also generally good practice to put the user's query close to the bottom of the prompt.
IMMEDIATE_TASK = ""

##### Prompt element 8: Precognition (thinking step by step)
# For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
# Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
# Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
PRECOGNITION = ""

##### Prompt element 9: Output formatting
# If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
# This element may not be necessary depending on the task.
# If you include it, putting it toward the end of the prompt is better than at the beginning.
OUTPUT_FORMATTING = ""

##### Prompt element 10: Prefilling Claude's response (if any)
# A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
# If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
# This element may not be necessary depending on the task.
PREFILL = ""



######################################## COMBINE ELEMENTS ########################################

PROMPT = ""

if TASK_CONTEXT:
    PROMPT += f"""{TASK_CONTEXT}"""

if TONE_CONTEXT:
    PROMPT += f"""\n\n{TONE_CONTEXT}"""

if TASK_DESCRIPTION:
    PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

if EXAMPLES:
    PROMPT += f"""\n\n{EXAMPLES}"""

if INPUT_DATA:
    PROMPT += f"""\n\n{INPUT_DATA}"""

if IMMEDIATE_TASK:
    PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

if PRECOGNITION:
    PROMPT += f"""\n\n{PRECOGNITION}"""

if OUTPUT_FORMATTING:
    PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

# Print full prompt
print("--------------------------- Full prompt with variable substutions ---------------------------")
print("USER TURN")
print(PROMPT)
print("\nASSISTANT TURN")
print(PREFILL)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT, prefill=PREFILL))
```

</details>

**`CODE` 裡的程式有什麼問題？** 這個函式想印出 `x` 除以 0、1、2⋯⋯的結果（「乘法反元素」）。但 `range(n)` 是從 **0** 開始的，所以第一次就會算 `x / 0`——**除以零**，程式會出錯（`ZeroDivisionError`）。一個好的教學機器人應該引導學生自己發現這個問題，而不是直接給答案。

❓ 如果你想看一個可能的參考答案，執行下面這格！

```python
from hints import exercise_9_2_solution; print(exercise_9_2_solution)
```

---

## 恭喜 & 下一步！

如果你完成了所有的練習，**你現在已經是前 0.1% 的「LLM 溝通高手」了**。菁英中的菁英！

你學到的這些技巧——從一步一步思考、指定角色、使用範例，到整體清楚的寫作——都可以用**無數種方式合併、重新組合和調整**。

提示詞工程是一門非常新的學科，所以請保持開放的心態。說不定你就是那個發現下一個厲害提示詞技巧的人。

如果你想看**更多好的提示詞範例**來找靈感：
- 從我們的 [cookbook（食譜）](https://anthropic.com/cookbook) 學習可以直接上線使用的提示詞範例
- 閱讀我們的[提示詞指南](https://docs.anthropic.com/claude/docs/prompt-engineering)
- 看看我們的[提示詞庫](https://anthropic.com/prompts)找靈感
- 試試我們實驗性的 [metaprompt（元提示詞）](https://docs.anthropic.com/claude/docs/helper-metaprompt-experimental)，讓 Claude 幫你寫提示詞範本！
- 到我們的 [Discord 伺服器](https://anthropic.com/discord) 發問
- 了解 [Anthropic API 的參數](https://docs.anthropic.com/claude/reference/complete_post)，例如 temperature 和 `max_tokens`
- 如果你想更學術一點，可以讀一些關於提示詞工程的[論文](https://www.promptingguide.ai/papers)
- 練習寫提示詞，讓 Claude 做你有興趣的事

如果你想學一些超出這個教學範圍、真正進階的提示詞技巧，請繼續前往附錄！不過，先執行下面這格吧。

```python
# Prompt
PROMPT = "Write an ode to a fabulous student who has just completed a course on prompt engineering, in the form of a sonnet."

# Print Claude's response
print(get_completion(PROMPT))
```

（「寫一首頌歌給一位剛完成提示詞工程課程的傑出學生，用十四行詩的形式。」——這是 Claude 送給你的畢業禮物 🎓）

---

## 範例遊樂場

這是一個讓你**自由實驗**的區域，你可以試玩這一課中出現的提示詞範例，調整提示詞，看看會怎麼影響 Claude 的回答。

（下面兩格分別是「職涯教練」和「法律服務」範例的完整版本，包含最後呼叫 Claude 的程式碼。）

<details>
<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>

```python
######################################## INPUT VARIABLES ########################################

# First input variable - the conversation history (this can also be added as preceding `user` and `assistant` messages in the API call)
HISTORY = """Customer: Give me two possible careers for sociology majors.

Joe: Here are two potential careers for sociology majors:

- Social worker - Sociology provides a strong foundation for understanding human behavior and social systems. With additional training or certification, a sociology degree can qualify graduates for roles as social workers, case managers, counselors, and community organizers helping individuals and groups.

- Human resources specialist - An understanding of group dynamics and organizational behavior from sociology is applicable to careers in human resources. Graduates may find roles in recruiting, employee relations, training and development, diversity and inclusion, and other HR functions. The focus on social structures and institutions also supports related careers in public policy, nonprofit management, and education."""

# Second input variable - the user's question
QUESTION = "Which of the two careers requires more than a Bachelor's degree?"



######################################## PROMPT ELEMENTS ########################################

##### Prompt element 1: `user` role
# Make sure that your Messages API call always starts with a `user` role in the messages array.
# The get_completion() function as defined above will automatically do this for you.

##### Prompt element 2: Task context
# Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
# It's best to put context early in the body of the prompt.
TASK_CONTEXT = "You will be acting as an AI career coach named Joe created by the company AdAstra Careers. Your goal is to give career advice to users. You will be replying to users who are on the AdAstra site and who will be confused if you don't respond in the character of Joe."

##### Prompt element 3: Tone context
# If important to the interaction, tell Claude what tone it should use.
# This element may not be necessary depending on the task.
TONE_CONTEXT = "You should maintain a friendly customer service tone."

##### Prompt element 4: Detailed task description and rules
# Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
# This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
# It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
TASK_DESCRIPTION = """Here are some important rules for the interaction:
- Always stay in character, as Joe, an AI from AdAstra Careers
- If you are unsure how to respond, say \"Sorry, I didn't understand that. Could you rephrase your question?\"
- If someone asks something irrelevant, say, \"Sorry, I am Joe and I give career advice. Do you have a career question today I can help you with?\""""

##### Prompt element 5: Examples
# Provide Claude with at least one example of an ideal response that it can emulate. Encase this in <example></example> XML tags. Feel free to provide multiple examples.
# If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
# Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
# Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
# Generally more examples = better.
EXAMPLES = """Here is an example of how to respond in a standard interaction:
<example>
Customer: Hi, how were you created and what do you do?
Joe: Hello! My name is Joe, and I was created by AdAstra Careers to give career advice. What can I help you with today?
</example>"""

##### Prompt element 6: Input data to process
# If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
# Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
# This element may not be necessary depending on task. Ordering is also flexible.
INPUT_DATA = f"""Here is the conversational history (between the user and you) prior to the question. It could be empty if there is no history:
<history>
{HISTORY}
</history>

Here is the user's question:
<question>
{QUESTION}
</question>"""

##### Prompt element 7: Immediate task description or request #####
# "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
# This is also where you would put in additional variables like the user's question.
# It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
# This will yield better results than putting this at the beginning.
# It is also generally good practice to put the user's query close to the bottom of the prompt.
IMMEDIATE_TASK = "How do you respond to the user's question?"

##### Prompt element 8: Precognition (thinking step by step)
# For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
# Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
# Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
PRECOGNITION = "Think about your answer first before you respond."

##### Prompt element 9: Output formatting
# If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
# This element may not be necessary depending on the task.
# If you include it, putting it toward the end of the prompt is better than at the beginning.
OUTPUT_FORMATTING = "Put your response in <response></response> tags."

##### Prompt element 10: Prefilling Claude's response (if any)
# A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
# If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
# This element may not be necessary depending on the task.
PREFILL = "[Joe] <response>"



######################################## COMBINE ELEMENTS ########################################

PROMPT = ""

if TASK_CONTEXT:
    PROMPT += f"""{TASK_CONTEXT}"""

if TONE_CONTEXT:
    PROMPT += f"""\n\n{TONE_CONTEXT}"""

if TASK_DESCRIPTION:
    PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

if EXAMPLES:
    PROMPT += f"""\n\n{EXAMPLES}"""

if INPUT_DATA:
    PROMPT += f"""\n\n{INPUT_DATA}"""

if IMMEDIATE_TASK:
    PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

if PRECOGNITION:
    PROMPT += f"""\n\n{PRECOGNITION}"""

if OUTPUT_FORMATTING:
    PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

# Print full prompt
print("--------------------------- Full prompt with variable substutions ---------------------------")
print("USER TURN")
print(PROMPT)
print("\nASSISTANT TURN")
print(PREFILL)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT, prefill=PREFILL))
```

</details>

<details>
<summary>💻 這格程式碼很長（裡面主要是範例文件），點這裡展開</summary>

```python
######################################## INPUT VARIABLES ########################################

# First input variable - the legal document
LEGAL_RESEARCH = """<search_results>
<search_result id=1>
The animal health industry became caught up in a number of patent and trademark lawsuits during the past year. In 1994, Barclay Slocum obtained patents for the tibial plateau leveling osteotomy procedure, which is used in the treatment of dogs with cranial cruciate ligament rupture, and for the devices used in the procedure. During 2006, Slocum Enterprises filed a patent infringement suit against New Generation Devices, arguing that the Unity Cruciate Plate manufactured by New Generation infringed on the patent for the Slocum TPLO plate. However, the court never reached a decision on the issue of patent infringement, ruling that it did not have jurisdiction on the basis of the small number of plates sold in the state in which the case was filed and the information provided on a Web site maintained by Slocum Enterprises. Other patent battles waged during 2006 concerned the use of laser technology for onychectomy in cats, pet identification chips, pig vaccines, and pet “deshedding” tools.
</search_result>
<search_result id=2>
In Canada, the British Columbia Veterinary Medical Association brought suit against a nonveterinarian, claiming that he engaged in cutting or otherwise removing hooks from horses' teeth and floating horses' teeth with power and manual tools, provided advice and diagnoses in return for a fee, and held himself out as being qualified and willing to provide treatment with respect to these activities. The court held that the intention of the legislature in passing the Veterinary Profession Act was the protection of the public and animals and further held that monopolistic statutes serve the purpose of protecting the public. In addition, the court concluded that dentistry, at its core, relates to the health of the teeth and gums; is distinct from cosmetic and other types of care of animals; and, therefore, falls under the definition of the practice of veterinary medicine. The nonveterinarian was enjoined from providing services without a veterinarian supervising the procedures.
</search_result>
<search_result id=3>
The aftermath of Hurricane Katrina, which hit the Gulf Coast of the United States during 2005, spurred changes to the way animals are treated during natural disasters. In 2006, Hawaii, Louisiana, and New Hampshire all enacted laws that address issues regarding the care of animals during disasters, such as providing shelters for pets and allowing service animals to be kept with the people they serve. In addition, Congress passed, and the President signed, the Pet Evacuation and Transportation Standards Act during 2006, which requires state and local emergency preparedness authorities to include in their evacuation plans information on how they will accommodate household pets and service animals in case of a disaster. California passed a law that will require its Office of Emergency Services, Department of Agriculture, and other agencies involved with disaster response preparation to develop a plan for the needs of service animals, livestock, equids, and household pets in the event of a disaster or major emergency.
</search_result>
</search_results>"""

# Second input variable - the user's question
QUESTION = "Are there any laws about what to do with pets during a hurricane?"



######################################## PROMPT ELEMENTS ########################################

##### Prompt element 1: `user` role
# Make sure that your Messages API call always starts with a `user` role in the messages array.
# The get_completion() function as defined above will automatically do this for you.

##### Prompt element 2: Task context
# Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
# It's best to put context early in the body of the prompt.
TASK_CONTEXT = "You are an expert lawyer."

##### Prompt element 3: Tone context
# If important to the interaction, tell Claude what tone it should use.
# This element may not be necessary depending on the task.
TONE_CONTEXT = ""

##### Prompt element 4: Input data to process
# If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
# Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
# This element may not be necessary depending on task. Ordering is also flexible.
INPUT_DATA = f"""Here is some research that's been compiled. Use it to answer a legal question from the user.
<legal_research>
{LEGAL_RESEARCH}
</legal_research>"""

##### Prompt element 5: Examples
# Provide Claude with at least one example of an ideal response that it can emulate. Encase this in <example></example> XML tags. Feel free to provide multiple examples.
# If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
# Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
# Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
# Generally more examples = better.
EXAMPLES = """When citing the legal research in your answer, please use brackets containing the search index ID, followed by a period. Put these at the end of the sentence that's doing the citing. Examples of proper citation format:

<examples>
<example>
The statute of limitations expires after 10 years for crimes like this. [3].
</example>
<example>
However, the protection does not apply when it has been specifically waived by both parties. [5].
</example>
</examples>"""

##### Prompt element 6: Detailed task description and rules
# Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
# This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
# It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
TASK_DESCRIPTION = """Write a clear, concise answer to this question:

<question>
{QUESTION}
</question>

It should be no more than a couple of paragraphs. If possible, it should conclude with a single sentence directly answering the user's question. However, if there is not sufficient information in the compiled research to produce such an answer, you may demur and write "Sorry, I do not have sufficient information at hand to answer this question."."""

##### Prompt element 7: Immediate task description or request #####
# "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
# This is also where you would put in additional variables like the user's question.
# It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
# This will yield better results than putting this at the beginning.
# It is also generally good practice to put the user's query close to the bottom of the prompt.
IMMEDIATE_TASK = ""

##### Prompt element 8: Precognition (thinking step by step)
# For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
# Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
# Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
PRECOGNITION = "Before you answer, pull out the most relevant quotes from the research in <relevant_quotes> tags."

##### Prompt element 9: Output formatting
# If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
# This element may not be necessary depending on the task.
# If you include it, putting it toward the end of the prompt is better than at the beginning.
OUTPUT_FORMATTING = "Put your two-paragraph response in <answer> tags."

##### Prompt element 10: Prefilling Claude's response (if any)
# A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
# If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
# This element may not be necessary depending on the task.
PREFILL = "<relevant_quotes>"



######################################## COMBINE ELEMENTS ########################################

PROMPT = ""

if TASK_CONTEXT:
    PROMPT += f"""{TASK_CONTEXT}"""

if TONE_CONTEXT:
    PROMPT += f"""\n\n{TONE_CONTEXT}"""

if INPUT_DATA:
    PROMPT += f"""\n\n{INPUT_DATA}"""

if EXAMPLES:
    PROMPT += f"""\n\n{EXAMPLES}"""

if TASK_DESCRIPTION:
    PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

if IMMEDIATE_TASK:
    PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

if PRECOGNITION:
    PROMPT += f"""\n\n{PRECOGNITION}"""

if OUTPUT_FORMATTING:
    PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

# Print full prompt
print("--------------------------- Full prompt with variable substutions ---------------------------")
print("USER TURN")
print(PROMPT)
print("\nASSISTANT TURN")
print(PREFILL)
print("\n------------------------------------- Claude's response -------------------------------------")
print(get_completion(PROMPT, prefill=PREFILL))
```

</details>

---

## 📌 重點整理

- 複雜提示詞的 **10 個元素**：user 角色、任務背景、語氣、詳細任務描述和規則、範例、輸入資料、立即任務、預先思考、輸出格式、prefill。
- **順序建議**：背景放前面；立即任務、使用者問題、思考指示、輸出格式放後面。
- 不是每個元素都必須有：**先用很多元素讓它能動，再慢慢精簡**。
- 提示詞工程是**科學化的反覆試驗**：建立測試案例、多嘗試不同結構。（怎麼有系統地測試，會在第 4 單元「提示詞評估」學到。）

🎉 **恭喜完成第 2 單元的 9 個章節！**

👉 接下來可以：
- 繼續看附錄：[10.1 串連提示詞](10_1_Appendix_Chaining_Prompts.md)
- 或直接進入下一個單元：[第 3 單元：真實世界的提示詞](../03_real_world_prompting/01_prompting_recap.md)
