# Quick Start Guide - Talnora After All 7 Phases

## 🚀 Start Here (5 minutes)

### Step 1: Setup Environment
```bash
cd /path/to/TalnoraAIAgency

# Backend config
cp apps/api/.env.example apps/api/.env

# Frontend config
cp apps/web/.env.example apps/web/.env.local

# Edit with your API keys (IMPORTANT!)
nano apps/api/.env
# Add: LITELLM_API_KEY=sk-or-v1-xxx
# Add: SUPABASE_URL=https://xxx.supabase.co
# Add: SUPABASE_KEY=eyxxx...
```

### Step 2: Start Services
```bash
# One command starts everything
docker-compose up

# Wait for "Backend running on 0.0.0.0:8000"
# Then visit http://localhost:3000
```

### Step 3: Seed Demo Data (Optional)
```bash
# In another terminal
cd apps/api
python -m app.db.seed
```

### Step 4: Test Everything Works
```bash
# Backend API
curl http://localhost:8000/docs

# Frontend
open http://localhost:3000

# Qdrant Vector DB
open http://localhost:6333/dashboard
```

Done! You have a running AI recruitment platform.

---

## 📋 What Each Component Does

### Frontend (http://localhost:3000)
- **Dashboard** - See KPI metrics and agent status
- **Jobs** - Create and manage job listings
- **Candidates** - View candidate profiles and matches
- **Interviews** - Schedule and track interviews
- **Analytics** - View recruitment funnel and metrics
- **Copilot** - Chat with AI to execute commands

### Backend API (http://localhost:8000)
- **Workflows** - Orchestrate multi-agent jobs
- **Agents** - Execute specialized recruitment tasks
- **Jobs** - CRUD operations for job postings
- **Candidates** - Candidate profile management
- **Analytics** - Recruitment metrics and KPIs

### Key Features
- ✅ Parse job descriptions automatically
- ✅ Search and match candidates semantically
- ✅ Score candidates by job fit
- ✅ Draft personalized outreach messages
- ✅ Schedule interviews with calendar integration
- ✅ Generate analytics and reports
- ✅ Track AI costs and enforce budgets
- ✅ Multi-org with role-based access

---

## 🔑 Key Files You Need to Know

### Configuration
- **Backend:** `apps/api/.env` - LLM keys, database, auth
- **Frontend:** `apps/web/.env.local` - API URL, analytics

### Agents (The Intelligence)
- `apps/api/app/agents/orchestrator.py` - Understands natural language
- `apps/api/app/agents/reporting.py` - Analytics and KPIs
- `apps/api/app/agents/scheduling.py` - Interview scheduling
- `apps/api/app/agents/scoring.py` - Candidate matching
- Other agents in same directory

### API Endpoints
- `apps/api/app/api/v1/agents.py` - Agent operations
- `apps/api/app/api/v1/workflows.py` - Workflow orchestration

### Frontend Components
- `apps/web/components/dashboard/` - Dashboard widgets
- `apps/web/components/copilot-panel.tsx` - AI chat interface
- `apps/web/stores/` - State management (Zustand)

### Database
- `infra/supabase/schema.sql` - 13 tables with RLS
- `apps/api/app/db/seed.py` - Demo data

---

## 💻 Common Commands

### Development
```bash
# Start everything
docker-compose up

# Backend only (if frontend is running elsewhere)
cd apps/api && uvicorn app.main:app --reload

# Frontend only (if backend is running elsewhere)
cd apps/web && npm run dev
```

### Testing
```bash
# Backend tests
cd apps/api && pytest tests/ -v

# Frontend tests
cd apps/web && npm run test

# With coverage
cd apps/api && pytest tests/ --cov=app
```

### Database
```bash
# Seed demo data
cd apps/api && python -m app.db.seed

# Connect to PostgreSQL
psql postgresql://talnora:talnora_pass@localhost:5432/talnora
```

### Cleanup
```bash
# Stop all services
docker-compose down

# Remove all data (careful!)
docker-compose down -v
```

---

## 🧪 Try It Out (Examples)

### Example 1: Execute a Command via Orchestrator
```bash
curl -X POST http://localhost:8000/api/v1/agents/orchestrator/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Find 50 senior engineers in San Francisco",
    "org_id": "org_123"
  }'

# Response:
# {
#   "status": "planning",
#   "plan_id": "plan_abc123",
#   "agents": ["TalentIntelligence", "Matching", "Screening"],
#   "estimated_duration": 120,
#   "estimated_cost": 0.75
# }
```

### Example 2: Check Cost Tracking
```bash
curl http://localhost:8000/api/v1/agents/costs/summary \
  -H "Authorization: Bearer {your-jwt-token}"

# Shows:
# - Today's spending
# - Monthly spending
# - Breakdown by model
# - Alerts if over budget
```

