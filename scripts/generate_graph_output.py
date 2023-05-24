"""
This module is used to generate the GraphViz DOT and PNG files.
It manually creates each table and key using string concatenation,
then sends the table and key lists to other files to determine the edges between nodes
(which differs depending on if the file is a database or a programming file).
"""


from datetime import datetime
from graphviz import Digraph
from determine_edge import database_determine_edge, prog_determine_edge


def generate_graph_output(parsed_text, key_list, banned_words):
    """
    Goes through the process of creating tables and keys,
    then sends the necessary information to the appropriate edge finding modules.
    """

    dot = Digraph()

    # Moves file names from parsedText to fileNames, sorts tables from biggest to smallest
    parsed_text, file_names = initialize_graph_generation(parsed_text, [])
    primary_keys = {}
    table_names = []
    nodes = []

    # Loops through each file...
    for i, file in enumerate(parsed_text):

        # ...stores all table names and primary keys while adding each table to GraphViz...
        file_primary_keys, new_tables, file_table_names = add_tables (
            file, primary_keys, [], []
        )
        table_names += file_table_names
        primary_keys.update(file_primary_keys)

        # ...then adds each key to the new tables
        nodes, dot = add_keys(
            file, key_list, new_tables, file_table_names,
            file_names[i], nodes, dot
        )

    # Searches for relationships between keys
    edges_to_add = []
    edges_to_add = find_foreign_keys(parsed_text, table_names, file_names, key_list, banned_words)

    # Adds the found relationships as edges on the graph
    dot, edges_to_add = generate_edges_dot(edges_to_add, nodes, dot)

    # Does some settings to make it look pwetty uwu
    graph_creation_time = datetime.now()
    graph_creation_time = graph_creation_time.strftime("%m/%d/%Y %I:%M %p")
    dot.graph_attr.update({
        'bgcolor': '#FFDAB9',
        'table': 'style=invis',
        'label': f'Parsed by Data Prometheus at {graph_creation_time}',
        'labelloc': 't',
        'rankdir': 'LR',
        'ranksep': '1.5',
        'nodesep': '0.5',
        'sep': '10',
        'dpi': '200'
    })

    # Renders the graph as a PNG to the output folder
    dot.render('./output/output', format='png')
    return edges_to_add


def initialize_graph_generation(parsed_text, file_names):
    """
    Cleans the parsed text and organizes the tables.
    """

    for file_iterator, file in enumerate(parsed_text):
        file_name = file[0][0]
        file_names.append(file_name)

        # Removes file name from parsed text, sorts from biggest to smallest if database
        if not is_programming_file(file_name):
            file = sorted(file[1:], key=len, reverse=True)
        else:
            file = file[1:]

        parsed_text[file_iterator] = file

    return parsed_text, file_names


def is_programming_file(file_name):
    """
    Determines if the inputted file name is py, java, or cpp (true)
    """

    supported_programming_extensions = ["py", "java", "cpp"]
    extension = file_name.split(".")[-1]
    return extension in supported_programming_extensions


def add_tables(file, primary_keys, new_tables, table_names):
    """
    Parses the inputted information for the relevant table information,
    then sends it to be converted to DOT format. 
    """

    for i, table_list in enumerate(file):
        new_tables.append(
            '''<\n\n\n\n<table border="1" cellborder="1" cellspacing="0" color="#932525">''')

        table_name = table_list[0][0]
        # Determines if this table has a class
        if "." in table_name:
            # Adds initializer as className
            if table_name.split(".")[0] not in table_names:
                table_names.append(table_name.split(".")[0])
                table_descriptor = "Class " + \
                    table_name.split(".")[0] + " Initializer"
            else:
                table_names.append(table_name.split(".")[1])
                table_descriptor = "Class " + table_name.split(".")[0]
        else:
            table_names.append(table_name)
            table_descriptor = " "

        new_tables[i] += generate_table_dot(table_names[i], table_descriptor)
        primary_keys[table_names[i]] = table_names[i]

    return primary_keys, new_tables, table_names


