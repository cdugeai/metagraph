// Retourne les tables ayant le pus d'enfants directs

MATCH (t:Table)-[r:ALIMENTE]->(cible:%) 
WITH t, count(cible) as nchild where nchild>1
RETURN t.schema, t.name,nchild 
ORDER BY nchild DESC
LIMIT 25
