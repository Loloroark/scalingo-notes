# scalingo-notes

Mini-appli de notes : client React (Vite) + API FastAPI + PostgreSQL, déployée sur Scalingo.

## Architecture

Navigateur → App 1 (client React, buildpack Node.js) → App 2 (API FastAPI, buildpack Python) → addon PostgreSQL Starter 512.
Monorepo : `client/` et `api/`, chaque app Scalingo pointe vers son dossier via `PROJECT_DIR`.

## Lancer en local

```bash
docker compose up -d
cd api && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
alembic upgrade head
python seed.py
uvicorn app.main:app --reload
# autre terminal
cd client && cp .env.example .env && npm install && npm run dev
```

## Déploiement

```bash
# API
scalingo create <app-api>
scalingo --app <app-api> env-set PROJECT_DIR=api CORS_ORIGINS=https://<url-client>
scalingo --app <app-api> addons-add postgresql postgresql-starter-512
git push scalingo main        # ou Auto Deploy GitHub
scalingo --app <app-api> run python seed.py

# Client
scalingo create <app-client>
scalingo --app <app-client> env-set PROJECT_DIR=client VITE_API_URL=https://<url-api>
```

Ordre : API d'abord, puis client (`VITE_API_URL` est figée au build), puis mettre l'URL du client dans `CORS_ORIGINS`.

## Variables d'environnement

| App | Variable | Rôle |
|---|---|---|
| API | `SCALINGO_POSTGRESQL_URL` | URL de la base (fournie par l'addon) |
| API | `CORS_ORIGINS` | URL(s) du client, séparées par des virgules |
| API | `PROJECT_DIR` | `api` |
| Client | `VITE_API_URL` | URL publique de l'API |
| Client | `PROJECT_DIR` | `client` |

## Coût mensuel

- Estimé : _à remplir (simulateur Scalingo)_
- Réel : _à remplir (Billing)_

## En cas de panne

_À compléter avec les commandes réellement testées :_

```bash
scalingo --app <app-api> logs --lines 200
scalingo --app <app-api> deployments
scalingo --app <app-api> deployment-rollback   # à tester
scalingo --app <app-api> backups               # sauvegarde / restauration à tester
```
