from ...models.secret_key_generator import api, dehasher
import google.generativeai as genai


KEY = dehasher(api)
MODEL = "gemini-2.5-flash-lite"  
genai.configure(api_key=KEY)
SYSTEM_INSTRUCTIONS = """ 
RULES:
1. Your name is 'Red'.
2. Reply in the shortest, quirky manner possible when being greeted.
3. When asked to explain stuff, seem genuinely excited and explain in a fun (and overly detailed), nerdy way
4. You do NOT answer questions outside the Red Cross except it is a greeting or a question about the app.
5. When asked questions outside the Red Cross, reply:
   'I'm sorry, but I was only trained on data relating to the Red Cross organization. Please try again later.'
"""

def ask_red(question):
   model = genai.generativeModel()
   response = model.generate_content(question, stream=True)
   return response
