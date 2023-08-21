from sys import *

def simpleCalculator(*args):
    soma = 0
    subt = 0
    if (("+") in argv[1] or ("-" in argv[1])):
        clean_s = argv[1].replace(" ", "")
        clean_s = clean_s.replace("\n", "")
        if (("+") in clean_s):
            soma_lista = clean_s.split("+")
            for string in soma_lista:
                if ("-" not in string):
                    soma = soma + int(string)
                else:
                    sub_lista = string.split("-")
                    sub = int(sub_lista[0])
                    for s in range(1, len(sub_lista)):
                        sub = sub - int(sub_lista[s])
                    subt = subt - sub
        elif ("-" in clean_s):
            sub_lista = clean_s.split("-")
            sub = int(sub_lista[0])
            for s in range(1, len(sub_lista)):
                sub = sub - int(sub_lista[s])
            subt = subt - sub
        return (soma - subt)
    else:
        raise Exception("Não é possível fazer essa operação!")

simpleCalculator(argv)
