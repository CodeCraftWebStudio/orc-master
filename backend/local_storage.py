import shelve

class localStorage:
    def __init__(self, filename="local_storage"):
        self.filename = filename  # the file that acts like storage
        self.passkey = self.filename + "4$jduy9y93yhsi03yg_3g9s-+jsehu%=azbajahisols223#ihihdihdsj@ihihsi!hgkshiheljhdroruh^"
    def setItem(self, key, value):
        with shelve.open(self.filename) as db:
            db[key] = value

    def getItem(self, key):
        with shelve.open(self.filename) as db:
            return db.get(key, None)  # return None if not found

    def removeItem(self, key):
        with shelve.open(self.filename) as db:
            if key in db:
                del db[key]

    def clear(self):
        with shelve.open(self.filename) as db:
            db.clear()
    def generate(self, name, value):
        with shelve.open(self.filename) as db:
            if name in db:               
                return db.get(name, value)
            else:
                db[name] = value
    def getAll(self, passkey):
        if passkey == self.passkey:
            with shelve.open(self.filename) as db:
                return db
        else:
            return "Invalid password for the file"

