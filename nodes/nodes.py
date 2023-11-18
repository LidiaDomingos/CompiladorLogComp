from typing import List

from symboltable.functable import FunctionTable
from symboltable.symboltable import SymbolTable

class Node():
    def __init__(self, variant, children):
        self.variant = variant
        self.children = children

    def __str__(self):
        return f"<Node ({self.variant})>"
    
    def Evaluate(self, symbolTable):
        pass


class BinOp(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)

    def Evaluate(self, symbolTable):
        
        nodeL, typeNodeL = self.children[0].Evaluate(symbolTable)
        nodeR, typeNodeR = self.children[1].Evaluate(symbolTable)

        if (typeNodeL == typeNodeR):
                
            if (self.variant == "."):
                result = str(nodeL) + str(nodeR)
                return (str(result), "string")
            
            if (self.variant == "+"):
                result = nodeL + nodeR
                return (result, "int")

            elif (self.variant == "-"):
                result = nodeL - nodeR
                return (result, "int")
            
            elif (self.variant == "/"):
                result = nodeL // nodeR
                return (result, "int")
            
            elif (self.variant == "*"):
                result = nodeL * nodeR
                return (result, "int")
                        
            elif (self.variant == "&&"):
                result = nodeL and nodeR
                return (int(result), "int")
                        
            elif (self.variant == "||"):
                result = nodeL or nodeR
                return (int(result), "int")
                   
            elif (self.variant == "=="):
                result = nodeL == nodeR
                return (int(result), "int")
            
            elif (self.variant == ">"):
                result = nodeL > nodeR
                return (int(result), "int")
            
            elif (self.variant == "<"):
                result = nodeL < nodeR
                return (int(result), "int")
            
        elif (typeNodeL != typeNodeR):
            if (self.variant == "."):
                result = str(nodeL) + str(nodeR)
                return (result, "string")

        else:
            raise TypeError("There is something wrong in variable types!")
            
    
class UnOp(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)
        
    def Evaluate(self, symbolTable):
        result = self.children[0]
        value, type = result.Evaluate(symbolTable)

        if (self.variant == "+"):
            return (value, type)
        
        elif (self.variant == "-"):
            return ((-1)*value, type)
        
        elif (self.variant == "!"):
            return (int(value), type)


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
    def __init__(self, variant, children):
        super().__init__(variant, children)

    def Evaluate(self, symbolTable):
        identifier = self.children[0].variant
        type1 = self.variant
        symbolTable.create(self.children[0].variant, self.variant)

        if (len(self.children) == 2):
            boolExpression, type2 = self.children[1].Evaluate(symbolTable)
            if (type1 == type2):
                symbolTable.set(identifier, boolExpression)
            else:
                raise TypeError("Value type error!")

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])
    
    def Evaluate(self, symbolTable):
        return None, None

class Assign(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)

    def Evaluate(self, symbolTable):
        (key, value) = self.children
        valueSymbol, type1 = symbolTable.get(key.variant)

        result_expression, type2 = value.Evaluate(symbolTable)
        if (type1 == type2):
            symbolTable.set(key.variant, result_expression)

        else:
            raise TypeError("Cannot assign an int to a string variable!")
        return (None, None)
        
class Block(Node):
    def __init__(self, variant, children):
        super().__init__(None, children)

    def Evaluate(self, symbolTable):
        for node in self.children:
            if (node.variant != "ENTER"):
                result = node.Evaluate(symbolTable)
            else:
                node.Evaluate(symbolTable)
            
            if (node.variant == "return"):
                return result
            
        return result

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
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self, symbolTable):
        node = self.children[0]
        expression, type = node.Evaluate(symbolTable)
        print(expression)

class Scanln(Node):
    def __init__(self, variant):
        super().__init__(None, variant)

    def Evaluate(self, symbolTable):
        number = int(input())
        return (number, "int")

class If(Node):

    def __init__(self, variant, children):
        super().__init__(variant, children)
        
    def Evaluate(self, symbolTable):
        expression = self.children[0]
        if_block = self.children[1]
        if (expression.Evaluate(symbolTable)[0]):
            if_block.Evaluate(symbolTable)
        elif(len(self.children) > 2):
            if (not expression.Evaluate(symbolTable)[0]):
                self.children[2].Evaluate(symbolTable)
        
class For(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)
    def Evaluate(self, symbolTable):
        init = self.children[0]
        condition = self.children[1]
        increment = self.children[2]
        block = self.children[3]
        init = init.Evaluate(symbolTable)

        value, type = condition.Evaluate(symbolTable)
        while (value):
            block.Evaluate(symbolTable)
            increment.Evaluate(symbolTable)
            value, type = condition.Evaluate(symbolTable)

class FuncDec(Node):

    def __init__(self, variant, children):
        super().__init__(variant, children)
        self.funcTable = FunctionTable
        
    def Evaluate(self, symbolTable):
        declaration = self.children[0]
        name = declaration.children[0].variant
        self.funcTable.create(name, self, declaration.variant)

class FuncCall(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)
        self.funcTable = FunctionTable()

    def Evaluate(self, symbolTable):
        
        localSymboltable = SymbolTable()
        funcNode, typeNode = self.funcTable.get(self.variant)
        declaration, *nodes, block = funcNode.children

        if (len(self.children) != len(nodes)):
            raise Exception("Different numbers of nodes.")
        
        for i in range(len(self.children)):
            nodes[i].Evaluate(localSymboltable)
            identifier = nodes[i].children[0]
            returnValue, returnType = self.children[i].Evaluate(symbolTable)
            localSymboltable.set(identifier.variant, returnValue)

        resultNode, returnType = block.Evaluate(localSymboltable)
        if (returnType != None and returnType != typeNode):
            raise TypeError("Must return the same type defined by the function")
        
        return resultNode, returnType

class Return(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)

    def Evaluate(self, symbolTable):
        value, type = self.children[0].Evaluate(symbolTable)
        return value,type