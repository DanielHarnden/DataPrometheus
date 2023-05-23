def generate_sql_output(parsed_text, parsed_inserts, key_list, edges_to_add):
    """
    Generates a single SQL file based on the parsed text.
    """

    all_sql_tables = ""
    table_column_dict = {}

    # Add each table with keys
    for file in parsed_text:
        for table in file[1:]:
            table_name = table[0][0]
            keys = table[1:]
            key_statements = []
            added_keys = set()

            # Append each key and key type
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

            # Keys for each table are stored in a dictionary
            key_names = ", ".join([key_name for key_name, key_type in keys])
            table_column_dict[table_name] = key_names

            # Add foreign key relationships
            for start_table, start_key, end_table, end_key in edges_to_add:
                start_table = start_table.replace("[table]", "").strip()

                if table_name == start_table:
                    start_key = start_key.replace("[table]", "").strip()
                    end_table = end_table.replace("[table]", "").strip()
                    end_key = end_key.replace("[table]", "").strip()

                    statement = f"\tFOREIGN KEY ({start_key}) REFERENCES {end_table}({end_key})"
                    key_statements.append(statement)

            # Finalize table statement and append to all_sql_tables string
            joined_statements = ",\n".join(key_statements)
            sql_table = f"CREATE TABLE IF NOT EXISTS {table_name} (\n{joined_statements}\n);\n\n"
            all_sql_tables += (sql_table)

    # Add insert statements (if they exist)
    all_inserts = ""
    # Remove outermost []
    for outermost_brackets in parsed_inserts:
        for row in outermost_brackets:
            insert_statements = []
            table_name = row[0]

            # Cleans and adds each key to a list
            for key in row[1:]:
                if key is None:
                    insert_statements.append("NULL")
                elif isinstance(key, str):
                    key = key.replace("'", "''")
                    insert_statements.append(f"'{key}'")
                else:
                    insert_statements.append(str(key))

            # Turns the list into a single string separated by commas
            joined_inserts = ", ".join(insert_statements)

            try:
                new_statement = (
                    f"INSERT INTO {table_name} "
                    f"({table_column_dict[table_name]}) "
                    f"VALUES ({joined_inserts});\n"
                )
            except Exception as exception:
                print(exception)
                table_name = table_name.replace("_", "")

            # Adds everything to a single string, then adds that to the string of inserts
            new_statement = (
                f"INSERT INTO {table_name} "
                f"({table_column_dict[table_name]}) "
                f"VALUES ({joined_inserts});\n"
            )
            all_inserts += (new_statement)

    # Writes tables and inserts to sql file
    with open("output/output.sql", "w", encoding="utf-8") as file:
        file.write(all_sql_tables)
        file.write(all_inserts)
