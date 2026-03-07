from ..local_storage import localStorage


def dehasher(string):
    return string
def hasher(string):
    return string
LOCAL_STORAGE = localStorage()
orc = 'ORC'
orc_key = 'Xh84PtDmGYycPnlLCyPLBVYBzpUZbPJdA2t2zxJhZKQ='
api_key = 'GEMINI_API_KEY'
api = 'AIzaSyDce1_NgK4GA0YeT--tZ0QWCk2-AnKRRnM'
LOCAL_STORAGE.setItem(api_key, api)
LOCAL_STORAGE.setItem(orc, orc_key)
print(LOCAL_STORAGE.getItem(orc)) 