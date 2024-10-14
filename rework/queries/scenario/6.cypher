// Carte avec 1 seul enfant

MATCH (parent:Card)-[:ALIMENTE]->(enfant:Card)
with parent, count(enfant) as n_enfants
where count(enfant)=1
OPTIONAL MATCH (coll:Collection)-[:CONTIENT]->(parent)
return coll.name, coll.archived as coll_archived, parent.name, parent.archived as card_archived, parent.updated_at, parent.creator_email, n_enfants

// Voir au cas par cas
// Supprimer les coll perso des comptes de test
