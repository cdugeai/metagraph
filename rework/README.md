Pour lancer la db, et le script Python de création des fichiers CSV:
```sh
docker compose up 
```

Ou directement via une instruction Docker (conteneur db: `metagraph-neo4j`):
```sh
docker exec --interactive --tty metagraph-neo4j neo4j-admin database import full neo4j --overwrite-destination --nodes=/root/out/nodes/tables.csv --nodes=/root/out/nodes/databases.csv --nodes=/root/out/nodes/dashboard.csv --nodes=/root/out/nodes/collections.csv --nodes=/root/out/nodes/cards_content.csv --relationships=/root/out/relations/card_relation_table.csv --relationships=/root/out/relations/dashboard_relation_collection.csv --relationships=/root/out/relations/card_relation_card.csv --relationships=/root/out/relations/table_relation_db.csv --relationships=/root/out/relations/card_relation_collection.csv
docker container restart metagraph-neo4j
# Ou en exécutant cette commande dans le conteneur de la db (puis redémarrer le conteneur)
neo4j-admin database import full neo4j --overwrite-destination --nodes=/root/out/nodes/tables.csv --nodes=/root/out/nodes/databases.csv --nodes=/root/out/nodes/cards_content.csv  --nodes=/root/out/nodes/dashboards.csv --nodes=/root/out/nodes/collections.csv --relationships=/root/out/nodes/card_relation_table.csv --relationships=/root/out/relations/dashboard_relation_collection.csv --relationships=/root/out/relations/card_relation_card.csv --relationships=/root/out/relations/table_relation_db.csv --relationships=/root/out/relations/card_relation_collection.csv
```

Si besoin de relancer uniquement le script Python de création des fichiers CSV:
```sh
docker compose run --rm metagraph 
```

## Fonctionnement

Lorsque la question est en SQL uniquement, on parse ce sql via `sql-metadata.get_query_tables()` pour obtenir les tables parentes. On obtient schema+table. On fait une jointure avec les CSV des Table sur ce même nom+schema et on en récupère l'ID. Avec celui-ci, on créé une nouvelle relation entre la question SQL et les tables sources.

## TODOS

- ajouter Dashboard
- parsing du SQL pour établir les relations de ces cartes
