import os, tempfile, time
from generateGraph import generateGraph
from mapText import mapText
from combineFiles import combineFiles, generateSQL

# Import the various parsers from the parsers folder
from parsers.sqliteParse import sqliteParse, sqliteInsertParse
from parsers.sqlParse import sqlParse, sqlInsertParse
from parsers.pythonParse import pythonParse
from parsers.cppParse import cppParse
from parsers.javaParse import javaParse

# Lists containing the files that Data Prometheus can read. The first item is the name of the  function that will be called and the following items are the extensions that that function supports
sqLiteReadable = [sqliteParse, sqliteInsertParse,  "db", "db3", "s3db", "sqlite", "sqlite3", "sqlitedb", "sl3"]
sqlParseReadable = [sqlParse, sqlInsertParse, "sql"]
pythonParseReadable = [pythonParse, None, "py"]
cppParseReadable = [cppParse, None, "cpp"]
javaReadable = [javaParse, None, "java"]

# A list containing the previous lists, for streamlining later
supportedFileTypes = [sqLiteReadable, sqlParseReadable, pythonParseReadable, javaReadable]
supportedMergeFileTypes = [sqLiteReadable, sqlParseReadable]



def mapDatabase(files):
    beginTime = time.time()
    parsedText = []  
    
    for i, file in enumerate(files):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        if len(files) == 1 and file.filename == "":
            errorMessage = f"No file(s) chosen."
            return 0, errorMessage, time.time() - beginTime


        function = None
        extension = determineFileType(file.filename)

        for typeList in supportedFileTypes:
            if extension in typeList:
                function = typeList[0]

        if function is None:
            errorMessage = f"Files of extension .{extension} are not currently supported by Data Prometheus's mapping function."
            return 0, errorMessage, time.time() - beginTime

        tempStartTime = time.time()
        print(f"Beginning parse {i+1} of {len(files)}...")
        try:
            parsedText.append(function(temp_file, file.filename))
        except:
            errorMessage = f"There was an error parsing {file.filename}. Please make sure that the file is a valid {extension} file or that Data Prometheus is in a stable build."
            return 0, errorMessage, time.time() - beginTime
        print(f"Parse {i+1} completed. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

        temp_file.close()
        os.unlink(temp_file.name)

    tempStartTime = time.time()
    print("Beginning mapping...")
    try:
        keyList, bannedWords = mapText(parsedText)
    except:
        errorMessage = f"There was an error while mapping keys. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage, time.time() - beginTime 
    print(f"Mapping completed. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    tempStartTime = time.time()
    print("Generating GraphViz PNG...")
    try:
        generateGraph(parsedText, keyList, bannedWords)
    except:
        errorMessage = f"There was an error while generating the graph output. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage, time.time() - beginTime
    print(f"PNG generated. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    print(f"Total Operational Time: {time.time() - beginTime} seconds.\n")
    return 1, "Successful operation.", -1



def mergeDatabase(files):
    beginTime = time.time()
    parsedText = []
    parsedInserts = []

    if len(files) < 2:
        errorMessage = f"Please choose two or more files to merge."
        return 0, errorMessage, time.time() - beginTime

    for i, file in enumerate(files):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        function = None
        extension = determineFileType(file.filename)

        for typeList in supportedMergeFileTypes:
            if extension in typeList:
                function = typeList[0]
                insertParser = typeList[1]

        if function is None:
            errorMessage = f"Files of extension .{extension} are not currently supported by Data Prometheus's database merging function. If you want to view a graph visualization of this file, please try Data Prometheus's mapper."
            return 0, errorMessage, time.time() - beginTime

        tempStartTime = time.time()
        print(f"Beginning parse and copying values {i+1} of {len(files)}...")
        try:
            parsedText.append(function(temp_file, file.filename))
            parsedInserts.append(insertParser(temp_file))
        except:
            errorMessage = f"There was an error parsing {file.filename}. Please make sure that the file is a valid {extension} file or that Data Prometheus is in a stable build."
            return 0, errorMessage, time.time() - beginTime 
        print(f"Parse and copying {i+1} completed. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

        temp_file.close()
        os.unlink(temp_file.name)

    tempStartTime = time.time()
    print("Beginning mapping...")
    try:
        keyList, bannedWords = mapText(parsedText)
    except:
        errorMessage = f"There was an error while mapping keys. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage, time.time() - beginTime
    print(f"Mapping completed. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    tempStartTime = time.time()
    print("Generating GraphViz PNG...")
    try:
        newParsedText = combineFiles(parsedText)
        edgesToAdd = generateGraph(newParsedText, keyList, bannedWords)
    except:
        errorMessage = f"There was an error while generating the graph output. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage, time.time() - beginTime 
    
    print(f"PNG generated. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    tempStartTime = time.time()
    print("Generating SQL file...")
    #try:
    generateSQL(parsedText, parsedInserts, keyList, edgesToAdd)
    #except:
    #    errorMessage = f"There was an error while generating the SQL output. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
    #    return 0, errorMessage, time.time() - beginTime
    print(f"SQL generated. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    print(f"Total Operational Time: {time.time() - beginTime} seconds.\n")
    return 1, "Successful operation.", -1


# Determines the file's type
def determineFileType(fileName):
    if "." not in fileName:
        return ""
    extension = fileName.split(".")[-1]
    return extension