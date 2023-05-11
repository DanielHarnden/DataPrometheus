def combineFiles(parsedText):

    newParsedText = [["output.sql"]]

    for file in parsedText:
        newParsedText += file[1:]

    newParsedText = [newParsedText]

    return newParsedText

def generateSQL(parsedText, edgesToAdd):
    allSqlTables = ""

    for file in parsedText:
        for table in file[1:]:
            tableName = table[0][0]
            keys = table[1:]
            keyStatements = []

            for key in keys:
                keyName = key[0]
                keyType = key[1]
                statement = "\t{} {}".format(keyName, keyType)
                keyStatements.append(statement)

            for startTable, startKey, endTable, endKey in edgesToAdd:
                startTable = startTable.replace("[table]", "").strip()
                startKey = startKey.replace("[table]", "").strip()
                endTable = endTable.replace("[table]", "").strip()
                endKey = endKey.replace("[table]", "").strip()

                print(startTable, startKey, endTable, endKey)

                if tableName == startTable:
                    statement = "\tFOREIGN KEY ({}) REFERENCES {}({})".format(startKey, endTable, endKey)
                    keyStatements.append(statement)

            joinedStatements = ",\n".join(keyStatements)
            sqlTable = "CREATE TABLE IF NOT EXISTS {} (\n{}\n);\n\n".format(tableName, joinedStatements)
            allSqlTables += (sqlTable)

    with open("output/output.sql", "w") as file:
        file.write(allSqlTables)