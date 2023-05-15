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
supportedFileTypes = [sqLiteReadable, sqlParseReadable, pythonParseReadable, cppParseReadable, javaReadable]
supportedMergeFileTypes = [sqLiteReadable, sqlParseReadable]



def mapDatabase(files):
    beginTime = time.time()
    parsedText = []
    
    for i, file in enumerate(files):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        function = None
        extension = determineFileType(file.filename)

        for typeList in supportedFileTypes:
            if extension in typeList:
                function = typeList[0]

        if function is None:
            print(f"File types of extension .{extension} are not currently supported.")
            return 0

        tempStartTime = time.time()
        print(f"Beginning parse {i+1} of {len(files)}...")
        parsedText.append(function(temp_file, file.filename))
        print(f"Parse {i+1} completed. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

        temp_file.close()
        os.unlink(temp_file.name)

    tempStartTime = time.time()
    print("Beginning mapping...")
    keyList, bannedWords = mapText(parsedText)
    print(f"Mapping completed. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    tempStartTime = time.time()
    print("Generating GraphViz PNG...")
    generateGraph(parsedText, keyList, bannedWords)
    print(f"PNG generated. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    print(f"Total Operational Time: {time.time() - beginTime} seconds.\n")



def mergeDatabase(files):
    beginTime = time.time()
    parsedText = []
    parsedInserts = []
    
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
            print(f"File types of extension .{extension} are not currently supported.")
            return 0

        tempStartTime = time.time()
        print(f"Beginning parse and copying values {i+1} of {len(files)}...")
        parsedText.append(function(temp_file, file.filename))
        parsedInserts.append(insertParser(temp_file))
        print(f"Parse and copying {i+1} completed. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

        temp_file.close()
        os.unlink(temp_file.name)

    tempStartTime = time.time()
    print("Beginning mapping...")
    keyList, bannedWords = mapText(parsedText)
    print(f"Mapping completed. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    tempStartTime = time.time()
    print("Generating GraphViz PNG...")
    newParsedText = combineFiles(parsedText)
    edgesToAdd = generateGraph(newParsedText, keyList, bannedWords)
    print(f"PNG generated. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    tempStartTime = time.time()
    print("Generating SQL file...")
    generateSQL(parsedText, parsedInserts, edgesToAdd)
    print(f"SQL generated. Time Elapsed: {time.time() - tempStartTime} seconds.\n")

    print(f"Total Operational Time: {time.time() - beginTime} seconds.\n")


# Determines the file's type
def determineFileType(fileName):
    if "." not in fileName:
        return ""
    extension = fileName.split(".")[-1]
    return extension