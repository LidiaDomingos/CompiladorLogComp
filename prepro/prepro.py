class PrePro():
    def __init__(self) -> None:
        pass

    def filter(self, string: str):
        new_lines = []
        for line in string.split('\n'):
            line = line.strip()    
            if "//" in line:
                for i in range(0, len(line)):
                    if line[i] == "/":
                        if (line[i+1] == "/"):
                            index = i
                            break
                if (len(line[0:index]) != 0):
                    new_lines.append(line[0:index])
                    
            else:
                if (len(line) != 0):
                    new_lines.append(line)
        cleanString = '\n'.join(new_lines)
        cleanString = cleanString + '\n'
        
        return cleanString