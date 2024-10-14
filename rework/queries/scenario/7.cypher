// Carte sur aucun dashboard, et qui n’est pas dans le dossier 7 (collectionId:33)

MATCH (c:Card)
where not (:Dashboard)-[:CONTIENT]->(c) 
OPTIONAL MATCH (coll:Collection)-[:CONTIENT]->(c)
match (c:Card) where coll.collectionId is null or coll.collectionId<>'33'
return coll.name as collection, coll.archived, c.cardId, c.name, c.archived, c.updated_at, c.creator_email
//return c.name, c.archived, c.updated_at, c.creator_email
order by coll.name

// Ces cartes semblent inutiles. Les supprimer