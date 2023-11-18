class FunctionTable:
    table = {}

    @classmethod
    def create(cls, name: str, node: any, type: str):
        if name not in cls.table.keys():
            cls.table[name] = (node, type)
        else:
            raise ValueError("Function already created!")
    
    @classmethod
    def get(cls, name: str):
        return cls.table[name][0], cls.table[name][1]