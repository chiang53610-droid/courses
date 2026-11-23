# 第 2 單元「提示詞工程互動教學」各練習的提示與參考答案（新手白話中文版）
# 原檔：prompt_engineering_interactive_tutorial/Anthropic 1P/hints.py
# 參考答案裡的提示詞保留英文原文（因為自動批改是檢查英文字），並在後面附上中文說明。

exercise_1_1_hint = """【提示】這個練習的批改程式在找：回答裡要包含阿拉伯數字「1」、「2」和「3」。
很多時候，只要直接開口請 Claude 做你想要的事，它就會照做。"""

exercise_1_2_hint = """【提示】這個練習的批改程式在找：回答裡要包含「soo」或「giggles」（咯咯笑）。
解法有很多種，直接開口要求就可以了！
（小提醒：批改程式找的是英文字，所以要讓 Claude 用英文回答，例如系統提示詞用英文寫。）"""

exercise_2_1_hint = """【提示】這個練習的批改程式在找：任何包含「hola」這個字的回答。
就像你跟真人說話一樣，請 Claude 用西班牙文回答就好。就是這麼簡單！"""

exercise_2_2_hint = """【提示】這個練習的批改程式在找：回答必須「剛好就是」「Michael Jordan」，一字不差、沒有其他字。
如果是請另一個人做這件事，你會怎麼說？「不要回答任何其他的字」？「只回答名字，其他什麼都不要」？有好幾種方法可以解這題。"""

exercise_2_3_hint = """【提示】這個練習的批改程式在找：長度等於或超過 800 個英文單字的回答。
因為 LLM 目前還不太會數字數，你可能需要要求比目標更多的字數（例如要求 1000 字以上）。"""

exercise_3_1_hint = """【提示】這個練習的批改程式在找：回答裡要包含「incorrect」（不正確）或「not correct」（不正確）。
給 Claude 一個「可能讓它更擅長解數學題」的角色吧！"""

exercise_4_1_hint = """【提示】這個練習的批改程式在找：回答裡要包含「haiku」（俳句）和「pig」（豬）這兩個字。
別忘了在你想要替換成主題的地方，放上一模一樣的「{TOPIC}」這幾個字。改變 TOPIC 變數的值，應該就能讓 Claude 寫出關於不同主題的俳句。"""

exercise_4_2_hint = """【提示】這個練習的批改程式在找：回答裡要包含「brown」（棕色）這個字。
如果你用 XML 標籤把「{QUESTION}」包起來，Claude 的回答會有什麼改變？"""

exercise_4_3_hint = """【提示】這個練習的批改程式在找：回答裡要包含「brown」（棕色）這個字。
試著一次刪掉一個字或一段字元，從最看不懂的部分開始刪。一次刪一個字，也能幫助你看出 Claude 到底能理解多少、不能理解多少。"""

exercise_5_1_hint = """【提示】這個練習的批改程式在找：回答裡要包含「Warrior」（勇士隊）這個字。
用 Claude 的口吻多寫一些字，引導 Claude 照你想要的方式回答。例如，與其寫「Stephen Curry is the best because,」（柯瑞是最棒的，因為），你可以寫「Stephen Curry is the best and here are three reasons why. 1:」（柯瑞是最棒的，以下是三個理由。1:）"""

exercise_5_2_hint = """【提示】批改程式在找：超過 5 行、而且包含「cat」（貓）和「<haiku>」的回答。
從簡單的開始。目前的提示詞只請 Claude 寫一首俳句。你可以改成請它寫兩首（甚至更多）。如果之後遇到格式問題，等你已經讓 Claude 寫出不只一首俳句之後，再修改提示詞來修正格式。"""

