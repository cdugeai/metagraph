// Collection non archivée et vide (sans enfant)

match (collection:Collection {archived: "False"})
where not (collection)-[:CONTIENT]->()
return collection.name, collection

// TODO: Vérifier (car si uniquement sous-dossiers -> apparait vide) puis supprimer ces collections