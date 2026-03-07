try:    
    import ollama
    import subprocess
    import time
except Exception as e:
    print(f"Error: {e}")

SIMPLE_MODEL = "phi3"
EXIT_PROMPTS = ["exit", "quit", "stop", "dux09i%_", ""]
SYSTEM_INSTRUCTIONS = """ Reply in the shortest, quirky manner possible """
SYSTEM_ROLE, USER_ROLE = "system", "user"

def init_ollama(model=SIMPLE_MODEL, messages=[]):
    previous_messages = messages[:-1]
    new_prompt = f"""
                    { SYSTEM_INSTRUCTIONS }
                History: {previous_messages}
                Currrent Request: {messages[-1]}

""".encode()
    cmd = subprocess.run(f'ollama run { model }', input=new_prompt, capture_output=True)
    print(cmd.stdout)
    return cmd.stdout
def create_message(role="user", content="Introduce yourself"):
    print("Creating message... ")
    return {
        "role": role,
        "content": content,
    }



def ask_query(message_object, model_name=SIMPLE_MODEL):
    print("Referencing Data models...")
    ollama.chat(model=model_name, messages=message_object)["messages"]["content"]


def chat_loop():
    messages = [create_message(role=SYSTEM_ROLE, content=SYSTEM_INSTRUCTIONS)]
    running = True
    while running:
        query = input("Ask anything: ")
        if query.lower().strip() in EXIT_PROMPTS:
            print("Exited")
            running = False
        messages.append(create_message(role=USER_ROLE, content=query))
        print("Message added, final process starting...")
        response = ask_query(message_object=messages)
        print(f"\nSypher: { response }\n")


        
if __name__ == "__main__":
    start = time.time()
    myQuery = "Hi, how are you"
    myNewQuery = myQuery.encode()
    print(type(myQuery))
    print(type(myNewQuery))
    init_ollama(messages=myNewQuery)
    print(time.time() - start)
  #  chat_loop()