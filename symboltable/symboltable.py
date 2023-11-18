class SymbolTable:
    def __init__(self):
        self.table = {}

    def get(self, key:str):
        if key not in self.table.keys():
            raise ValueError("Variable not in symbol table!")

        return self.table[key]
    
    def create(self, key: str, type:any):
        if key not in self.table.keys():
            self.table[key] = (None, type)
        else:
            raise ValueError("Variable already created!")

    def set(self, key: str, value:any):
        if (type(value) == int and self.table[key][1] == "int" ):
            self.table[key] = (value, self.table[key][1])
        elif (self.table[key][1] == "string" and type(value) == str):
            self.table[key] = (value, self.table[key][1])
        else:
            raise TypeError("Must be the same type!")