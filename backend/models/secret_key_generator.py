import os
from ..local_storage import localStorage
from dotenv import load_dotenv

def dehasher(string):
    return string


def hasher(string):
    return string

load_dotenv()
LOCAL_STORAGE = localStorage
orc = 'ORC'
orc_key = 'Xh84PtDmGYycPnlLCyPLBVYBzpUZbPJdA2t2zxJhZKQ='
api_key = 'GEMINI_API_KEY'
api = os.getenv('GEMINI_API_KEY')
LOCAL_STORAGE.setItem(api_key, api)
LOCAL_STORAGE.setItem(orc, orc_key)
print(LOCAL_STORAGE.getItem(orc))
