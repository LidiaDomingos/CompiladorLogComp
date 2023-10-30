class SymbolTable:
    def __init__(self):
        self.table = {}

    def get(self, key:str):
        if key not in self.table.keys():
            raise ValueError("Variable not in symbol table!")
        return self.table[key]
    
    def create(self, key: str, type:any):
        self.table[key] = (None, type)

    def set(self, key: str, value:any):
        self.table[key] = (value, self.table[key][1])