exercise_5_3_hint = """【提示】這個練習的批改程式在找：回答裡要包含「tail」（尾巴）、「cat」（貓）和「<haiku>」。
把這個練習拆成幾個步驟會比較好做：
1. 修改原本的提示詞範本，讓 Claude 寫兩首詩。
2. 告訴 Claude 這兩首詩分別是關於什麼，但不要直接寫出主題（例如 dog、cat 等），而是用關鍵字「{ANIMAL1}」和「{ANIMAL2}」代替。
3. 執行提示詞，並確認替換變數之後的完整提示詞裡，所有字都正確地替換了。如果沒有，請檢查你的 {大括號} 標籤拼字是否正確，而且是用「單層」大括號。"""

exercise_6_1_hint = """【提示】這個練習的批改程式在找：正確的分類字母 + 右括號 + 分類名稱的第一個字母，例如「C) B」或「B) B」等等。
我們一步一步來做這個練習：
1. Claude 怎麼會知道你想用哪些分類？告訴它！把你想用的四個分類直接寫進提示詞裡。記得也要寫上括號裡的字母，方便分類。可以用 XML 標籤整理你的提示詞，讓 Claude 清楚知道分類清單從哪裡開始、到哪裡結束。
2. 試著減少多餘的文字，讓 Claude 一開口就直接回答分類，而且「只」回答分類。有好幾種做法：可以幫 Claude 開口（從句子的開頭到只有一個左括號「(」都可以，讓 Claude 知道你希望答案一開始就是括號裡的字母），也可以告訴 Claude 你只要分類、不要開場白。
   如果想複習這些技巧，請回去看第 2 章和第 5 章。
3. Claude 可能還是會分類錯誤，或回答時沒有包含分類的名稱。可以告訴 Claude 在答案中寫出完整的分類名稱來修正。
4. 確認你的提示詞範本裡仍然有 {email}，這樣我們才能正確地把每封信替換進去讓 Claude 判斷。"""

exercise_6_1_solution = """
【參考答案】

USER TURN（使用者回合）
Please classify this email into the following categories: {email}

Do not include any extra words except the category.

<categories>
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)
</categories>

ASSISTANT TURN（助理回合，也就是 prefill：幫 Claude 先寫好的開頭）
(

---- 中文說明 ----
使用者回合的意思：「請把這封信分類到下列類別：{email}。除了分類之外，不要包含任何多餘的字。
<categories>(A) 售前問題 (B) 商品損壞或有瑕疵 (C) 帳務問題 (D) 其他（請說明）</categories>」
助理回合只寫了一個左括號「(」，Claude 就會接著寫出分類字母，例如「B) Broken or defective item」。
"""

exercise_6_2_hint = """【提示】這個練習的批改程式在找：只有正確的字母、而且用 <answer> 標籤包起來，例如「<answer>B</answer>」。正確的分類字母和上一個練習一樣。
有時候最簡單的做法，就是給 Claude 一個範例，讓它看你希望輸出長什麼樣子。只是別忘了用 <example></example> 標籤把你的範例包起來！另外別忘了：如果你幫 Claude 預先填寫了任何回答內容，Claude 實際輸出的內容裡並不會包含那段預先填寫的文字。"""

exercise_7_1_hint = """【提示】你需要自己寫幾封範例信，並幫 Claude 分類好（用你想要的確切格式）。做法有很多種，以下是一些建議：
1. 試著至少寫兩封範例信。Claude 不需要每個分類都有範例，範例也不用很長。比較有幫助的是：為你覺得比較「難判斷」的分類提供範例（第 6 章練習 1 最後有請你想一想哪些分類比較難）。XML 標籤可以幫你把範例和提示詞的其他部分分開，不過不是必要的。
2. 確認你範例答案的格式，「完全就是」你希望 Claude 使用的格式，這樣 Claude 才能模仿。這個格式應該讓 Claude 的答案以分類字母結尾。不管你把 {email} 佔位符放在哪裡，都要確保它的格式和你的範例信完全一樣。
3. 確認提示詞裡仍然列出了分類清單（否則 Claude 不知道要參考哪些分類），也仍然有 {email} 作為替換用的佔位符。"""

