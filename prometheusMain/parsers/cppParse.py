import re

def cppParse(file, originalFileName):

    cleanedTables = [[originalFileName]]
    cppFunctionStyle = r'^\s*(\w+)\s+(\w+)\s*\((.*)\)\s*{'

    with open(file.name, 'r') as f:
        cppText = f.read()

    matches = re.findall(cppFunctionStyle, cppText, re.MULTILINE)

    print(matches)

    return 0