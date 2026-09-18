# Cinema API

## Présentation

Cinema API est une API REST développée avec FastAPI.

Elle permet de gérer les films d'un cinéma, les acteurs, les salles, les séances et les billets.

Les données sont stockées dans des listes Python. Aucune base de données n'est utilisée dans ce projet.

## Ressources

L'API possède 5 ressources principales :

* **Movies** : les films disponibles.
* **Actors** : les acteurs.
* **Rooms** : les salles de cinéma.
* **Sessions** : les séances de projection.
* **Tickets** : les billets vendus.

## Relations

Plusieurs relations existent entre les ressources :

* Un film peut avoir plusieurs acteurs grâce à la liste `cast`.
* Une séance est liée à un film grâce à `movie_id`.
* Une séance est liée à une salle grâce à `room_id`.
* Un billet est lié à une séance grâce à `session_id`.

## Fonctionnalités

L'API propose :

* création de ressources avec `POST`
* consultation avec `GET`
* modification avec `PATCH`
* suppression avec `DELETE`
* validation des données avec Pydantic
* recherche de films
* filtrage par genre
* pagination
* tri par titre ou durée
* statistiques
* gestion des erreurs avec `HTTPException`
* modèles de réponse permettant de cacher certaines informations

## Validations

Plusieurs contraintes sont utilisées avec Pydantic :

* longueur minimale et maximale des textes
* valeurs numériques minimales et maximales
* genres de films avec un `Enum`
* statuts des séances avec un `Enum`
* validation personnalisée des titres et des noms
* vérification de la durée des films d'horreur
* vérification des heures de début et de fin d'une séance

## Installation

Créer un environnement virtuel :

```bash
python3 -m venv venv
```

Activer l'environnement :

```bash
source venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement

Lancer l'API avec :

```bash
uvicorn main:app --reload
```

L'API est alors disponible sur :

```text
http://127.0.0.1:8000
```

La documentation interactive est disponible sur :

```text
http://127.0.0.1:8000/docs
```

## Recherche

Exemple :

```text
GET /search/movies?title=inter
```

Filtrer par genre :

```text
GET /search/movies?genre=science-fiction
```

Pagination :

```text
GET /search/movies?page=1&limit=10
```

Tri :

```text
GET /search/movies?sort_by=duration
```

## Statistiques

La route :

```text
GET /stats
```

calcule notamment :

* le nombre de films
* le nombre d'acteurs
* le nombre de salles
* le nombre de séances
* le nombre de billets
* le chiffre d'affaires total

## Documentation interactive

FastAPI génère automatiquement une documentation Swagger accessible depuis `/docs`.

Toutes les routes peuvent être testées directement depuis cette interface.
