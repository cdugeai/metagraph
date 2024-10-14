// Enfants des 2 cartes 'vue_min_ch_ind_terr_2'

match (c:Card {name: "vue_min_ch_ind_terr_2"})-[:ALIMENTE*1..]->(enfant:Card)
optional match (coll:Collection)-[:CONTIENT]->(c)
optional match (coll_enfant:Collection)-[:CONTIENT]->(enfant)
set enfant:Enfant
return toInteger(c.cardId) as cardId, c.name, c.archived, c.updated_at, c.creator_email, coll.name as collection , enfant.name, coll_enfant.name as collection_enfant, enfant.archived, c, enfant, coll_enfant
