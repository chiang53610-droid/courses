# ─────────────────────────────────────────────────────────────
# 新手版說明：三個摘要提示詞函式（基本、較好、最好），promptfoo 會把文章內容傳進來。
# 這個檔案從原課程複製而來，只把已停用的模型名稱換成目前可用的模型，其他內容完全沒有修改。
# ─────────────────────────────────────────────────────────────
def basic_summarize(article):
  return f"Summarize this article {article}"

def better_summarize(article):
  return f"""
  Summarize this article for a grade-school audience: {article}"""

def best_summarize(article):
  return f"""
  You are tasked with summarizing long wikipedia articles for a grade-school audience.
  Write a short summary, keeping it as concise as possible. 
  The summary is intended for a non-technical, grade-school audience. 
  This is the article: {article}"""

