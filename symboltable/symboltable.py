class SymbolTable:
    def __init__(self):
        self.table = {}
        self.row = 0

    def get(self, key:str):
        if key not in self.table.keys():
            raise ValueError("Variable not in symbol table!")

        return (self.table[key][0], self.table[key][1])

    def get_position(self, key:str):
        if key not in self.table.keys():
            raise ValueError("Variable not in symbol table!")

        return self.table[key][2]
    
    def create(self, key: str, type:any):
        if key not in self.table.keys():
            self.table[key] = (None, type, 4 + self.row*4)
            self.row += 1
        else:
            raise ValueError("Variable already created!")

    def set(self, key: str, value:any):
        self.table[key] = (value, self.table[key][1], self.table[key][2])