### Example 3: Generate Analytics Report
```bash
curl -X POST http://localhost:8000/api/v1/agents/reporting/generate \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "kpi",
    "period": "monthly"
  }'

# Shows KPIs like:
# - Open roles
# - Sourced candidates
# - Interviews scheduled
# - Placement rate
# - Time to fill
# - Cost per hire
```

---

## 🔐 Security & Auth

### JWT Token
```python
# Backend creates tokens like:
{
  "sub": "user_123",           # User ID
  "org_id": "org_456",          # Organization
  "role": "Recruiter",          # Role (6 options)
  "exp": 1704067200            # Expires in 24 hours
}

# Use token in API calls:
Authorization: Bearer {token}
```

### Roles & Permissions
```
SuperAdmin       → All permissions
AgencyAdmin      → Jobs, candidates, users, analytics, costs
Recruiter        → Jobs, candidates, analytics
HiringManager    → Read jobs/candidates, analytics
Client           → Read jobs/candidates, analytics
Candidate        → Read jobs
```

---

## 📊 Understanding Cost Tracking

### How Costs Work
- Each LLM call costs money ($0.0001-$0.15 per 1K tokens)
- Platform tracks every call and calculates cost
- Daily/monthly limits prevent overspending
- Alerts when approaching budget limits

### Example Cost Breakdown
```
Job parsing (Claude):           $0.02
Search 1000 candidates (GPT):   $0.15
Score candidates (Claude):      $0.08
Draft outreach (Claude):        $0.10
Total per workflow:             $0.35

Daily budget:                   $100
Monthly budget:                 $2000
```

---

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check if ports are in use
lsof -i :3000    # Frontend
lsof -i :8000    # Backend
lsof -i :5432    # PostgreSQL
lsof -i :6333    # Qdrant

# Kill processes if needed
kill -9 <PID>
```

### LLM API Key Error
```bash
# Make sure LITELLM_API_KEY is set
echo $LITELLM_API_KEY

# Or add to .env
export LITELLM_API_KEY=sk-or-v1-xxx
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose ps db

# Test connection
psql postgresql://talnora:talnora_pass@localhost:5432/talnora

# Check .env DATABASE_URL
cat apps/api/.env | grep DATABASE_URL
```

### Qdrant Vector DB Error
```bash
# Check Qdrant is running
docker-compose ps qdrant

# Check it's responding
curl http://localhost:6333/health

# Dashboard: http://localhost:6333/dashboard
```

---

## 📚 Documentation

- **Architecture:** ARCHITECTURE.md
- **Setup:** SETUP_GUIDE.md
- **Testing:** TESTS.md
- **All Phases:** IMPLEMENTATION_ROADMAP.md
- **File Index:** INDEX.md
- **Directory Map:** DIRECTORY_STRUCTURE.md

---

## 🎯 Next Steps

### Immediate
1. Start services with `docker-compose up`
2. Check API docs at http://localhost:8000/docs
3. Visit frontend at http://localhost:3000
4. Run demo data seeding

### This Week
1. Test workflow execution end-to-end
2. Verify cost tracking is working
3. Test authentication and RBAC
4. Run integration tests

### This Month
1. Connect frontend components to API
2. Deploy to staging environment
3. Load testing and optimization
4. Security hardening

---

## 💡 Pro Tips

### Faster Development
```bash
# Skip docker, run locally
cd apps/api
uvicorn app.main:app --reload

cd apps/web
npm run dev

# Then just docker-compose up with db, qdrant, redis
docker-compose up db qdrant redis
```

### Debug LLM Calls
```bash
# Set log level to debug
export LOG_LEVEL=DEBUG

# Then check logs for LLM request/response
docker-compose logs backend
```

### Monitor Agent Execution
```bash
# Check agent status
curl http://localhost:8000/api/v1/agents/agents/status

# Shows all agents with task counts and latency
```

### Database Inspection
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U talnora talnora

# Common queries:
SELECT * FROM organizations;      # See orgs
SELECT * FROM users;               # See users
SELECT * FROM jobs;                # See jobs
SELECT * FROM candidates;          # See candidates
```

---

## 📞 Support Resources

- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Database Schema:** `infra/supabase/schema.sql`
- **Example Workflows:** `apps/api/app/agents/job_fill_workflow.yaml`
- **Test Cases:** `test_agents.py` and `test_components.tsx`

---

## ✅ Verification Checklist

After starting, verify:
- [ ] Frontend loads at http://localhost:3000
- [ ] Backend API responds at http://localhost:8000/docs
- [ ] PostgreSQL is running: `docker-compose ps db`
- [ ] Qdrant is running: `docker-compose ps qdrant`
- [ ] Redis is running: `docker-compose ps redis`
- [ ] No errors in `docker-compose logs`
- [ ] Demo data seeded: `curl http://localhost:8000/api/v1/jobs`

All green? **You're ready to use Talnora!** 🎉

---

**Last Updated:** 2024  
**Status:** ✅ All 7 phases complete and ready for use
