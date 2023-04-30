import os, tempfile, time
from generateGraph import generateGraph
from mapText import mapText

# Import the various parsers from the parsers folder
from parsers.sqlite3Parse import sqlite3Parse
from parsers.sqlParse import sqlParse
from parsers.pythonParse import pythonParse

# Lists containing the files that Data Prometheus can read. The first item is the name of the  function that will be called and the following items are the extensions that that function supports
#TODO: Determine all file types supported by sqlite3
sqLiteReadable = [sqlite3Parse, "db", "sqlite", "db3"]
sqlParseReadable = [sqlParse, "sql"]
pythonParseReadable = [pythonParse, "py"]

# A list containing the previous lists, for streamlining later
supportedFileTypes = [sqLiteReadable, sqlParseReadable, pythonParseReadable]



# Maps a single database
def mapDatabase(fileName, file, reversing):
    beginTime = time.time()
    # Sets the function to None type and determines the extension of the inputted file
    function = None
    extension = determineFileType(fileName)

    # Goes through the list of supported files. If the extension is supported, the function is marked
    for typeList in supportedFileTypes:
        if extension in typeList:
            function = typeList[0]

    if function is None:
        print("That file type is not yet supported by Data Prometheus.")
        return 0

    # Saves a temporary file for the parsers to use
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    # The file is sent to its designated parser
    startTime = time.time()
    print("Beginning parse...")
    parsedText = function(temp_file)
    print(f"Parsing completed. Time Elapsed: {time.time() - startTime} seconds.\n\n\n")

    # The temporary file is deleted
    temp_file.close()
    os.unlink(temp_file.name)

    startTime = time.time()
    print("Beginning mapping...")
    keyList, bannedWords = mapText(parsedText)
    print(f"Mapping completed. Time Elapsed: {time.time() - startTime} seconds.\n\n\n")

    startTime = time.time()
    print("Generating Graphviz png...")
    generateGraph(parsedText, keyList, fileName.split(".")[0], reversing, bannedWords)
    print(f"PNG generated. Time Elapsed: {time.time() - startTime} seconds.\n\n\n")

    print(f"Total Operational Time: {time.time() - beginTime} seconds.\n\n\n")



# Determines the file's type
def determineFileType(fileName):
    if "." not in fileName:
        return ""
    extension = fileName.split(".")[-1]
    return extension