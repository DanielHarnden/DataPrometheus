import re

def cppParse(file, originalFileName):

    cleanedTables = [[originalFileName]]
    cppFunctionStyle = r'^\s*(\w+)\s+(\w+)\s*\((.*)\)\s*{'

    with open(file.name, 'r') as f:
        cppText = f.read()

    # [0] = return type, [1] = function name, [2] = input
    matches = re.findall(cppFunctionStyle, cppText, re.MULTILINE)

    for function in matches:
        cleanedTables.append([[function[1], function[0]]])

    print(cleanedTables)

    return cleanedTables