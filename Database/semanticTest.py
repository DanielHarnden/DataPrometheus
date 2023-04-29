import nltk
from nltk.corpus import wordnet
import json, os, re

def semanticTest():

    with open(os.getcwd() + "\Database\keyInformation\keyList.json") as f:
        try:
            data = json.load(f)
            dataDict = {item: data[item] for item in data}
        except:
            dataDict = {}

    temp = []
    connectedList = []

    for i in range(len(temp)):
        for j in range(i+1, len(temp)):
            if temp[i] in temp[j]:
                print(f"{temp[i]} is a word within {temp[j]}")

    
    # Compare every word in temp using nltk wordnet
    print("Wordnet analysis.")
    for i in range(len(temp)):
        for j in range(i+1, len(temp)):
            word1 = wordnet.synsets(temp[i])
            word2 = wordnet.synsets(temp[j])
            if word1 and word2:
                # Get the similarity of the first synset of each word
                similarity = word1[0].path_similarity(word2[0])
                if similarity is not None and similarity > 0.2:
                    print(temp[i], 'and', temp[j], 'are connected.')
                    connectedList.append([temp[i], temp[j]])                    




    for primaryKey, reference in connectedList:
        if primaryKey not in dataDict:
            print(f"Adding {primaryKey} as new type of entry.")
            dataDict.update({primaryKey: [primaryKey]})
        else:
            if reference not in dataDict[primaryKey]:
                addKey = dataDict[primaryKey]
                addKey.append(reference)
                dataDict.update({primaryKey: addKey})

    # Write updated data back to json file
    with open(os.getcwd() + "\Database\keyInformation\keyList.json", 'w') as f:
        json.dump(dataDict, f, indent=4, separators=(',', ': '))


    return




def cleanText(keyList):
    temp = []

    for table in keyList:
        cleanedTable = []  # create an empty list to store cleaned words
        for word in table:
            cleanedWord = re.sub(r'[^\w\s]', '', word).replace('_', '').lower()
            cleanedTable.append(cleanedWord)  # append the cleaned word to the cleaned table
        temp.append(cleanedTable)  # append the cleaned table to the main list

    return temp