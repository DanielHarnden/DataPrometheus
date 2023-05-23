import re

def cppParse(file, originalFileName):

    cleanedTables = [[originalFileName]]
    cppFunctionStyle = r'^\s*(\w+)\s+(\w+)\s*\((.*)\)\s*{'
    cppCallStyle = r'([^\s(]+)\s*\('
    illegalLines = ["", "if", "return", "for", "while", "<<", ">>"]

    with open(file.name, 'r') as f:
        cppText = f.read()

    # [0] = return type, [1] = function name, [2] = input
    functionDefinitions = re.findall(cppFunctionStyle, cppText, re.MULTILINE)

    for function in functionDefinitions:
        cleanedTables.append([[function[1], function[0]]])

    currentFunction = 0
    for line in cppText.split("\n"):
        lineIsFunction = False
        if currentFunction < len(functionDefinitions):
            newFunction = all(substring in line for substring in functionDefinitions[currentFunction])

            if newFunction:
                lineIsFunction = True
                currentFunction += 1

        if "(" in line and not lineIsFunction:

            lines = re.findall(cppCallStyle, line, flags=re.DOTALL)

            for subLine in lines:
                subLine = re.sub(r'[^a-zA-Z0-9\s]', '', subLine)
                if subLine not in illegalLines:
                    cleanedTables[currentFunction].append([subLine, "FUNCTION CALL"])

    return cleanedTables