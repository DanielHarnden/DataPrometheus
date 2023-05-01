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

    # Sorts the parsed text from biggest to smallest table
    parsedText = sorted(parsedText, key=lambda x: len(x))
    parsedText.reverse()

    # Iterates through all of the tables from the original txt of the inputted database
    for tableList in parsedText:
        # A temp list of added keys to avoid duplicates
        tempKeys = set()
        
        nodeInfo = '''<\n\t<table border="1" cellborder="1" cellspacing="0" color="#973835">'''

        # Generates the table using the table name
        nodeInfo += generateTable(tableList[0], tableNum)
        tableNum += 1

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
                nodeInfo += generateKey(key, "VARCHAR(50)")

        # Finishes the table then adds the node using the temporary information
        nodeInfo += "\n</table>\n>"
        dot.node(tableList[0], shape='none', label=nodeInfo)

    # Created a nested function since reverse parsing changes very little code
    def generateForeignKeys(parsedText, reverse):
        parsedText = list(reversed(parsedText)) if reverse else parsedText
        print(parsedText)

        # Iterates through each key (again)
        for tableList in parsedText:

            # The name of the table is stored
            table = tableList[0]
            tableList = list(reversed(tableList)) if reverse else tableList
            print(tableList)
            foreignKeysRemaining = foreignKeyNum

            for key in tableList:
                # Checks to see if this key has appeared before in the new database. If not, it is set as the primary key of the new database, and any subsequent mentions of the key will reference the key/table it first appears
                if key in jsonKeyList[keySynonyms]:
                    key = keySynonyms

                if key in primaryKeys and table is not primaryKeys[key]:
                    # Checks to see if there are any foreign key additions left for this table and checks to ensure the table is not referencing itself
                    if foreignKeysRemaining > 0 and key not in bannedWords:
                        temp = [primaryKeys[key], table, key]
                        if temp not in edgesToAdd:
                            edgesToAdd.append(temp)
                            foreignKeysRemaining = foreignKeysRemaining - 1
                else:
                    primaryKeys[key] = table
    
    # Calls the function
    generateForeignKeys(parsedText, False)
    generateForeignKeys(parsedText, True) if allowReverseParsing else None

    # Now that all of the tables are mapped, foreign keys can added to the graph in the order they were found
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