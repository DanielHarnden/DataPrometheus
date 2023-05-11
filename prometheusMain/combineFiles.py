def combineFiles(parsedText):

    newParsedText = [["output.sql"]]

    for file in parsedText:
        newParsedText += file[1:]

    newParsedText = [newParsedText]

    generateSQL(newParsedText)

    return newParsedText

def generateSQL(parsedText):
    print("alrihght")