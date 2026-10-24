# Talnora Quick Reference Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 14+

### Quick Setup
```bash
# Clone repo
git clone <repo>
cd TalnoraAIAgency

# Backend setup
cd apps/api
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend setup (new terminal)
cd apps/web
npm install
npm run dev

# Services (Docker Compose)
docker-compose up -d
```

Visit `http://localhost:3000` (frontend) and `http://localhost:8000/docs` (API docs)

---

## 📁 Project Structure

```
TalnoraAIAgency/
├── apps/
│   ├── api/                          # FastAPI backend
│   │   ├── app/
│   │   │   ├── agents/              # AI agents (12 files)
│   │   │   ├── api/v1/              # REST endpoints (10 files)
│   │   │   ├── services/            # External integrations (8 files)
│   │   │   ├── core/                # Auth, RBAC, config
│   │   │   ├── models/              # Pydantic schemas
│   │   │   ├── main.py              # FastAPI app
│   │   │   └── config.py            # Configuration
│   │   └── requirements.txt         # Python dependencies
│   └── web/                         # Next.js frontend
│       ├── components/              # React components
│       ├── hooks/                   # Custom hooks & API integration
│       ├── pages/                   # Next.js pages
│       └── package.json             # Node dependencies
├── infra/                           # Infrastructure & deployment
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
└── tests/                           # Test files
```

---

## 🔑 Core Concepts

### Agents
12 AI agents handle recruitment tasks:
- **Orchestrator** - Coordinates all agents
- **Job Agent** - Parses job descriptions
- **Resume Agent** - Parses resumes
- **Matching Agent** - Scores candidates
- **Screening Agent** - Filters candidates
- **Outreach Agent** - Sends emails
- **Scheduling Agent** - Books interviews
- **Interview Agent** - Conducts interviews
- **Submission Agent** - Creates packages
- **Reporting Agent** - Generates reports
- **Talent Intelligence** - Market analysis
- **Compliance Agent** - GDPR compliance

### Authentication & Authorization
- **JWT tokens** for API authentication
- **RBAC** with 10+ permission levels
- **Org-level** isolation for multi-tenancy

### Multi-Tenancy
- `org_id` in every request
- Row-level security
- Org-scoped data access

---

## 🔌 Key APIs

### Job Management
```python
POST   /api/v1/jobs                    # Create job
GET    /api/v1/jobs                    # List jobs
GET    /api/v1/jobs/{id}               # Get job details
PUT    /api/v1/jobs/{id}               # Update job
DELETE /api/v1/jobs/{id}               # Delete job
POST   /api/v1/jobs/{id}/clone         # Clone job
GET    /api/v1/jobs/{id}/pipeline      # Get pipeline status
```

### Candidate Management
```python
POST   /api/v1/candidates              # Create candidate
GET    /api/v1/candidates              # List candidates
GET    /api/v1/candidates/{id}         # Get candidate
PUT    /api/v1/candidates/{id}         # Update candidate
DELETE /api/v1/candidates/{id}         # Delete candidate
GET    /api/v1/candidates/{id}/360     # Full candidate view
```

### Interviews
```python
POST   /api/v1/interviews              # Schedule interview
GET    /api/v1/interviews              # List interviews
PUT    /api/v1/interviews/{id}         # Complete interview
```

### Placements
```python
POST   /api/v1/placements              # Create offer
PUT    /api/v1/placements/{id}/accept  # Accept offer
GET    /api/v1/placements/kpis         # Placement metrics
```

### Billing
```python
GET    /api/v1/billing/tiers           # List subscription tiers
POST   /api/v1/billing/subscribe       # Create subscription
GET    /api/v1/billing/subscription    # Current subscription
GET    /api/v1/billing/invoices        # Billing history
```

---

## 🛠️ Common Workflows

### Create a Job & Source Candidates
```python
# 1. Create job
POST /api/v1/jobs {
  "title": "Senior DevOps Engineer",
  "description": "...",
  "location": "Toronto, Canada"
}

# 2. Trigger orchestrator to find candidates
POST /api/v1/agents/orchestrator/execute {
  "goal": "Find 10 DevOps Engineers in Toronto"
}

# 3. Check pipeline
GET /api/v1/jobs/{job_id}/pipeline
```

### Screen & Rate Candidates
```python
# 1. Get candidates for job
GET /api/v1/jobs/{job_id}/pipeline

# 2. Screen candidate
POST /api/v1/agents/screening/evaluate {
  "candidate_id": "...",
  "job_id": "..."
}

# 3. Update pipeline status
PUT /api/v1/candidates/{id}/application {
  "job_id": "...",
  "status": "pass"
}
```

### Schedule Interviews
```python
# 1. Create interview
POST /api/v1/interviews {
  "candidate_id": "...",
  "job_id": "...",
  "scheduled_at": "2024-02-15T10:00:00Z"
}

# 2. Triggers calendar integration automatically
# Google Calendar event created

# 3. Track interview
GET /api/v1/interviews/{id}
```

### Send Offers & Track Placements
```python
# 1. Create offer
POST /api/v1/placements {
  "candidate_id": "...",
  "job_id": "...",
  "offer_amount": 150000
}

# 2. Candidate accepts
PUT /api/v1/placements/{id}/accept

# 3. Track joining
PUT /api/v1/placements/{id}/join {
  "joined_date": "2024-03-01"
}

# 4. Get KPIs
GET /api/v1/placements/kpis
```

