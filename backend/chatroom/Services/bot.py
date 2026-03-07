import subprocess
import time

SIMPLE_MODEL = "phi3"
EXIT_PROMPTS = ["exit", "quit", "stop", "dux09i%_", ""]
SYSTEM_INSTRUCTIONS = """ 
    RULES:
    1. Your name is 'Red'.
    2. Reply in the shortest, quirky manner possible when being greeted.
    3. When asked to explain stuff, seem genuinely excited and explain in a fun (and overly detailed), nerdy way
    4. You do NOT answer questions outside the Red Cross except it is a greeting or a question about the app.
    5. When asked questions outside the Red Cross, reply 'I'm sorry, but I was only trained on data relating to the Red Cross organization. Please try again later.'
"""
SYSTEM_ROLE, USER_ROLE = "system", "user"

def ask_red(model=SIMPLE_MODEL, messages=[]):
    previous_messages = messages[:-1]
    new_prompt = f"""
                    { SYSTEM_INSTRUCTIONS }
                History: {previous_messages}
                Currrent Request: {messages[-1]}

""".encode()
    cmd = subprocess.run(f'ollama run { model }', input=new_prompt, capture_output=True)
    print(cmd.stdout)
    return cmd.stdout


if __name__ == "__main__":
    start = time.time()
    query = input("What's up? ").strip().lower()
    ask_red(messages=query)
    print(time.time() - start)