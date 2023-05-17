import re

def sqlParse(file, originalFileName):

    cleanedTables = [[originalFileName]]

    with open(file.name, 'r', encoding='utf-8') as f:
        sqlText = f.read()

    cleanedText = sqlText.split("\n")
    cleanedText = [line for line in cleanedText if "--" not in line and line != "" and "/*" not in line and "*/" not in line]

    tables = []
    inserts = []
    tempLine = []
    for line in cleanedText:
        tempLine.append(line)

        if ";" in line:
            if any("CREATE TABLE" in s for s in tempLine):
                tables.append(tempLine)
            tempLine = []

        if "INSERT INTO" in line:
            inserts.append(tempLine)
            tempLine = []

    if len(tables) != 0:
        return parseTables(cleanedTables, tables)
    else:
        return parseInsertStatements(cleanedTables, inserts)



def parseTables(cleanedTables, tables):
    for table in tables:
            results = []
            for i, line in enumerate(table):
                if i == 0:
                    line = re.sub(r'[^a-zA-Z0-9\s]', '', line)
                    results.append([line.split()[-1], "TABLE"])
                elif ";" not in line and "KEY" not in line and "ENGINE" not in line and "CONSTRAINT" not in line:
                    lineSplit = line.split()
                    keyName = re.sub(r'[^a-zA-Z0-9\s]', '', lineSplit[0])
                    keyType = re.sub(r'[^a-zA-Z0-9\s()]', '', lineSplit[1])
                    results.append([keyName, keyType])

            cleanedTables.append(results)

    return cleanedTables



def parseInsertStatements(cleanedTables, inserts):
    for statement in inserts:
            for line in statement:
                results = []
                line = line.split("VALUES")[0]
                line = line.split("INSERT INTO")[1]
                line = re.sub(r'[^a-zA-Z0-9\s]', ' ', line)
                line = line.split()

                for i, item in enumerate(line):
                    if i == 0:
                        results.append([item, "TABLE"])
                    else:
                        results.append([item, "VARCHAR(50)"])

                cleanedTables.append(results)
    return cleanedTables



def sqlInsertParse(file):
    with open(file.name, 'r', encoding='utf-8') as f:
        sqlText = f.read()

    insertStatements = re.findall(r'VALUES\s*(.*?);', sqlText)
    print(insertStatements)