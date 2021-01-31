
class sUN_user():
     def __init__(self, kvdict):
        self.values = kvdict

     def make_db_object(self):
         return self.values

     def __str__(self):
         out = ""
         for part in self.values:
             out = out + f"{part} -> {self.values[part]}\n"
         return out