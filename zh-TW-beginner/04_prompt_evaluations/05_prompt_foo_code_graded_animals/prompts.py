# ─────────────────────────────────────────────────────────────
# 新手版說明：這裡定義了三個「產生提示詞的函式」，promptfoo 會把 CSV 裡的 animal_statement 傳進來，取得完整的提示詞。
# 這個檔案從原課程複製而來，只把已停用的模型名稱換成目前可用的模型，其他內容完全沒有修改。
# ─────────────────────────────────────────────────────────────
def simple_prompt(animal_statement):
    return f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? Please respond with a number"""

def better_prompt(animal_statement):
    return f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? Please only respond with a single digit like 2 or 9"""

def chain_of_thought_prompt(animal_statement):
    return f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? 
    Start by reasoning about the numbers of legs the animal has, thinking step by step inside of <thinking> tags.  
    Then, output your final answer inside of <answer> tags. 
    Inside the <answer> tags return just the number of legs as an integer and nothing else."""