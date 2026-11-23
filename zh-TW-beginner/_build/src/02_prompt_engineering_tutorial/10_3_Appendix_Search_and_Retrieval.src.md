<!--meta {"orig": "prompt_engineering_interactive_tutorial/Anthropic 1P/10.3_Appendix_Search & Retrieval.ipynb", "out": "02_prompt_engineering_tutorial/10_3_Appendix_Search_and_Retrieval", "md_only": true} -->
# 附錄 10.3：搜尋與檢索（Search & Retrieval）

> 📚 **第 2 單元：提示詞工程互動教學**｜附錄 3 / 共 3 篇（超越標準提示詞）
> ⏱️ 預估時間：5 分鐘（這篇是純閱讀，原課程只有一段說明和幾個延伸閱讀連結，沒有程式碼）

## 原文翻譯

你知道你可以用 Claude **幫你搜尋維基百科**嗎？Claude 可以找出並取回文章，接著你還可以用 Claude 摘要、整合這些文章，根據找到的內容寫出新的東西，還有更多用途。而且不只是維基百科！你也可以搜尋你自己的文件——不管是存成純文字，還是嵌入（embed）在向量資料庫裡的文件都可以。

請參考我們的 [RAG cookbook 範例](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Wikipedia/wikipedia-search-cookbook.ipynb)，學習怎麼利用從向量資料庫、維基百科、網際網路等地方取回的資料，來**補充 Claude 的知識**，並提升 Claude 回答的準確度和相關性。在那裡，你也可以學到怎麼使用某些 [embeddings（嵌入向量）](https://docs.anthropic.com/claude/docs/embeddings) 和向量資料庫工具。

如果你有興趣學習使用 Claude 的進階 RAG 架構，可以看看我們的 [Claude 3 技術簡報：RAG 架構](https://docs.google.com/presentation/d/1zxkSI7lLUBrZycA-_znwqu8DDyVhHLkQGScvzaZrUns/edit#slide=id.g2c736259dac_63_782)。

---

## 🧩 白話小補充：這些名詞是什麼意思？

| 名詞 | 白話解釋 |
|---|---|
| **檢索（Retrieval）** | 「把相關的資料找出來」。 |
| **RAG**（Retrieval-Augmented Generation，檢索增強生成） | 先**找資料**，再把找到的資料放進提示詞裡，讓 Claude **根據這些資料回答**。就像考試可以「翻書」：Claude 不用全部背起來，需要時先查資料再作答，答案會更準確、更新，也比較不會產生幻覺。 |
| **Embedding（嵌入向量）** | 把一段文字轉換成一串數字，意思相近的文字，轉出來的數字也會很接近。這樣電腦就能用「意思」而不只是「關鍵字」來找資料。 |
| **向量資料庫（Vector database）** | 專門存放 embedding、能快速找出「意思最接近」的資料的資料庫。 |

**RAG 的基本流程：**

```
使用者的問題
   ↓
① 搜尋：從文件庫／維基百科／網路找出最相關的幾段資料
   ↓
② 組合：把找到的資料放進提示詞（例如用 <document> 標籤包起來，第 4 章學過）
   ↓
③ 回答：請 Claude 只根據這些資料回答（可以搭配第 8 章「先找引文再回答」的技巧）
```

> 🔄 **2026 更新**：
> - 原文中的連結有些可能已經搬家（例如 Anthropic 的文件網站和 cookbook 的網址有改版），如果打不開，可以到 Anthropic 官方文件網站搜尋「RAG」、「embeddings」或「retrieval」。
> - 現在 Claude API 也提供內建的「**網路搜尋工具（web search tool）**」，Claude 可以自己上網搜尋資料再回答。
> - 本套課程的**第 5 單元「工具使用」**會實際做一個「讓 Claude 搜尋維基百科」的練習，到時候你就會親手實作上面說的流程！

---

## 📌 重點整理

- Claude 可以搭配**搜尋**（維基百科、網路、你自己的文件）來補充知識。
- **RAG** = 先檢索相關資料，再讓 Claude 根據資料回答，能提升準確度、減少幻覺。
- embedding 和向量資料庫是「用意思來找資料」的常用工具。

🎉 **恭喜你完成第 2 單元「提示詞工程互動教學」的全部內容！**

👉 加碼內容（AWS Bedrock 版才有的附錄）：[附錄 10.4：實證效能評估](10_4_Appendix_Empirical_Performance_Evaluations.md)
👉 下一個單元：[第 3 單元：真實世界的提示詞](../03_real_world_prompting/01_prompting_recap.md)
