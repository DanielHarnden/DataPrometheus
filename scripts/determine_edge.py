"""
This module has functions for determining edges between nodes in
database and programming files.
"""


from snowballstemmer import stemmer


def database_determine_edge(parsed_text, key_list, table_names, banned_words):
    """
    Prepares the given information to be sent to database_find_edges.
    """
    primary_keys = {}
    tables_visited = {}
    edges_to_add = set()

    # Iterates through each key
    for file in parsed_text:
        for table_columns in file:
            table_name = table_names[len(tables_visited)]
            tables_visited[table_name] = []

            # Stores the key name
            for column in table_columns:
                current_key = column[0]

                # Converts each key to its "root" key based on the keyInformation.json dictionary
                for key_synonym, synonyms in key_list.items():
                    if current_key in synonyms:
                        current_key = key_synonym

                edges_to_add, tables_visited, primary_keys = database_find_edges(
                    current_key, primary_keys, table_name, table_names,
                    tables_visited, edges_to_add, banned_words
                )

    return edges_to_add


def database_find_edges(
        current_key, primary_keys, table_name, table_names,
        tables_visited, edges_to_add, banned_words
):
    """
    Finds the edges between nodes in database files, which is much more difficult 
    than in programming files, and liberties are taken to accurately determine edges.
    """

    snowball_stemmer = stemmer('english')

    # Does some logic using the current key / table and the referencing key / table
    # to try and accurately determine which order the keys reference each other
    if current_key in primary_keys and table_name != primary_keys[current_key]:
        if (
            primary_keys[current_key] not in tables_visited[table_name] and
            current_key not in banned_words
        ):
            referenced_table = primary_keys[current_key]
            cleanedtable_name = table_name.replace("_", "")
            table_stem = snowball_stemmer.stemWord(cleanedtable_name).lower()

            if current_key in table_names:
                if table_stem in current_key.lower():
                    temp_edge = (referenced_table, current_key, table_name, table_name)
                else:
                    temp_edge = (table_name, current_key, referenced_table, referenced_table)
            else:
                if table_stem in current_key.lower():
                    temp_edge = (referenced_table, current_key, table_name, current_key)
                else:
                    temp_edge = (table_name, current_key, referenced_table, current_key)

            edges_to_add.add(temp_edge)
            tables_visited[table_name].append(primary_keys[current_key])
    else:
        primary_keys[current_key] = table_name

    return edges_to_add, tables_visited, primary_keys


def prog_determine_edge(parsed_text):
    """
    This function finds the edges between nodes in programming files
    (which are more rigid and therefore easier to find edges in compared to database files).
    """
    function_calls = set()

    # Recursive function
    def traverse_functions(parsed_data, current_function):
        for key in parsed_data:
            if isinstance(key, list):
                # Determines if the key is a function call
                if len(key) > 1 and key[1] == 'FUNCTION CALL':
                    called_table = split_class_and_key(key[0])
                    current_function_name = split_class_and_key(current_function[0])
                    call = (current_function_name, called_table, called_table, called_table)
                    function_calls.add(call)
                else:
                    # Recursively traverse nested lists
                    nested_data = key
                    nested_current_function = key[0]
                    traverse_functions(nested_data, nested_current_function)
            elif isinstance(key, str):
                # Update the current function name
                current_function = key

    current_function = ['']
    traverse_functions(parsed_text, current_function)

    return function_calls

def split_class_and_key(key):
    """
    Removes the class from the current ky
    """

    remove_class = key.split(".")

    # Determines the class and key names
    if len(remove_class) == 1:
        return key

    current_class = remove_class[0]
    current_key = remove_class[1]

    # Replaces __init__ with class name
    # TODO: Make this language independent (only works with Python right now)
    if "__init__" in current_key or "main" in current_key:
        current_key = current_class

    return current_key
    