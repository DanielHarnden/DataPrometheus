# This file is used to generate the GraphViz DOT file used to generate the PNG. It manually creates each table and key using string concatenation, then send the table and key lists to other files to determine the edges between nodes (which differs depending on if it is a programming file or a database).

import graphviz
from datetime import datetime
from determine_Edge import databaseDetermineEdge,progDetermineEdge



def generateGraphOutput(parsedText, keyList, bannedWords):
    dot = graphviz.Digraph()

    # Moves file names from parsedText to fileNames, sorts tables from biggest to smallest
    parsedText, fileNames = initializeGraphGeneration(parsedText, [])
    primaryKeys = {}
    tableNames = []
    nodes = []

    # Loops through each file...
    for i, file in enumerate(parsedText):

        # ...stores all table names and primary keys while adding each table to GraphViz...
        filePrimaryKeys, newTables, fileTableNames = addTables(
            file, primaryKeys, [], [])
        tableNames += fileTableNames
        primaryKeys.update(filePrimaryKeys)

        # ...then adds each key to the new tables
        nodes, dot = addKeys(file, keyList, newTables, fileTableNames, fileNames[i], nodes, dot)

    # Searches for relationships between keys
    edgesToAdd = []
    edgesToAdd = findForeignKeys(parsedText, tableNames, fileNames, keyList, bannedWords)

    # Adds the found relationships as edges on the graph
    dot, edgesToAdd = generateEdgesDOT(edgesToAdd, nodes, dot)

    # Does some settings to make it look pwetty uwu
    graphCreationTime = datetime.now()
    graphCreationTime = graphCreationTime.strftime("%m/%d/%Y %I:%M %p")
    dot.graph_attr.update({
        'bgcolor': '#FFDAB9',
        'table': 'style=invis',
        'label': f'Parsed by Data Prometheus at {graphCreationTime}',
        'labelloc': 't',
        'rankdir': 'LR',
        'ranksep': '1.5',
        'nodesep': '0.5',
        'sep': '10',
        'dpi': '200'
    })

    # Renders the graph as a PNG to the output folder
    dot.render('./output/output', format='png')
    return edgesToAdd



def initializeGraphGeneration(parsedText, fileNames):
    for fileIterator, file in enumerate(parsedText):
        fileName = file[0][0]
        fileNames.append(fileName)

        # Removes file name from parsed text, sorts from biggest to smallest if database
        if not isProgrammingFile(fileName):
            file = sorted(file[1:], key=lambda x: len(x))
            file.reverse()
        else:
            file = file[1:]

        parsedText[fileIterator] = file

    return parsedText, fileNames

def isProgrammingFile(fileName):
    supportedProgrammingExtensions = ["py", "java", "cpp"]
    extension = fileName.split(".")[-1]
    return extension in supportedProgrammingExtensions



def addTables(file, primaryKeys, newTables, tableNames):
    for i, tableList in enumerate(file):
        newTables.append(
            '''<\n\n\n\n<table border="1" cellborder="1" cellspacing="0" color="#932525">''')

        tableName = tableList[0][0]
        # Determines if this table has a class
        if "." in tableName:
            # Adds initializer as className
            if tableName.split(".")[0] not in tableNames:
                tableNames.append(tableName.split(".")[0])
                tableDescriptor = "Class " + \
                    tableName.split(".")[0] + " Initializer"
            else:
                tableNames.append(tableName.split(".")[1])
                tableDescriptor = "Class " + tableName.split(".")[0]
        else:
            tableNames.append(tableName)
            tableDescriptor = " "

        newTables[i] += generateTableDOT(tableNames[i], tableDescriptor)
        primaryKeys[tableNames[i]] = tableNames[i]

    return primaryKeys, newTables, tableNames

def generateTableDOT(tableName, tableNumber):
    return f'''
  <tr>
    <td colspan='2' bgcolor='#932525' port="{tableName}.start" align='left'><font color="#FFFFEB"><b><i>{tableName}</i></b></font></td>
    <td bgcolor='#932525' align='right' port="{tableName}.end" ><font color="#FFFFEB"><b><i>{tableNumber}</i></b></font></td>
  </tr>
    '''



def addKeys(file, keyList, newTables, tableNames, fileName, nodes, dot):
    # Iterates through all of the tables from the original txt of the inputted database
    for tableIterator, tableList in enumerate(file):
        addedKeys = set()

        for i, key in enumerate(tableList):
            keyName = key[0]
            keyType = key[1]

            if i == 0:
                nodes.append(f"{tableNames[tableIterator]}:{keyName}")
                continue

            # Determines if they key has to be renamed based on the mapping
            for keySynonym in keyList:
                if keyName in keyList[keySynonym]:
                    keyName = keySynonym

            if keyName not in addedKeys and "Built-In" not in keyType:
                newTables[tableIterator] += generateKeyDOT(keyName, keyType)
                nodes.append(f"{tableNames[tableIterator]}:{keyName}")
                addedKeys.add(keyName)

        # Finishes the table then adds the node using the temporary information
        newTables[tableIterator] += "</table>\n>"

    # Adds each file as a subgraph
    with dot.subgraph(name=f'Cluster-{fileName}') as subDot:
        subDot.attr(label=fileName, color='#FFA07A',
                    bgcolor='#FFC6A5', style='solid')

        for tableIterator, tableList in enumerate(file):
            subDot.node(tableNames[tableIterator],
                        shape='none', label=newTables[tableIterator])

    return nodes, dot

def generateKeyDOT(keyName, keyType):
    return f'''
  <tr>
    <td colspan='2' bgcolor='#C43131' port="{keyName}.start" align='left'><font color="#FFFFEB"><b><i>{keyName}</i></b></font></td>
    <td bgcolor='#C43131' port="{keyName}.end" align='right'><font color="#FFFFEB">{keyType}</font></td>
  </tr>
    '''



def findForeignKeys(parsedText, tableNames, fileNames, keyList, bannedWords):
    edgesToAdd = set()
    # TODO: Make this dependent on parse_Files.py
    for fileType in fileNames:
        fileType = fileType.split(".")[-1]

        if fileType == "py" or fileType == "cpp":
            newEdges = progDetermineEdge(parsedText)
            edgesToAdd.update(newEdges)
        else:
            newEdges = databaseDetermineEdge(parsedText, keyList, tableNames, bannedWords)
            edgesToAdd.update(newEdges)  
        
    return edgesToAdd

def generateEdgesDOT(edgesToAdd, nodes, dot):
    lineColors = ["#22052D", "#361941", "#4B2C54", "#5F4068", "#73547B", "#88678F", "#9C7BA2"]
    i = 0

    for startTable, startKey, endTable, endKey in edgesToAdd.copy():
        i = i % len(lineColors)
        if startTable != endTable and f"{startTable}:{startKey}" in nodes and f"{endTable}:{endKey}" in nodes:
            dot.edge(
                # .end means the right side of the table (it is referencing another table)
                f"{startTable}:{startKey}.end",
                # .start means the left side of the table (it is being referenced)
                f"{endTable}:{endKey}.start",
                arrowhead='normal', arrowtail='odot', dir='both', style='solid', color=lineColors[i], penwidth='2.5'
            )
            i += 1
        else:
            print(f"Head node {endTable}:{endKey} does not exist. Skipping edge {startTable}:{startKey} -> {endTable}:{endKey}")
            edgesToAdd.remove((startTable, startKey, endTable, endKey))

    return dot, edgesToAdd