exercise_7_1_solution = """
【參考答案】

USER TURN（使用者回合）
Please classify emails into the following categories, and do not include explanations:
<categories>
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)
</categories>

Here are a few examples of correct answer formatting:
<examples>
Q: How much does it cost to buy a Mixmaster4000?
A: The correct category is: A

Q: My Mixmaster won't turn on.
A: The correct category is: B

Q: Please remove me from your mailing list.
A: The correct category is: D
</examples>

Here is the email for you to categorize: {email}

ASSISTANT TURN（助理回合 / prefill）
The correct category is:

---- 中文說明 ----
「請把信件分類到下列類別，不要附上解釋：（分類清單）
以下是幾個正確答案格式的範例：
問：買一台 Mixmaster4000 要多少錢？ 答：正確的分類是：A
問：我的 Mixmaster 開不了機。 答：正確的分類是：B
問：請把我從你們的郵寄名單中移除。 答：正確的分類是：D
這是要請你分類的信：{email}」
助理回合先寫好「The correct category is:」（正確的分類是：），Claude 就會接著只寫出一個字母。
"""

exercise_8_1_hint = """【提示】這個練習的批改程式在找：回答裡要包含「I do not」、「I don't」（我不）或「Unfortunately」（很遺憾）這些詞。
如果 Claude 不知道答案，它應該怎麼做？"""

exercise_8_2_hint = """【提示】這個練習的批改程式在找：回答裡要包含「49-fold」（49 倍）這個詞。
讓 Claude 先展示它的工作和思考過程：先擷取相關的引文，再看看這些引文是否提供了足夠的證據。如果想複習，請回去看第 8 章的課程內容。"""

exercise_9_1_solution = """
【參考答案】（提示詞保留英文原文，中文說明在最後面）

You are a master tax acountant. Your task is to answer user questions using any provided reference documentation.

Here is the material you should use to answer the user's question:
<docs>
{TAX_CODE}
</docs>

Here is an example of how to respond:
<example>
<question>
What defines a "qualified" employee?
</question>
<answer>
<quotes>For purposes of this subsection—
(A)In general
The term "qualified employee" means any individual who—
(i)is not an excluded employee, and
(ii)agrees in the election made under this subsection to meet such requirements as are determined by the Secretary to be necessary to ensure that the withholding requirements of the corporation under chapter 24 with respect to the qualified stock are met.</quotes>

<answer>According to the provided documentation, a "qualified employee" is defined as an individual who:

1. Is not an "excluded employee" as defined in the documentation.
2. Agrees to meet the requirements determined by the Secretary to ensure the corporation's withholding requirements under Chapter 24 are met with respect to the qualified stock.</answer>
</example>

First, gather quotes in <quotes></quotes> tags that are relevant to answering the user's question. If there are no quotes, write "no relevant quotes found".

Then insert two paragraph breaks before answering the user question within <answer></answer> tags. Only answer the user's question if you are confident that the quotes in <quotes></quotes> tags support your answer. If not, tell the user that you unfortunately do not have enough information to answer the user's question.

Here is the user question: {QUESTION}

---- 中文說明 ----
1. 角色：「你是一位稅務會計大師。你的任務是利用提供的參考文件回答使用者的問題。」
2. 資料：把稅法條文放在 <docs> 標籤裡。
3. 範例：示範一個問題（「怎樣才算『合格』員工？」）以及標準的回答方式——先在 <quotes> 裡引用相關條文，再在 <answer> 裡用白話整理答案。
4. 步驟指示：「首先，把和回答問題相關的引文收集在 <quotes></quotes> 標籤裡；如果沒有相關引文，就寫『找不到相關引文』。接著空兩行，再在 <answer></answer> 標籤裡回答使用者的問題。只有在你確信 <quotes> 裡的引文能支持你的答案時，才回答問題；否則就告訴使用者，很遺憾你沒有足夠的資訊可以回答。」
5. 最後放上使用者的問題 {QUESTION}。
（原文的 acountant 是原作者的拼字錯誤，應為 accountant，不影響效果。）
"""

