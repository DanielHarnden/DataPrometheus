def combineFiles(parsedText):

    newParsedText = [["output.sql"]]

    for file in parsedText:
        newParsedText += file[1:]

    newParsedText = [newParsedText]

    return newParsedText

def generateSQL(parsedText, parsedInserts, edgesToAdd):
    allSqlTables = ""
    tableDict = {}

    # Add each table with keys
    for file in parsedText:
        for table in file[1:]:
            tableName = table[0][0]
            keys = table[1:]
            keyStatements = []

            # Append each key and key type
            for key in keys:
                keyName = key[0]
                keyType = key[1]
                statement = "\t{} {}".format(keyName, keyType)
                keyStatements.append(statement)

            # Keys for each table are stored in a dictionary
            keyNames = ", ".join([keyName for keyName, keyType in keys])
            tableDict[tableName] = keyNames

            # Add foreign key relationships
            for startTable, startKey, endTable, endKey in edgesToAdd:
                startTable = startTable.replace("[table]", "").strip()

                if tableName == startTable:
                    startKey = startKey.replace("[table]", "").strip()
                    endTable = endTable.replace("[table]", "").strip()
                    endKey = endKey.replace("[table]", "").strip()

                    statement = "\tFOREIGN KEY ({}) REFERENCES {}({})".format(startKey, endTable, endKey)
                    keyStatements.append(statement)

            # Finalize table statement and append to allSqlTables string
            joinedStatements = ",\n".join(keyStatements)
            sqlTable = "CREATE TABLE IF NOT EXISTS {} (\n{}\n);\n\n".format(tableName, joinedStatements)
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

            # Adds everything to a single string, then adds that to the string of inserts
            newStatement = "INSERT INTO {} ({}) VALUES ({});\n".format(tableName, tableDict[tableName], joinedInserts)
            allInserts += (newStatement)


    # Writes tables and inserts to sql file
    with open("output/output.sql", "w", encoding="utf-8") as file:
        file.write(allSqlTables)
        file.write(allInserts)