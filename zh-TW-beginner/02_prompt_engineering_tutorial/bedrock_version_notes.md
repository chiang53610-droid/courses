<!-- 本檔由 _build/build.py 自動產生，請修改 _build/src 中的原稿 -->
# 關於 Amazon Bedrock 版本的說明

> 這份說明是新手版整理的，對應原課程的 `prompt_engineering_interactive_tutorial/AmazonBedrock/` 資料夾。

## Bedrock 版是什麼？

原課程的「提示詞工程互動教學」有兩個版本：

| 版本 | 資料夾 | 怎麼連線到 Claude |
|---|---|---|
| **Anthropic 1P 版**（新手版以這個為主） | `Anthropic 1P/` | 用 Anthropic 的 API 金鑰，直接呼叫 Anthropic 的 API |
| **Amazon Bedrock 版** | `AmazonBedrock/` | 透過 AWS（亞馬遜雲端）的 **Bedrock** 服務呼叫 Claude，用的是 AWS 帳號權限 |

> 🧩 **白話小補充**：「1P」是 first party（第一方）的縮寫，意思是「直接跟 Anthropic 買」。Bedrock 則是「透過 AWS 這個通路使用 Claude」。就像同一款飲料，可以在品牌官網買，也可以在便利商店買，飲料本身是一樣的。

Bedrock 版的 README 說明（翻譯）：「這門課的目的，是讓你一步一步、全面地了解如何**在 Bedrock 上**設計 Claude 的最佳提示詞。」課程目標、9 章的結構、練習、範例遊樂場都和 1P 版相同。參考答案也是同一份——「雖然這份參考答案是以 1P API 請求的格式整理的，但答案是一樣的」。

## 兩個版本有什麼不同？

我們逐章比對過，**課程說明文字幾乎完全相同**，差別只有：

1. **連線方式（準備工作那一格）**
   - Bedrock 版又分成兩種寫法：
     - `AmazonBedrock/anthropic/`：用 Anthropic SDK 的 **`AnthropicBedrock`** 客戶端
       ```python
       from anthropic import AnthropicBedrock
       client = AnthropicBedrock(aws_region=AWS_REGION)
       ```
     - `AmazonBedrock/boto3/`：用 AWS 官方的 **`boto3`** 套件，直接呼叫 `bedrock-runtime` 的 `invoke_model`，自己組 JSON 請求、自己解析 JSON 回應
       ```python
       import boto3, json
       client = boto3.client('bedrock-runtime', region_name=AWS_REGION)
       body = json.dumps({"anthropic_version": "", "max_tokens": 2000,
                          "messages": [{"role": "user", "content": prompt}],
                          "temperature": 0.0, "top_p": 1, "system": system})
       response = client.invoke_model(body=body, modelId=MODEL_NAME)
       text = json.loads(response.get('body').read()).get('content')[0].get('text')
       ```
   - 模型名稱格式不同：Bedrock 上是 `anthropic.claude-3-haiku-20240307-v1:0`（前面多了 `anthropic.`，後面多了版本號）。
   - 第 0 課要用 `boto3.Session()` 取得 AWS 區域，並用 `%store` 存下 `MODEL_NAME` 和 `AWS_REGION`（而不是 `API_KEY`）。
   - 第 0 課用 `requirements.txt` 安裝固定版本的套件（`awscli`、`boto3`、`botocore`、`anthropic==0.21.3`、`pickleshare`），裝完要**重新啟動核心**。

2. **提示（hints）放的位置**：Bedrock 版放在 `AmazonBedrock/utils/hints.py`，用 `from utils import hints` 匯入；1P 版放在同一個資料夾的 `hints.py`。提示內容相同。

3. **文件連結**：Bedrock 版把 Anthropic 文件的連結換成了 AWS Bedrock 文件的連結。

4. **第 1 章多了兩句警告**：Bedrock 版在兩個「故意寫錯格式」的範例前面加了提醒：
   - 「⚠️ 警告：因為提示詞中 messages 參數的格式錯誤，下面這格會回傳錯誤。這是預期中的行為。」
   - 「⚠️ 警告：因為 `user` 和 `assistant` 角色沒有輪流交替，Claude 會回傳錯誤訊息。這是預期中的行為。」

5. **多了一篇附錄**：Bedrock 版有一篇 **「10.3 實證效能評估（Empirical Performance Evaluations）」**，1P 版沒有。新手版已經把它翻譯成 [附錄 10.4（加碼）](10_4_Appendix_Empirical_Performance_Evaluations.md)，並改寫成用 Anthropic API 金鑰就能執行。（Bedrock 版的「10.4 搜尋與檢索」就是 1P 版的 [10.3](10_3_Appendix_Search_and_Retrieval.md)，內容相同。）

6. **AWS 工作坊用的 CloudFormation 範本**：`AmazonBedrock/cloudformation/workshop-v1-final-cfn.yml` 是一份 AWS CloudFormation 設定檔，用來在 AWS 上**自動建立一個 SageMaker Jupyter 筆記本環境**（包含執行角色、Bedrock 存取權限、加密金鑰，並自動下載課程程式碼）。這是給參加 AWS 官方工作坊的人用的，自己在電腦上學習的話不需要它。原課程 README 也提供了 [AWS 工作坊版本](https://catalog.us-east-1.prod.workshops.aws/workshops/0644c9e9-5b82-45f2-8835-3b5aa30b1848/en-US) 的連結。

## 我應該用哪個版本？

- **你有 Anthropic API 金鑰** → 用新手版（以 1P 版為基礎），就是你現在在看的這套。
- **你的公司／學校只能透過 AWS 使用 Claude** → 可以把新手版每章「準備工作」那一格，換成上面 Bedrock 的連線寫法，其他內容完全相同。

> 🔄 **2026 更新**：Bedrock 上的模型名稱和可用模型會依 AWS 的規劃而變動（AWS 有自己的模型停用時程），Claude 3 Haiku 在 Bedrock 上也可能已經無法使用。請到 AWS Bedrock 主控台查詢你的區域目前可用的 Claude 模型。另外，Anthropic SDK 現在推薦在 Bedrock 上使用新的 `AnthropicBedrockMantle` 客戶端，舊的 `AnthropicBedrock` 仍可使用但屬於舊路徑。

👉 回到 [第 2 單元目錄](00_Tutorial_How-To.md#目錄)
