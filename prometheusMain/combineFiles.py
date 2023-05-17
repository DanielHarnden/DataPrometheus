def combineFiles(parsedText):

    newParsedText = [["output.sql"]]

    for file in parsedText:
        newParsedText.extend(file[1:])

    return [newParsedText]

def generateSQL(parsedText, parsedInserts, keyList, edgesToAdd):
    allSqlTables = ""
    tableColumnDict = {}

    # Add each table with keys
    for file in parsedText:
        for table in file[1:]:
            tableName = table[0][0]
            keys = table[1:]
            keyStatements = []
            addedKeys = set()

            # Append each key and key type
            for key in keys:
                keyName = key[0]
                keyType = key[1]

                for keySynonym in keyList:
                    if keyName in keyList[keySynonym]:
                        keyName = keySynonym

                if keyName not in addedKeys:
                    statement = f"\t{keyName} {keyType}"
                    keyStatements.append(statement)
                    addedKeys.add(keyName)

            # Keys for each table are stored in a dictionary
            keyNames = ", ".join([keyName for keyName, keyType in keys])
            tableColumnDict[tableName] = keyNames

            # Add foreign key relationships
            for startTable, startKey, endTable, endKey in edgesToAdd:
                startTable = startTable.replace("[table]", "").strip()

                if tableName == startTable:
                    startKey = startKey.replace("[table]", "").strip()
                    endTable = endTable.replace("[table]", "").strip()
                    endKey = endKey.replace("[table]", "").strip()

                    statement = f"\tFOREIGN KEY ({startKey}) REFERENCES {endTable}({endKey})"
                    keyStatements.append(statement)

            # Finalize table statement and append to allSqlTables string
            joinedStatements = ",\n".join(keyStatements)
            sqlTable = f"CREATE TABLE IF NOT EXISTS {tableName} (\n{joinedStatements}\n);\n\n"
            allSqlTables += (sqlTable)

    # Add insert statements (if they exist)
    allInserts = ""
    # Remove outermost []
    for outermostBrackets in parsedInserts:
        for row in outermostBrackets:
            insertStatements = []
            tableName = row[0]

            # Cleans and adds each key to a list
            for key in row[1:]:
                if key is None:
                    insertStatements.append("NULL")
                elif isinstance (key, str):
                    key = key.replace("'", "''")
                    insertStatements.append(f"'{key}'")
                else:
                    insertStatements.append(str(key))
            
            # Turns the list into a single string separated by commas
            joinedInserts = ", ".join(insertStatements)
            tableName = tableName.replace("_", "")

            # Adds everything to a single string, then adds that to the string of inserts
            newStatement = f"INSERT INTO {tableName} ({tableColumnDict[tableName]}) VALUES ({joinedInserts});\n"
            allInserts += (newStatement)


    # Writes tables and inserts to sql file
    with open("output/output.sql", "w", encoding="utf-8") as file:
        file.write(allSqlTables)
        file.write(allInserts)