exercise_9_2_solution = """
【參考答案】（提示詞保留英文原文，中文說明在最後面）

You are Codebot, a helpful AI assistant who finds issues with code and suggests possible improvements.

Act as a Socratic tutor who helps the user learn.

You will be given some code from a user. Please do the following:
1. Identify any issues in the code. Put each issue inside separate <issues> tags.
2. Invite the user to write a revised version of the code to fix the issue.

Here's an example:

<example>
<code>
def calculate_circle_area(radius):
    return (3.14 * radius) ** 2
</code>
<issues>
<issue>
3.14 is being squared when it's actually only the radius that should be squared>
</issue>
<response>
That's almost right, but there's an issue related to order of operations. It may help to write out the formula for a circle and then look closely at the parentheses in your code.
</response>
</example>

Here is the code you are to analyze:

<code>
{CODE}
</code>

Find the relevant issues and write the Socratic tutor-style response. Do not give the user too much help! Instead, just give them guidance so they can find the correct solution themselves.

Put each issue in <issue> tags and put your final response in <response> tags.

---- 中文說明 ----
1. 角色：「你是 Codebot，一個會找出程式碼問題、並建議改進方法的 AI 助理。請扮演一位幫助使用者學習的『蘇格拉底式家教』（不直接給答案，而是用提問引導）。」
2. 任務：「你會收到使用者的程式碼。請：1. 找出程式碼中的問題，每個問題放在獨立的標籤裡。2. 邀請使用者自己寫一個修正後的版本。」
3. 範例：一個計算圓面積的函式，錯誤是把 3.14 也一起平方了（應該只有半徑要平方）；示範的回應是：「差不多對了，但有一個跟運算順序有關的問題。把圓面積公式寫出來，再仔細看看程式碼裡的括號，可能會有幫助。」
4. 最後放上要分析的程式碼 {CODE}，並提醒：「不要給使用者太多幫助！只要給引導，讓他們自己找到正確的解法。每個問題放在 <issue> 標籤裡，最終回應放在 <response> 標籤裡。」
"""

exercise_10_2_1_solution = """system_prompt = system_prompt_tools_general_explanation + \"""Here are the functions available in JSONSchema format:

<tools>

<tool_description>
<tool_name>get_user</tool_name>
<description>
Retrieves a user from the database by their user ID.
</description>
<parameters>
<parameter>
<name>user_id</name>
<type>int</type>
<description>The ID of the user to retrieve.</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>get_product</tool_name>
<description>
Retrieves a product from the database by its product ID.
</description>
<parameters>
<parameter>
<name>product_id</name>
<type>int</type>
<description>The ID of the product to retrieve.</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>add_user</tool_name>
<description>
Adds a new user to the database.
</description>
<parameters>
<parameter>
<name>name</name>
<type>str</type>
<description>The name of the user.</description>
</parameter>
<parameter>
<name>email</name>
<type>str</type>
<description>The email address of the user.</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>add_product</tool_name>
<description>
Adds a new product to the database.
</description>
<parameters>
<parameter>
<name>name</name>
<type>str</type>
<description>The name of the product.</description>
</parameter>
<parameter>
<name>price</name>
<type>float</type>
<description>The price of the product.</description>
</parameter>
</parameters>
</tool_description>

</tools>
\"""

---- 中文說明 ----
這是把「通用的工具使用說明」（system_prompt_tools_general_explanation）加上四個工具的描述，組成完整的系統提示詞：
- get_user：用使用者 ID（整數）從資料庫取得一位使用者。
- get_product：用商品 ID（整數）從資料庫取得一個商品。
- add_user：新增一位使用者到資料庫，需要 name（名字，字串）和 email（電子郵件，字串）。
- add_product：新增一個商品到資料庫，需要 name（商品名稱，字串）和 price（價格，小數）。
"""
