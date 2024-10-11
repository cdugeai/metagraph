// Tableaux de bord qui contiennent au moins une carte qui a comme parent une carte archivée

MATCH (d:Dashboard )-[:CONTIENT]->(c:Card)<-[:ALIMENTE]-(c_a:Card {archived: "True"}) 
SET c_a:CardArchived
RETURN d,c,c_a LIMIT 250