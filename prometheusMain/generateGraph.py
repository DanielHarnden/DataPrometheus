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
        
    
    # Searches for relationships between foreign keys
    tablesVisited = {}
    edgesToAdd = []
    edgesToAdd, tablesVisited = addForeignKeys(parsedText, tableNames, tablesVisited, edgesToAdd, keyList, primaryKeys, bannedWords)

    # Adds the found relationships as edges on the graph
    generateForeignKeys(edgesToAdd, nodes)

    graphCreation = datetime.now()
    graphCreation = graphCreation.strftime("%m/%d/%Y %I:%M %p")
    # Does some settings to make it look pwetty
    dot.graph_attr.update({
        'table': 'style=invis',
        'label': f'Parsed by Data Prometheus at {graphCreation}',
        'labelloc': 't',
        'rankdir': 'LR',
        'dpi': '200'
    })

    # Renders the graph as a PNG to the output folder
    dot.render('./output/output', format='png')





def initializeGraphGeneration(parsedText, fileNames):
    for i, file in enumerate(parsedText):
        fileNames.append(file[0][0])
        # Sorts the parsed text from biggest to smallest table
        file = sorted(file[1:], key=lambda x: len(x))
        file.reverse()
        parsedText[i] = file

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
    for i, tableList in enumerate(file):
        # A temp list of added keys to avoid duplicates
        tempKeys = set()
        # Iterates through each table from the original text of the inputted database
        for key in tableList[1:]:
            # Determines if they key has to be renamed based on the mapping
            # Iterates through each key...
            for keySynonym in keyList:
                # ...compares the current key to the values. If the key is a synonym...
                if key[0] in keyList[keySynonym]:
                    # ...the current key is replaced with the synonym (the key from the table)
                    key[0] = keySynonym

            # Prevents duplicate keys
            #if key[0] not in tempKeys:
            #    tempKeys.add(key[0])
            newTables[i] += generateKey(key[0], key[1])
            nodes.append(f"{tableNames[i]}:{key[0]}")

        # Finishes the table then adds the node using the temporary information
        newTables[i] += "</table>\n>"

    # The cluster needs a random int because clusters can't be named the same
    with dot.subgraph(name=f'Cluster-{random.randint(1,1000)}') as subDot:
        for i, tableList in enumerate(file):
            subDot.attr(label=fileName, color='#FFA07A', bgcolor='#FFC6A5', style='solid')
            subDot.node(tableNames[i], shape='none', label=newTables[i])

    return nodes



def addForeignKeys(parsedText, tableNames, tablesVisited, edgesToAdd, keyList, primaryKeys, bannedWords):
    stemmer = snowballstemmer.stemmer('english')

    i = 0
    # Iterates through each key (again)
    for file in parsedText:

        for tableList in file:

            # The name of the table is stored
            table = tableNames[i]
            i += 1
            if table not in tablesVisited:
                tablesVisited[table] = []

            for key in tableList:
                # Checks to see if this key has appeared before in the new database. If not, it is set as the primary key of the new database, and any subsequent mentions of the key will reference the key/table it first appears
                for keySynonym in keyList:
                    if key[0] in keyList[keySynonym]:
                        key[0] = keySynonym

                if key[0] in primaryKeys and table is not primaryKeys[key[0]]:
                    # Checks to see if there are any foreign key additions left for this table and checks to ensure the table is not referencing itself
                    if primaryKeys[key[0]] not in tablesVisited[table] and key[0] not in bannedWords:

                        # Determines if the key is a substring of the stem of the table name it is going to be referencing. e.g. if MusicLabel is the current key and finds Artists as a key to reference, MusicLabel/ArtistId would be added as the primary key referencing Artists. However, Artists/ArtistId is clearly the primary key, and since Arist (the stem of Artists) is in ArtistId, the it is correctly label as the primary key.
                        #       Artists [table] | MusicLabel [table]
                        #       ArtistId        | ArtistId
                        cleanedTableName = table.replace(" [table]", "")
                        cleanedTableName = cleanedTableName.replace("_", "")
                        tableStem = stemmer.stemWord(cleanedTableName)
                    
                        if key[0] + " [table]" in tableNames:
                            if tableStem in key[0].lower():
                                tempEdge = (primaryKeys[key[0]], primaryKeys[key[0]], table, key[0], True)
                            else:
                                tempEdge = (table, key[0], primaryKeys[key[0]], primaryKeys[key[0]], True)
                        else:
                            if tableStem in key[0].lower():
                                tempEdge = (primaryKeys[key[0]], key[0], table, key[0], False)
                            else:
                                tempEdge = (table, key[0], primaryKeys[key[0]], key[0], False)

                        if tempEdge not in edgesToAdd:
                            edgesToAdd.append(tempEdge)
                            tablesVisited[table].append(primaryKeys[key[0]])
                            
                else:
                    primaryKeys[key[0]] = table

    return edgesToAdd, tablesVisited



def generateTable(tableName, tableNumber):
    return f'''
  <tr>
    <td colspan='2' bgcolor='#932525' port="{tableName}.start" align='left'><font color="#FFFFEB"><b><i>{tableName}</i></b></font></td>
    <td bgcolor='#932525' align='right' port="{tableName}.end" ><font color="#FFFFEB"><b><i>{tableNumber}</i></b></font></td>
  </tr>
    '''



def generateKey(keyName, varType):
    return f'''
  <tr>
    <td colspan='2' bgcolor='#C43131' port="{keyName}.start" align='left'><font color="#FFFFEB"><b><i>{keyName}</i></b></font></td>
    <td bgcolor='#C43131' port="{keyName}.end" align='right'><font color="#FFFFEB">{varType}</font></td>
  </tr>
    '''



def generateForeignKeys(edgesToAdd, nodes):
    global dot

    for tableReferencing, keyReferencing, referencedTable, referencedKey, referencingTable in edgesToAdd:
        if referencedTable != tableReferencing:
            if f"{tableReferencing}:{keyReferencing}" in nodes:
                dot.edge(f"{tableReferencing}:{keyReferencing}.end", f"{referencedTable}:{referencedKey}.start", arrowhead='normal', arrowtail='odot', dir='both', style='solid', color='#141414', penwidth='1.5')
            elif f"{referencedTable}:{keyReferencing}" in nodes and referencingTable:
                dot.edge(f"{referencedTable}:{keyReferencing}.end", f"{tableReferencing}:{tableReferencing}.start", arrowhead='normal', arrowtail='odot', dir='both', style='solid', color='#141414', penwidth='1.5')
            else:
                print(f"{referencedTable}:{keyReferencing}.end {tableReferencing}:{tableReferencing}.start")
                print("Node does not exist.")