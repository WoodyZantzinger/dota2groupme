
class sUN_user():
    def __init__(self, kvdict):
        self.values = kvdict

    def make_db_object(self):
        return self.values

    def __getitem__(self, key):
        if not key in self.values:
            return None
        return self.values[key]

    def __setitem__(self,  key, value):
        self.values[key] = value

    def __str__(self):
        out = ""
        for part in self.values:
            out = out + f"{part} -> {self.values[part]}\n"
        return out