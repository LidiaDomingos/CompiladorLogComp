from sys import *
from typing import List
from nodes.nodes import Assembler

from parser.parser import Parser
from symboltable.symboltable import SymbolTable

def main():

    with open(argv[1], "r", encoding="utf-8") as file:
        source = file.read()

    result = Parser().run(source)
    result = result.Evaluate(SymbolTable())
    Assembler().write_header(argv[1])
    Assembler().write_body(argv[1])
    Assembler().write_footer(argv[1])



if __name__ == "__main__":
    main()
