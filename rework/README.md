Pour lancer la db, et le script Python de création des fichiers CSV:
```sh
docker compose up 
```

Ou directement via une instruction Docker (conteneur db: `metagraph-neo4j`):
```sh
docker exec --interactive --tty metagraph-neo4j neo4j-admin database import full neo4j --overwrite-destination --nodes=/root/out/tables.csv --nodes=/root/out/databases.csv --nodes=/root/out/collections.csv --nodes=/root/out/cards_content.csv --relationships=/root/out/card_relation_table.csv --relationships=/root/out/card_relation_card.csv --relationships=/root/out/table_relation_db.csv --relationships=/root/out/card_relation_collection.csv
docker container restart metagraph-neo4j
# Ou en exécutant cette commande dans le conteneur de la db (puis redémarrer le conteneur)
neo4j-admin database import full neo4j --overwrite-destination --nodes=/root/out/tables.csv --nodes=/root/out/databases.csv --nodes=/root/out/cards_content.csv --nodes=/root/out/collections.csv --relationships=/root/out/card_relation_table.csv --relationships=/root/out/card_relation_card.csv --relationships=/root/out/table_relation_db.csv --relationships=/root/out/card_relation_collection.csv
```

Si besoin de relancer uniquement le script Python de création des fichiers CSV:
```sh
docker compose run --rm metagraph 
```
