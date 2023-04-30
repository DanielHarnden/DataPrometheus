import re

def pythonParse(file):

    with open(file.name, 'r') as f:
        pythonText = f.read()

    cols = []

    for line in pythonText.split("\n"):
        if "def" in line:
            line = line.split(" ")[1]
            line = line.split("(")[0]

            temp = []
            temp.append(line)
            cols.append(temp)


    i = -1
    for line in pythonText.split("\n"):
        if "(" in line:
            line = line.split("(")[0]
            line = line.split(".")[-1]

            if "def" in line:
                i += 1

            if i >= 0:
                line = line.split(" ")[-1]
                if line != cols[i][0] and line != "":
                    cols[i].append(line)

    return cols