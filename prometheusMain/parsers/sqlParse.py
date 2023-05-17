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

    cleanedText = sqlText.split("\n")
    cleanedText = [line for line in cleanedText if "--" not in line and line != "" and "/*" not in line and "*/" not in line]



    tempCleanedText = " ".join(cleanedText)
    patternOne = r'(?<=VALUES).*?(?=;)'
    matches = re.findall(patternOne, tempCleanedText)
    tableNames = re.findall(r'INSERT INTO (\S+)\s', tempCleanedText)

    if matches == []:
        tempCleanedText = "\n".join(cleanedText)
        patternTwo = r'(?<=VALUES).*?(?=\n)'
        matches = re.findall(patternTwo, tempCleanedText)
        tableNames += re.findall(r'INSERT INTO (\S+)\s', tempCleanedText)

    if matches == []:
        print("Unable to find insert statements in this SQL file.")
        return []
    
    tableNames = [string[1:-1] for string in tableNames]
    finalMatches = re.findall(r'\((.*?)\)', str(matches))

    results = []
    for i, line in enumerate(finalMatches):
        items = line.split(',')
        results.append([tableNames[i % len(tableNames)]] + [re.sub(r'\W+', '', item.strip()) for item in items])

    return results