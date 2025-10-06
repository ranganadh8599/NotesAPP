# Notes API - FastAPI Backend

A RESTful API for managing notes with user authentication, built with FastAPI and MySQL.

## Overview

This is the backend service for a notes-taking application, providing secure user authentication and full CRUD operations for notes management.

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: MySQL 8.0
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: Bcrypt
- **Server**: Uvicorn
- **Containerization**: Docker & Docker Compose

## Project Structure

```
backend/
├── main.py                 # FastAPI entrypoint, initializes app, CORS, lifespan, routers
├── config.py               # Centralized settings management (env & static options)
├── models.py               # Pydantic models for users, notes, tokens
├── database/
│   └── connection.py       # DB connection class
├── dependencies.py         # Dependency injection (service/repo initializers, auth resolvers)
├── repositories/
│   ├── user_repository.py
│   └── note_repository.py
├── routers/
│   ├── auth.py             # Auth, signup/signin/user info
│   ├── health.py
│   └── notes.py
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   └── note_service.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example            # Env settings template
├── performace/
│   ├── performance_test.py
│   ├── generate_report.py
│   └── PERFORMANCE_TESTING_GUIDE.md
├── test_api.py (if present)  # Integration tests
├── DOCKER_SETUP.md
└── README.md
```

## Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop installed and running

**Steps:**

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **Verify it's running**
   ```bash
   curl http://localhost:8000/health
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

For detailed Docker instructions, see DOCKER_SETUP.md

### Option 2: Local Development

**Prerequisites:**
- Python 3.11+
- MySQL 8.0 running locally

**Steps:**

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Health Check
- `GET /` - API status
- `GET /health` - Detailed health check with database status

### Authentication
- `POST /auth/signup` - Register new user
  ```json
  {
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "password": "securepassword"
  }
  ```

- `POST /auth/signin` - Login and get JWT token
  ```json
  {
    "user_email": "john@example.com",
    "password": "securepassword"
  }
  ```

- `GET /auth/me` - Get current user info (requires authentication)

### Notes Management
All notes endpoints require authentication via `Authorization: Bearer <token>` header.

- `POST /notes` - Create a new note
  ```json
  {
    "note_title": "My Note",
    "note_content": "Note content here"
  }
  ```

- `GET /notes` - Get all user's notes
- `GET /notes/{note_id}` - Get specific note by ID
- `PUT /notes/{note_id}` - Update note
  ```json
  {
    "note_title": "Updated Title",
    "note_content": "Updated content"
  }
  ```

- `DELETE /notes/{note_id}` - Delete note

## Database Schema

### USER Table
| Column | Type | Constraints |
|--------|------|-------------|
| user_id | VARCHAR(36) | PRIMARY KEY (UUID) |
| user_name | VARCHAR(255) | NOT NULL |
| user_email | VARCHAR(255) | UNIQUE, NOT NULL |
| password | VARCHAR(255) | NOT NULL (Hashed) |
| created_on | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| last_update | DATETIME | ON UPDATE CURRENT_TIMESTAMP |

### NOTES Table
| Column | Type | Constraints |
|--------|------|-------------|
| note_id | VARCHAR(36) | PRIMARY KEY (UUID) |
| note_title | VARCHAR(255) | NOT NULL |
| note_content | TEXT | NOT NULL |
| user_id | VARCHAR(36) | FOREIGN KEY → USER(user_id) |
| created_on | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| last_update | DATETIME | ON UPDATE CURRENT_TIMESTAMP |

## Authentication Flow

1. User registers via `/auth/signup` (password is hashed with bcrypt)
2. User logs in via `/auth/signin` (receives JWT token)
3. Client includes token in `Authorization: Bearer <token>` header
4. Server validates token and extracts user information
5. User can access protected endpoints

**Token Details:**
- Algorithm: HS256
- Expiration: 30 minutes
- Payload: user_id, user_email

### Performance Tests

Run comprehensive performance benchmarks:
```bash
python performance_test.py
```

Generate HTML/Markdown reports:
```bash
python generate_report.py performance_results_<timestamp>.json
```

For detailed performance testing guide, see PERFORMANCE_TESTING_GUIDE.md

## Docker Configuration

### Services

**MySQL Database:**
- Image: mysql:8.0
- Port: 3307 (external) → 3306 (internal)
- Volume: mysql_data (persistent storage)
- Health checks enabled

**Backend API:**
- Built from Dockerfile
- Port: 8000
- Depends on MySQL (waits for healthy status)
- Auto-restarts on failure

### Environment Variables

Configured in `docker-compose.yml`:
- `DB_HOST`: mysql
- `DB_PORT`: 3306
- `DB_USER`: notesuser
- `DB_PASSWORD`: notespass
- `DB_NAME`: notes_db
- `SECRET_KEY`: JWT signing key
- `ALGORITHM`: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30

For production, move these to a `.env` file.

## Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Authentication**: Secure token-based auth
- **SQL Injection Prevention**: Parameterized queries
- **CORS Configuration**: Restricted origins
- **Input Validation**: Pydantic models
- **Error Handling**: No sensitive data in error messages

## Performance

Based on performance testing (650 total requests):

- **Success Rate**: 100%
- **Average Response Time**: 54.24ms
- **Health Endpoint**: 10.36ms avg, 95.29 req/s
- **User Signin**: 14.50ms avg, 68.27 req/s
- **Notes Creation**: 21.81ms avg, 45.56 req/s
- **Notes Read**: 17.13ms avg, 57.94 req/s
- **Concurrent Requests**: 78.37 req/s (20 threads)

See performance reports in `performance_results_*.html` for detailed metrics.

## Code Quality

- **Type Hints**: Used throughout for clarity
- **Error Handling**: Proper HTTP status codes
- **Validation**: Pydantic models for request/response
- **Clean Code**: Clear variable names, no verbose comments
- **Security**: Best practices for authentication and data handling
- **Documentation**: Comprehensive inline and external docs

## Development

### Adding New Endpoints

1. Define Pydantic models in `models.py`
2. Add route handler in `main.py`
3. Use `get_current_user` dependency for protected routes
4. Return appropriate HTTP status codes
5. Update API documentation

### Database Migrations

Currently using direct SQL for table creation. For production:
1. Consider using Alembic for migrations
2. Version control schema changes
3. Test migrations in staging environment

## Troubleshooting

### Docker Issues

**Port already in use:**
```bash
# Change MySQL port in docker-compose.yml
ports:
  - "3308:3306"  # Use different external port
```

**Database connection failed:**
```bash
# Check MySQL container health
docker ps

# View MySQL logs
docker logs notes_mysql

# Restart containers
docker-compose restart
```

**Cryptography package error:**
```bash
# Already included in requirements.txt
# If issue persists, rebuild container
docker-compose up --build
```

### Application Issues

**Import errors:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

**Database tables not created:**
```bash
# Tables are auto-created on startup
# Check application logs for errors
docker logs notes_backend
``` 

## Support

**Common Commands:**

```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker logs notes_backend -f

# Run tests
python test_api.py

# Performance tests
python performance_test.py

# Access API docs
# Open http://localhost:8000/docs in browser
```

**Need Help?**
1. Check Docker logs: `docker-compose logs`
2. Verify containers are running: `docker ps`
3. Test health endpoint: `curl http://localhost:8000/health`
4. Review DOCKER_SETUP.md for detailed troubleshooting

---

**Status**: Complete and Tested  
**Last Updated**: October 2025  
**Version**: 1.0.0