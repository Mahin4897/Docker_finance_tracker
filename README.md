# Docker Finance Tracker

A Django-based finance tracker project, fully containerized with Docker and using MySQL as the database.

---

## Table of Contents

- [Docker Finance Tracker](#docker-finance-tracker)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Setup \& Run](#setup--run)
  - [Docker Commands](#docker-commands)
  - [Environment Variables](#environment-variables)
  - [Project Structure](#project-structure)
  - [Notes](#notes)

---

## Features

- Track finances and manage transactions  
- Django REST Framework APIs ready  
- MySQL database for persistent storage  
- Fully containerized with Docker  

---

## Prerequisites

- Docker  
- Docker Compose  
- Python 3.12 (for local development, optional)  

---

## Setup & Run

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Docker_finance_tracker
```

2. **Create `.env` file** in the project root:

```env
DB_NAME=financetracke
DB_USER=Mahin
DB_PASSWORD=your_password
```

3. **Build and start the Docker containers**

```bash
docker compose up --build
```

4. **Access the app**

- Django: `http://localhost:8000`  
- MySQL: accessible via container `mysql_db`  

---

## Docker Commands

- **Build images and start containers**

```bash
docker compose up --build
```

- **Run containers in detached mode**

```bash
docker compose up -d --build
```

- **Execute Django commands inside container**

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py runserver 0.0.0.0:8000
```

- **Stop containers**

```bash
docker compose down
```

---

## Environment Variables

| Variable     | Description                  |
|-------------|------------------------------|
| `DB_NAME`   | Name of MySQL database       |
| `DB_USER`   | MySQL user                   |
| `DB_PASSWORD` | Password for MySQL user    |

---

## Project Structure

```
Docker_finance_tracker/
├─ finance_tracker/         # Django project root
│  ├─ manage.py
│  ├─ core/                 # Django project settings & WSGI
│  └─ ...  
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .env
└─ README.md
```

---

## Notes

- Make sure the `manage.py` file exists at the root of your Django project (`finance_tracker/manage.py`).  
- All Django commands inside Docker should be run with `python manage.py <command>`.  
- If MySQL port `3306` is already in use, update the `docker-compose.yml` port mapping.  
