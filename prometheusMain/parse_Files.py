# This file is used to determine which parser to call when given a list of files.

from parsers.sqliteParse import sqliteParse, sqliteInsertParse
from parsers.sqlParse import sqlParse, sqlInsertParse
from parsers.pythonParse import pythonParse
from parsers.cppParse import cppParse
from parsers.javaParse import javaParse
import os, tempfile, time

# Lists containing the files that Data Prometheus can read.
# Index 0 = The name of the parser function.
# Index 1 = The name of the insert statement parser (only for database files).
# Index 2+ = The file extensions those parsers support.
sqLiteReadable = [sqliteParse, sqliteInsertParse,  "db", "db3", "s3db", "sqlite", "sqlite3", "sqlitedb", "sl3"]
sqlParseReadable = [sqlParse, sqlInsertParse, "sql"]
pythonParseReadable = [pythonParse, None, "py"]
cppParseReadable = [cppParse, None, "cpp"]
javaReadable = [javaParse, None, "java"]

# A list containing the previous lists (for streamlining)
supportedFileTypes = [sqLiteReadable, sqlParseReadable, pythonParseReadable, javaReadable]
supportedMergeFileTypes = [sqLiteReadable, sqlParseReadable]



def parseFiles(files, operation):
    parsedText = []
    parsedInserts = []

    # Determine which file types are supported based on the current operation
    if operation == "mapDatabase":
        fileTypes = supportedFileTypes
    elif operation == "mergeDatabase":
        fileTypes = supportedMergeFileTypes

    for i, file in enumerate(files):
        # Generates a temporary file to send to the parser
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)
        extension = determineFileType(file.filename)
        parsingFunction = None

        # Chooses the appropriate parser
        for typeList in fileTypes:
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
            return 0, errorMessage

        startTime = time.time()
        print(f"Beginning parse {i+1} of {len(files)}...")

        try:
            parsedText.append(parsingFunction(temp_file, file.filename))
        except:
            errorMessage = f"There was an error parsing {file.filename}. Please make sure that the file is a valid {extension} file or that Data Prometheus is in a stable build."
            return 0, errorMessage

        # Add the insert statements (if merging)
        if operation == "mergeDatabase":
            parsedInserts.append(insertParsingFunction(temp_file))

        # Deletes the temporary file
        temp_file.close()
        os.unlink(temp_file.name)
        print(f"Parse {i+1} completed. Time Elapsed: {time.time() - startTime} seconds.\n")

    return parsedText, parsedInserts



def determineFileType(fileName):
    if "." not in fileName:
        return ""
    extension = fileName.split(".")[-1]
    return extension