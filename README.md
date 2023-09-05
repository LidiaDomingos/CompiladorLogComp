# Status dos testes

![git status](http://3.129.230.99/svg/LidiaDomingos/CompiladorLogComp/)

### EBNF

```py
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;
```

### Grámatica

![Alt text](image-3.png)

### Diagrama Sintático

![Alt text](image-2.png)
