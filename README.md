# Production Agent API

Production Agent API is a FastAPI service that wraps a LangGraph-based chat agent with security checks, response caching, rate limiting, and basic observability. It is designed as a small production-style reference implementation for building AI agent APIs with Google Gemini models.

## What the project does

The service exposes a chat endpoint that accepts a message, runs it through a security pipeline, sends it to a LangGraph agent, and returns a validated response. The agent uses a primary Gemini model with a fallback model if the primary call fails.

The app also provides:

- Input sanitization and prompt-injection filtering
- PII masking on input and output
- In-memory response caching with TTL
- Rate limiting through SlowAPI
- JSON logging and request timing metrics
- LangSmith tracing for agent and security steps
- Health, metrics, and cache statistics endpoints

## Why the project is useful

This project shows a practical way to assemble common production concerns around an AI agent without turning the codebase into a large framework. It is useful if you want a clear starting point for:

- Building a chat API around Gemini and LangGraph
- Adding lightweight security checks before and after model calls
- Caching repeated prompts to reduce latency and cost
- Exposing operational endpoints for health checks and dashboards
- Running the service locally, in Docker, or on Render

## Project layout

- `app/main.py`: FastAPI app, endpoints, lifespan setup, and request flow
- `app/agent.py`: LangGraph agent with primary and fallback model handling
- `app/security.py`: Input sanitization, PII detection, and output validation
- `app/cache.py`: In-memory TTL cache for responses
- `app/monitoring.py`: JSON logging, timers, and metrics collection
- `app/models.py`: Pydantic request and response models
- `app/config.py`: Environment-based settings
- `tests/`: Fast, deterministic tests for cache and security logic

## Getting started

### Prerequisites

- Python 3.11.8 or newer
- `uv` installed locally
- A Google Gemini API key
- Optional: a LangSmith API key if you want tracing in LangSmith

### Installation

1. Clone the repository.
2. Create or activate your virtual environment.
3. Install dependencies:

```bash
uv sync
```

### Environment variables

Create a `.env` file in the project root. The included `.env.example` shows the expected keys:

```env
GOOGLE_API_KEY=your_google_api_key
PRIMARY_MODEL=gemini-3.1-flash-lite
FALLBACK_MODEL=gemini-3.5-flash

LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=prod-agent-api

APP_ENV=development
LOG_LEVEL=INFO
RATE_LIMIT=20/minute
CACHE_TTL_SECONDS=300
MAX_RETRIES=3
```

### Run locally

Start the API with Uvicorn:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The app will be available at `http://127.0.0.1:8000`.

### Use the API

Send a chat request:

```bash
curl -X POST http://127.0.0.1:8000/chat \
	-H "Content-Type: application/json" \
	-d '{
		"message": "Write a short welcome message for a production API.",
		"thread_id": "demo"
	}'
```

Expected response fields include:

- `response`: the model output
- `thread_id`: the conversation thread identifier
- `model_used`: `primary`, `fallback`, or `cache`
- `cached`: whether the response came from cache
- `processing_time_ms`: request latency
- `security_notes`: masking or validation notes

### Check service health

```bash
curl http://127.0.0.1:8000/health
```

Other useful endpoints:

- `GET /metrics`: request and token metrics
- `GET /cache/stats`: cache hit and miss statistics

### Run tests

```bash
uv run pytest
```

## Deployment

### Docker Compose

```bash
docker compose up --build
```

### Render

The repository includes `render.yaml` for deploying the app on Render with the same environment variables used locally.

## Notes

- The cache is in-memory, so it resets when the process restarts.
- The app expects valid Google Gemini credentials before the chat endpoint can respond successfully.
- Rate limiting is enabled per client IP.

## Acknowledgements

This project is based on the learnings from the course [Production AI Agents with LangChain + LangGraph](https://www.udemy.com/course/production-ai-agents/).
