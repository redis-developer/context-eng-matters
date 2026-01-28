# Setup Guide for Context Engineering Workshop

This guide will help you set up everything you need to run the workshop notebooks (`workshop/`) and the staged agent demos (`demos/`).

## Prerequisites

- **Python 3.11+** installed
- **Docker and Docker Compose** installed
- **OpenAI API key** (get one at https://platform.openai.com/api-keys)

## Quick Setup (5 minutes)

### Step 1: Set Your OpenAI API Key

The OpenAI API key is needed by both the Jupyter notebooks AND the Agent Memory Server. The easiest way to set it up is to use a `.env` file.

```bash
# From the repository root
cp .env.example .env

# Edit .env and add your OpenAI API key
```

Your `.env` file should look like this:
```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (defaults provided)
REDIS_URL=redis://localhost:6379
AGENT_MEMORY_SERVER_URL=http://localhost:8088
REDIS_INDEX_NAME=course_catalog
```

**Important:** The `.env` file is already in `.gitignore` so your API key won't be committed to git.

### Step 2: Start Required Services

Start Redis and the Agent Memory Server using Docker Compose:

```bash
# Start services in the background
docker-compose up -d

# Verify services are running
docker-compose ps

# Check that the Agent Memory Server is healthy
curl http://localhost:8088/v1/health
```

You should see:
- `redis-context-engineering` running on port 6379 (Redis 8)
- `agent-memory-server` running on port 8088

**Important:** The Agent Memory Server requires `OPENAI_API_KEY` for long-term memory features. The docker-compose.yml passes this from your `.env` file. If you see warnings about "OpenAI API key is required", ensure your `.env` file is properly configured and restart the services.

### Step 3: Install Python Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip with virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Step 4: Load Course Data

```bash
# Load hierarchical courses into Redis (required for workshop and demos)
uv run load-hierarchical-courses \
  -i src/redis_context_course/data/hierarchical/hierarchical_courses.json \
  --force

# Alternative: Load flat course format (for backward compatibility)
uv run python -m redis_context_course.scripts.ingest_courses \
  --catalog src/redis_context_course/data/courses.json \
  --index-name hierarchical_courses \
  --clear
```

**Note:** Use `--force` to clear and reload data if you've regenerated the course catalog or if you're seeing duplicate courses.

### Step 5: Run the Workshop Notebooks

```bash
# Start Jupyter for the workshop
uv run jupyter notebook workshop/
```

The notebooks will automatically load your `.env` file using `python-dotenv`, so your `OPENAI_API_KEY` will be available.

## Verifying Your Setup

### Check Redis
```bash
# Test Redis connection
docker exec redis redis-cli ping
# Should return: PONG
```

### Check Agent Memory Server
```bash
# Test health endpoint
curl http://localhost:8088/v1/health
# Should return: {"now":<timestamp>}
```

### Check Python Environment
```bash
# Verify the package is installed
uv run python -c "import redis_context_course; print('✅ Package installed')"

# Verify OpenAI key is set
uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ OpenAI key set' if os.getenv('OPENAI_API_KEY') else '❌ OpenAI key not set')"
```

## Troubleshooting

### "OPENAI_API_KEY not found"

**In Notebooks:** The notebooks will prompt you for your API key if it's not set. However, it's better to set it in the `.env` file so you don't have to enter it repeatedly.

**In Docker:** Make sure:
1. Your `.env` file exists and contains `OPENAI_API_KEY=your-key`
2. You've restarted the services: `docker-compose down && docker-compose up -d`
3. Check the logs: `docker-compose logs agent-memory-server`

### "Connection refused" to Agent Memory Server

Make sure the services are running:
```bash
docker-compose ps
```

If they're not running, start them:
```bash
docker-compose up -d
```

Check the logs for errors:
```bash
docker-compose logs agent-memory-server
```

### "Connection refused" to Redis

Make sure Redis is running:
```bash
docker-compose ps redis
```

Test the connection:
```bash
docker exec redis redis-cli ping
```

### Port Already in Use

If you get errors about ports already in use (6379 or 8088), you can either:

1. Stop the conflicting service
2. Change the ports in `docker-compose.yml`:
   ```yaml
   ports:
     - "6380:6379"  # Use 6380 instead of 6379
   ```
   Then update `REDIS_URL` or `AGENT_MEMORY_URL` in your `.env` file accordingly.

## Stopping Services

```bash
# Stop services but keep data
docker-compose stop

# Stop and remove services (keeps volumes/data)
docker-compose down

# Stop and remove everything including data
docker-compose down -v
```

## Alternative: Using Existing Redis or Cloud Redis

If you already have Redis running or want to use Redis Cloud:

1. Update `REDIS_URL` in your `.env` file:
   ```bash
   REDIS_URL=redis://default:password@your-redis-cloud-url:port
   ```

2. You still need to run the Agent Memory Server locally:
   ```bash
   docker-compose up -d agent-memory-server
   ```

## Next Steps

Once setup is complete:

**For the Workshop (condensed):**
1. Start with **Module 1** (Introduction) to understand context types
2. Work through **Module 2** (RAG Essentials) for vector search fundamentals
3. Complete **Module 3** (Data Engineering) for data pipeline patterns
4. Master **Module 4** (Memory Systems) for working and long-term memory
5. Explore the staged demos in `demos/` to see the same ideas evolve into increasingly capable agents

## Getting Help

- Check the main [README.md](README.md) for course structure and learning path
- Review the **Workshop Outline** and **Agent Demos (CLI)** sections in the main [README.md](README.md)

