import nltk, os
from nltk.corpus import gutenberg
from spellchecker import SpellChecker
import json

def mapTxt(inputKeys):
    # Load existing key and banned word data
    with open(os.getcwd() + "\Database\keyInformation\keyList.json") as f:
        try:
            data = json.load(f)
            dataDict = {item: data[item] for item in data}
        except:
            dataDict = {}
    
    with open(os.getcwd() + "\Database\keyInformation\\bannedWords.txt") as bw:
        try:
            bannedWords = [word.strip() for word in bw.readlines()]
        except:
            bannedWords = []

    spell = SpellChecker()
    words = gutenberg.words()
    freq_dist = nltk.FreqDist(words)

    # Add new keys to dataDict
    for item in inputKeys:
        for key in item:

            tempKey = spell.correction(key)
            # Determine if key is already in database before processing
            if key not in dataDict and (tempKey is not None and tempKey not in dataDict):
                newKey = None
                useNewKey = False

                if key != item[0]:
                    # Determines if there is a similar word that can be used
                    if spell.unknown(key):
                        if tempKey is not None:
                            newKey = tempKey
                            freq = freq_dist[newKey]
                            print(f'\n\nThe word "{newKey}" appears {freq} times in the Gutenberg Corpus.')

                            if freq > 2 and newKey != key:
                                print(f'That meets the threshold. Replacing old key {key} with {newKey}')
                                useNewKey = True
                            else:
                                print(f'Retaining old key: {key}')

                    # If there is a similar word, add both the original and new key as a reference to the new key
                    if useNewKey:
                        if newKey not in dataDict:
                            print(f"Adding {newKey} as new type of entry.")
                            dataDict.update({newKey: [newKey]})

                            addKey = dataDict[newKey]
                            addKey.append(key)
                        else:
                            if newKey not in dataDict[newKey]:
                                addKey = dataDict[newKey]
                                addKey.append(key)
                                addKey.append(newKey)
                                dataDict.update({key: addKey})
                    # If there is not a similar word, only add the original key
                    else:
                        if key not in dataDict:
                            print(f"Adding {key} as new type of entry.")
                            dataDict.update({key: [key]})
                        else:
                            if key not in dataDict[key]:
                                addKey = dataDict[key]
                                addKey.append(key)
                                addKey.append(newKey)
                                dataDict.update({key: addKey})


#if key not in bannedWords:
#print(f'{key} is common, adding {key} as banned word.')
#bannedWords.append(key)

                    

    # Write updated data back to json file
    with open(os.getcwd() + "\Database\keyInformation\keyList.json", 'w') as f:
        json.dump(dataDict, f, indent=4, separators=(',', ': '))

    with open(os.getcwd() + "\Database\keyInformation\\bannedWords.txt", 'w') as bw:
        for item in bannedWords:
            bw.write(item + "\n")

    # Return the json file for the grapher
    with open(os.getcwd() + "\Database\keyInformation\keyList.json") as f:
        return json.load(f), bannedWords