# Deployment

## Backend on Railway

Deploy the `backend/` service with Docker. If Railway uses the repository root, the included `railway.toml` points to `backend/Dockerfile`. Alternatively set the Railway service Root Directory to `/backend`.

Environment variables:
- `CORS_ORIGINS=https://YOUR-VERCEL-DOMAIN`
- `HF_TOKEN=` only if Hugging Face access requires authentication
- `WHISPER_MODEL=base`
- `TRANSLATION_BATCH_SIZE=8`

The first request for a language pair downloads that model from Hugging Face if it is not already cached.

## Frontend on Vercel

Set the project Root Directory to `frontend` and configure:

`NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-DOMAIN/api`

## Production hardening

Before public launch:
1. Add authentication/API keys.
2. Add rate limiting.
3. Add per-user quotas.
4. Validate file content and consider malware scanning for arbitrary uploads.
5. Add persistent object storage only when files/results need to survive requests.
6. Add monitoring and error tracking.
7. Consider a worker queue for long documents and audio.
