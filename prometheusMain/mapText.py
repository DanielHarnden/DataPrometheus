import nltk, os
from nltk.corpus import gutenberg
from spellchecker import SpellChecker
import json
from functools import lru_cache

commonIdentifiers = ["Key", "Id"]

def mapText(inputKeys):
    # Load or generate NLTK information from cache
    freqDist = getFreqDist() 
    spell = SpellChecker()

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

    # Only get unique keys (minus table names)
    inputKeys = list(set(item for sublist in inputKeys for item in sublist[1:]))

    # Add new keys to dataDict
    for key in inputKeys:
        # Does an entire song and dance to determine if there are any spell checks that can be made
        tempKey = None
        # Identifiers like "key" or "id" are technically incorrect, but we still want them
        for identifier in commonIdentifiers:
            if identifier in key:
                tempKey = key
                break
        # If there are no identifiers, replace with corrected word
        if tempKey is None:
            tempKey = spell.correction(key)
            # Word may not always have a correction. In that case, default to original key
            if tempKey is None:
                tempKey = key

        # Checks if the new key exists before attempting any of the complex stuff
        if tempKey not in dataDict and tempKey not in dataDict.values():
            useNewKey = False
            inFreqDist = False

            # Checks to see if the key exists in the Gutenberg Corpus. If it does, it is assumed that the key is a good replacement.
            if tempKey in freqDist:
                inFreqDist = True
                print(f'\nThe word "{tempKey}" appears in the Gutenberg Corpus at least once.')

                if tempKey != key:
                    print(f'Replacing old key {key} with {tempKey}')
                    useNewKey = True
            else:
                print(f'\nThe word "{tempKey}" does not appear in the Gutenberg Corpus.')
                print(f'Retaining old key: {key}')
                
            if useNewKey:
                dataDict = addKey(tempKey, key, dataDict)
            else:
                dataDict = addKey(key, None, dataDict)

    # Write updated data back to json and banned word files
    with open(os.getcwd() + "\prometheusMain\keyInformation\keyList.json", 'w') as f:
        json.dump(dataDict, f, indent=4, separators=(',', ': '))
    with open(os.getcwd() + "\prometheusMain\keyInformation\\bannedWords.txt", 'w') as bw:
        for item in bannedWords: 
            bw.write(item + "\n")

    # Return the json file for the grapher
    return dataDict, bannedWords



def addKey(key, keyTwo, dataDict):
    if key not in dataDict:
        print(f"Adding {key} as new type of entry.")
        dataDict.update({key: [key]})

        if keyTwo is not None:
            addKey = dataDict[key]
            addKey.append(keyTwo)
    else:
        addKey = dataDict[key]
        addKey.append(key)
        addKey.append(keyTwo)
        dataDict.update({key: addKey})

    return dataDict



@lru_cache(maxsize=None)
def getFreqDist():
    return nltk.FreqDist(gutenberg.words())