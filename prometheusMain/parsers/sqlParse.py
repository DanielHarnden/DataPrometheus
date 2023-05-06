import re

def sqlParse(file, originalFileName):

    cleanedTables = [[originalFileName]]
    sqlInsertStyles = [r"`(.*?)`", r"\[(.*?)\]"]

    with open(file.name, 'r') as f:
        sqlText = f.read()


    cleanedText = sqlText.split("\n")
    cleanedText = [line for line in cleanedText if "--" not in line]
    insertInto = [line for line in cleanedText if "INSERT INTO" in line]

    # Finding keys using INSERT INTO is far more convenient so it's checked first
    if insertInto:
        for line in insertInto:
            results = []
            for style in sqlInsertStyles:
                results += re.findall(style, line)
            cleanedTables.append(results)

    else:
        
        temporaryTables = []
        temporaryLine = []

        # Finds each table using some basic logic
        for line in cleanedText:
            inTable = False

            if not inTable:
                if ";" in line:
                    inTable = False
                    temporaryTables.append(temporaryLine)
                    temporaryLine = []
                else:
                    temporaryLine.append(line)
            else:
                if "TABLE" in line:
                    inTable = True
                    temporaryLine.append(line)

        # Cleans the results from each table
        for table in temporaryTables:
            results = []
            
            for line in table:
                line = re.sub(r'[^a-zA-Z0-9\s]', '', line)
                
                if "TABLE" in line:
                    print(line.split()[-1])
                    results.append(line.split()[-1])
                else:
                    if line != "":
                        print(line.strip().split()[0])
                        results.append(line.strip().split()[0])

            cleanedTables.append(results)



    return cleanedTables