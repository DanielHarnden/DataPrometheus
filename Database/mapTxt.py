import nltk, os
from nltk.corpus import gutenberg
from spellchecker import SpellChecker
import json
from functools import lru_cache

commonIdentifiers = ["Key", "Id"]

def mapTxt(inputKeys):
    # Load or generate NLTK information from cache
    words = get_gutenberg_words()
    freq_dist = get_freq_dist() 
    spell = SpellChecker()

    # Load existing key and banned word data
    with open(os.getcwd() + "\Database\keyInformation\keyList.json") as f:
        try:
            data = json.load(f)
            dataDict = {item: data[item] for item in data}
        except:
            dataDict = {}
    with open(os.getcwd() + "\Database\keyInformation\\bannedWords.txt") as f:
        try:
            bannedWords = [word.strip() for word in f.readlines()]
        except:
            bannedWords = []

    # Add new keys to dataDict
    for item in inputKeys:
        # TODO: This function is kinda slow 
        for key in item:
            if key not in dataDict:
                # Uses some common identifiers to determine whether a key should be replaced or not
                for identifier in commonIdentifiers:
                    if identifier in key:
                        tempKey = key
                    else:
                        tempKey = spell.correction(key)

                # Determine if key is already in database before attempting processing
                if key not in dataDict and (tempKey is not None and tempKey not in dataDict):
                    useNewKey = False

                    if key != item[0]:
                        # Determines if there is a similar word that can be used
                        if spell.unknown(key):
                            freq = freq_dist[tempKey]
                            print(f'\n\nThe word "{tempKey}" appears {freq} times in the Gutenberg Corpus.')

                            if freq > 2 and tempKey != key:
                                print(f'That meets the threshold. Replacing old key {key} with {tempKey}')
                                useNewKey = True
                            else:
                                print(f'Retaining old key: {key}')

                        # If there is a similar word, add both the original and new key as a reference to the new key
                        if useNewKey:
                            addKey(tempKey, key, dataDict)
                        else:
                            addKey(key, None, dataDict)

    # Write updated data back to json and banned word files
    with open(os.getcwd() + "\Database\keyInformation\keyList.json", 'w') as f:
        json.dump(dataDict, f, indent=4, separators=(',', ': '))
    with open(os.getcwd() + "\Database\keyInformation\\bannedWords.txt", 'w') as bw:
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



@lru_cache(maxsize=None)
def get_gutenberg_words():
    return gutenberg.words()

@lru_cache(maxsize=None)
def get_freq_dist():
    return nltk.FreqDist(get_gutenberg_words())