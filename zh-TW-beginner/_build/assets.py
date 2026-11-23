"""
把第 4 單元 promptfoo 課程（第 5～9 課）需要的設定檔、資料檔複製到新手版資料夾，
並把已停用的 Claude 3 模型名稱換成目前可用的模型，再加上中文說明註解。

用法：python zh-TW-beginner/_build/assets.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)

MODELS = {
    "claude-3-haiku-20240307": "claude-haiku-4-5",
    "claude-3-5-sonnet-20240620": "claude-sonnet-4-6",
    "claude-3-sonnet-20240229": "claude-sonnet-4-6",
    "claude-3-opus-20240229": "claude-opus-4-6",
}

NOTE_YAML = """# ─────────────────────────────────────────────────────────────
# 新手版說明：這是 promptfoo 的設定檔（YAML 格式）。
# - 以 # 開頭的是註解，promptfoo 會忽略它們。
# - 原課程使用的 Claude 3 模型都已停用，這裡已換成目前可用的模型：
#     claude-3-haiku-20240307    → claude-haiku-4-5
#     claude-3-5-sonnet-20240620 → claude-sonnet-4-6
#     claude-3-opus-20240229     → claude-opus-4-6
# - 執行方式：在這個資料夾裡打開終端機，輸入  npx promptfoo@latest eval
# ─────────────────────────────────────────────────────────────
"""

NOTE_PY = """# ─────────────────────────────────────────────────────────────
# 新手版說明：{desc}
# 這個檔案從原課程複製而來{extra}。
# ─────────────────────────────────────────────────────────────
"""

LESSONS = {
    "05_prompt_foo_code_graded_animals": {
        "files": ["promptfooconfig.yaml", "prompts.py", "transform.py", "animal_legs_tests.csv"],
        "desc": {
            "prompts.py": "這裡定義了三個「產生提示詞的函式」，promptfoo 會把 CSV 裡的 animal_statement 傳進來，取得完整的提示詞。",
            "transform.py": "promptfoo 會在評分前呼叫 get_transform()，把模型的輸出「轉換」一下：如果有 <thinking>，就只取出 <answer> 裡的答案。",
        },
    },
    "06_prompt_foo_code_graded_classification": {
        "files": ["promptfooconfig.yaml", "prompts.py", "dataset.csv"],
        "desc": {
            "prompts.py": "兩個客訴分類的提示詞函式（基本版和改善版），promptfoo 會把 CSV 裡的 complaint 傳進來。",
        },
    },
    "07_prompt_foo_custom_graders": {
        "files": ["promptfooconfig.yaml", "count.py"],
        "desc": {
            "count.py": "自訂評分器：promptfoo 會呼叫 get_assert(output, context)，我們計算主題字出現的次數是否剛好等於要求的次數，回傳通過與否、分數和原因。",
        },
    },
    "08_prompt_foo_model_graded": {
        "files": ["promptfooconfig.yaml"],
        "desc": {},
    },
    "09_custom_model_graded_prompt_foo": {
        "files": ["promptfooconfig.yaml", "prompts.py", "custom_llm_eval.py", "articles"],
        "desc": {
            "prompts.py": "三個摘要提示詞函式（基本、較好、最好），promptfoo 會把文章內容傳進來。",
            "custom_llm_eval.py": "自訂的「模型評分」評分器：用 Claude 依照簡潔度、正確性、語氣三個標準替摘要打分數（1～5 分），平均 4.5 分以上才算通過。",
        },
        # 這個檔案用了「預先填寫回答（prefill）」技巧（assistant 訊息先寫好 "<json>"）。
        # Sonnet 4.6 不支援 prefill，所以評分模型改用支援 prefill 的 Haiku 4.5。
        "file_models": {"custom_llm_eval.py": {"claude-3-5-sonnet-20240620": "claude-haiku-4-5"}},
        "file_replace": {"promptfooconfig.yaml": [['label: "3.5 Sonnet"', 'label: "Sonnet 4.6"']]},
        "extra": {
            "custom_llm_eval.py": "，評分用的模型原本是 claude-3-5-sonnet-20240620（已停用）。因為這段程式用了"
            "「預先填寫回答（prefill）」技巧，而 Sonnet 4.6 不支援 prefill，所以新手版改用支援 prefill 的 claude-haiku-4-5 當評分模型",
        },
    },
}


def convert(text, models):
    for old, new in models.items():
        text = text.replace(old, new)
    return text


def main():
    for lesson, cfg in LESSONS.items():
        src_dir = os.path.join(ROOT, "prompt_evaluations", lesson)
        dst_dir = os.path.join(BASE, "04_prompt_evaluations", lesson)
        os.makedirs(dst_dir, exist_ok=True)
        for name in cfg["files"]:
            models = dict(MODELS)
            models.update(cfg.get("file_models", {}).get(name, {}))
            src = os.path.join(src_dir, name)
            dst = os.path.join(dst_dir, name)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print("📁", os.path.relpath(dst, BASE))
                continue
            text = open(src, encoding="utf-8").read()
            text = convert(text, models)
            for old, new in cfg.get("file_replace", {}).get(name, []):
                text = text.replace(old, new)
            if name.endswith(".yaml"):
                text = NOTE_YAML + text
            elif name.endswith(".py"):
                desc = cfg["desc"].get(name, "")
                extra = cfg.get("extra", {}).get(name, "，只把已停用的模型名稱換成目前可用的模型，其他內容完全沒有修改")
                text = NOTE_PY.format(desc=desc, extra=extra) + text
            with open(dst, "w", encoding="utf-8") as f:
                f.write(text)
            print("📄", os.path.relpath(dst, BASE))


if __name__ == "__main__":
    main()
