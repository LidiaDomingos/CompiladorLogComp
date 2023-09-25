from sys import *
from typing import List


class Token:

    def __init__(self, type: str, value: int or str):
        self.type = type
        self.value = value


class PrePro():
    def __init__(self) -> None:
        pass

    def filter(self, string: str):
        new_lines = []
        for line in string.split('\n'):    
            if "//" in line:
                for i in range(0, len(line)):
                    if line[i] == "/":
                        if (line[i+1] == "/"):
                            index = i
                            break
                new_lines.append(line[0:index])
            else:
                new_lines.append(line)
        cleanString = '\n'.join(new_lines)
        return cleanString

class SymbolTable:
    def __init__(self):
        self.table = {}

    def get(self, key:str):
        if key not in self.table.keys():
            raise ValueError("Variable not in symbol table!")
        return self.table[key]

    def set(self, key: str, value:any):
        self.table[key] = value

class Node():
    def __init__(self, variant, children):
        self.variant = variant
        self.children = children

    def Evaluate(self, symbolTable):
        pass


class BinOp(Node):

    def Evaluate(self, symbolTable):
        nodeL = self.children[0]
        nodeR = self.children[1]

        if (self.variant == "+"):
            result = nodeL.Evaluate(symbolTable) + nodeR.Evaluate(symbolTable)

        elif (self.variant == "-"):
            result = nodeL.Evaluate(symbolTable) - nodeR.Evaluate(symbolTable)

        elif (self.variant == "/"):
            result = nodeL.Evaluate(symbolTable) // nodeR.Evaluate(symbolTable)

        elif (self.variant == "*"):
            result = nodeL.Evaluate(symbolTable) * nodeR.Evaluate(symbolTable)

        return result


class UnOp(Node):

    def Evaluate(self, symbolTable):
        result = self.children[0]
        
        if (self.variant == "+"):
            return result.Evaluate(symbolTable)

        elif (self.variant == "-"):
            return (-1)*result.Evaluate(symbolTable)


class IntVal(Node):
    def __init__(self, variant):
        self.variant = variant

    def Evaluate(self, symbolTable):
        return self.variant


class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

class Assign(Node):
    def __init__(self, key: Node, value: Node):
        super().__init__(None, [key, value])

    def Evaluate(self, symbolTable):
        [key, value] = self.children
        symbolTable.set(key.variant, value.Evaluate(symbolTable))
        
class Block(Node):
    def __init__(self, statements: List[Node] = []):
        super().__init__(None, statements)

    def append_statement(self, statement: Node):
        self.children.append(statement)

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
        print(node.Evaluate(symbolTable))

