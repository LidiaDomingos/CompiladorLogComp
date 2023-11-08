from typing import List

class Assembler():
    header = '''
            ; constantes
            SYS_EXIT equ 1
            SYS_READ equ 3
            SYS_WRITE equ 4
            STDIN equ 0
            STDOUT equ 1
            True equ 1
            False equ 0

            segment .data
            formatin: db "%d", 0
            formatout: db "%d", 10, 0 ; newline, null terminator
            scanint: times 4 db 0 ; 32-bit integer = 4 bytes

            segment .bss ; variáveis
            res RESB 1
            extern fflush
            extern stdout

            section .text
            global main ; linux
            extern scanf ; linux
            extern printf ; linux

            ; subrotinas if/while
            binop_je:
                JE binop_true
                JMP binop_false
            binop_jg:
                JG binop_true
                JMP binop_false
            binop_jl:
                JL binop_true
                JMP binop_false
            binop_false:
                MOV EAX, False
                JMP binop_exit
            binop_true:
                MOV EAX, True
            binop_exit:
                RET

            main:
                PUSH EBP ; guarda o base pointer
                MOV EBP, ESP ; estabelece um novo base pointer\n
'''
    
    body = ''

    footer = '''
                PUSH DWORD [stdout]
                CALL fflush
                ADD ESP, 4
                MOV ESP, EBP
                POP EBP
                MOV EAX, 1
                XOR EBX, EBX
                INT 0x80
    '''

    @staticmethod
    def write_header(filename: str) -> None:
        _filename = filename.split('.go')
        filename = _filename[0] + '.asm'

        with open(filename, "w") as file:
            file.write(Assembler.header)

    @staticmethod
    def write_footer(filename: str) -> None:
        _filename = filename.split('.go')
        filename = _filename[0] + '.asm'

        with open(filename, "a") as file:
            file.write(Assembler.footer)

    @staticmethod
    def write_body(filename: str) -> None:
        _filename = filename.split('.go')
        filename = _filename[0] + '.asm'

        with open(filename, "a") as file:
            file.write(Assembler.body)

class Counter:
    counter = 0

class Node():
    id = 0

    def __init__(self, variant, children):
        self.variant = variant
        self.children = children
        self.id = Counter.counter
        Counter.counter += 1

        self.writeASM = Assembler

    def __str__(self):
        return f"<Node ({self.variant}, id ({self.id}) )>"
    
    def Evaluate(self, symbolTable):
        pass


class BinOp(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)

    def Evaluate(self, symbolTable):

        nodeR, typeNodeR = self.children[1].Evaluate(symbolTable)
        self.writeASM.body += 'PUSH EAX\n'

        nodeL, typeNodeL = self.children[0].Evaluate(symbolTable)
        self.writeASM.body += 'POP EBX\n'

        if (typeNodeL == typeNodeR):
                
            if (self.variant == "."):
                result = str(nodeL) + str(nodeR)
                return (str(result), "string")
            
            if (self.variant == "+"):
                result = nodeL + nodeR
                self.writeASM.body += 'ADD EAX, EBX\n '
                return (result, "int")

            elif (self.variant == "-"):
                result = nodeL - nodeR
                self.writeASM.body += 'SUB EAX, EBX\n'
                return (result, "int")
            
            elif (self.variant == "/"):
                result = nodeL // nodeR
                self.writeASM.body += 'IDIV EBX\n'
                return (result, "int")
            
            elif (self.variant == "*"):
                result = nodeL * nodeR
                self.writeASM.body += 'IMUL EAX, EBX\n'
                return (result, "int")
                        
            elif (self.variant == "&&"):
                result = nodeL and nodeR
                self.writeASM.body += 'AND EAX, EBX\n'
                return (int(result), "int")
                        
            elif (self.variant == "||"):
                result = nodeL or nodeR
                self.writeASM.body += 'OR EAX, EBX\n'
                return (int(result), "int")
                   
            elif (self.variant == "=="):
                result = nodeL == nodeR
                self.writeASM.body += 'CMP EAX, EBX\nCALL binop_je\n'
                return (int(result), "int")
            
            elif (self.variant == ">"):
                result = nodeL > nodeR
                self.writeASM.body +=  'CMP EAX, EBX\nCALL binop_jg\n'
                return (int(result), "int")
            
            elif (self.variant == "<"):
                result = nodeL < nodeR
                self.writeASM.body += 'CMP EAX, EBX\nCALL binop_jl\n'
                return (int(result), "int")
            
        elif ( typeNodeL != typeNodeR):
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
            self.writeASM.body += f'MOV EAX, {value}\n'
            return (value, type)
        
        elif (self.variant == "-"):
            self.writeASM.body += 'NEG EAX\n'
            return ((-1)*value, type)
        
        elif (self.variant == "!"):
            self.writeASM.body += f'MOV EAX, {not value}\n'    
            return (int(value), type)

