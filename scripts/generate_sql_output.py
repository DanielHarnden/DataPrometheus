"""
This module manually generates an SQL file based on the information provided by
Data Prometheus's parsers and graph generation function.
"""


def generate_sql_output(parsed_text, parsed_inserts, key_list, edges_to_add):
    """
    Generates a single SQL file based on the parsed text.
    """

    all_sql_tables = ""
    all_inserts = ""
    table_column_dict = {}

    for file in parsed_text:
        for table in file[1:]:
            table_name = table[0][0]
            keys = table[1:]

            key_statements = process_keys(keys, key_list)
            key_statements = process_foreign_keys(table_name, key_statements, edges_to_add)
            table_column_dict[table_name] = ", ".join([key_name for key_name, key_type in keys])

            joined_statements = ",\n".join(key_statements)
            all_sql_tables += (
                f"CREATE TABLE IF NOT EXISTS {table_name} (\n{joined_statements}\n);\n\n"
            )

    for outermost_brackets in parsed_inserts:
        for row in outermost_brackets:
            table_name = row[0]
            all_inserts += process_inserts(table_name, row, table_column_dict)

    with open("output/output.sql", "w", encoding="utf-8") as file:
        file.write(all_sql_tables)
        file.write(all_inserts)


def process_keys(keys, key_list):
    """
    Adds each key and key type to the key_statements variable
    """

    added_keys = set()
    key_statements = []

    for key in keys:
        key_name = key[0]
        key_type = key[1]

        for key_synonym in key_list:
            if key_name in key_list[key_synonym]:
                key_name = key_synonym

        if key_name not in added_keys:
            statement = f"\t{key_name} {key_type}"
            key_statements.append(statement)
            added_keys.add(key_name)

    return key_statements


def process_foreign_keys(table_name, key_statements, edges_to_add):
    """
    Determines the foreign key relationships for each table using
    information from edges_to_add.
    """

    for start_table, start_key, end_table, end_key in edges_to_add:
        start_table = start_table.replace("[table]", "").strip()

        if table_name == start_table:
            start_key = start_key.replace("[table]", "").strip()
            end_table = end_table.replace("[table]", "").strip()
            end_key = end_key.replace("[table]", "").strip()

            statement = f"\tFOREIGN KEY ({start_key}) REFERENCES {end_table}({end_key})"
            key_statements.append(statement)

    return key_statements


def process_inserts(table_name, row, table_column_dict):
    """
    Generates the insert statements for each table.
    """

    insert_statements = []

    for key in row[1:]:
        if key is None:
            insert_statements.append("NULL")
        elif isinstance(key, str):
            key = key.replace("'", "''")
            insert_statements.append(f"'{key}'")
        else:
            insert_statements.append(str(key))

    joined_inserts = ", ".join(insert_statements)

    try:
        table_columns = table_column_dict[table_name]
    except KeyError:
        table_name = table_name.replace("_", "")
        table_columns = table_column_dict[table_name]

    new_statement = f"INSERT INTO {table_name} ({table_columns}) VALUES ({joined_inserts});\n"
    return new_statement