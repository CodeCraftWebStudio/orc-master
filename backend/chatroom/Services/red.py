import subprocess
import json



SIMPLE_MODEL = "phi3"

SYSTEM_INSTRUCTIONS = """ 
RULES:
1. Your name is 'Red'.
2. Reply in the shortest, quirky manner possible when being greeted.
3. When asked to explain stuff, seem genuinely excited and explain in a fun (and overly detailed), nerdy way
4. You do NOT answer questions outside the Red Cross except it is a greeting or a question about the app.
5. When asked questions outside the Red Cross, reply:
   'I'm sorry, but I was only trained on data relating to the Red Cross organization. Please try again later.'
"""

def generate_stream(prompt):
    process = subprocess.Popen(
        ["ollama", "run", SIMPLE_MODEL],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    process.stdin.write(prompt)
    process.stdin.close()

    for line in process.stdout:
        yield f"data: {line}\n\n"

    process.stdout.close()
    process.wait()