class IntVal(Node):
    def __init__(self, variant):
        super().__init__(variant, [])

    def Evaluate(self, symbolTable):
        self.writeASM.body += f'MOV EAX, {self.variant}\n'
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
        symbolTable.create(identifier, type1)
        self.writeASM.body += 'PUSH DWORD 0\n'
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
        position = symbolTable.get_position(key.variant)

        result_expression, type2 = value.Evaluate(symbolTable)
        if (type1 == type2):
            self.writeASM.body += f'MOV[EBP - {position}], EAX\n'
            symbolTable.set(key.variant, result_expression)
        else:
            raise TypeError("Cannot assign an int to a string variable!")
        
class Block(Node):
    def __init__(self):
        super().__init__(None, [])

    def append_statement(self, statement: Node):
        self.children.append(statement)

    def Evaluate(self, symbolTable):
        for node in self.children:
            node.Evaluate(symbolTable)

class Program(Node):
    def __init__(self):
        super().__init__(None, [])

    def appendProgram(self, program: Node):
        self.children.append(program)

    def Evaluate(self, symbolTable):
        for node in self.children:
            node.Evaluate(symbolTable)

class Identifier(Node):
    def __init__(self, variant):
        super().__init__(variant, [])

    def Evaluate(self, symbolTable):
        value, type = symbolTable.get(self.variant)
        position = symbolTable.get_position(self.variant)
        self.writeASM.body += f'MOV EAX, [EBP - {position}]\n'
        return value, type
    
class Print(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self, symbolTable):
        node = self.children[0]
        expression, type = node.Evaluate(symbolTable)
        self.writeASM.body += 'PUSH EAX\nPUSH formatout\nCALL printf\nADD ESP, 8\n'
        print(expression)

class Scanln(Node):
    def __init__(self, variant):
        super().__init__(None, variant)

    def Evaluate(self, symbolTable):
        number = int(input())
        self.writeASM.body += 'PUSH scanint\nPUSH formatin\nCALL scanf\nADD ESP, 8\nMOV EAX, DWORD [scanint]\nMOV [EBP - 4], EAX\n'
        return (number, "int")

class If(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)

    def Evaluate(self, symbolTable):
        if (len(self.children) > 2):
            (expression, if_block, else_block) = self.children
        else:
            (expression, if_block) = self.children
        
        expression.Evaluate(symbolTable)
        self.writeASM.body += f'IF_{self.id}:\nCMP EAX, False\nJMP ELSE_{self.id}\n'
        if_block.Evaluate(symbolTable)
        self.writeASM.body += f'JMP EXIT_IF_{self.id}\n'
        self.writeASM.body += f'ELSE_{self.id}:\n'

        if len(self.children) > 2:
            else_block.Evaluate(symbolTable)
        
        self.writeASM.body += f'EXIT_IF_{self.id}:\n'
        
class For(Node):
    def __init__(self, variant, children):
        super().__init__(variant, children)

    def Evaluate(self, symbolTable):
        init = self.children[0]
        condition = self.children[1]
        increment = self.children[2]
        block = self.children[3]

        init.Evaluate(symbolTable)
        self.writeASM.body += f'LOOP_{self.id}:\n'
        condition.Evaluate(symbolTable)  
        self.writeASM.body += f'CMP EAX, False\nJE EXIT_LOOP_{self.id}\n'
        block.Evaluate(symbolTable)
        increment.Evaluate(symbolTable)  
        self.writeASM.body += f'JMP LOOP_{self.id}\nEXIT_LOOP_{self.id}:\n'