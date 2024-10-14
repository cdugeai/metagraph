// Cartes créées par d’autres utilisateurs que Gaelle et Laurène

match (p:%) where not p.creator_email=~ 'laurene.*|gaelle.*' 
return p.cardId, p.name, p.creator_email, p.archived, 'https://copilot-metabase.osc-secnum-fr1.scalingo.io/question/'+p.cardId as url

// vérifier l'utilité, supprimer si inutile