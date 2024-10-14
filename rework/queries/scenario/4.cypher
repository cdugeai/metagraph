// Collection archivée et vide (sans enfant)

match (collection:Collection {archived: "True"})
where not (collection)-[:CONTIENT]->()
return collection.name, collection

// TODO: supprimer ces collections