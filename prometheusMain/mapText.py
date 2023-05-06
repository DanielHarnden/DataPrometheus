import os
import json
from functools import lru_cache

commonIdentifiers = ["Key", "Id"]

def mapText(inputKeys):

    # Load existing key and banned word data
    with open(os.getcwd() + "\prometheusMain\keyInformation\keyList.json") as f:
        try:
            data = json.load(f)
            dataDict = {item: data[item] for item in data}
        except:
            dataDict = {}
    with open(os.getcwd() + "\prometheusMain\keyInformation\\bannedWords.txt") as f:
        try:
            bannedWords = [word.strip() for word in f.readlines()]
        except:
            bannedWords = []


    for fileTables in inputKeys:
        # Only get unique keys (minus table names)
        fileTables = list(set(tuple(item) for sublist in fileTables for item in sublist[1:]))

        # Add new keys to dataDict
        for key in fileTables:

            # Checks if the new key exists before attempting any of the complex stuff
            if key[0] not in dataDict and key[0] not in dataDict.values():
                dataDict = addKey(key[0], None, dataDict)

            if "Built-In" in key[1] and key[0] not in bannedWords:
                bannedWords.append(key[0])

        # Write updated data back to json and banned word files
        with open(os.getcwd() + "\prometheusMain\keyInformation\keyList.json", 'w') as f:
            json.dump(dataDict, f, indent=4, separators=(',', ': '))
        with open(os.getcwd() + "\prometheusMain\keyInformation\\bannedWords.txt", 'w') as bw:
            for item in bannedWords: 
                bw.write(item + "\n")

    # Return the json file for the grapher
    return dataDict, bannedWords



def addKey(primaryKey, keySynonym, dataDict):
    if primaryKey not in dataDict:
        print(f"Adding {primaryKey} as new type of entry.")
        dataDict.update({primaryKey: [primaryKey]})

        if keySynonym is not None:
            print(f"Adding {keySynonym} as a synonym of {primaryKey}.")
            appendKey = dataDict[primaryKey]
            appendKey.append(keySynonym)
    else:
        print(f"Adding {keySynonym} as a synonym of {primaryKey}.")
        appendKey = dataDict[primaryKey]
        appendKey.append(primaryKey)
        appendKey.append(keySynonym)
        dataDict.update({primaryKey: appendKey})

    return dataDict