---

## 📊 Frontend Components

### Dashboard Components
- `<Dashboard />` - Main dashboard
- `<KPICards />` - Key metrics
- `<AgentControlCenter />` - Agent status
- `<PipelineFunnel />` - Hiring funnel
- `<CopilotChat />` - AI command center

### Page Components
- `<JobsPage />` - Job management
- `<CandidatesPage />` - Candidate database
- `<InterviewsPage />` - Interview tracking
- `<PlacementsPage />` - Offer management
- `<BillingPage />` - Subscriptions

### Feature Components
- `<Candidate360 />` - Full candidate view
- `<Job360 />` - Full job view
- `<InterviewScheduler />` - Calendar integration
- `<SubmissionPackage />` - Candidate packets
- `<AnalyticsBoard />` - Reports

---

## 🔗 Integrations

### Email (SendGrid)
```python
from app.services.email_service import EmailService

service = EmailService()
service.send_offer_email(
    candidate_email="john@example.com",
    offer_amount=150000,
    position_title="Senior Engineer"
)
```

### Calendar (Google Calendar)
```python
from app.services.google_calendar_service import GoogleCalendarService

service = GoogleCalendarService()
service.create_interview_event(
    candidate_name="John Doe",
    interviewer_email="recruiter@company.com",
    scheduled_time="2024-02-15T10:00:00Z"
)
```

### Job Boards
```python
from app.services.job_board_service import JobBoardAggregator

aggregator = JobBoardAggregator()
results = aggregator.post_to_all({
    "title": "Senior Engineer",
    "location": "Toronto"
})
```

### LLM Models
```python
from app.services.llm_service import LLMService

service = LLMService()
response = service.generate_response(
    prompt="Analyze this resume...",
    model="claude-3-sonnet"
)
```

---

## 💾 Database

### PostgreSQL Tables
- `users` - User accounts
- `organizations` - Orgs
- `teams` - Teams within org
- `jobs` - Job postings
- `candidates` - Candidate profiles
- `applications` - Job applications
- `interviews` - Interview records
- `placements` - Offers & placements
- `subscriptions` - Billing
- `invoices` - Invoices

### Qdrant Vectors
- Resume embeddings
- Job description embeddings
- Candidate profile embeddings

---

## 🧪 Testing

### Run Backend Tests
```bash
cd apps/api
pytest                           # All tests
pytest tests/test_agents.py     # Specific test file
pytest -v                       # Verbose
pytest --cov                    # With coverage
```

### Run Frontend Tests
```bash
cd apps/web
npm test                        # All tests
npm test -- useJobs.test.ts    # Specific test
npm run test:coverage          # With coverage
```

### E2E Tests
```bash
npm run test:e2e
```

---

## 📈 Monitoring & Observability

### Structured Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Candidate screening started", extra={"candidate_id": "123"})
```

### Cost Tracking
```python
from app.services.cost_tracker import CostTracker

tracker = CostTracker()
tracker.track_llm_call(
    agent="screening",
    model="claude-3-sonnet",
    tokens_used=500,
    cost_cents=15
)
```

### Performance Monitoring
- API response times tracked
- Agent execution times logged
- LLM token usage recorded

---

## 🔐 Security Best Practices

### API Key Management
```python
from app.core.config import settings

api_key = settings.SENDGRID_API_KEY
# Never log or expose keys
```

### RBAC Checks
```python
from app.core.rbac import require_permission

@router.post("/jobs")
async def create_job(
    current_user: User = Depends(require_permission("job:create"))
):
    # User has job:create permission
    pass
```

### Data Validation
```python
from pydantic import BaseModel, EmailStr

class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    
    class Config:
        json_schema_extra = {"example": {...}}
```

---

## 📝 Common Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version

# Clear cache
rm -rf __pycache__ .pytest_cache

# Reinstall dependencies
pip install -r requirements.txt

# Check PostgreSQL connection
psql -h localhost -U postgres
```

### Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next
npm run dev
```

### Vector DB Issues
```bash
# Check Qdrant is running
curl http://localhost:6333/health

# Reset collections
curl -X DELETE http://localhost:6333/collections/candidates
```

---

## 🚀 Deployment

### Docker Build
```bash
docker build -f apps/api/Dockerfile -t talnora-api:latest .
docker build -f apps/web/Dockerfile -t talnora-web:latest .
```

### Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### GitHub Actions
Automatically triggered on:
- Push to main branch
- Pull request to main

Runs:
- Linting
- Tests
- Docker build
- Registry push

---

## 📚 Documentation

- **API Documentation:** `http://localhost:8000/docs`
- **Architecture:** See `ARCHITECTURE.md`
- **Deployment:** See `SETUP_GUIDE.md`
- **Features:** See `COMPLETION_FINAL_REPORT.md`

---

## 🆘 Support

### Getting Help
1. Check `ARCHITECTURE.md` for system design
2. Review `COMPLETION_FINAL_REPORT.md` for features
3. Check API docs at `/docs`
4. Review test files for examples

### Reporting Issues
Include:
- Error message
- Steps to reproduce
- Environment (Python/Node version, OS)
- Logs if available

---

## 📞 Key Contacts

- **Questions:** Check docs
- **Bugs:** Create issue on GitHub
- **Features:** Check roadmap

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Status:** ✅ Production Ready

