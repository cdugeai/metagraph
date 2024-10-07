import asyncio
from concurrent.futures import ThreadPoolExecutor
from metabase_api import Metabase_API
import pandas as pd
import re
import os
from utils import async_get_dashboards_relations, get_source_table_ids
import tqdm

url=os.environ.get('MB_URL', '')
mb = Metabase_API(url, api_key=os.environ.get('MB_API_KEY', ''))

print('Databases...')
databases = mb.get("/api/database/")['data']
# with open("out/databases.json", 'w') as f: f.write(json.dumps(databases))
pd.DataFrame([
    {
        "dbId:ID(Database-ID)": x['id'],
        ":LABEL": "Database",
        "name": x['name'],
        "description": x['description'],
        "updated_at": x['updated_at'],
        "created_at": x['created_at']
    } for x in databases
]).to_csv("out/nodes/databases.csv", index=False)


print('Dashboards...')
dashboard = mb.get("/api/dashboard/")+mb.get("/api/dashboard?f=archived")
# with open("out/dashboard.json", 'w') as f: f.write(json.dumps(dashboard))
pd.DataFrame([
    {
        "dashboardId:ID(Dashboard-ID)": x['id'],
        ":LABEL": "Dashboard",
        "name": x['name'],
        # "description": x['description'],
        "updated_at": x['updated_at'],
        "created_at": x['created_at'],
        "archived": x['archived'],
        "collection_id": x['collection_id'],
        "creator_id": x['creator_id']
    } for x in dashboard
]).to_csv("out/nodes/dashboard.csv", index=False)


# Relation Dashboard -1-n-> cards
card_relation_dashboard = asyncio.run(async_get_dashboards_relations(mb, ThreadPoolExecutor(2), [x['id'] for x in dashboard]))
pd.DataFrame(card_relation_dashboard).to_csv('out/relations/card_relation_dashboard.csv', index=False)

# Add relation Collection->Dashboard if collection-id exists
pd.DataFrame([
    {
        ":START_ID(Collection-ID)": x['collection_id'],
        "some_property": "empty",
        ":END_ID(Dashboard-ID)": x['id'],
        ":TYPE": "CONTIENT"     
    } for x in dashboard if x['collection_id'] is not None
]).to_csv("out/relations/dashboard_relation_collection.csv", index=False)

print('Collections...')
collections = mb.get("/api/collection/") + mb.get("/api/collection?archived=true")
pd.DataFrame([
    {
        "collectionId:ID(Collection-ID)": str(x['id']),
        ":LABEL": "Collection",
        "slug": x.get('slug',None),
        "name": x['name'],
        "archived": x.get('archived',False), # Default Collection has no "archived" property. So we set to False.
        "location": x.get('location',None),
        "created_at": x.get('created_at',None)
    } for x in collections
]).to_csv("out/nodes/collections.csv", index=False)
# with open("out/collections.json", 'w') as f: f.write(json.dumps(collections))

print('Tables...')
tables = mb.get("/api/table/")
tables_df = pd.DataFrame([
    {
        "tableId:ID(Table-ID)": x['id'],
        ":LABEL": "Table",
        "db_id": x['db_id'],
        "entity_type": x['entity_type'],
        "schema": x['schema'],
        "name": x['name'],
        "updated_at": x['updated_at'],
        "display_name": x['display_name'],
        "created_at": x['created_at']
    } for x in tables
])
tables_df.to_csv("out/nodes/tables.csv", index=False)
pd.DataFrame([
    {
        ":START_ID(Database-ID)": x['db_id'],
        "some_property": "empty",
        ":END_ID(Table-ID)": x['id'],
        ":TYPE": "CONTIENT"
    } for x in tables
]).to_csv("out/relations/table_relation_db.csv", index=False)

print('Cards...')
cards_content=[]
card_relation_card=[]
card_relation_table=[]
card_relation_collection=[]
# Archived and non archived cards
cards=mb.get("/api/card/")+mb.get("/api/card?f=archived")
for card_i in tqdm.tqdm(cards):
    card_id=str(card_i['id'])
    # print('Handling card',card_id)

    x=card_i

    source_table=""
    joins=""
    sql_query=None
    if x['dataset_query']['type']=='query':
        if 'source-query' in x['dataset_query']['query']:
            source_table = x['dataset_query']['query']['source-query']['source-table']
            joins = "|".join([str(z["source-table"]) for z in x['dataset_query']['query']['source-query'].get('joins', [])])
        else:
            source_table = x['dataset_query']['query']['source-table']
            joins = "|".join([str(z["source-table"]) for z in x['dataset_query']['query'].get('joins', [])])
    elif x['dataset_query']['type']=='native':
        sql_query = x['dataset_query']['native']['query']
        source_table=get_source_table_ids(sql_query, card_id, tables_df)

    card_collection=str((x['collection'] or {'id': "-1"})['id'])
    cards_content.append(
        {
            "cardId:ID(Card-ID)": card_id,
            ":LABEL": "Card",
            "collection_id": card_collection,
            # "description": x['description'],
            "archived": x['archived'],
            "table_id": x['table_id'],
            "creator_email": x['creator']['email'],
            "database_id": x['database_id'],
            "collection_id": x['collection_id'],
            "query_type": x['query_type'],
            "name": x['name'],
            # "last_query_start": x['last_query_start'],
            "type": x['type'],
            "updated_at": x['updated_at'],
            "dataset_query_type": x['dataset_query']['type'],
            # "sql_query": sql_query,
            "source_table": source_table,
            "joins": joins
        }
    )

    # If the Card has a linked collection
    if card_collection!="-1":
        card_relation_collection.append({
                ":START_ID(Collection-ID)": card_collection,
                "some_property": "empty",
                ":END_ID(Card-ID)": card_id,
                ":TYPE": "CONTIENT"            
        })

    parents_tables_or_cards='|'.join([str(source_table), joins]).split('|')
    parents_tables_or_cards_not_empty=filter(lambda x: len(x)>0, parents_tables_or_cards)
    for parent_element in parents_tables_or_cards_not_empty:
        if parent_element.startswith("card__"):
            parent_card_id=re.findall(r'card__(\d+)', parent_element)[0]
            card_relation_card.append({
                ":START_ID(Card-ID)": parent_card_id, 
                "some_property": "empty", 
                ":END_ID(Card-ID)": card_id,
                ":TYPE": "ALIMENTE"
                })
        else:
            parent_table_id=parent_element
            card_relation_table.append({
                ":START_ID(Table-ID)": parent_table_id, 
                "some_property": "empty", 
                ":END_ID(Card-ID)": card_id,
                ":TYPE": "ALIMENTE"
            })

pd.DataFrame(cards_content).to_csv("out/nodes/cards_content.csv", index=False)
pd.DataFrame(card_relation_card).to_csv("out/relations/card_relation_card.csv", index=False)
pd.DataFrame(card_relation_table).to_csv("out/relations/card_relation_table.csv", index=False)
pd.DataFrame(card_relation_collection).to_csv("out/relations/card_relation_collection.csv", index=False)
print("Done !")
