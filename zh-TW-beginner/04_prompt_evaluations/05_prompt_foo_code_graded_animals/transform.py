# ─────────────────────────────────────────────────────────────
# 新手版說明：promptfoo 會在評分前呼叫 get_transform()，把模型的輸出「轉換」一下：如果有 <thinking>，就只取出 <answer> 裡的答案。
# 這個檔案從原課程複製而來，只把已停用的模型名稱換成目前可用的模型，其他內容完全沒有修改。
# ─────────────────────────────────────────────────────────────
def get_transform(output, context):
    if "<thinking>" in output:
        try:
            return output.split("<answer>")[1].split("</answer>")[0].strip()
        except Exception as e:
            print(f"Error in get_transform: {e}")
            return output
    return output

