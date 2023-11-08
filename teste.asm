
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
                MOV EBP, ESP ; estabelece um novo base pointer

PUSH DWORD 0
PUSH DWORD 0
MOV EAX, 1
PUSH EAX
MOV EAX, 3
POP EBX
ADD EAX, EBX
 MOV[EBP - 4], EAX
MOV EAX, [EBP - 4]
MOV[EBP - 8], EAX
MOV EAX, 1
PUSH EAX
MOV EAX, [EBP - 4]
POP EBX
CMP EAX, EBX
CALL binop_jg
IF_30:
CMP EAX, False
JMP ELSE_30
MOV EAX, 1
PUSH EAX
MOV EAX, 5
POP EBX
SUB EAX, EBX
MOV[EBP - 4], EAX
JMP EXIT_IF_30
ELSE_30:
EXIT_IF_30:
MOV EAX, 3
PUSH EAX
MOV EAX, [EBP - 4]
POP EBX
CMP EAX, EBX
CALL binop_je
IF_43:
CMP EAX, False
JMP ELSE_43
JMP EXIT_IF_43
ELSE_43:
MOV EAX, 3
MOV[EBP - 4], EAX
EXIT_IF_43:
MOV EAX, 3
MOV[EBP - 4], EAX
LOOP_65:
MOV EAX, 5
PUSH EAX
MOV EAX, [EBP - 4]
POP EBX
CMP EAX, EBX
CALL binop_jl
CMP EAX, False
JE EXIT_LOOP_65
MOV EAX, 1
PUSH EAX
MOV EAX, [EBP - 4]
POP EBX
SUB EAX, EBX
MOV[EBP - 8], EAX
MOV EAX, 1
PUSH EAX
MOV EAX, [EBP - 4]
POP EBX
ADD EAX, EBX
 MOV[EBP - 4], EAX
JMP LOOP_65
EXIT_LOOP_65:
MOV EAX, [EBP - 4]
PUSH EAX
PUSH formatout
CALL printf
ADD ESP, 8

                PUSH DWORD [stdout]
                CALL fflush
                ADD ESP, 4
                MOV ESP, EBP
                POP EBP
                MOV EAX, 1
                XOR EBX, EBX
                INT 0x80
    