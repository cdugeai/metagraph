from sql_metadata.compat import get_query_tables
import pandas as pd
import aiohttp
import asyncio
import tqdm

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



async def async_get_dashboard(mb_, executor_, dashboard_id_):
    sync_get_dashboard = lambda dashboard_id: mb_.get("/api/dashboard/"+str(dashboard_id))
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor_, sync_get_dashboard, dashboard_id_)


async def async_get_dashboards_relations(mb_, executor_, dashboard_ids):
    card_relation_dashboard=[]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for dashboard_id_ in tqdm.tqdm(dashboard_ids, desc="Start dashboard requests"):
            # Start API requests
            tasks.append(async_get_dashboard(mb_, executor_, dashboard_id_))

        for completed in tqdm.tqdm(asyncio.as_completed(tasks), total=len(dashboard_ids), desc="Export dashboard cards relations"):
            dashboard_json = await completed
            if (dashboard_json==False):
                # error API response when querying Dashboard endpoint
                # print("problem avec un dashboard")
                pass
            else:
                dashboard_id = dashboard_json['id']
                cards_child_list_raw = [x['card_id'] for x in dashboard_json['dashcards']]
                cards_child_list = pd.Series(cards_child_list_raw).dropna().astype(int).unique().astype(str).tolist()
                # Build relation file: card_relation_dashboard
                for card_id in cards_child_list:
                    card_relation_dashboard.append({
                        ":START_ID(Dashboard-ID)": dashboard_id,
                        "some_property": "empty",
                        ":END_ID(Card-ID)": card_id,
                        ":TYPE": "CONTIENT"            
                    })
        # await all tasks again (may not be necessary)
        await asyncio.gather(*tasks, return_exceptions=True)
        return card_relation_dashboard
