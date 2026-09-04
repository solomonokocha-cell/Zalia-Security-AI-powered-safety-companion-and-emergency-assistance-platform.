# Zalia Security - Deployment Guide

This guide covers deploying Zalia Security to production environments.

---

## Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] HTTPS certificate obtained
- [ ] OpenAI API key is valid and has funds
- [ ] Database backups configured (if using)
- [ ] Security headers enabled
- [ ] CORS origins whitelisted
- [ ] Rate limiting configured
- [ ] Logging system setup
- [ ] Error monitoring configured (Sentry, etc.)
- [ ] CDN configured for static assets

---

## Environment Configuration

### Required Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=sk-your-production-key

# Flask
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=use-a-strong-random-key-here

# Security
CORS_ORIGINS=yourdomain.com,www.yourdomain.com

# Logging
LOG_LEVEL=INFO
```

### Generate Strong Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Deployment Methods

### 1. Heroku Deployment

**Step 1: Create Procfile**
```
web: gunicorn app:app
release: echo "Deploying Zalia"
```

**Step 2: Create runtime.txt**
```
python-3.11.0
```

**Step 3: Add Gunicorn to requirements.txt**
```
gunicorn==21.2.0
```

**Step 4: Deploy**
```bash
heroku create zalia-security
heroku config:set OPENAI_API_KEY=sk-your-key
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

**Step 5: Monitor**
```bash
heroku logs --tail
heroku open
```

### 2. AWS EC2 Deployment

**Step 1: Launch EC2 Instance**
- Ubuntu 22.04 LTS
- t3.medium or larger
- Security group: Allow ports 80, 443, 22

**Step 2: Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
sudo pip install gunicorn
```

**Step 3: Clone Application**
```bash
cd /home/ec2-user
git clone your-repo zalia-security
cd zalia-security
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 4: Configure Gunicorn**
Create `/etc/systemd/system/zalia.service`:
```ini
[Unit]
Description=Zalia Security API
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/zalia-security
Environment="PATH=/home/ec2-user/zalia-security/venv/bin"
ExecStart=/home/ec2-user/zalia-security/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    app:app

[Install]
WantedBy=multi-user.target
```

**Step 5: Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/zalia
```

Add:
```nginx
upstream zalia {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 1M;

    location / {
        proxy_pass http://zalia;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

**Step 6: Enable SSL/TLS (Let's Encrypt)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Step 7: Start Services**
```bash
sudo systemctl start zalia
sudo systemctl enable zalia
sudo systemctl restart nginx
```

### 3. Docker Deployment

**Step 1: Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

**Step 2: Create .dockerignore**
```
__pycache__
.git
.gitignore
*.pyc
*.pyo
.env
venv/
```

**Step 3: Build & Run**
```bash
docker build -t zalia:latest .
docker run -p 5000:5000 -e OPENAI_API_KEY=sk-key zalia:latest
```

**Step 4: Docker Compose (optional)**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

---

## SSL/TLS Configuration

### HTTPS Headers in Nginx
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

---

## Performance Optimization

### 1. CDN Configuration

Set up CloudFlare or similar:
- Cache static assets (CSS, JS, images)
- Enable gzip compression
- Enable minification
- Setup auto HTTPS

### 2. Database Optimization (if applicable)

```sql
CREATE INDEX idx_incidents_timestamp ON incidents(timestamp);
CREATE INDEX idx_incidents_location ON incidents(location);
```

### 3. Caching Headers

In Flask app:
```python
@app.route('/images/<path:filename>')
def send_image(filename):
    response = send_from_directory('images', filename)
    response.cache_control.max_age = 31536000  # 1 year
    return response
```

---

## Monitoring & Logging

### 1. Application Monitoring

Use error tracking services:
- **Sentry** - Error tracking
- **Datadog** - Infrastructure monitoring
- **New Relic** - Performance monitoring

### 2. Logging Setup

```python
# In app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/zalia.log', 
                                      maxBytes=10240, 
                                      backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 3. Monitoring Script

```bash
#!/bin/bash
# monitor.sh

while true; do
    curl -f http://localhost:5000/api/health || \
        echo "API is down! Alert on $(date)"
    sleep 300  # Check every 5 minutes
done
```

---

## Backup & Recovery

### 1. Database Backups

```bash
# Daily backup
0 2 * * * pg_dump zalia_db > /backups/zalia_$(date +\%Y\%m\%d).sql
```

### 2. Application Backups

```bash
# Weekly backup
0 3 * * 0 tar -czf /backups/zalia_$(date +\%Y\%m\%d).tar.gz /app
```

---

## Scaling

### Horizontal Scaling (Multiple Servers)

1. Setup load balancer (nginx, HAProxy)
2. Deploy app to multiple servers
3. Use shared session storage (Redis)
4. Setup database replication

### Vertical Scaling (Single Server)

1. Increase server resources (CPU, RAM)
2. Increase Gunicorn workers
3. Optimize database queries
4. Enable caching

---

## Security Hardening

### 1. Firewall Rules

```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw default deny incoming
```

### 2. Fail2Ban (Prevent Brute Force)

```bash
sudo apt install fail2ban
# Configure for SSH and API endpoints
```

### 3. Rate Limiting

Configure in production:
```python
# In .env
RATELIMIT_REQUESTS=10
RATELIMIT_WINDOW=60
```

---

## Rollback Procedure

If deployment fails:

```bash
# Check current version
git log --oneline -1

# Rollback to previous version
git revert HEAD
git push

# Or rollback to specific commit
git reset --hard <commit-hash>
git push --force

# Restart services
sudo systemctl restart zalia
```

---

## Performance Benchmarks

Expected performance metrics:

- **Response Time:** < 500ms (for AI responses)
- **Throughput:** 100+ requests/second
- **Uptime:** 99.9%+
- **API Availability:** 99.95%+

---

## Common Issues

### Issue: High Memory Usage
**Solution:** Reduce Gunicorn workers or increase server RAM

### Issue: Slow Response Times
**Solution:** Enable caching, optimize queries, use CDN

### Issue: API Rate Limits Hit
**Solution:** Implement client-side caching, increase limits

### Issue: SSL Certificate Renewal Fails
**Solution:** Setup auto-renewal with certbot hooks

---

## Support & Documentation

- Deployment logs: `/var/log/syslog`
- Application logs: `logs/zalia.log`
- Error tracking: Check Sentry dashboard
- Performance: Check monitoring tool dashboards

---

**Deploy with confidence. Zalia's got your back. 🐾✨**
