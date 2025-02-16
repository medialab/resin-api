# resin-api

API et back-office pour [le site de Résin](https://github.com/medialab/resin-annuaire).

## Développement

Ce projet utilise [Poetry](https://python-poetry.org/) pour gérer ses dépendances.

Pour installer les dépendances, et lancer le serveur, exécutez la commande suivante :

```bash
poetry install

# lancer les migrations de la base de données
poetry run python manage.py migrate
# créer un superutilisateur
poetry run python manage.py createsuperuser

# lancer le serveur de développement
poetry run python manage.py runserver
```

## Installation en production

Ceci est une application [Django](https://www.djangoproject.com/). Elle peut être déployée
[comme n'importe quelle application Django](https://docs.djangoproject.com/fr/5.0/howto/deployment/), avec
un serveur comme Nginx ou Apache, qui servira les fichiers statiques, et passera le reste des requêtes à
l'application Django, via Gunicorn ou uWSGI.

En résumé :
- Le serveur exposé publiquement doit servir /uploads/* et /static/* depuis
  respectivement les dossiers /app/uploads et /app/static du conteneur Django
- Le serveur doit rediriger toutes les autres requêtes vers le conteneur Django

Le Dockerfile fourni permet de construire une image Docker pour l'application Django,
qui peut être déployée sur n'importe quelle plateforme qui supporte Docker.  Le fichier
docker-compose.yml fourni est un exemple de configuration pour déployer l'application.

## Configuration

L'application utilise les variables d'environnement suivantes pour sa configuration :
* `RESIN_DEBUG`: doit être `False` en production
* `RESIN_SECRET`: une chaîne de caractères aléatoire, utilisée pour chiffrer les cookies
* `RESIN_HOST`: le nom de domaine de l'application

Ces variables sont décrites dans `.env.example`.

Le moyen le plus simple de configurer ces variables d'environnement est de les définir dans un fichier
`.env` à la racine du projet, qui sera copié dans le conteneur Docker lors du build.

## Mises à jour des listes de choix

Les listes de languages et de compétences disponibles au choix des utilisateurs
sont versionnées dans des fichiers JSON ou dans les fichiers de modèles.

Pour mettre à jour ces listes, il suffit de modifier les fichiers correspondants.
Nouveaux choix disponibles seront automatiquement pris en compte lors de la prochaine
mise à jour de la base de données.

À noter que les listes de choix précédemment enregistrées dans la base de données
ne seront pas supprimées, même si elles ne sont plus disponibles dans les fichiers
de modèles, afin de ne pas perdre de données utilisateurs.
Il est possible de les supprimer manuellement depuis l'interface d'administration.