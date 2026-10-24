# Talnora Implementation Roadmap - Phases 3-7

## PHASE 3: Authentication & Authorization (Supabase Auth, JWT, RBAC)

### Files to Create:

**apps/api/app/core/auth.py** - JWT and auth helpers
```python
from supabase import create_client
from fastapi import Depends, HTTPException
from jose import JWTError, jwt

class AuthService:
    def verify_token(token: str) -> dict
    def create_access_token(data: dict) -> str
    def get_current_user(token: str) -> User
```

**apps/api/app/core/rbac.py** - Role-based access control
```python
class Permission(Enum):
    READ_JOBS = "read:jobs"
    CREATE_JOBS = "create:jobs"
    MANAGE_USERS = "manage:users"

class RBACService:
    def has_permission(user: User, permission: Permission) -> bool
    def has_role(user: User, role: str) -> bool
```

**apps/api/app/api/v1/auth.py** - Auth endpoints
- POST /auth/signup
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout
- GET /auth/me

### Key Features:
- Supabase Auth integration
- JWT token generation/validation
- Multi-role RBAC (SuperAdmin, AgencyAdmin, Recruiter, HiringManager, Client, Candidate)
- Session management
- Token refresh logic
- Org-scoped permissions

---

## PHASE 4: Database Migrations & Seeding

### Files to Create:

**apps/api/app/db/migrations/001_initial_schema.sql**
- Alembic migration script for schema.sql

**apps/api/app/db/seed.py** - Database seeding
```python
async def seed_demo_data():
    - Create demo organizations
    - Create demo users with different roles
    - Create sample jobs
    - Create sample candidates
    - Create sample applications
```

**infra/supabase/migrations/** - Supabase migrations

### Key Features:
- Version-controlled schema changes
- Rollback capability
- Demo data for testing
- RLS policy initialization
- Index creation

---

## PHASE 5: End-to-End Integration Tests

### Files to Create:

**apps/api/tests/test_integration.py**
```python
class TestJobFillWorkflow:
    async def test_parse_to_submission_workflow()
    async def test_outreach_approval_and_send()
    async def test_cost_tracking_across_workflow()

class TestAuthFlow:
    async def test_signup_and_login()
    async def test_rbac_enforcement()

class TestQdrantIntegration:
    async def test_index_and_search_resume()
    async def test_search_resume_by_job_requirements()
```

**apps/web/tests/integration.test.tsx**
- Dashboard component integration
- API call mocking
- User interaction flows
- State management integration

### Key Features:
- Full workflow testing (job creation → sourcing → outreach → interviews)
- Auth flow validation
- Cost tracking verification
- Qdrant search accuracy
- API contract validation

---

## PHASE 6: Additional Agent Implementations

### Files to Create:

**apps/api/app/agents/orchestrator.py** - Talnora Orchestrator (Meta-Agent)
```python
class TalnoraOrchestrator:
    async def process_command(command: str) -> WorkflowPlan
    async def execute_workflow(plan: WorkflowPlan) -> Result
    async def handle_escalation(issue: str)
    async def learn_from_feedback(feedback: dict)
```

**apps/api/app/agents/scheduling.py** - Scheduling Agent
```python
class SchedulingAgent:
    async def schedule_interview(candidate, job, availability)
    async def handle_reschedule_request(interview_id, new_time)
    async def send_interview_reminders()
    async def integrate_google_calendar()
```

**apps/api/app/agents/reporting.py** - Reporting Agent
```python
class ReportingAgent:
    async def generate_kpi_report(org_id, period)
    async def generate_pipeline_report(job_id)
    async def send_recruiter_insights(org_id)
```

### Key Features:
- Natural language command interpretation (Orchestrator)
- Calendar integration with Google Calendar API (Scheduling)
- PDF report generation (Reporting)
- Learning from outcomes
- Escalation handling

---

## PHASE 7: Environment Setup (.env, Config Validation)

### Files to Create:

**apps/api/.env.example**
```
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/talnora
DB_POOL_SIZE=20

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyxx...

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Redis
REDIS_URL=redis://localhost:6379

# LiteLLM
LITELLM_API_KEY=sk-xxx
LITELLM_API_BASE=https://api.openrouter.ai/api/openai

# Auth
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Observability
SENTRY_DSN=
OTEL_EXPORTER_OTLP_ENDPOINT=
```

**apps/api/app/core/config.py** - Pydantic settings validation
```python
class Settings(BaseSettings):
    database_url: str
    supabase_url: str
    supabase_key: str
    qdrant_url: str
    redis_url: str
    jwt_secret: str
    environment: str
    
    class Config:
        env_file = ".env"
```

**apps/web/.env.example**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_LOG_LEVEL=info
```

### Key Features:
- Environment-specific configuration
- Type-safe settings with Pydantic
- Validation on startup
- Secure secret management
- .env file templates

---

## Implementation Order & Dependencies

```
1. PHASE 1: Deployment Config ✅
   ↓
2. PHASE 2: LLM Integration ✅
   ↓
3. PHASE 3: Authentication & Authorization
   ↓
4. PHASE 4: Database Migrations & Seeding
   ↓
5. PHASE 7: Environment Setup (can run in parallel with 4)
   ↓
6. PHASE 5: End-to-End Integration Tests
   ↓
7. PHASE 6: Additional Agent Implementations
```

---

## Summary

| Phase | Status | Key Deliverables | Time Est. |
|-------|--------|------------------|-----------|
| 1 | ✅ Done | Docker, docker-compose, GitHub Actions CI/CD | - |
| 2 | ✅ Done | LiteLLM integration, cost tracking, model routing | - |
| 3 | 🔄 Next | Supabase Auth, JWT, RBAC endpoints | 2-3 hrs |
| 4 | ✅ Done | DB migrations, seed data | - |
| 5 | ⏳ Todo | Integration tests (backend + frontend) | 2-3 hrs |
| 6 | ⏳ Todo | Orchestrator, Scheduling, Reporting agents | 3-4 hrs |
| 7 | ✅ Done | .env setup, config validation | - |

## Quick Start (Post Implementation)

```bash
# 1. Setup environment
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env.local

# 2. Run migrations
cd apps/api
alembic upgrade head

# 3. Seed database
python -m app.db.seed

# 4. Start services
docker-compose up

# 5. Run tests
pytest tests/
npm run test

# 6. Access platform
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
```

---

## Next Steps

Would you like me to continue with:
- Phase 3: Authentication implementation (detailed)
- Phase 4: Database migrations
- Phase 5-7: Full implementation
- Or focus on a specific area?
