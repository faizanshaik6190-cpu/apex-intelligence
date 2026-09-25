# Apex Intelligence

An AI-powered growth and consulting company that uses 6 specialized agents to:

- Generate leads from local businesses
- Negotiate service contracts  
- Create professional 3-page growth audits
- Deliver implementation roadmaps
- Handle customer support
- Report to the CEO/owner

## 🎯 PRIVATE SERVER VERSION

This is a **production-ready private server** for Apex Intelligence. It runs as a self-contained backend on your own infrastructure with:

- ✅ Docker containerization (all-in-one deployment)
- ✅ PostgreSQL database (production-grade)
- ✅ Redis cache & message broker
- ✅ Celery workers for background tasks
- ✅ Supervisor process management
- ✅ API Key + JWT authentication
- ✅ Health monitoring & logging
- ✅ Backup automation
- ✅ Secure configuration management

## 🚀 Quick Start (Private Server)

### Prerequisites
- Docker & Docker Compose installed
- Linux/Mac server or Windows with WSL2
- 2GB+ RAM, 10GB+ disk space

### 1. Clone and Setup

```bash
cd apex-intelligence
chmod +x scripts/*.sh
./scripts/setup.sh
```

This will:
- Build Docker image
- Start all services (API, Redis, PostgreSQL, Celery, Supervisor)
- Initialize database
- Verify health

### 2. Configure API Keys

Edit `.env` with your credentials:

```env
# Required for production
SECRET_KEY=your-very-secure-random-key
APEX_API_KEY=your-api-key-for-private-access

# Optional integrations
GOOGLE_MAPS_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
OPENAI_API_KEY=your_key

# Database
DATABASE_URL=postgresql://apex_user:apex_secure_password_change_me@postgres:5432/apex_intelligence
REDIS_URL=redis://redis:6379/0
```

### 3. Start Server

```bash
docker-compose up -d
```

### 4. Access Your Server

```
API:           http://localhost:8000
API Docs:      http://localhost:8000/docs
Supervisor:    http://localhost:9001
Celery Flower: http://localhost:5555
```

## 🔐 Security

### API Authentication

All requests require API key:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/ceo/summary
```

### JWT Tokens

Get a token:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json"
```

Use the token:

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/ceo/summary
```

### Network Security

- Only listens on localhost by default
- Use reverse proxy (Nginx) to expose externally
- Firewall rules recommended
- HTTPS recommended for external access

## 📊 Monitoring & Logs

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi
docker-compose logs -f celery_worker
docker-compose logs -f redis
```

### Health Check

```bash
./scripts/health_check.sh
```

### Supervisor Dashboard

Open http://localhost:9001 to monitor processes

### Celery Flower Dashboard

Open http://localhost:5555 to monitor background tasks

## 🔄 Database

### Backup

```bash
./scripts/backup.sh
```

Backups saved to `./backups/`

### Restore

```bash
# SQLite
cp backups/apex_intelligence_TIMESTAMP.db apex_intelligence.db

# PostgreSQL
docker exec apex_intelligence-postgres-1 psql -U apex_user apex_intelligence < backups/apex_intelligence_pg_TIMESTAMP.sql
```

### Migrations

```bash
./scripts/migrate.sh
```

## 🛑 Server Management

### Stop

```bash
docker-compose down
```

### Restart

```bash
docker-compose restart
```

### Rebuild

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Clean Everything

```bash
docker-compose down -v
rm -rf logs backups
```

## 📡 External Access (Optional)

### Using Nginx Reverse Proxy

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name your.domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then start Nginx:

```bash
nginx -c nginx.conf
```

### Using SSH Tunnel

```bash
ssh -L 8000:localhost:8000 your_server
```

Then access via http://localhost:8000

## 🏗️ Architecture

```
Docker Container (apex)
├── FastAPI App (port 8000)
├── Celery Worker (background tasks)
├── Celery Beat (scheduled tasks)
├── Redis (port 6379)
├── Supervisor (port 9001)
└── Application Files

External Services
├── PostgreSQL (port 5432)
├── Google Maps API
├── Twilio
└── OpenAI
```

## 📈 Performance Tuning

### Increase Celery Workers

Edit `supervisord.conf`:

```ini
[program:celery_worker_1]
command=celery -A integrations.celery_tasks worker --loglevel=info

[program:celery_worker_2]
command=celery -A integrations.celery_tasks worker --loglevel=info
```

### Database Connection Pool

Edit `app/database.py` (PostgreSQL):

```python
engine = create_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=40,
)
```

### Redis Memory

Edit `docker-compose.yml`:

```yaml
redis:
  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

## 🐛 Troubleshooting

### API not responding

```bash
# Check if container is running
docker-compose ps

# View logs
docker-compose logs fastapi

# Restart API
docker-compose restart fastapi
```

### Database connection errors

```bash
# Check PostgreSQL
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

### Celery tasks not running

```bash
# Check Redis
docker-compose logs redis

# Check Celery worker
docker-compose logs celery_worker

# Restart
docker-compose restart celery_worker
```

## 📚 API Documentation

### Health Check

```bash
GET /health
```

### Generate Leads

```bash
POST /leads/generate
X-API-Key: your-key

{
  "city": "Austin, TX",
  "category": "dental",
  "limit": 10
}
```

### Get CEO Summary

```bash
GET /ceo/summary
X-API-Key: your-key
```

### Voice Command

```bash
POST /ceo/voice/command
X-API-Key: your-key

{
  "command": "Show me the strongest leads"
}
```

For full API docs, visit: http://localhost:8000/docs

## 🎯 Next Steps

- [ ] Set up SSL/TLS certificates (Let's Encrypt)
- [ ] Configure DNS records
- [ ] Set up monitoring (DataDog, New Relic, Prometheus)
- [ ] Enable automated backups to cloud storage
- [ ] Configure email alerts for errors
- [ ] Set up load balancing (multiple servers)
- [ ] Enable audit logging for compliance

## 📞 Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review `.env` configuration
- Verify API keys are correct
- Ensure all services are healthy: `./scripts/health_check.sh`

## 📄 License

MIT
