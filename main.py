from sys import *
from typing import List

from parser.parser import Parser

def main():

    with open(argv[1], "r", encoding="utf-8") as file:
        source = file.read()

    Parser().run(source)


if __name__ == "__main__":
    main()
