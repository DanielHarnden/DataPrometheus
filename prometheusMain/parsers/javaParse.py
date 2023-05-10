import re

def javaParse(file, originalFileName):

    cleanedTables = [[originalFileName]]
    javaClassStyle = r'^\s*(public|protected|private)?\s*(final)?\s*(class)\s+(\w+)\s*({)?'
    javaFunctionStyle = r'^\s*(public|protected|private)?\s*(static)?\s*(final)?\s*(\w+)\s+(\w+)\s*\((.*)\)\s*(throws\s+\w+(\s*,\s*\w+)*)?\s*'



    javaCallStyle = r'([^\s(]+)\s*\('
    illegalLines = ["", "if", "return", "for", "while", "<<", ">>"]

    with open(file.name, 'r') as f:
        javaText = f.read()

    # [0] = access, [1] = static?, [2] = class, [3] = class name
    classDefinitions = re.findall(javaClassStyle, javaText, re.MULTILINE)
    # [0] = access, [1] = static?, [2] = final?, [3] = return type, [4] = function name, [5] = arguments, [6] = throws?
    functionDefinitions = re.findall(javaFunctionStyle, javaText, re.MULTILINE)

    classIterator = 0
    functionIterator = 0
    currentClass = ''
    calls = []

    # iterate through each line of text
    for line in javaText.split("\n"):
        # check if a new class is being defined in this line
        if classIterator < len(classDefinitions):
            if all(substring in line for substring in classDefinitions[classIterator]): 
                currentClass = classDefinitions[classIterator][3]
                classIterator += 1

        # check if a new function is being defined in this line
        if functionIterator < len(functionDefinitions):
            if all(substring in line for substring in functionDefinitions[functionIterator]):
                # build the callName in the format of "className.functionName"
                callName = currentClass + "." + functionDefinitions[functionIterator][4]
                # append the callName and return type to the calls list
                cleanedTables.append([[callName, functionDefinitions[functionIterator][3]]])
                # increment the functionIterator
                functionIterator += 1

    currentFunction = 0
    for line in javaText.split("\n"):
        lineIsFunction = False
        if currentFunction < len(functionDefinitions):
            newFunction = all(substring in line for substring in functionDefinitions[currentFunction])

            if newFunction:
                lineIsFunction = True
                currentFunction += 1

        if "(" in line and not lineIsFunction:

            lines = re.findall(javaCallStyle, line, flags=re.DOTALL)

            for subLine in lines:
                subLine = re.sub(r'[^a-zA-Z0-9\s]', '', subLine)
                if subLine not in illegalLines:
                    cleanedTables[currentFunction].append([subLine, "FUNCTION CALL"])

    return cleanedTables