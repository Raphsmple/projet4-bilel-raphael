# Journal de bord - Cinema API

## Ressources choisies

Nous avons choisi de créer une API de gestion d'un cinéma.

Nous avons choisi 5 ressources :

* Movie
* Actor
* Room
* Session
* Ticket

Ces ressources sont liées entre elles de manière logique.

Les séances sont liées aux films et aux salles. Les billets sont liés aux séances. Les films peuvent également contenir une liste d'acteurs avec leur rôle.

## Validations

Nous avons utilisé Pydantic pour vérifier les données envoyées à l'API.

Nous avons utilisé plusieurs contraintes `Field`, notamment pour limiter la longueur des textes et les valeurs numériques.

Nous avons également utilisé deux `Enum` :

* `MovieGenre` pour les genres des films
* `SessionStatus` pour le statut des séances

Deux `field_validator` permettent de vérifier les titres des films et les noms des acteurs.

Deux `model_validator` permettent de vérifier des règles entre plusieurs champs :

* un film d'horreur doit durer au moins 60 minutes
* l'heure de fin d'une séance doit être supérieure à l'heure de début

## Difficulté rencontrée

Une difficulté a été de gérer les relations entre les ressources.

Par exemple, une séance contient un `movie_id` et un `room_id`. Il fallait vérifier que le film et la salle existaient avant de créer la séance.

Nous avons donc ajouté des vérifications avec `HTTPException` afin de retourner une erreur `404` lorsque l'identifiant lié n'existe pas.

Une autre difficulté a été de respecter le fonctionnement demandé pour les modifications. Les routes de modification utilisent `PATCH`.

## Fonctionnalités avancées

Nous avons ajouté une route permettant de rechercher et filtrer les films.

Cette route permet également de faire une pagination et de trier les résultats.

Une route `/stats` permet de calculer des statistiques à partir des données présentes dans l'API.

## Robustesse

Nous avons ajouté des erreurs `HTTPException` lorsque des ressources ou des identifiants liés n'existent pas.

Nous avons également utilisé `response_model` pour ne pas exposer certaines informations dans les réponses publiques.

Par exemple, certaines informations d'un acteur et d'un billet ne sont pas renvoyées par les routes GET correspondantes.

## Bilan

Le projet nous a permis de réutiliser les notions vues pendant les séances précédentes : FastAPI, routes REST, CRUD, Pydantic, validation, relations entre ressources et gestion des erreurs.
