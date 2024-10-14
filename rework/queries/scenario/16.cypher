// Enfants de la Database Copilot {dbId: 2}

MATCH (d:Database {name: "Copilot"})-[:CONTIENT]->(t:Table)-[:ALIMENTE*1..]->(c:Card)
RETURN t.name, t.tableId,t.schema, c.cardId, c.name, c.archived,c.creator_email, c.updated_at, t,c