# Margam AI — Learning Platform for AI Engineers

*(Working name: Margam AI — from Sanskrit/Tamil "Margam," a structured learning progression from simple to complex)*

## 1. Vision & Positioning

Build a learning platform for AI engineers that becomes what LeetCode is for DSA — but the core mechanic isn't algorithmic puzzles, it's **design judgment**: making the right architectural calls when building RAG pipelines and AI agents, and knowing how to debug and optimize them.

**The flagship feature is practical questions, not MCQs.** MCQs and learning paths exist, but they are secondary/retention features layered on top of a working practical-questions core.

The core loop, modeled on why LeetCode worked:
> Scenario → your design/answer or code → structured feedback → compare to a strong reference solution → retry

## 2. Content Structure

### Learning paths (sequential tracks)
- ML Fundamentals
- DL Fundamentals
- GenAI / LLM Foundations
- RAG Track
- Agentic AI Track
- Interview Prep (timed, mixes everything, company/role-focused)

### Practical question types
- **Build** — design a RAG pipeline or agent architecture for a given scenario
- **Optimize** — improve a working-but-flawed system (accuracy, latency, cost) — should use real measurable metrics, not just opinion
- **Debug** — given a broken pipeline/agent trace, find and fix the root cause
- **Code** — LeetCode-style: implement specific functions/methods against premade infrastructure, graded by weighted test cases

## 3. Tech Stack

- **Backend:** FastAPI, async endpoints/streaming
- **DB:** PostgreSQL + Prisma (pgvector for embeddings)
- **Agents/grading:** LangGraph (rubric grader, study-planner agent)
- **Queue:** Redis + Celery/ARQ
- **Sandbox:** Docker (or nsjail/gVisor for tighter isolation)
- **Deployment:** Docker, CI

## 4. Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis
- Docker

### Setup

```bash
# Clone the repository
git clone https://github.com/pratikgadhave211/Margam-AI---a-smart-Learning-Platform-for-AI-Engineers.git

# Navigate to backend
cd margam-ai-backend

# Install dependencies
pip install -r requirements.txt

# Generate Prisma Client
prisma generate

# Start the application
uvicorn app.main:app --reload
```
