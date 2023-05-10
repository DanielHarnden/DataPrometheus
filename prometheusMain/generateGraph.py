import graphviz, os, random, snowballstemmer
from datetime import datetime

dot = graphviz.Digraph()

def generateGraph(parsedText, keyList, bannedWords):
    global dot 
    dot = graphviz.Digraph()
    
    # Moves file names from parsedText to fileNames, sorts tables from biggest to smallest
    parsedText, fileNames = initializeGraphGeneration(parsedText, [])
    primaryKeys = {}
    tableNames = []
    nodes = []

    # Loops through each file...
    for i, file in enumerate(parsedText):
    
        # ...stores all table names and primary keys while adding each table to GraphViz...
        filePrimaryKeys, newTables, fileTableNames = addTables(file, primaryKeys, [], [])
        tableNames += fileTableNames
        primaryKeys.update(filePrimaryKeys)
        
        # ...then adds each key to the new tables
        nodes = addKeys(file, keyList, newTables, fileTableNames, fileNames[i], nodes)
        
    # Searches for relationships between keys
    tablesVisited = {}
    edgesToAdd = []
    edgesToAdd, tablesVisited = addForeignKeys(parsedText, tableNames, tablesVisited, edgesToAdd, keyList, primaryKeys, bannedWords)

    # Adds the found relationships as edges on the graph
    generateForeignKeys(edgesToAdd, nodes)

    # Does some settings to make it look pwetty uwu
    graphCreationTime = datetime.now()
    graphCreationTime = graphCreationTime.strftime("%m/%d/%Y %I:%M %p")
    dot.graph_attr.update({
        'table': 'style=invis',
        'label': f'Parsed by Data Prometheus at {graphCreationTime}',
        'labelloc': 't',
        'rankdir': 'LR',
        'dpi': '200'
    })

    # Renders the graph as a PNG to the output folder
    dot.render('./output/output', format='png')



def initializeGraphGeneration(parsedText, fileNames):
    for fileIterator, file in enumerate(parsedText):
        fileNames.append(file[0][0])
        # Sorts the parsed text from biggest to smallest table ONLY IF it is not a programming file
        # Programming files retain their original structure to avoid errors
        if file[0][0].split(".")[-1] not in ["py", "java", "cpp"]:
            file = sorted(file[1:], key=lambda x: len(x))
            file.reverse()
        else:
            file = file[1:]
        parsedText[fileIterator] = file

    return parsedText, fileNames



def addTables(file, primaryKeys, newTables, tableNames):
    # Adds each table to the database
    for i, tableList in enumerate(file):
        newTables.append('''<\n\n\n\n<table border="1" cellborder="1" cellspacing="0" color="#932525">''')

        # Generates the table using the table name
        tableNames.append(tableList[0][0] + " [table]")
        newTables[i] += generateTable(tableNames[i], i)
        primaryKeys[tableNames[i]] = tableNames[i]

    return primaryKeys, newTables, tableNames



def addKeys(file, keyList, newTables, tableNames, fileName, nodes):
    global dot

    # Iterates through all of the tables from the original txt of the inputted database
    for tableIterator, tableList in enumerate(file):
        for key in tableList[1:]:
            keyName = key[0]
            keyType = key[1]

            # Determines if they key has to be renamed based on the mapping
            for keySynonym in keyList:
                if keyName in keyList[keySynonym]:
                    keyName = keySynonym

            newTables[tableIterator] += generateKey(keyName, keyType)
            nodes.append(f"{tableNames[tableIterator]}:{keyName}")

        # Finishes the table then adds the node using the temporary information
        newTables[tableIterator] += "</table>\n>"

    # The cluster needs a random int because clusters can't be named the same
    with dot.subgraph(name=f'Cluster-{random.randint(1,1000)}') as subDot:
        for tableIterator, tableList in enumerate(file):
            subDot.attr(label=fileName, color='#FFA07A', bgcolor='#FFC6A5', style='solid')
            subDot.node(tableNames[tableIterator], shape='none', label=newTables[tableIterator])

    return nodes



def addForeignKeys(parsedText, tableNames, tablesVisited, edgesToAdd, keyList, primaryKeys, bannedWords):
    stemmer = snowballstemmer.stemmer('english')
    tableIterator = 0
    
    for file in parsedText:
        for tableList in file:
            currentTable = tableNames[tableIterator]
            tableIterator += 1

            if currentTable not in tablesVisited:
                tablesVisited[currentTable] = []

            for key in tableList:
                currentKey = key[0]

                for keySynonym in keyList:
                    if currentKey in keyList[keySynonym]:
                        currentKey = keySynonym

                if currentKey in primaryKeys and currentTable is not primaryKeys[currentKey]:
                    if primaryKeys[currentKey] not in tablesVisited[currentTable] and currentKey not in bannedWords:
                        referencedTable = primaryKeys[currentKey]
                        # Used to determine if the current key is part of the table name (if so, it is assumed that the relationship start/end are swapped) 
                        cleanedTableName = currentTable.replace(" [table]", "").replace("_", "")
                        tableStem = stemmer.stemWord(cleanedTableName).lower()
                        
                        if currentKey + " [table]" in tableNames:
                            if tableStem in currentKey.lower():
                                tempEdge = (referencedTable, currentKey, currentTable, currentTable)
                            else:
                                tempEdge = (currentTable, currentKey, referencedTable, referencedTable)
                        else:
                            if tableStem in currentKey.lower():
                                tempEdge = (referencedTable, currentKey, currentTable, currentKey)
                            else:
                                tempEdge = (currentTable, currentKey, referencedTable, currentKey)

                        if tempEdge not in edgesToAdd:
                            edgesToAdd.append(tempEdge)
                            tablesVisited[currentTable].append(primaryKeys[currentKey])
                else:
                    primaryKeys[currentKey] = currentTable

    return edgesToAdd, tablesVisited



def generateTable(tableName, tableNumber):
    return f'''
  <tr>
    <td colspan='2' bgcolor='#932525' port="{tableName}.start" align='left'><font color="#FFFFEB"><b><i>{tableName}</i></b></font></td>
    <td bgcolor='#932525' align='right' port="{tableName}.end" ><font color="#FFFFEB"><b><i>{tableNumber}</i></b></font></td>
  </tr>
    '''

def generateKey(keyName, keyType):
    return f'''
  <tr>
    <td colspan='2' bgcolor='#C43131' port="{keyName}.start" align='left'><font color="#FFFFEB"><b><i>{keyName}</i></b></font></td>
    <td bgcolor='#C43131' port="{keyName}.end" align='right'><font color="#FFFFEB">{keyType}</font></td>
  </tr>
    '''

def generateForeignKeys(edgesToAdd, nodes):
    global dot

    for startTable, startKey, endTable, endKey in edgesToAdd:
        if startTable != endTable and f"{startTable}:{startKey}" in nodes:
            dot.edge(
                # .end means the right side of the table (it is referencing another table)
                f"{startTable}:{startKey}.end", 
                # .start means the left side of the table (it is being referenced)
                f"{endTable}:{endKey}.start", 
                arrowhead='normal', arrowtail='odot', dir='both', style='solid', color='#141414', penwidth='1.5'
            )
        else:
            print(f"{startTable}:{startKey} referencing {endTable}:{endKey}\t\tError: Node does not exist.")