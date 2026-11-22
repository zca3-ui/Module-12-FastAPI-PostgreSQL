# Module 12 – FastAPI Calculator and User API

## Project Overview

This project uses Python, FastAPI, SQLAlchemy, PostgreSQL, and Pydantic to build a calculator and user management API.

The application allows users to register and log in, and supports creating, viewing, updating, and deleting calculations. It also includes input validation, password security, automated testing, and Docker deployment.

## Technologies Used

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Pydantic
- Argon2
- Docker and Docker Compose
- Pytest
- Playwright
- GitHub Actions
- Trivy

## Application Features

**Calculator API**

Supports addition, subtraction, multiplication, and division.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/calculations/` | View all calculations |
| GET | `/calculations/{calculation_id}` | View a calculation |
| POST | `/calculations/` | Create a calculation |
| PUT | `/calculations/{calculation_id}` | Update a calculation |
| DELETE | `/calculations/{calculation_id}` | Delete a calculation |

**User API**

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register` | Register a user |
| POST | `/users/login` | Log in |
| GET | `/users/` | View all users |
| GET | `/users/{user_id}` | View a user |

Passwords are hashed using Argon2. The application also validates user and calculation data and handles errors such as duplicate registrations and division by zero.

## Running the Application

### Prerequisites

- Python 3.14
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone https://github.com/zca3-ui/Module-12-FastAPI-PostgreSQL.git
cd Module-12-FastAPI-PostgreSQL
```

### 2. Start the application

```bash
docker compose up --build -d
```

### 3. Access the application

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- pgAdmin: http://localhost:5050

## Running Automated Tests

The project includes unit, integration, and end-to-end tests.

### 1. Activate the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start PostgreSQL

```bash
docker compose up -d db
```

### 4. Initialize the development database

```bash
docker exec -i postgres_db psql -U postgres -d fastapi_db < sql/01_schema.sql
docker exec -i postgres_db psql -U postgres -d fastapi_db < sql/04_add_password_hash.sql
```

Create the SQLAlchemy tables:

```bash
python -c "from app.database.connection import Base, engine; from app.database.models import User, Calculation; Base.metadata.create_all(bind=engine)"
```

### 5. Create the API test database

```bash
docker exec postgres_db createdb -U postgres fastapi_test_db
```

The integration test fixture creates the required tables in this separate database.

### 6. Install Playwright

```bash
playwright install chromium
```

### 7. Run all tests

```bash
python -m pytest -v
```

To run individual test groups:

```bash
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/e2e/ -v
```

## CI/CD

GitHub Actions automatically runs the tests, builds the Docker image, scans it with Trivy, and pushes the image to Docker Hub when changes are pushed to the `main` branch.

## Docker Hub

[FastAPI Calculation API – Docker Hub](https://hub.docker.com/repository/docker/zca3/fastapi-calculation-api/general)

## GitHub Repository

[Module 12 – FastAPI PostgreSQL](https://github.com/zca3-ui/Module-12-FastAPI-PostgreSQL)