def generate_table_dot(table_name, table_number):
    """
    Converts an inputted table name and number to valid DOT format.
    """

    return f'''
  <tr>
    <td colspan='2' bgcolor='#932525' port="{table_name}.start" align='left'><font color="#FFFFEB"><b><i>{table_name}</i></b></font></td>
    <td bgcolor='#932525' align='right' port="{table_name}.end" ><font color="#FFFFEB"><b><i>{table_number}</i></b></font></td>
  </tr>
    '''


def add_keys(file, key_list, new_tables, table_names, file_name, nodes, dot):
    """
    Parses the inputted information for the relevant key information,
    then sends it to be converted to DOT format. 
    """

    # Iterates through all of the tables from the original txt of the inputted database
    for table_iterator, table_list in enumerate(file):
        added_keys = set()

        for i, key in enumerate(table_list):
            key_name = key[0]
            key_type = key[1]

            if i == 0:
                nodes.append(f"{table_names[table_iterator]}:{split_class_and_key(key_name)}")
                continue

            # Determines if they key has to be renamed based on the mapping
            for key_synonym in key_list:
                if key_name in key_list[key_synonym]:
                    key_name = key_synonym

            if key_name not in added_keys and "Built-In" not in key_type:
                new_tables[table_iterator] += generate_key_dot(key_name, key_type)
                nodes.append(f"{table_names[table_iterator]}:{split_class_and_key(key_name)}")
                added_keys.add(key_name)

        # Finishes the table then adds the node using the temporary information
        new_tables[table_iterator] += "</table>\n>"

    # Adds each file as a subgraph
    with dot.subgraph(name=f'Cluster-{file_name}') as sub_dot:
        sub_dot.attr(label=file_name, color='#FFA07A',
                    bgcolor='#FFC6A5', style='solid')

        for table_iterator, table_list in enumerate(file):
            sub_dot.node(table_names[table_iterator],
                        shape='none', label=new_tables[table_iterator])

    return nodes, dot

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


def generate_key_dot(key_name, key_type):
    """
    Converts an inputted key name and type to valid DOT format.
    """

    return f'''
  <tr>
    <td colspan='2' bgcolor='#C43131' port="{key_name}.start" align='left'><font color="#FFFFEB"><b><i>{key_name}</i></b></font></td>
    <td bgcolor='#C43131' port="{key_name}.end" align='right'><font color="#FFFFEB">{key_type}</font></td>
  </tr>
    '''


def find_foreign_keys(parsed_text, table_names, file_names, key_list, banned_words):
    """
    Sends the necessary information to the appropriate edge finding modules.
    """

    edges_to_add = set()
    # TODO: Make this dependent on parse_Files.py
    for file_name in file_names:

        if is_programming_file(file_name):
            new_edges = prog_determine_edge(parsed_text)
            edges_to_add.update(new_edges)
        else:
            new_edges = database_determine_edge(parsed_text, key_list, table_names, banned_words)
            edges_to_add.update(new_edges)

    return edges_to_add


def generate_edges_dot(edges_to_add, nodes, dot):
    """
    Adds each found edge to the graph as a digraph edge.
    Returns edges_to_add for the SQL file generater (if merging)
    """

    # A list of line colors to differentiate edges
    line_colors = ["#22052D", "#361941", "#4B2C54", "#5F4068", "#73547B", "#88678F", "#9C7BA2"]
    i = 0

    for start_table, start_key, end_table, end_key in edges_to_add.copy():
        i = i % len(line_colors)
        if (
            start_table != end_table and
            f"{start_table}:{start_key}" in nodes and
            f"{end_table}:{end_key}" in nodes
        ):
            dot.edge(
                # .end means the right side of the table (it is referencing another table)
                f"{start_table}:{start_key}.end",
                # .start means the left side of the table (it is being referenced)
                f"{end_table}:{end_key}.start",
                arrowhead='normal', arrowtail='odot', dir='both',
                style='solid', color=line_colors[i], penwidth='2.5'
            )
            i += 1
        else:
            print(f"Head node {end_table}:{end_key} does not exist. "
                  f"Skipping edge {start_table}:{start_key} -> {end_table}:{end_key}")
            edges_to_add.remove((start_table, start_key, end_table, end_key))

    return dot, edges_to_add
