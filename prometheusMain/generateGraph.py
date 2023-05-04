import graphviz, os, random, snowballstemmer

dot = graphviz.Digraph()

def generateGraph(parsedText, keyList, bannedWords):
    global dot 
    dot = graphviz.Digraph()
    stemmer = snowballstemmer.stemmer('english')

    # This is an embedded function because if it wasn't you'd have to send literally every other variable as an argument and I'm not about thta life
    edgesToAdd = []








    def addForeignKeys(parsedText, totalTables):

        # Iterates through each key (again)
        for i, tableList in enumerate(parsedText):
            tablesVisited.append([])

            # The name of the table is stored
            table = completeTableNames[i + totalTables]

            for key in tableList:
                # Checks to see if this key has appeared before in the new database. If not, it is set as the primary key of the new database, and any subsequent mentions of the key will reference the key/table it first appears
                for keySynonyms in keyList:
                    if key in keyList[keySynonyms]:
                        key = keySynonyms

                if key in primaryKeys and table is not primaryKeys[key]:
                    # Checks to see if there are any foreign key additions left for this table and checks to ensure the table is not referencing itself
                    if primaryKeys[key] not in tablesVisited[i] and key not in bannedWords:

                        stem = stemmer.stemWord(table.replace(" [table]", ""))

                        


                        if key + " [table]" in tableNames:
                            if stem in key.lower():
                                print(stem, key, primaryKeys[key], " ref ", table)
                                temp = (primaryKeys[key], primaryKeys[key], table, key, True)
                            else:
                                temp = (table, key, primaryKeys[key], primaryKeys[key], True)
                        else:
                            if stem in key.lower():
                                print(stem, key, primaryKeys[key], " ref ", table)
                                temp = (primaryKeys[key], key, table, key, False)
                            else:
                                temp = (table, key, primaryKeys[key], key, False)

                        if temp not in edgesToAdd:
                            edgesToAdd.append(temp)
                            tablesVisited[i].append(primaryKeys[key])
                            
                else:
                    primaryKeys[key] = table






    

    
    #
    parsedText, fileNames = initializeGraphGeneration(parsedText, [])

    completeTableNames = []

    for i, file in enumerate(parsedText):
    
        #
        primaryKeys, newTables, tableNames = addTables(file, {}, [], [])

        completeTableNames += tableNames
        

        #
        newTables, nodes = addKeys(file, keyList, newTables, tableNames, fileNames[i], [])
        

    totalTables = 0
    tablesVisited = []
    for file in parsedText:
        #
        addForeignKeys(file, totalTables)
        totalTables += len(file)

    totalTables = 0
    tablesVisited = list(reversed(tablesVisited))
    for file in reversed(parsedText):
        #
        addForeignKeys(file, totalTables)
        totalTables += len(file)

    #
    generateForeignKeys(edgesToAdd, nodes)

    # Does some settings to make it look pwetty
    dot.graph_attr.update({
        'table': 'style=invis',
        'label': ' LABEL TEMPORARY NAME!!!!!!!!!!!!! as parsed by Data Prometheus (copyright me do not steal!!!)',
        'labelloc': 't',
        'rankdir': 'LR',
        'dpi': '200'
    })

    # Renders the graph as a PNG to the output folder
    dot.render('./output/output', format='png')



#
def initializeGraphGeneration(parsedText, fileNames):
    for i, file in enumerate(parsedText):
        fileNames.append(file[0][0])
        # Sorts the parsed text from biggest to smallest table
        file = sorted(file[1:], key=lambda x: len(x))
        file.reverse()
        parsedText[i] = file

    return parsedText, fileNames



#
def addTables(file, primaryKeys, newTables, tableNames):
    # Adds each table to the database
    for i, tableList in enumerate(file):
        newTables.append('''<\n\n\n\n<table border="1" cellborder="1" cellspacing="0" color="#973835">''')

        # Generates the table using the table name
        tableNames.append(tableList[0] + " [table]")
        newTables[i] += generateTable(tableNames[i], i)
        primaryKeys[tableNames[i]] = tableNames[i]

    return primaryKeys, newTables, tableNames



#
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
            for keySynonyms in keyList:
                # ...compares the current key to the values. If the key is a synonym...
                if key in keyList[keySynonyms]:
                    # ...the current key is replaced with the synonym (the key from the table)
                    key = keySynonyms

            # Prevents duplicate keys
            if key not in tempKeys:
                tempKeys.add(key)
                # Adds every key as a varchar(50)
                # TODO: Use VARCHAR(50) as a fallback and impliment type stealing (when applicable)
                newTables[i] += generateKey(key, "VARCHAR(50)")
                nodes.append(f"{tableNames[i]}:{key}")

        # Finishes the table then adds the node using the temporary information
        newTables[i] += "</table>\n>"

    with dot.subgraph(name=f'Cluster-{random.randint(1,1000)}') as subDot:
        for i, tableList in enumerate(file):
            subDot.attr(label=fileName, color='blue', bgcolor='lightblue', style='solid')
            subDot.node(tableNames[i], shape='none', label=newTables[i])

    return newTables, nodes



#
def generateTable(tableName, tableNumber):
    return f'''
  <tr>
    <td colspan='2' bgcolor='#B0413E' port="{tableName}.start" align='left'><font color="#FFFFEB"><b><i>{tableName}</i></b></font></td>
    <td bgcolor='#B0413E' align='right' port="{tableName}.end" ><font color="#FFFFEB"><b><i>{tableNumber}</i></b></font></td>
  </tr>
    '''

#
def generateKey(keyName, varType):
    return f'''
  <tr>
    <td colspan='2' bgcolor='#973835' port="{keyName}.start" align='left'><font color="#FFFFEB"><b><i>{keyName}</i></b></font></td>
    <td bgcolor='#973835' port="{keyName}.end" align='right'><font color="#FFFFEB">{varType}</font></td>
  </tr>
    '''

#
def generateForeignKeys(edgesToAdd, nodes):
    global dot

    for tableReferencing, keyReferencing, referencedTable, referencedKey, referencingTable in edgesToAdd:

        
        if referencedTable != tableReferencing:
            if f"{tableReferencing}:{keyReferencing}" in nodes:
                dot.edge(f"{tableReferencing}:{keyReferencing}.end", f"{referencedTable}:{referencedKey}.start", arrowhead='vee', arrowtail='odot', dir='both', label=f"{tableReferencing} ref.  {referencedTable}", style='solid')
            elif f"{referencedTable}:{keyReferencing}" in nodes and referencingTable:
                dot.edge(f"{referencedTable}:{keyReferencing}.end", f"{tableReferencing}:{tableReferencing}.start", arrowhead='vee', arrowtail='odot', dir='both', label=f"{referencedTable} ref.  {tableReferencing}", style='solid')
            else:
                print("Node does not exist.")