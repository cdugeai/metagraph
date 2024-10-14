// Noms de cartes en doublon


match (c:Card) 
with c.name as cardname,  count(*) as cnt where count(*)>1
return cardname, cnt 