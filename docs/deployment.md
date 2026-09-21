# AI-AgriVision Deployment Guide

This document outlines best practices for deploying the AI-AgriVision platform into production on containerized cloud infrastructure (AWS ECS, Google Cloud Run, DigitalOcean, or Bare-Metal Linux).

---

## 1. Production Architecture

In production, the platform is orchestrated as decoupled microservices behind an Nginx or Traefik reverse proxy:

```
[ Internet / Farmers ]
         │
         ▼
[ Nginx Reverse Proxy (SSL / TLS termination, Port 443) ]
         │
         ├──► /api/v1/predictions  ──► [ Node.js Backend Cluster (PM2 or Docker) ]
         │                                       │
         │                                       ├──► [ MongoDB Atlas / Replica Set ]
         │                                       ├──► [ Cloudinary Image CDN ]
         │                                       │
         └──► Forward image buffer ──────────────┴──► [ FastAPI ML Microservice ]
```

---

## 2. Docker Compose Deployment

### Step 1: Clone Repository & Configure Environment
```bash
git clone https://github.com/your-org/AI-AgriVision.git
cd AI-AgriVision
cp backend/.env.example backend/.env
```

Ensure production values are set in `backend/.env`:
- Generate a cryptographically secure 64-character `JWT_SECRET`.
- Configure actual `CLOUDINARY_*` credentials.
- Set `NODE_ENV=production`.

### Step 2: Build and Launch Containers
```bash
docker compose up -d --build
```

### Step 3: Verify Health
```bash
curl http://localhost:5000/health
curl http://localhost:8000/health
```

---

## 3. Production Hardening Checklist

| Domain | Recommendation |
|---|---|
| **HTTPS / SSL** | Terminate SSL at Nginx / Cloudflare. Never transmit unencrypted patient/farmer tokens over HTTP. |
| **Secrets Management** | Inject secrets through AWS Secrets Manager, HashiCorp Vault, or environment variables. Never commit `.env`. |
| **ML Concurrency** | Deploy FastAPI with multiple Uvicorn workers: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`. |
| **Model Quantization** | For edge deployment, convert Keras weights to INT8 TFLite via `python scripts/export_model.py --quantize`. |
| **Database Backups** | Enable automated snapshots on MongoDB Atlas or configure nightly `mongodump` cron jobs. |
| **Rate Limiting** | Set reasonable API request throttles (`RATE_LIMIT_MAX=100` per 15 minutes) to protect against DDoS attacks. |

---

## 4. Render.com Cloud Deployment

The repository includes a `render.yaml` Blueprint to deploy both microservices (`ai-agrivision-backend` and `ai-agrivision-ml`) directly to Render.

### Prerequisites:
1. **GitHub Repository**: Push this project to GitHub.
2. **MongoDB Atlas**: Create a free M0 cluster and copy connection string (`mongodb+srv://...`).
3. **Cloudinary Account**: Obtain Cloud Name, API Key, and API Secret.

### Deployment Options:
- **Option A (Blueprint - Recommended)**: Go to Render Dashboard -> **New +** -> **Blueprint** -> Connect repository. Fill in `MONGO_URI`, `ML_SERVICE_URL`, and Cloudinary variables.
- **Option B (Manual Web Services)**: Create two Web Services (Docker runtime) for `./ml-service` and `./backend` respectively.

