// Carte archivée avec enfant(s) archivés


MATCH (parent:Card {archived:"True"})-[:ALIMENTE]->(enfant:Card {archived: "False"}) 
OPTIONAL MATCH (coll:Collection)-[:CONTIENT]->(parent) 
set enfant:ChildCard, parent:ParentCard
RETURN coll.name, parent.cardId, parent.name, parent.archived,parent.updated_at, parent.creator_email, enfant.name, enfant.archived, parent, enfant
order by coll.name asc, parent.updated_at asc

// TODO: Vérifier pourquoi les cartes archivées ont des enfants, puis supprimer si possible.

