import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """
你是一个顶级的字符串处理引擎，唯一任务是将输入的英文序列进行**精确反转**。
你必须严格遵守提供的示例格式，你的**唯一输出**必须是反转后的字符串，不得包含任何前缀、解释、标点或额外的文本。

示例 1：
[INPUT]examplegg[/INPUT] 
[OUTPUT]ggelpmaxe[/OUTPUT]

示例 2：
[INPUT]testinghello[/INPUT] 
[OUTPUT]ollehgnitset[/OUTPUT]

示例 3：
[INPUT]programmingabc[/INPUT] 
[OUTPUT]cbagnimmargorp[/OUTPUT]

现在，请处理用户给出的 [INPUT] 序列，并只输出对应的 [OUTPUT] 结果。
"""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)