import os, tempfile, time
from generateGraph import generateGraph
from mapText import mapText

# Import the various parsers from the parsers folder
from parsers.sqliteParse import sqliteParse
from parsers.sqlParse import sqlParse
from parsers.pythonParse import pythonParse

# Lists containing the files that Data Prometheus can read. The first item is the name of the  function that will be called and the following items are the extensions that that function supports
#TODO: Determine all file types supported by sqlite3
sqLiteReadable = [sqliteParse, "db", "db3", "s3db", "sqlite", "sqlite3", "sqlitedb", "sl3"]
sqlParseReadable = [sqlParse, "sql"]
pythonParseReadable = [pythonParse, "py"]

# A list containing the previous lists, for streamlining later
supportedFileTypes = [sqLiteReadable, sqlParseReadable, pythonParseReadable]



# Maps a single database
def mapDatabase(files, reversing):
    beginTime = time.time()

    # Sets the function to None type and determines the extension of the inputted file
    function = None
    fileTypes = set()

    # Checks the extensions to see if they're compatable
    for file in files:
        extension = determineFileType(file.filename)
        fileTypes.add(extension)

    # If the extensions are not compatable, exit the program
    if len(fileTypes) != 1:
        print("Multi file type parsing is not yet supported by Data Prometheus.")
        return 0

    # Goes through the list of supported files. If the extension is supported, the function is marked
    for typeList in supportedFileTypes:
        if extension in typeList:
            function = typeList[0]

    # If no supported function is found, exit the program
    if function is None:
        print("That file type is not yet supported by Data Prometheus.")
        return 0

    # Holds the text parsed from the input files
    parsedText = []

    # Parse each of the sent files and append it to parsedText
    for i, file in enumerate(files):
        # Saves a temporary file for the parsers to use
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        # The file is sent to its designated parser
        startTime = time.time()
        print(f"Beginning parse {i+1} of {len(files)}...")
        parsedText.append(function(temp_file, file.filename))
        print(f"Parse {i+1} completed. Time Elapsed: {time.time() - startTime} seconds.\n")

        # The temporary file is deleted
        temp_file.close()
        os.unlink(temp_file.name)

    # Maps the parsed text
    startTime = time.time()
    print("Beginning mapping...")
    keyList, bannedWords = mapText(parsedText)
    print(f"Mapping completed. Time Elapsed: {time.time() - startTime} seconds.\n")

    # Generates a graph based on th parsed text
    startTime = time.time()
    print("Generating Graphviz png...")
    generateGraph(parsedText, keyList, reversing, bannedWords)
    print(f"PNG generated. Time Elapsed: {time.time() - startTime} seconds.\n")

    print(f"Total Operational Time: {time.time() - beginTime} seconds.\n")



# Determines the file's type
def determineFileType(fileName):
    if "." not in fileName:
        return ""
    extension = fileName.split(".")[-1]
    return extension