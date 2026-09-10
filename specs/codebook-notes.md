# Colonnes du dataset ACLED — explication rapide

Basé sur le codebook ACLED, appliqué aux colonnes présentes dans nos fichiers US et Sahel.

| Colonne | Explication |
|---|---|
| `event_id_cnty` | Identifiant unique de l'événement (préfixe pays, ex. USA, NIR, BFO, MLI) |
| `event_date` | Date de l'événement (ou date estimée si imprécision) |
| `year` | Année de l'événement |
| `time_precision` | Fiabilité de la date : 1 = date exacte connue, 2 = fenêtre de quelques jours, 3 = fenêtre large (mois) |
| `disorder_type` | Catégorie macro : Political violence / Demonstrations / Strategic developments |
| `event_type` | Type d'événement (6 possibles) : Battles, Explosions/Remote violence, Violence against civilians, Protests, Riots, Strategic developments |
| `sub_event_type` | Sous-type précis (25 possibles), ex. "Peaceful protest", "Mob violence", "Armed clash", "Air/drone strike" |
| `actor1` | Acteur principal de l'événement (celui qui initie/est à l'origine) |
| `assoc_actor_1` | Acteur(s) associé(s) à actor1 (soutien, allié) |
| `inter1` | Catégorie d'actor1 : ex. State forces, Rebel group, Political militia, Protesters, Civilians, Rioters |
| `actor2` | Second acteur impliqué (cible ou adversaire), vide si aucun (ex. protestation pacifique sans opposant) |
| `assoc_actor_2` | Acteur(s) associé(s) à actor2 |
| `inter2` | Catégorie d'actor2 |
| `interaction` | Résumé textuel du type d'interaction entre actor1 et actor2 (ex. "State forces-Rebel group") |
| `civilian_targeting` | Rempli si des civils ont été délibérément visés ("Civilian targeting"), sinon vide |
| `iso` | Code pays numérique ISO (ex. 840 = USA) |
| `region` | Grande région ACLED (ex. "North America") — peu discriminant pour nos analyses US |
| `country` | Pays |
| `admin1` | Niveau administratif 1 = État (US) / région (Sahel) |
| `admin2` | Niveau administratif 2 = comté (US) / département ou cercle (Sahel) |
| `admin3` | Niveau administratif 3, plus fin, souvent vide |
| `location` | Nom de la localité précise de l'événement |
| `latitude` / `longitude` | Coordonnées géographiques du point codé |
| `geo_precision` | Fiabilité de la localisation : 1 = lieu exact, 2 = zone proche, 3 = zone large (ex. région) |
| `source` | Média ou source ayant rapporté l'événement |
| `source_scale` | Portée de la source : Local, Subnational, National, International, New media, etc. |
| `notes` | Description textuelle libre de l'événement — c'est là qu'on a extrait le sous-thème "data center" et les motifs (eau, électricité...), car ces infos ne sont pas dans des colonnes structurées |
| `fatalities` | Nombre de morts rapportés pour cet événement |
| `tags` | Attributs additionnels séparés par `;` : crowd size (taille de foule), counter-demonstration, armed, Repression, etc. — pas de thème topique dedans |
| `timestamp` | Horodatage Unix de dernière mise à jour de la ligne dans la base ACLED (pas la date de l'événement) |

## Spécificité du fichier Sahel "actor-based"

`ACLED_Sahel_actor-based_...csv` a le même événement dupliqué en plusieurs lignes (une ligne par acteur impliqué), sans colonnes `actor2`/`assoc_actor_2`/`inter2` : chaque ligne ne documente qu'un seul acteur (`actor1`/`inter1`) pour un même `event_id_cnty`. Utile si on veut compter/filtrer par acteur (ex. tous les événements impliquant JNIM) sans avoir à gérer les deux côtés actor1/actor2 en même temps.
