// Carte/Dashboard dans aucune collection, possible ?

MATCH (c:Dashboard|Card)
where not (:Collection)-[:CONTIENT]->(c)
return labels(c), c.name, c.archived, c.updated_at, c.created_at, c order by labels(c) desc

// Les ARCHIVED peuvent simplifier l'analyse de tous ces cas