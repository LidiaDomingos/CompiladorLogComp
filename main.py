from sys import *


class Token:

    def __init__(self, type: str, value: int or str):
        self.type = type
        self.value = value


class PrePro():
    def __init__(self) -> None:
        pass

    def filter(self, string: str):
        if "//" in string:
            for i in range(0, len(string)):
                if string[i] == "/":
                    if (string[i+1] == "/"):
                        index = i
                        break
            return string[0:index]
        else:
            return string


class Node():
    def __init__(self, variant, children):
        self.variant = variant
        self.children = children

    def Evaluate(self):
        pass


class BinOp(Node):

    def Evaluate(self):
        nodeL = self.children[0]
        nodeR = self.children[1]

        if (self.variant == "+"):
            result = nodeL.Evaluate() + nodeR.Evaluate()

        elif (self.variant == "-"):
            result = nodeL.Evaluate() - nodeR.Evaluate()

        elif (self.variant == "/"):
            result = nodeL.Evaluate() // nodeR.Evaluate()

        elif (self.variant == "*"):
            result = nodeL.Evaluate() * nodeR.Evaluate()

        return result


class UnOp(Node):

    def Evaluate(self):
        result = self.children

        if (self.variant == "+"):
            return result.Evaluate()

        elif (self.variant == "-"):
            return (-1)*result.Evaluate()


class IntVal(Node):

    def __init__(self, variant):
        self.variant = variant

    def Evaluate(self):
        return self.variant


class NoOp(Node):
    pass


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
            elif (self.source[self.position] == " " or self.source[self.position] == "\n"):
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
        else:
            raise ValueError(
                "Contains invalid character! The possible ones are: {[0-9], +, -, *, /, (, ) }")


class Parser():

    tokenizer: Tokenizer

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

        else:
            raise SyntaxError("Something is wrong!")

    @classmethod
    def run(cls, source: str):
        str = PrePro().filter(source)
        cls.tokenizer = Tokenizer(str)
        cls.tokenizer.selectNext()
        result = cls.parseExpression()
        if (Parser().tokenizer.next.type == "EOF"):
            print(result.Evaluate())
            return result.Evaluate()
        else:
            raise SyntaxError(
                "Check if everything is correct! Did not arrive in EOF type")


def main():

    with open(argv[1], "r", encoding="utf-8") as file:
        source = file.read()

    Parser().run(source)


if __name__ == "__main__":
    main()
