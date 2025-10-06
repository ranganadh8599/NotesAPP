# Docker Setup Guide

This guide will help you run the Notes API using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed (comes with Docker Desktop)

## Quick Start

### 1. Start the Application

```bash
cd backend
docker-compose up --build
```

This will:
- Pull MySQL 8.0 image
- Build the FastAPI backend image
- Create a MySQL database container
- Create a FastAPI backend container
- Set up networking between containers
- Initialize the database automatically

### 2. Access the Application

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Stop the Application

```bash
docker-compose down
```

To stop and remove all data (reset database):
```bash
docker-compose down -v
```

## Docker Commands

### Start in Background
```bash
docker-compose up -d
```

### View Logs
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# MySQL only
docker-compose logs -f mysql
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
docker-compose up --build
```

### Check Running Containers
```bash
docker-compose ps
```

### Execute Commands in Container
```bash
# Access backend shell
docker-compose exec backend bash

# Access MySQL shell
docker-compose exec mysql mysql -u notesuser -p notes_db
```

## Configuration

The `docker-compose.yml` file includes:

### MySQL Service
- **Image**: mysql:8.0
- **Port**: 3306
- **Database**: notes_db
- **User**: notesuser
- **Password**: notespass
- **Root Password**: rootpassword
- **Volume**: Persistent data storage

### Backend Service
- **Build**: From local Dockerfile
- **Port**: 8000
- **Environment**: All config from docker-compose.yml
- **Depends on**: MySQL (waits for health check)

## Environment Variables

The backend uses these environment variables (set in docker-compose.yml):

```yaml
DB_HOST: mysql
DB_PORT: 3306
DB_USER: notesuser
DB_PASSWORD: notespass
DB_NAME: notes_db
SECRET_KEY: your-secret-key-change-in-production-12345
ALGORITHM: HS256
ACCESS_TOKEN_EXPIRE_MINUTES: 30
CORS_ORIGINS: http://localhost:3000,http://localhost:3001
```

## Troubleshooting

### MySQL Connection Issues

If you see "Can't connect to MySQL server":
1. Wait 10-20 seconds for MySQL to fully start
2. Check MySQL health: `docker-compose ps`
3. View MySQL logs: `docker-compose logs mysql`

### Port Already in Use

If port 8000 or 3306 is already in use:
1. Stop other services using those ports
2. Or change ports in docker-compose.yml:
   ```yaml
   ports:
     - "8001:8000"  # Use port 8001 instead
   ```

### Database Not Initializing

The backend automatically creates tables on startup. If tables aren't created:
1. Check backend logs: `docker-compose logs backend`
2. Restart: `docker-compose restart backend`
3. Reset database: `docker-compose down -v && docker-compose up`

### Code Changes Not Reflecting

After changing code:
```bash
docker-compose up --build
```

Or for faster development, use volume mounting (already configured).

## Production Considerations

For production deployment:

1. **Change Passwords**: Update all passwords in docker-compose.yml
2. **Use Secrets**: Don't hardcode sensitive data
3. **Environment File**: Use `.env` file instead of hardcoding
4. **Remove Volumes**: Don't mount source code in production
5. **Add Nginx**: Use reverse proxy
6. **SSL/TLS**: Add HTTPS support
7. **Resource Limits**: Set memory and CPU limits

## Testing the Setup

Once running, test with:

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"user_name":"Test","user_email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"user_email":"test@example.com","password":"test123"}'
```

## Database Access

To access MySQL directly:

```bash
# Using docker exec
docker-compose exec mysql mysql -u notesuser -p notes_db
# Password: notespass

# Or using MySQL client on host
mysql -h 127.0.0.1 -P 3306 -u notesuser -p notes_db
```

## Cleanup

Remove everything (containers, volumes, networks):
```bash
docker-compose down -v
docker system prune -a
```

## Next Steps

1. Start the containers: `docker-compose up`
2. Test the API: http://localhost:8000/docs
3. Build the frontend to connect to this backend
4. Deploy to production with proper security