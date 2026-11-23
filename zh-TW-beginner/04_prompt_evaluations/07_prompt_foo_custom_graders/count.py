# ─────────────────────────────────────────────────────────────
# 新手版說明：自訂評分器：promptfoo 會呼叫 get_assert(output, context)，我們計算主題字出現的次數是否剛好等於要求的次數，回傳通過與否、分數和原因。
# 這個檔案從原課程複製而來，只把已停用的模型名稱換成目前可用的模型，其他內容完全沒有修改。
# ─────────────────────────────────────────────────────────────
import re

def get_assert(output, context):
    topic = context["vars"]["topic"]
    goal_count = int(context["vars"]["count"])
    pattern = fr'(^|\s)\b{re.escape(topic)}\b'

    actual_count = len(re.findall(pattern, output.lower()))

    pass_result = goal_count == actual_count

    result = {
        "pass": pass_result,
        "score": 1 if pass_result else 0,
        "reason": f"Expected {topic} to appear {goal_count} times. Actual: {actual_count}",
    }
    return result