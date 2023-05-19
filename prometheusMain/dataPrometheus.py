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



def processDatabase(files, operation):
    beginTime = time.time()
    
    # Checks for common errors
    status, errorMessage = errorCheck(files, operation)
    if status == 0:
        return 0, errorMessage

    # 1) Parse an inputted file for relevant information.
    status, errorMessage, parsedText, parsedInserts = attemptParse(files, operation)
    if status == 0:
        return 0, errorMessage

    # 2) Map the parsed information to itself to find relationships between "keys" and "tables."
    status, errorMessage, keyList, bannedWords = attemptMap(parsedText)
    if status == 0:
        return 0, errorMessage

    # 3) Generate a visualization of the mapped information using GraphViz.
    status, errorMessage, edgesToAdd = attemptGraph(operation, parsedText, keyList, bannedWords)
    if status == 0:
        return 0, errorMessage
    
    # 3.5) Generate SQL file (if merging)
    if operation == "mergeDatabase":
        status, errorMessage = attemptSQLGeneration(parsedText, parsedInserts, keyList, edgesToAdd)
        if status == 0:
            return 0, errorMessage
        
    print(f"Total Operational Time: {time.time() - beginTime} seconds.\n")
    return 1, "Successful operation."



def errorCheck(files, operation):
    if len(files) == 1 and files[0].filename == "":
        errorMessage = f"No file(s) chosen."
        return 0, errorMessage
    
    if operation == "mergeDatabase" and len(files) < 2:
        errorMessage = f"Please choose two or more files to merge."
        return 0, errorMessage
    
    return None, None


def attemptParse(files, operation):
    parsedText = []  
    parsedInserts = []

    for i, file in enumerate(files):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)
        extension = determineFileType(file.filename)
        parsingFunction = None

        # Chooses the appropriate parser
        if operation == "mapDatabase":
            for typeList in supportedFileTypes:
                if extension in typeList:
                    parsingFunction = typeList[0]
                    break
                    
        elif operation == "mergeDatabase":
            for typeList in supportedMergeFileTypes:
                if extension in typeList:
                    parsingFunction = typeList[0]
                    insertParsingFunction = typeList[1]
                    break

        # Returns an error if there is no parser
        if parsingFunction is None:
            if operation == "mapDatabase":
                errorMessage = f"Files of extension .{extension} are not currently supported by Data Prometheus's mapping function."
            elif operation == "mergeDatabase":
                errorMessage = f"Files of extension .{extension} are not currently supported by Data Prometheus's database merging function. If you want to view a graph visualization of this file, please try Data Prometheus's mapper."
            return 0, errorMessage, None, None

        startTime = time.time()
        print(f"Beginning parse {i+1} of {len(files)}...")

        try:
            parsedText.append(parsingFunction(temp_file, file.filename))
        except:
            errorMessage = f"There was an error parsing {file.filename}. Please make sure that the file is a valid {extension} file or that Data Prometheus is in a stable build."
            return 0, errorMessage, None, None

        if operation == "mergeDatabase":
            parsedInserts.append(insertParsingFunction(temp_file))
        
        temp_file.close()
        os.unlink(temp_file.name)
        print(f"Parse {i+1} completed. Time Elapsed: {time.time() - startTime} seconds.\n")

    return None, None, parsedText, parsedInserts



def attemptMap(parsedText):
    startTime = time.time()
    print("Beginning mapping...")

    try:
        keyList, bannedWords = mapText(parsedText)
    except:
        errorMessage = f"There was an error while mapping keys. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage, None, None
    
    print(f"Mapping completed. Time Elapsed: {time.time() - startTime} seconds.\n")
    return None, None, keyList, bannedWords
    


def attemptGraph(operation, parsedText, keyList, bannedWords):
    startTime = time.time()
    print("Generating GraphViz PNG...")

    try:
        if operation == "mapDatabase":
            generateGraph(parsedText, keyList, bannedWords)
            print(f"PNG generated. Time Elapsed: {time.time() - startTime} seconds.\n")
            return None, None, None
        elif operation == "mergeDatabase":
            tempParsedText = combineFiles(parsedText)
            edgesToAdd = generateGraph(tempParsedText, keyList, bannedWords)
            print(f"PNG generated. Time Elapsed: {time.time() - startTime} seconds.\n")
            return None, None, edgesToAdd
    except:
        errorMessage = f"There was an error while generating the graph output. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage, None, None
    


def attemptSQLGeneration(parsedText, parsedInserts, keyList, edgesToAdd):
    startTime = time.time()
    print("Generating SQL file...")

    try:
        generateSQL(parsedText, parsedInserts, keyList, edgesToAdd)
    except:
        errorMessage = f"There was an error while generating the SQL output. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage
    
    print(f"SQL generated. Time Elapsed: {time.time() - startTime} seconds.\n")
    return None, None



# Determines the file's type
def determineFileType(fileName):
    if "." not in fileName:
        return ""
    extension = fileName.split(".")[-1]
    return extension