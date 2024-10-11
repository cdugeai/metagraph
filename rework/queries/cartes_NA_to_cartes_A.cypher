// Liste des cartes archivées (A) qui ont pour enfant des cartes non archivées (NA) 

MATCH (n:Card {archived: "True"})-[:ALIMENTE]->(c2:Card {archived:"False"})<-[:CONTIENT]-(coll:Collection) 
SET n:CardArchived
RETURN n,c2,coll LIMIT 250