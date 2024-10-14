// Entité uniquement dans une collection archivée

match (collection:Collection {archived: "True"})-[:CONTIENT]->(entity:%)
return collection.name, labels(entity), collection,entity

// entity semble a chaque fois archivé donc tb