# Docker Finance Tracker

A Django-based finance tracker application fully containerized with **Docker**, using **PostgreSQL** as the database and **pgAdmin** for database management.

---

## Table of Contents

* [Docker Finance Tracker](#docker-finance-tracker)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Quick Start](#quick-start)
* [Environment Variables](#environment-variables)
* [Docker Commands](#docker-commands)
* [Services & Ports](#services--ports)
* [Project Structure](#project-structure)
* [Notes](#notes)

---

## Features

* Django + Django REST Framework
* PostgreSQL database (Dockerized)
* pgAdmin for database inspection
* Docker Compose–based setup
* Ready for development & production workflows

---

## Prerequisites

Make sure you have the following installed:

* Docker
* Docker Compose (v2+)
* Git

(Optional for local development without Docker)

* Python 3.12+

---

## Quick Start

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd Docker_finance_tracker
```

### 2️⃣ Create `.env` file (required)

Create a `.env` file in the project root:

```env
DEBUG=1
SECRET_KEY="django-insecure-change-me"

POSTGRES_DB=finance_tracker
POSTGRES_USER=finance_user
POSTGRES_PASSWORD=finance_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

> ⚠️ **Important**: The `SECRET_KEY` must be quoted if it contains `$` characters.

---

### 3️⃣ Build and start containers

```bash
docker compose up --build
```

---

### 4️⃣ Access the application

* **Django app** → [http://localhost:8000](http://localhost:8000)
* **pgAdmin** → [http://localhost:5050](http://localhost:5050)

  * Email: 
  * Password: 

---

## Environment Variables

| Variable            | Description                           |
| ------------------- | ------------------------------------- |
| `DEBUG`             | Enable Django debug mode (`1` or `0`) |
| `SECRET_KEY`        | Django secret key                     |
| `POSTGRES_DB`       |              |
| `POSTGRES_USER`     | PostgreSQL user                       |
| `POSTGRES_PASSWORD` |                  |
| `POSTGRES_HOST`     | Database host (use `db` for Docker)   |
| `POSTGRES_PORT`     | PostgreSQL port (`5432`)              |

---

## Docker Commands

### Build & run containers

```bash
docker compose up --build
```

### Run in detached mode

```bash
docker compose up -d --build
```

### Stop containers

```bash
docker compose down
```

### Remove containers and volumes (⚠️ deletes DB data)

```bash
docker compose down -v
```

### Run Django commands inside container

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic
```

---

## Services & Ports

| Service   | Description         | Port              |
| --------- | ------------------- | ----------------- |
| `web`     | Django application  | `8000`            |
| `db`      | PostgreSQL database | `5432` (internal) |
| `pgadmin` | PostgreSQL admin UI | `5050`            |

---

## Project Structure

```text
Docker_finance_tracker/
├─ finance_tracker/          # Django project root
│  ├─ manage.py
│  ├─ finance_tracker/       # settings, urls, wsgi, asgi
│  ├─ apps/                  # Django apps
│  └─ ...
├─ docker-compose.yml
├─ Dockerfile
├─ requirements.txt
├─ .env
└─ README.md
```

---

## Notes

* Django runs inside Docker using `runserver` (development mode).
* PostgreSQL data is persisted using Docker volumes.
* pgAdmin connects to PostgreSQL using host `db` (not `localhost`).
* Static files must be collected for DRF Browsable API styling in production.
* For production, consider adding:

  * Gunicorn
  * Nginx
  * Celery + Redis

---

🚀 **You’re now ready to develop with Docker + Django + PostgreSQL!**
