import graphviz, os

def generateGraph(parsedText, jsonKeyList, graphName, allowReverseParsing, bannedWords):
    # Initializes variables
    primaryKeys = {}
    edgesToAdd = []
    tableNum = 0

    tableNames = []
    tempTables = []
    nodes = []




    allowReverseParsing = True if allowReverseParsing == "true" else False

    # Creates the graphviz object that will hold the graph
    dot = graphviz.Digraph()

    print(parsedText)

    for fileTables in parsedText:

        #tempTables.append('''<\n\t<table border="1" cellborder="1" cellspacing="0" color="#973835">''')

        #fileTables[0]

        fileTables.pop(0)

        # Sorts the parsed text from biggest to smallest table
        fileTables = sorted(fileTables, key=lambda x: len(x))
        fileTables.reverse()

        # Adds each table to the database
        for i, tableList in enumerate(fileTables):
            tempTables.append('''<\n\t<table border="1" cellborder="1" cellspacing="0" color="#973835">''')

            # Generates the table using the table name
            tableNames.append(tableList[0] + " [table]")
            tempTables[i] += generateTable(tableNames[i], tableNum)
            primaryKeys[tableNames[i]] = tableNames[i]
            tableNum += 1

        # Iterates through all of the tables from the original txt of the inputted database
        for i, tableList in enumerate(fileTables):
            # A temp list of added keys to avoid duplicates
            tempKeys = set()
            # Iterates through each table from the original text of the inputted database
            for key in tableList[1:]:
                # Determines if they key has to be renamed based on the mapping
                # Iterates through each key...
                for keySynonyms in jsonKeyList:
                    # ...compares the current key to the values. If the key is a synonym...
                    if key in jsonKeyList[keySynonyms]:
                        # ...the current key is replaced with the synonym (the key from the table)
                        key = keySynonyms

                # Prevents duplicate keys
                if key not in tempKeys:
                    tempKeys.add(key)
                    # Adds every key as a varchar(50)
                    # TODO: Use VARCHAR(50) as a fallback and impliment type stealing (when applicable)
                    tempTables[i] += generateKey(key, "VARCHAR(50)")
                    nodes.append(f"{tableNames[i]}:{key}")

            # Finishes the table then adds the node using the temporary information
            tempTables[i] += "\n</table>\n>"
            dot.node(tableNames[i], shape='none', label=tempTables[i])

    tablesVisited = []
    # Created a nested function since reverse parsing changes very little code
    def generateForeignKeys(parsedText, reverse):
        parsedText = list(reversed(parsedText)) if reverse else parsedText

        # Iterates through each key (again)
        for i, tableList in enumerate(parsedText):
            if not reverse:
                tablesVisited.append([])

            # The name of the table is stored
            table = tableNames[i]
            tableList = list(reversed(tableList)) if reverse else tableList

            for key in tableList:
                # Checks to see if this key has appeared before in the new database. If not, it is set as the primary key of the new database, and any subsequent mentions of the key will reference the key/table it first appears
                if key in jsonKeyList[keySynonyms]:
                    key = keySynonyms

                if key in primaryKeys and table is not primaryKeys[key]:
                    # Checks to see if there are any foreign key additions left for this table and checks to ensure the table is not referencing itself
                    if primaryKeys[key] not in tablesVisited[i] and key not in bannedWords:

                        if key + " [table]" in tableNames:
                            temp = (table, key, primaryKeys[key], primaryKeys[key], True)
                        else:
                            temp = (table, key, primaryKeys[key], key, False)

                        if temp not in edgesToAdd:
                            edgesToAdd.append(temp)
                            tablesVisited[i].append(primaryKeys[key])
                            
                else:
                    primaryKeys[key] = table

    for fileTables in parsedText:
        fileTables.pop(0)

        # Sorts the parsed text from biggest to smallest table
        fileTables = sorted(fileTables, key=lambda x: len(x))
        fileTables.reverse()
        
        # Calls the function
        generateForeignKeys(fileTables, False)

        if allowReverseParsing:
            tablesVisited = list(reversed(tablesVisited))
            generateForeignKeys(fileTables, True)

    # Now that all of the tables are mapped, foreign keys can added to the graph in the order they were found
    for tableReferencing, keyReferencing, referencedTable, referencedKey, referencingTable in edgesToAdd:
        if referencedTable != tableReferencing:
            if f"{tableReferencing}:{keyReferencing}" in nodes:
                dot.edge(f"{tableReferencing}:{keyReferencing}.end", f"{referencedTable}:{referencedKey}.start", arrowhead='vee', arrowtail='odot', dir='both', label=f"{tableReferencing} ref.  {referencedTable}", style='solid')
            elif f"{referencedTable}:{keyReferencing}" in nodes and referencingTable:
                dot.edge(f"{referencedTable}:{keyReferencing}.end", f"{tableReferencing}:{tableReferencing}.start", arrowhead='vee', arrowtail='odot', dir='both', label=f"{referencedTable} ref.  {tableReferencing}", style='solid')
            else:
                print("Node does not exist.")

    # Does some settings to make it look pwetty
    dot.graph_attr.update({
        'table': 'style=invis',
        'label': graphName + ' as parsed by Data Prometheus (copyright me do not steal!!!)',
        'labelloc': 't',
        'rankdir': 'LR',
        'dpi': '200'
    })

    # Renders the graph as a PNG to the output folder
    dot.render('./output/output', format='png')



def generateTable(tableName, tableNum):
    return f'''
    \t<tr>
        \t<td colspan='2' bgcolor='#B0413E' port="{tableName}.start" align='left'><font color="#FFFFEB"><b><i>{tableName}</i></b></font></td>
        \t<td bgcolor='#B0413E' align='right' port="{tableName}.end" ><font color="#FFFFEB"><b><i>{tableNum}</i></b></font></td>
    \t</tr>
    '''

def generateKey(keyName, varType):
    return f'''
    \t<tr>
        \t<td colspan='2' bgcolor='#973835' port="{keyName}.start" align='left'><font color="#FFFFEB"><b><i>{keyName}</i></b></font></td>
        \t<td bgcolor='#973835' port="{keyName}.end" align='right'><font color="#FFFFEB">{varType}</font></td>
    \t</tr>
    '''