from typing import List

class Node():
    def __init__(self, variant, children):
        self.variant = variant
        self.children = children

    def __str__(self):
        return f"<Node ({self.variant})>"
    
    def Evaluate(self, symbolTable):
        pass


class BinOp(Node):

    def Evaluate(self, symbolTable):
        nodeL = self.children[0]
        nodeR = self.children[1]


        if (nodeL.Evaluate(symbolTable)[1] == nodeR.Evaluate(symbolTable)[1]):
                
            if (self.variant == "."):
                result = str(nodeL.Evaluate(symbolTable)[0]) + str(nodeR.Evaluate(symbolTable)[0])
                return (str(result), "string")
            
            if (self.variant == "+"):
                result = nodeL.Evaluate(symbolTable)[0] + nodeR.Evaluate(symbolTable)[0]
                return (result, "int")

            elif (self.variant == "-"):
                result = nodeL.Evaluate(symbolTable)[0] - nodeR.Evaluate(symbolTable)[0]
                return (result, "int")
            
            elif (self.variant == "/"):
                result = nodeL.Evaluate(symbolTable)[0] // nodeR.Evaluate(symbolTable)[0]
                return (result, "int")
            
            elif (self.variant == "*"):
                result = nodeL.Evaluate(symbolTable)[0] * nodeR.Evaluate(symbolTable)[0]
                return (result, "int")
                        
            elif (self.variant == "&&"):
                result = nodeL.Evaluate(symbolTable)[0] and nodeR.Evaluate(symbolTable)[0]
                return (int(result), "int")
                        
            elif (self.variant == "||"):
                result = nodeL.Evaluate(symbolTable)[0] or nodeR.Evaluate(symbolTable)[0]
                return (int(result), "int")
                   
            elif (self.variant == "=="):
                result = nodeL.Evaluate(symbolTable)[0] == nodeR.Evaluate(symbolTable)[0]
                return (int(result), "int")
            
            elif (self.variant == ">"):
                result = nodeL.Evaluate(symbolTable)[0] > nodeR.Evaluate(symbolTable)[0]
                return (int(result), "int")
            
            elif (self.variant == "<"):
                result = nodeL.Evaluate(symbolTable)[0] < nodeR.Evaluate(symbolTable)[0]
                return (int(result), "int")
            
        elif (nodeL.Evaluate(symbolTable)[1] != nodeR.Evaluate(symbolTable)[1]):
            if (self.variant == "."):
                result = str(nodeL.Evaluate(symbolTable)[0]) + str(nodeR.Evaluate(symbolTable)[0])
                return (result, "string")

        
        else:
            raise TypeError("There is something wrong in variable types!")
            
    

class UnOp(Node):
    def Evaluate(self, symbolTable):
        result = self.children[0]
        
        if (self.variant == "+"):
            return (result.Evaluate(symbolTable)[0], result.Evaluate(symbolTable)[1])
        
        elif (self.variant == "!"):
            return (int(not result.Evaluate(symbolTable)[0]), result.Evaluate(symbolTable)[1])

        elif (self.variant == "-"):
            return ((-1)*result.Evaluate(symbolTable)[0], result.Evaluate(symbolTable)[1])


class IntVal(Node):
    def __init__(self, variant):
        self.variant = variant

    def Evaluate(self, symbolTable):
        return (self.variant, "int")
    
class StrVal(Node):
    def __init__(self, variant):
        self.variant = variant

    def Evaluate(self, symbolTable):
        return (self.variant, "string")
    
class VarDec(Node):

    def Evaluate(self, symbolTable):
        if (len(self.children) == 1):
            symbolTable.create(self.children[0].variant, self.variant)
        else:
            symbolTable.create(self.children[0].variant, self.variant)
            symbolTable.set(self.children[0].variant, self.children[1].Evaluate(symbolTable)[0])

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

class Assign(Node):
    def __init__(self, key: Node, value: Node):
        super().__init__(None, [key, value])

    def Evaluate(self, symbolTable):
        [key, value] = self.children
        symbolTable.set(key.variant, value.Evaluate(symbolTable)[0])
        
class Block(Node):
    def __init__(self, statements: List[Node] = []):
        super().__init__(None, statements)

    def append_statement(self, statement: Node):
        self.children.append(statement)

    def Evaluate(self, symbolTable):
        for node in self.children:
            node.Evaluate(symbolTable)

class Program(Node):
    def __init__(self, programs: List[Node] = []):
        super().__init__(None, programs)

    def appendProgram(self, program: Node):
        self.children.append(program)

    def Evaluate(self, symbolTable):
        for node in self.children:
            node.Evaluate(symbolTable)

class Identifier(Node):
    def __init__(self, key: str):
        super().__init__(key, [])

    def Evaluate(self, symbolTable):
        return symbolTable.get(self.variant)

class Print(Node):
    def __init__(self, node: Node):
        super().__init__(None, [node])

    def Evaluate(self, symbolTable):
        node = self.children[0]
        print(node.Evaluate(symbolTable)[0])

class Scanln(Node):
    def __init__(self, variant):
        super().__init__(None, variant)

    def Evaluate(self, symbolTable):
        number = int(input())
        return (number, "int")

class If(Node):

    def Evaluate(self, symbolTable):
        expression = self.children[0]
        if_block = self.children[1]
        if (expression.Evaluate(symbolTable)[0]):
            if_block.Evaluate(symbolTable)
        elif(len(self.children) > 2):
            if (not expression.Evaluate(symbolTable)[0]):
                self.children[2].Evaluate(symbolTable)
        
class For(Node):

    def Evaluate(self, symbolTable):
        init = self.children[0].Evaluate(symbolTable)
        condition = self.children[1]
        increment = self.children[2]
        block = self.children[3]

        while(condition.Evaluate(symbolTable)[0]):
            block.Evaluate(symbolTable)
            increment.Evaluate(symbolTable)