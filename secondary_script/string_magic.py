string = ""
with open("input.txt", 'r') as f:
    for line in f:
        line = line.lstrip()
        line = line.replace("\uf0a7", "")
        line = line.replace("\t", "")
        string += f"{line}"
print(repr(string))