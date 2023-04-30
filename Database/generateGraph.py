import graphviz, os

def generateGraph(parsedText, jsonKeyList, graphName, allowReverseParsing, bannedWords):
    # Initializes variables
    foreignKeyNum = 1
    primaryKeys = {}
    edgesToAdd = []
    tableNum = 0

    allowReverseParsing = True if allowReverseParsing == "true" else False

    # Creates the graphviz object that will hold the graph
    dot = graphviz.Digraph()

    parsedText = sorted(parsedText, key=lambda x: len(x))
    parsedText.reverse()

    # Iterates through all of the tables from the original txt of the inputted database
    for tableList in parsedText:
        # A temp list of added keys to avoid duplicates
        tempKeys = set()
        
        nodeInfo = '''<\n\t<table border="1" cellborder="1" cellspacing="0" color="#973835">'''

        # Iterates through each table from the original txt of the inputted database
        for i, key in enumerate(tableList):

            if i == 0:
                # Generates the table using the table name
                nodeInfo += generateTable(key, tableNum)
                tableNum += 1
            else:
                # Determines if they key has to be renamed based on the mapping
                # Iterates through each key...
                for keySynonyms in jsonKeyList:
                    # ...stores the values (a list of strings)...
                    values = jsonKeyList[keySynonyms]
                    # ...and compares the current key to the values. If the key is a synonym...
                    if key in values:
                        # ...the current key is replaced with the synonym (the key from the table)
                        key = keySynonyms

                # Prevents duplicate keys
                if key not in tempKeys:
                    tempKeys.add(key)
                    # Adds every key as a varchar(50)
                    # TODO: Use VARCHAR(50) as a fallback and impliment type stealing (when applicable)
                    nodeInfo += generateKey(key, "VARCHAR(50)")

        # Finishes the table then adds the node using the temporary information
        nodeInfo += "\n</table>\n>"
        dot.node(tableList[0], shape='none', label=nodeInfo)

    print(parsedText)

    for tableList in parsedText:
        # Iterates through each key (again)
        for j, key in enumerate(tableList):
            # The name of the table is stored
            if j == 0:
                foreignKeysRemaining = foreignKeyNum
                table = key
            else:
                # Checks to see if this key has appeared before in the new database. If not, it is set as the primary key of the new database, and any subsequent mentions of the key will reference the key/table it first appears
                for keySynonyms in jsonKeyList:
                    values = jsonKeyList[keySynonyms]
                    if key in values:
                        key = keySynonyms

                print(key)

                if key in primaryKeys:
                    # Checks to see if there are any foreign key additions left for this table and checks to ensure the table is not referencing itself
                    if foreignKeysRemaining > 0 and key not in bannedWords:
                        edgesToAdd.append(primaryKeys[key])
                        edgesToAdd.append(table)
                        edgesToAdd.append(key)
                        foreignKeysRemaining = foreignKeysRemaining - 1
                else:
                    primaryKeys[key] = table

    if allowReverseParsing is True:
        for temp1, tableList in reversed(list(enumerate(parsedText))):
            table = tableList[0]

            for temp2, key in reversed(list(enumerate(tableList))):
                if temp2 == len(tableList) - 1:
                    foreignKeysRemaining = foreignKeyNum
                
                for keySynonyms in jsonKeyList:
                    values = jsonKeyList[keySynonyms]
                    if key in values:
                        key = keySynonyms

                if key in primaryKeys and table is not primaryKeys[key]:
                    if foreignKeysRemaining > 0 and key not in bannedWords:
                        edgesToAdd.append(primaryKeys[key])
                        edgesToAdd.append(table)
                        edgesToAdd.append(key)
                        foreignKeysRemaining = foreignKeysRemaining - 1
                else:
                    primaryKeys[key] = table

    # Removes any duplicate edges
    edgesToAdd = set(tuple(edgesToAdd[i:i+3]) for i in range(0, len(edgesToAdd), 3))

    print(edgesToAdd)

    # Remove items where first and second elements are swapped but third element is the same
    for firstTriple in edgesToAdd:
        for secondTriple in edgesToAdd:
            if firstTriple[0] == secondTriple[1] and firstTriple[1] == secondTriple[2] and firstTriple[3] == secondTriple[3]:
                edgesToAdd.remove(secondTriple)
        
    
    # Now that all of the foreign keys are mapped, they're added to the graph in the order they were found
    for referencedTable, tableReferencing, key in edgesToAdd:
        if referencedTable != tableReferencing:
            dot.edge(f"{tableReferencing}:{key}.end", f"{referencedTable}:{key}.start", arrowhead='vee', arrowtail='odot', dir='both', label=f"{tableReferencing} ref.  {referencedTable}", style='solid')

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
    <tr>
        <td colspan='2' bgcolor='#B0413E' align='left'><font color="#FFFFEB"><b><i>{tableName}</i></b></font></td>
        <td bgcolor='#B0413E' align='right'><font color="#FFFFEB"><b><i>{tableNum}</i></b></font></td>
    </tr>
    '''

def generateKey(keyName, varType):
    return f'''
    <tr>
        <td colspan='2' bgcolor='#973835' port="{keyName}.start" align='left'><font color="#FFFFEB"><b><i>{keyName}</i></b></font></td>
        <td bgcolor='#973835' port="{keyName}.end" align='right'><font color="#FFFFEB">{varType}</font></td>
    </tr>
    '''