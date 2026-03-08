import shelve
import os


class LocalStorage:
    def __init__(self, filename="local_storage.db"):
        # Ensure file path works on Render
        self.filename = os.path.join(os.getcwd(), filename)

    def setItem(self, key, value):
        with shelve.open(self.filename, flag="c") as db:
            db[str(key)] = value

    def getItem(self, key):
        with shelve.open(self.filename, flag="c") as db:
            return db.get(str(key))

    def removeItem(self, key):
        with shelve.open(self.filename, flag="c") as db:
            if str(key) in db:
                del db[str(key)]


LOCAL_STORAGE = LocalStorage()
