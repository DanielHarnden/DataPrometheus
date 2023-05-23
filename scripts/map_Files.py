"""
This module is used to map the parsed text upon itself.
Eventually an AI will be used to determine if there are 
relationships between new and existing keys, creating a 
network of keys that can be used to find relationships 
between keys when graphing.
"""


from os import getcwd
from json import load, dump


def map_files(input_keys):
    """
    Maps the keys against each other.
    Takes in a list of key names and checks them against each other
    in an attempt to find relationships between them.
    """

    try:
        with open(
            f"{getcwd()}\\scripts\\keyInformation\\keyList.json",
            encoding="utf-8"
        ) as key_list_file:
            try:
                data = load(key_list_file)
                data_dict = {item: data[item] for item in data}
            except Exception as exception:
                print(exception)
                data_dict = {}
    except FileNotFoundError as exception:
        print(exception)
        data_dict = {}

    try:
        with open(
            f"{getcwd()}\\scripts\\keyInformation\\bannedWords.txt",
            encoding="utf-8"
        ) as banned_words_file:
            try:
                banned_words = [word.strip() for word in banned_words_file.readlines()]
            except Exception as exception:
                print(exception)
                banned_words = []
    except FileNotFoundError as exception:
        print(exception)
        banned_words = []

    for file_tables in input_keys:
        # Only get unique keys (minus table names)
        file_tables = list(set(tuple(item) for sublist in file_tables for item in sublist[1:]))

        # Add new keys to dataDict
        for key in file_tables:

            # Checks if the new key exists before attempting any of the complex stuff
            if key[0] not in data_dict and key[0] not in data_dict.values():
                data_dict = add_key(key[0], None, data_dict)

            if "Built-In" in key[1] and key[0] not in banned_words:
                banned_words.append(key[0])

        # Write updated data back to json and banned word files
        with open(
            f"{getcwd()}\\scripts\\keyInformation\\keyList.json",
            'w', encoding="utf-8"
        ) as key_list_file:
            dump(data_dict, key_list_file, indent=4, separators=(',', ': '))

        with open(
            f"{getcwd()}\\scripts\\keyInformation\\bannedWords.txt",
            'w', encoding="utf-8"
        ) as banned_words_file:
            for item in banned_words:
                banned_words_file.write(item + "\n")

    # Return the json file for the grapher
    return data_dict, banned_words


def add_key(primary_key, key_synonym, data_dict):
    """
    Adds the primary key and key synonym to the data dictionary.
    If the primary key does not exist, it is added as a new
    primary key and as a synonym of itself.
    If the primary key does exist, the key synonym is added as a 
    synonym of the primary key.
    """

    if primary_key not in data_dict:
        print(f"Adding {primary_key} as new type of entry.")
        data_dict.update({primary_key: [primary_key]})

        if key_synonym is not None:
            print(f"Adding {key_synonym} as a synonym of {primary_key}.")
            append_key = data_dict[primary_key]
            append_key.append(key_synonym)
    else:
        print(f"Adding {key_synonym} as a synonym of {primary_key}.")
        append_key = data_dict[primary_key]
        append_key.append(primary_key)
        append_key.append(key_synonym)
        data_dict.update({primary_key: append_key})

    return data_dict
