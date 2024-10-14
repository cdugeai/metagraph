// Carte archivée sans enfant

MATCH (parent:Card {archived:"True"}) 
where not (parent)-[:ALIMENTE]->(:Card) 
OPTIONAL MATCH (coll:Collection)-[:CONTIENT]->(parent) 
RETURN coll.name, parent.cardId, parent.name, parent.archived,parent.updated_at, parent.creator_email
order by coll.name asc, parent.updated_at asc

// TODO: supprimer à la main dans metabase.com/archive
