# LocaleNLP Translation Platform

Full-stack translation platform for LocaleNLP MarianMT models.

## Included

- Next.js frontend suitable for Vercel
- FastAPI backend
- Lazy-loaded Hugging Face MarianMT models
- English ↔ Wolof
- English ↔ Hausa
- Text translation
- PDF, DOCX, HTML, Markdown, SRT and TXT extraction
- Audio transcription with Whisper
- Audio → text → translation endpoint
- Docker deployment
- Health/model/language endpoints
- File-size validation
- CORS configuration
- Basic request timing/logging

## Models

- `LocaleNLP/localenlp-eng-wol-0.03`
- `LocaleNLP/localenlp-wol-eng-0.03`
- `LocaleNLP/localenlp-eng-hau-0.01`
- `LocaleNLP/localenlp-hau-eng-0.01`

## Local development

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open `http://localhost:3000`.

Set `NEXT_PUBLIC_API_URL=http://localhost:8000/api`.

## Docker

```bash
cd backend
docker build -t localenlp-api .
docker run --env-file .env -p 8000:8000 localenlp-api
```

The container downloads Hugging Face models on first use and caches them.

## Production architecture

Vercel (frontend) → FastAPI service (backend) → Hugging Face Hub (model artifacts).

For a first deployment, uploaded files are processed in temporary storage and are not permanently retained.

## Security notes

Before opening the API to large public traffic, add authentication/API keys, rate limiting, request quotas, stronger file validation, and observability.
