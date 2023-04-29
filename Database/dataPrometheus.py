import os, tempfile
import json
from generateGraph import generateGraph

# Import the various parsers from the parsers folder
from parsers.sqlite3Parse import sqlite3Parse

# Lists containing the files that Data Prometheus can read. The first item is the name of the  function that will be called and the following items are the extensions that that function supports
#TODO: Determine all file types supported by sqlite3
sqLiteReadable = [sqlite3Parse, "db", "sqlite", "db3"]

# A list containing the previous lists, for streamlining later
supportedFileTypes = [sqLiteReadable]



# Maps a single database
def mapDatabase(fileName, file, reversing):
    # Sets the function to None type and determines the extension of the inputted file
    function = None
    extension = determineFileType(fileName)

    # Goes through the list of supported files. If the extension is supported, the function is marked
    for typeList in supportedFileTypes:
        if extension in typeList:
            function = typeList[0]

    # If the file type is supported...
    if function is not None:
        #... a temporary file is generated to store the database
        #TODO: Determine a better way of doing this. From what I understand about sending files through APIs, there's no way to read the file directly and instead it has to be saved locally (duplicated) which could be bad for huge files
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        # The file is sent to its designated parser
        parsedText = function(temp_file)

        # The temporary file is deleted
        temp_file.close()
        os.unlink(temp_file.name)
    else:
        print("That file type is not yet supported by Data Prometheus.")
        return 0

    keyList = mapTxt(parsedText)

    

    generateGraph(parsedText, keyList, fileName.split(".")[0], reversing)

    



# Determines the file's type
def determineFileType(fileName):
    if "." not in fileName:
        return ""
    extension = fileName.split(".")[-1]
    return extension


















def mapTxt(inputKeys):
    # Load existing data from database file
    with open(os.getcwd() + "\Database\keyList.json") as f:
        try:
            data = json.load(f)
            dataDict = {item: data[item] for item in data}
        except:
            dataDict = {}

    # Add new keys to dataDict
    for item in inputKeys:
        tableName = True
        for key in item:
            if tableName:
                tableName = False
                continue
            
            if key not in dataDict:
                print(f"Adding {key} as new type of entry.")
                dataDict.update({key: [key]})
            else:
                if key not in dataDict[key]:
                    addKey = dataDict[key]
                    addKey.append(key)
                    dataDict.update({key: addKey})

    # Write updated data back to json file
    with open(os.getcwd() + "\Database\keyList.json", 'w') as f:
        json.dump(dataDict, f, indent=4, separators=(',', ': '))
    
    # Return the json file for the grapher
    with open(os.getcwd() + "\Database\keyList.json") as f:
        return json.load(f)