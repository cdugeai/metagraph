from sql_metadata.compat import get_query_tables
import pandas as pd

def parse_source_tables(sql_statement, card_id):
    """Return tables found in sql_statement

    Args:
        sql_statement (str): Query to inspect
        card_id (str): ID of card (for debug purpose)

    Returns:
        dict[]: Format [{table_schema, table_name, is_parent_of_card}]
    """
    source_tables = get_query_tables(sql_statement)
    return [{
        "table_schema": t.split('.')[0],
        "table_name": t.split('.')[1] if len(t.split('.'))>1 else None,
        "is_parent_of_card": card_id
    } for t in source_tables]




def get_source_table_ids(sql_query, card_id, tables_df):
    """Get source tables IDs of this sql query

    Args:
        sql_query (str): Query to inspect
        card_id (str): ID of card (for debug purpose)
        tables_df (_type_): Df of tables. Used to join the schema+name of sql table in sql_query to find the id of table

    Returns:
        str: Table ids, format 'id1|id2|id3'
    """

    MSG_NO_PARENT_FOUND="[err] Pas de parent trouvé pour "+card_id

    parsed_df=pd.DataFrame(parse_source_tables((sql_query or ""), card_id))

    source_table=""
    if parsed_df.empty: 
        print(MSG_NO_PARENT_FOUND)
    else:
        parsed_df_joined = pd.merge(parsed_df,tables_df, left_on=['table_schema','table_name'], right_on=['schema','name'], how='left', suffixes=('_x', '_y'))[['table_schema','table_name', 'is_parent_of_card', 'tableId:ID(Table-ID)']]
        # on garde les ID des tables trouvées, puis on les formate avec '|'
        source_table='|'.join(parsed_df_joined['tableId:ID(Table-ID)'].dropna().unique().astype(int).astype(str).tolist())
    
    return source_table
