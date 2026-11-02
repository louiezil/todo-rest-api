# Task Manager API

A REST API for managing personal tasks, lists, and tags.

## Tech Stack
- Python
- Flask
- SQLite
- JWT Authentication

## Setup
1. Install: `pip install -r requirements.txt`
2. Run: `python app.py`

## Authentication
All endpoints (except register/login) require a JWT token.
Send token as: `Authorization: Bearer <token>`

## Endpoints

### Auth
- `POST /api/auth/register` → Create account
- `POST /api/auth/login` → Get token

### Users
- `GET /api/users/me` → Get current user

### Tasks
- `POST /api/tasks` → Create task
- `GET /api/tasks` → List all
- `GET /api/tasks/<id>` → Get one
- `PUT /api/tasks/<id>` → Update
- `DELETE /api/tasks/<id>` → Delete

### Lists
- (same 5 endpoints)

### Tags
- (same 5 endpoints)