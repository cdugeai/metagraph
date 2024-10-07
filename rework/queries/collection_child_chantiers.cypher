// Les collections qui utilisent le plus la table metadata_chantiers

MATCH (t:Table {name:"metadata_chantiers"})-[]->(enfant_direct:Card)<-[:CONTIENT]-(coll:Collection) 
WITH t.name as table_name, coll.name as collection_name, count(enfant_direct) as n_cards_child
return table_name, collection_name, n_cards_child
order by n_cards_child desc
limit 10