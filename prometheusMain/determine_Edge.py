import snowballstemmer
# This function finds the edges between nodes in database files, which is much more difficult than in programming files, and liberties are taken to accurately determine edges.
def databaseDetermineEdge(parsedText, keyList, tableNames, bannedWords):
    primaryKeys = {}
    tablesVisited = {}
    edgesToAdd = set()

    # Iterates through each key
    for file in parsedText:
        for tableColumns in file:
            tableName = tableNames[len(tablesVisited)]
            tablesVisited[tableName] = []

            # Stores the key name
            for column in tableColumns:
                currentKey = column[0]

                # Converts each key to its "root" key based on the keyInformation.json dictionary
                for keySynonym, synonyms in keyList.items():
                    if currentKey in synonyms:
                        currentKey = keySynonym

                edgesToAdd, tablesVisited, primaryKeys = determineEdgeToAdd(currentKey, primaryKeys, tableName, tableNames, tablesVisited, edgesToAdd, bannedWords)

    return edgesToAdd

def determineEdgeToAdd(currentKey, primaryKeys, tableName, tableNames, tablesVisited, edgesToAdd, bannedWords):
    stemmer = snowballstemmer.stemmer('english')

    # Does some logic using the current key / table and the referencing key / table to try and accurately determine which order the keys reference each other
    if currentKey in primaryKeys and tableName != primaryKeys[currentKey]:
        if primaryKeys[currentKey] not in tablesVisited[tableName] and currentKey not in bannedWords:
            referencedTable = primaryKeys[currentKey]
            cleanedTableName = tableName.replace("_", "")
            tableStem = stemmer.stemWord(cleanedTableName).lower()

            if currentKey in tableNames:
                if tableStem in currentKey.lower():
                    tempEdge = (referencedTable, currentKey, tableName, tableName)
                else:
                    tempEdge = (tableName, currentKey, referencedTable, referencedTable)
            else:
                if tableStem in currentKey.lower():
                    tempEdge = (referencedTable, currentKey, tableName, currentKey)
                else:
                    tempEdge = (tableName, currentKey, referencedTable, currentKey)

            edgesToAdd.add(tempEdge)
            tablesVisited[tableName].append(primaryKeys[currentKey])
    else:
        primaryKeys[currentKey] = tableName

    return edgesToAdd, tablesVisited, primaryKeys







# This function finds the edges between nodes in programming files (which are more rigid and therefore easier to find edges in compared to database files)
def progDetermineEdge(parsedText):
    functionCalls = set()

    # Recursive function
    def traverseFunctions(parsedData, currentFunction):
        for key in parsedData:
            if isinstance(key, list):
                # Determines if the key is a function call
                if len(key) > 1 and key[1] == 'FUNCTION CALL':
                    calledTable = splitClassAndKey(key[0])
                    currentFunctionName = splitClassAndKey(currentFunction[0])
                    call = (currentFunctionName, calledTable, calledTable, calledTable)
                    functionCalls.add(call)
                else:
                    # Recursively traverse nested lists
                    nestedData = key
                    nestedCurrentFunction = key[0]
                    traverseFunctions(nestedData, nestedCurrentFunction)
            elif isinstance(key, str):
                # Update the current function name
                currentFunction = key

    currentFunction = ['']
    traverseFunctions(parsedText, currentFunction)

    return functionCalls

def splitClassAndKey(key):
    removeClass = key.split(".")

    # Determines the class and key names
    if len(removeClass) == 1:
        return key
    else:
        currentClass = removeClass[0]
        currentKey = removeClass[1]

        # Replaces __init__ with class name
        # TODO: Make this language independent (only works with Python right now)
        if "__init__" in currentKey or "main" in currentKey:
            currentKey = currentClass

        return currentKey