from sys import *

class Token:

    def __init__(self, type: str, value: int or str):
        self.type = type
        self.value = value

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
        result = Parser().parseFactor()
        while (Parser().tokenizer.next.type == "TIMES" or Parser().tokenizer.next.type == "DIVISION"):
        
            if (Parser().tokenizer.next.type == "TIMES"):
                Parser().tokenizer.selectNext()
                resultFactor = Parser().parseFactor()
                result = result * resultFactor 
                
            elif (Parser().tokenizer.next.type == "DIVISION"):
                Parser().tokenizer.selectNext()
                resultFactor = Parser().parseFactor()
                result = result // resultFactor
        
        return result

    @staticmethod
    def parseExpression():
        result = Parser().parseTerm()
        while (Parser().tokenizer.next.type == "PLUS" or Parser().tokenizer.next.type == "MINUS"):
            if (Parser().tokenizer.next.type == "PLUS"):
                Parser().tokenizer.selectNext()
                resultTerm = Parser().parseTerm()
                result = result + resultTerm
                
            elif (Parser().tokenizer.next.type == "MINUS"):
                Parser().tokenizer.selectNext()
                resultTerm = Parser().parseTerm()
                result = result - resultTerm
        return result  

    @staticmethod
    def parseFactor():
        result = Parser().tokenizer.next.value

        if (Parser().tokenizer.next.type == "INT"):
            Parser().tokenizer.selectNext()
            return result
        
        elif (Parser().tokenizer.next.type == "PLUS"):
            Parser().tokenizer.selectNext()
            result = Parser().parseFactor()
            return result

        elif (Parser().tokenizer.next.type == "MINUS"):
            Parser().tokenizer.selectNext()
            result = Parser().parseFactor()           
            return (-1)*result
        
        elif (Parser().tokenizer.next.type == "START_PARENTHESES"):
            Parser().tokenizer.selectNext()
            resultExpression = Parser().parseExpression()

            if (Parser().tokenizer.next.type != "END_PARENTHESES"):
                raise SyntaxError("It must have an end parentheses!")
            
            Parser().tokenizer.selectNext()

            return resultExpression
        
        else:
            raise SyntaxError("Something is wrong!")

    @classmethod
    def run(cls, source: str):
        cls.tokenizer = Tokenizer(source)
        cls.tokenizer.selectNext()
        result = cls.parseExpression()
        if (Parser().tokenizer.next.type == "EOF"):
            print(result)
            return result
        else:
            raise SyntaxError("Check if everything is correct! Did not arrive in EOF type")

def main():
    Parser().run(argv[1])


if __name__ == "__main__":
    main()
