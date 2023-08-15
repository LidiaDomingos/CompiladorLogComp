from sys import *


def simpleCalculator(*args):
    soma = 0
    subt = 0
    string = argv[1].replace(" ", "")
    if (("+") in argv[1]):
        soma_lista = argv[1].split("+")
        print(soma_lista)
        for string in soma_lista:
            if ("-" not in string):
                soma = soma + int(string)
            else:
                sub_lista = string.split("-")
                sub = int(sub_lista[0])
                for s in range(1, len(sub_lista)):
                    sub = sub - int(sub_lista[s])
                subt = subt - sub
    else:
        sub_lista = string.split("-")
        sub = int(sub_lista[0])
        for s in range(1, len(sub_lista)):
            sub = sub - int(sub_lista[s])
        subt = subt - sub

    return (soma - subt)

    # print(lista)


simpleCalculator(argv)
