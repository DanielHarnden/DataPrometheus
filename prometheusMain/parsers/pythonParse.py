import re

def pythonParse(file, originalFileName):

    cleanedTables = [[originalFileName]]

    with open(file.name, 'r') as f:
        pythonText = f.read()

    for line in pythonText.split("\n"):
        if "def " in line:
            line = line.split(" ")[1]
            line = line.split("(")[0]

            temp = [line]
            cleanedTables.append(temp)


    i = 0
    for line in pythonText.split("\n"):
        if "(" in line:
            line = line.split("(")[0]
            line = line.split(".")[-1]

            if "def " in line:
                i += 1

            if i >= 0:
                line = line.split(" ")[-1]
                if line != cleanedTables[i][0] and line != "":
                    cleanedTables[i].append(line)

    return cleanedTables