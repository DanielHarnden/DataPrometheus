# This file contains the root function that calls all other functions in Data Prometheus.
# Each call is handled for errors, which are returned to the frontend.

from parse_Files import parseFiles
from map_Files import mapFiles
from generate_Graph_Output import generateGraphOutput
from generate_SQL_Output import generateSQLOutput
import time



def processFiles(files, operation):
    beginTime = time.perf_counter()

    # Checks for common errors
    status, errorMessage = errorCheck(files, operation)
    if status == 0:
        return 0, errorMessage

    # 1) Parse an inputted file for relevant information.
    parsedText, parsedInserts = parseFiles(files, operation)
    # Error message stored in parsedInserts (if there is an error)
    if parsedText == 0:
        return 0, parsedInserts

    # 2) Map the parsed information to itself to find relationships between "keys" and "tables."
    startTime = time.perf_counter()
    print("Beginning mapping...")
    try:
        keyList, bannedWords = mapFiles(parsedText)
    except:
        errorMessage = f"There was an error while mapping keys. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage
    print(f"Mapping completed. Time Elapsed: {time.perf_counter() - startTime} seconds.\n")

    # 3) Generate a visualization of the mapped information using GraphViz.
    startTime = time.perf_counter()
    print("Generating GraphViz PNG...")
    try:
        if operation == "mapDatabase":
            generateGraphOutput(parsedText, keyList, bannedWords)
        elif operation == "mergeDatabase":
            tempParsedText = combineFiles(parsedText)
            edgesToAdd = generateGraphOutput(tempParsedText, keyList, bannedWords)
    except:
        errorMessage = f"There was an error while generating the graph output. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
        return 0, errorMessage
    print(f"PNG generated. Time Elapsed: {time.perf_counter() - startTime} seconds.\n")

    # 3.5) Generate SQL file (if merging)
    if operation == "mergeDatabase":
        startTime = time.perf_counter()
        print("Generating SQL file...")

        try:
            generateSQLOutput(parsedText, parsedInserts, keyList, edgesToAdd)
        except:
            errorMessage = f"There was an error while generating the SQL output. Please make sure that Data Prometheus is in a stable build, or restart the program and try again."
            return 0, errorMessage

        print(f"SQL generated. Time Elapsed: {time.perf_counter() - startTime} seconds.\n")

    print(f"Total Operational Time: {time.perf_counter() - beginTime} seconds.\n")
    return 1, "Successful operation."



def errorCheck(files, operation):
    if len(files) == 1 and files[0].filename == "":
        errorMessage = f"No file(s) chosen."
        return 0, errorMessage

    if operation == "mergeDatabase" and len(files) < 2:
        errorMessage = f"Please choose two or more files to merge."
        return 0, errorMessage

    return 1, "Successful operation."

def combineFiles(parsedText):
    newParsedText = [["output.sql"]]
    for file in parsedText:
        newParsedText.extend(file[1:])

    return [newParsedText]