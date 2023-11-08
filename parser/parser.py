from nodes.nodes import UnOp, Assign, BinOp, Block, For, Identifier, If, IntVal, NoOp, Print, Program, Scanln, StrVal, VarDec
from prepro.prepro import PrePro
from symboltable.symboltable import SymbolTable
from tokenizer.tokenizer import Tokenizer


class Parser():

    tokenizer: Tokenizer

    @staticmethod
    def parseRLExpression():
        node = Parser().parseExpression()
        while (Parser().tokenizer.next.type == "EQUAL" or Parser().tokenizer.next.type == "GREATER_THAN" or Parser().tokenizer.next.type == "LESS_THAN"):

            if (Parser().tokenizer.next.type == "EQUAL"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseExpression()
                node = BinOp("==", [node, node2])

            if (Parser().tokenizer.next.type == "GREATER_THAN"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseExpression()
                node = BinOp(">", [node, node2])

            elif (Parser().tokenizer.next.type == "LESS_THAN"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseExpression()
                node = BinOp("<", [node, node2])
        return node
    
    @staticmethod
    def parseBoolTerm():
        node = Parser().parseRLExpression()
        while (Parser().tokenizer.next.type == "AND"):

            if (Parser().tokenizer.next.type == "AND"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseRLExpression()
                node = BinOp("&&", [node, node2])
        return node
    
    @staticmethod
    def parseBoolExpression():
        
        node = Parser().parseBoolTerm()
        while (Parser().tokenizer.next.type == "OR"):

            if (Parser().tokenizer.next.type == "OR"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseBoolTerm()
                node = BinOp("||", [node, node2])

        return node
    
    @staticmethod
    def parseAssign():
        key = Parser().tokenizer.next.value
        identifier = Identifier(Parser().tokenizer.next.value)
        Parser().tokenizer.selectNext()
        if (Parser().tokenizer.next.type == "ASSIGN"):
            Parser().tokenizer.selectNext()
            
            expression = Parser().parseBoolExpression()
            statement = Assign(key, [identifier, expression])
            
            if (Parser().tokenizer.next.type == "END_PARENTHESES"):
                raise SyntaxError("It needs a start parentheses before!")
        else:
            raise SyntaxError("Check if everything is correct!")
       
        return statement
    
    @staticmethod
    def parseStatement():

        node = NoOp()

        if (Parser().tokenizer.next.type == "ENTER"):
            node = NoOp()
            Parser().tokenizer.selectNext()
            return node

        if (Parser().tokenizer.next.type == "IDENTIFIER"):
            node = Parser().parseAssign()
            return node
        
        if (Parser().tokenizer.next.type == "VAR"):
            Parser().tokenizer.selectNext()
            if (Parser().tokenizer.next.type == "IDENTIFIER"):
                identifier = Identifier(Parser().tokenizer.next.value)
                Parser().tokenizer.selectNext()
                if (Parser().tokenizer.next.type == "TYPE"):
                    type = Parser().tokenizer.next.value
                    Parser().tokenizer.selectNext()
                    if (Parser().tokenizer.next.type == "ASSIGN"):
                        Parser().tokenizer.selectNext()
                        result = Parser().parseBoolExpression()
                        node = VarDec(type, [identifier, result])
                    else:
                        node = VarDec(type, [identifier])
                    return node
                else:
                    raise TypeError("It must have a type in a variable!")
            else:
                    raise TypeError("It needs an identifier in a variable!")
        
        elif (Parser().tokenizer.next.type == "PRINTLN"):
            Parser().tokenizer.selectNext()
            if (Parser().tokenizer.next.type == "START_PARENTHESES"):
                Parser().tokenizer.selectNext()
                node = Print([Parser().parseBoolExpression()])
                if (Parser().tokenizer.next.type != "END_PARENTHESES"):
                    raise SyntaxError("Must have a () after a print")
                Parser().tokenizer.selectNext()
                return node
            else:
                raise SyntaxError("Must have a () after a print")
            
        elif (Parser().tokenizer.next.type == "IF"):
            Parser().tokenizer.selectNext()

            expression = Parser().parseBoolExpression()

            if_block = Parser().parseBlock()
            if (Parser().tokenizer.next.type == "ELSE"):
                Parser().tokenizer.selectNext()
                else_block = Parser().parseBlock()
                node = If("IF", [expression, if_block, else_block])
            else:
                node = If("IF", [expression, if_block])
            return node

            
        elif (Parser().tokenizer.next.type == "FOR"):
            Parser().tokenizer.selectNext()
            init = Parser().parseAssign()

            if (Parser().tokenizer.next.type == "SEMICOLON"):
                Parser().tokenizer.selectNext()
                condition = Parser().parseBoolExpression()
                if (Parser().tokenizer.next.type == "SEMICOLON"):
                    Parser().tokenizer.selectNext()
                    increment = Parser().parseAssign()
                    block = Parser().parseBlock()
                    node = For("FOR", [init, condition, increment, block])
                    return node

                else:
                    raise SyntaxError("The syntax to for is: int a = 0; a < n; a++")
            else:
                raise SyntaxError("The syntax to for is: int a = 0; a < n; a++")

        elif (Parser().tokenizer.next.type == "ASSIGN"):
            raise SyntaxError("To have an equal, must be an identifier before!")


    @staticmethod
    def parseBlock():
        node = Block()
        if (Parser().tokenizer.next.type == "START_CURLY_BRACKET"):
            Parser().tokenizer.selectNext()
            if (Parser().tokenizer.next.type == "ENTER"):
                Parser().tokenizer.selectNext()
                while(Parser().tokenizer.next.type !="END_CURLY_BRACKET"):
                    statement = Parser().parseStatement()
                    node.append_statement(statement)
                Parser().tokenizer.selectNext()
                return node
            else:
                raise SyntaxError("Must have an end curly bracket (})!")

                
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
        while (Parser().tokenizer.next.type == "PLUS" or Parser().tokenizer.next.type == "MINUS" or Parser().tokenizer.next.type == "CONCAT"):
            if (Parser().tokenizer.next.type == "PLUS"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseTerm()
                node = BinOp("+", [node, node2])

            elif (Parser().tokenizer.next.type == "MINUS"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseTerm()
                node = BinOp("-", [node, node2])

            elif (Parser().tokenizer.next.type == "CONCAT"):
                Parser().tokenizer.selectNext()
                node2 = Parser().parseTerm()
                node = BinOp(".", [node, node2])

        return node

    @staticmethod
    def parseFactor():    
        if (Parser().tokenizer.next.type == "INT"):
            node = IntVal(Parser().tokenizer.next.value)
            Parser().tokenizer.selectNext()
            return node
        
        elif (Parser().tokenizer.next.type == "STR"):
            node = StrVal(Parser().tokenizer.next.value)
            Parser().tokenizer.selectNext()
            return node
        
        elif (Parser().tokenizer.next.type == "IDENTIFIER"):
            node = Identifier(Parser().tokenizer.next.value)
            Parser().tokenizer.selectNext()
            return node

        elif (Parser().tokenizer.next.type == "MINUS"):
            Parser().tokenizer.selectNext()
            nodeFactor = Parser().parseFactor()
            node = UnOp("-", [nodeFactor])
        
            return node
        
        elif (Parser().tokenizer.next.type == "PLUS"):
            Parser().tokenizer.selectNext()
            nodeFactor = Parser().parseFactor()
            node = UnOp("+", [nodeFactor])

            return node
        
        elif (Parser().tokenizer.next.type == "NOT"):
            Parser().tokenizer.selectNext()
            nodeFactor = Parser().parseFactor()
            node = UnOp("!", [nodeFactor])

            return node
        
        elif (Parser().tokenizer.next.type == "START_PARENTHESES"):
            Parser().tokenizer.selectNext()
            node = Parser().parseBoolExpression()
            
            if (Parser().tokenizer.next.type != "END_PARENTHESES"):
                raise SyntaxError("It must have an end parentheses!")
            
            Parser().tokenizer.selectNext()
            
            return node
        
        elif (Parser().tokenizer.next.type == "SCANLN"):
            Parser().tokenizer.selectNext()
            if (Parser().tokenizer.next.type == "START_PARENTHESES"):
                node = Scanln("SCANLN")
                Parser().tokenizer.selectNext()

                if (Parser().tokenizer.next.type != "END_PARENTHESES"):
                    raise SyntaxError("It must have an end parentheses!")

                Parser().tokenizer.selectNext()
                return node

        else:
            raise SyntaxError("Something is wrong!")

    @staticmethod
    def program():
        node = Program()
        while(Parser().tokenizer.next.type != "EOF"):
            state = Parser().parseStatement()
            if (Parser().tokenizer.next.type == "ENTER"):
                Parser().tokenizer.selectNext()
            else:
                raise SyntaxError("There is something wrong")
            node.appendProgram(state)
        Parser().tokenizer.selectNext()
        return node
    
    @classmethod
    def run(cls, source: str):
        str = PrePro().filter(source)
        symbolTable = SymbolTable()
        cls.tokenizer = Tokenizer(str)
        cls.tokenizer.selectNext()
        result = Parser().program()

        if (Parser().tokenizer.next.type == "EOF"):
            return result
        else:
            raise SyntaxError(
                "Check if everything is correct! Did not arrive in EOF type")