class Tokenizer:

    def __init__(self, source: str):
        self.source = source
        self.position = -1
        self.next = Token
        self.token_type = ""
        self.isTheLast = False

    def selectNext(self):
        self.position = self.position + 1
        while (True):            
            if (self.position == (len(self.source))):
                self.position = self.position - 1
                self.isTheLast = True
                break
            elif (self.source[self.position] == " "):
                self.position = self.position + 1
            else:
                break

        if (self.isTheLast):
            self.token_type = "EOF"
            self.next = Token(type=self.token_type,
                              value="")

        elif (self.source[self.position] == "+"):
            self.token_type = "PLUS"
            self.next = Token(type=self.token_type,
                              value=self.source[self.position])

        elif (self.source[self.position] == "-"):
            self.token_type = "MINUS"
            self.next = Token(type=self.token_type,
                              value=self.source[self.position])

        elif (self.source[self.position] == "*"):
            self.token_type = "TIMES"
            self.next = Token(type=self.token_type,
                              value=self.source[self.position])

        elif (self.source[self.position] == "/"):
            self.token_type = "DIVISION"
            self.next = Token(type=self.token_type,
                              value=self.source[self.position])

        elif (self.source[self.position] == "("):
            self.token_type = "START_PARENTHESES"
            self.next = Token(type=self.token_type,
                              value=self.source[self.position])

        elif (self.source[self.position] == ")"):
            self.token_type = "END_PARENTHESES"
            self.next = Token(type=self.token_type,
                              value=self.source[self.position])
        
        elif (self.source[self.position] == "\n"):
            self.token_type = "ENTER"
            self.next = Token(type=self.token_type,
                              value=self.source[self.position])
            
        elif (self.source[self.position] == "="):
            self.token_type = "ASSIGN"
            self.next = Token(type=self.token_type,
                              value=self.source[self.position])

        elif (self.source[self.position].isdigit()):
            self.token_type = "INT"
            number = ""
            while (self.source[self.position].isdigit()):
                number = number + self.source[self.position]
                self.position = self.position + 1
                if (self.position == (len(self.source))):
                    self.isTheLast = True
                    self.position = self.position - 1
                    break
            self.position = self.position - 1
            self.next = Token(type=self.token_type, value=int(number))

        elif (self.source[self.position].isalpha()):
            identifier = ""
            while (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"):
                identifier = identifier + str(self.source[self.position])
                self.position = self.position + 1
                if (self.position == (len(self.source))):
                    self.isTheLast = True
                    self.position = self.position - 1
                    break

            self.position = self.position - 1
            if (identifier == "Println"):
                self.token_type = "PRINTLN"
                self.next = Token(type=self.token_type, value="Println")
            else:
                self.token_type = "IDENTIFIER"
                self.next = Token(type=self.token_type, value=identifier)
        
        else:
            raise ValueError(
                "Contains invalid character! The possible ones are: {[0-9], +, -, *, /, (, ), = }")


class Parser():

    tokenizer: Tokenizer

    @staticmethod
    def parse_statement():
        statement = NoOp()

        if (Parser().tokenizer.next.type == "IDENTIFIER"):
            identifier = Identifier(Parser().tokenizer.next.value)
            Parser().tokenizer.selectNext()
            if (Parser().tokenizer.next.type == "ASSIGN"):
                Parser().tokenizer.selectNext()
                expression = Parser().parseExpression()
                statement = Assign(identifier, expression)
                if (Parser().tokenizer.next.type == "END_PARENTHESES"):
                    raise SyntaxError("Check if everything is correct!")
            else:
                raise SyntaxError("Check if everything is correct!")
        
        elif (Parser().tokenizer.next.type == "PRINTLN"):
            Parser().tokenizer.selectNext()
            if (Parser().tokenizer.next.type == "START_PARENTHESES"):
                Parser().tokenizer.selectNext()
                statement = Print(Parser.parseExpression())
                
                if (Parser().tokenizer.next.type != "END_PARENTHESES"):
                    raise SyntaxError("Must have a () after a print")
                
                Parser().tokenizer.selectNext()
            else:
                raise SyntaxError("Must have a () after a print")
            
        elif (Parser().tokenizer.next.type == "ASSIGN"):
            raise SyntaxError("To have an equal, must be an identifier before!")

        Parser().tokenizer.selectNext()
        return statement

    @staticmethod
    def parse_block():
        while (Parser().tokenizer.next.type != "EOF"):
            statement = Parser().parse_statement()
            Block().append_statement(statement)
        Parser().tokenizer.selectNext()
        return Block()

    @staticmethod
    def parseTerm():
        node = Parser().parseFactor()
        while (Parser().tokenizer.next.type == "TIMES" or Parser().tokenizer.next.type == "DIVISION"):

            if (Parser().tokenizer.next.type == "TIMES"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseFactor()
                node = BinOp("*", [node, node2])

            elif (Parser().tokenizer.next.type == "DIVISION"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseFactor()
                node = BinOp("/", [node, node2])

        return node

    @staticmethod
    def parseExpression():
        node = Parser().parseTerm()
        while (Parser().tokenizer.next.type == "PLUS" or Parser().tokenizer.next.type == "MINUS"):
            if (Parser().tokenizer.next.type == "PLUS"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseTerm()
                node = BinOp("+", [node, node2])

            elif (Parser().tokenizer.next.type == "MINUS"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseTerm()
                node = BinOp("-", [node, node2])

        return node

    @staticmethod
    def parseFactor():
        node = Parser().tokenizer.next.value
        if (Parser().tokenizer.next.type == "INT"):
            node = IntVal(node)
            Parser().tokenizer.selectNext()
            if (Parser().tokenizer.next.type == "INT"):
                raise SyntaxError("Something is wrong!")

            return node
        
        elif (Parser().tokenizer.next.type == "IDENTIFIER"):
            node = Identifier(Parser().tokenizer.next.value)
            Parser().tokenizer.selectNext()
            return node

        elif (Parser().tokenizer.next.type == "PLUS"):
            Parser().tokenizer.selectNext()
            nodeFactor = Parser().parseFactor()
            node = UnOp("+", [nodeFactor])
            return node

        elif (Parser().tokenizer.next.type == "MINUS"):
            Parser().tokenizer.selectNext()
            nodeFactor = Parser().parseFactor()
            node = UnOp("-", [nodeFactor])
            return node
        
        elif (Parser().tokenizer.next.type == "START_PARENTHESES"):
            Parser().tokenizer.selectNext()
            node = Parser().parseExpression()

            if (Parser().tokenizer.next.type != "END_PARENTHESES"):
                raise SyntaxError("It must have an end parentheses!")

            Parser().tokenizer.selectNext()

            return node

        elif (Parser().tokenizer.next.type == "END_PARENTHESES"):
            raise SyntaxError("It must have an start parentheses!")

        else:
            raise SyntaxError("Something is wrong!")

    @classmethod
    def run(cls, source: str):
        str = PrePro().filter(source)
        symbolTable = SymbolTable()
        cls.tokenizer = Tokenizer(str)
        cls.tokenizer.selectNext()
        result = cls.parse_block()
        if (Parser().tokenizer.next.type == "EOF"):
            return result.Evaluate(symbolTable)
        else:
            raise SyntaxError(
                "Check if everything is correct! Did not arrive in EOF type")


def main():

    with open(argv[1], "r", encoding="utf-8") as file:
        source = file.read()

    Parser().run(source)


if __name__ == "__main__":
    main()
