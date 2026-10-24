# Talnora AI Recruitment Agency - Master Architecture Document

## Executive Summary
Talnora is an AI-powered recruitment agency SaaS platform where autonomous AI agents perform sourcing, outreach, screening, interviewing, ranking, and candidate lifecycle management. Built as a modular monolith with clean boundaries for future microservice extraction, leveraging open-source, free-tier friendly technologies.

## Core Architecture Principles
- **Domain Driven Design** with clear bounded contexts
- **Clean/Hexagonal Architecture** separation of concerns
- **CQRS** for read/write separation where beneficial
- **Event-Driven Internal Architecture** using internal messaging
- **AI Agent Architecture** with LangGraph orchestration
- **API First Design** with comprehensive OpenAPI specs
- **Multi-Tenant** by design with Row Level Security
- **Production Ready** with observability, security, and testing

## Bounded Contexts (Modules)

### 1. Identity & Access Management (IAM)
**Responsibilities:** User authentication, authorization, role management, session handling
**Key Features:**
- Email/password login, OAuth (Google, GitHub)
- Role-based access control (Super Admin, Agency Admin, Recruiter, Hiring Manager, Client, Candidate)
- MFA readiness
- JWT token management
- Permission system based on resources and actions

### 2. Organization Management
**Responsibilities:** Tenant and team management within the platform
**Key Features:**
- Organization creation and management
- Team structures within organizations
- Recruiter and client role assignments
- Cross-organization permissions (for agencies managing multiple clients)
- Billing and subscription metadata

### 3. Job Management
**Responsibilities:** Job requisition lifecycle and AI-enhanced job description processing
**Key Features:**
- CRUD operations for job requisitions
- Job cloning and archiving
- Resume/CV upload for reference jobs
- AI Features:
  - JD parsing and structuring
  - Skill/experience/salary extraction
  - AI-generated JD templates
  - JD optimization suggestions
  - Market salary benchmarking (future)

### 4. Candidate Management
**Responsibilities:** Candidate profile lifecycle and talent pool management
**Key Features:**
- Candidate profile creation and enrichment
- Resume upload and parsing
- Timeline view of candidate interactions
- Notes and activity history
- Talent pool creation and management
- Duplicate candidate detection
- GDPR/PIPEDA compliance features (data export/deletion)

### 5. Resume Intelligence Engine
**Responsibilities:** AI-powered resume understanding and structuring
**Key Features:**
- Resume parsing (PDF, DOCX, TXT)
- Skill extraction and normalization
- Employment history extraction
- Certification and license extraction
- Education extraction
- Output: Structured JSON resume representation
- Storage of both parsed resume and vector embeddings
- Confidence scoring for extracted fields

### 6. AI Matching Engine
**Responsibilities:** Semantic candidate-job matching with explainability
**Key Features:**
- Bidirectional matching (candidate→job and job→candidate)
- Multi-factor scoring:
  - Skills match (semantic and keyword)
  - Experience level matching
  - Location compatibility
  - Salary expectation alignment
  - Certification/license matching
  - Cultural fit indicators (future)
- Explainable AI: Clear breakdown of match score components
- Missing skills identification
- Strengths and risk assessment
- Match score thresholds for auto-shortlisting

### 7. Headhunter Agent
**Responsibilities:** Proactive candidate discovery and talent sourcing
**Key Features:**
- Search internal talent database
- Rank candidates by match score
- Future: LinkedIn Recruiter-like search capabilities
- Boolean search capabilities
- Saved search alerts
- Candidate recommendation engine
- Automated shortlist generation
- Diversity-aware sourcing options

### 8. Outreach Agent
**Responsibilities:** Automated, personalized candidate communication
**Key Features:**
- Personalized email generation using candidate/job context
- Multi-step outreach sequences
- A/B testing for message templates
- Tone optimization (formal, casual, enthusiastic)
- Follow-up automation based on engagement
- LinkedIn message integration (future)
- Email performance tracking (open/click rates)
- Compliance with anti-spam regulations

### 9. Scheduling Agent
**Responsibilities:** Interview coordination and calendar management
**Key Features:**
- Google Calendar and Outlook integration
- Automated interview scheduling based on availability
- Calendar sync and conflict detection
- Reminder notifications (email/SMS)
- Rescheduling capabilities
- Time zone intelligence
- Interview type configuration (screening, technical, final)

### 10. AI Interview Agent
**Responsibilities:** Conducting and analyzing candidate interviews
**Key Features (Phase 1 - Chat):**
- Structured conversational interviews
- Adaptive questioning based on resume/job
- Real-time transcript generation
- Sentiment and engagement analysis
- Technical skill assessment through dialogue
- Output: Interview transcript, summary, score, and recommendation
**Future (Phase 2 - Voice):**
- Voice-to-text transcription
- Speech pattern analysis
- Video interview capabilities

### 11. Screening Agent
**Responsibilities:** Automated resume and candidate evaluation
**Key Features:**
- Resume screening against job requirements
- Ranking candidates by qualifications
- Interview screening (post-chat/voice interview)
- Decision outcomes: Pass/Hold/Reject with reasoning
- Configurable screening criteria
- Bias detection and mitigation
- Learning from recruiter feedback

### 12. Submission Agent
**Responsibilities:** Generating client-ready candidate submissions
**Key Features:**
- Candidate summary generation
- Submission report creation
- Candidate packet assembly (resume, cover letter, assessments)
- PDF export with branding
- Customizable submission templates
- Tracking of submission status
- Client feedback collection

### 13. Placement Management
**Responsibilities:** Tracking offers, acceptances, and successful placements
**Key Features:**
- Offer creation and management
- Offer acceptance tracking
- Placement confirmation
- Time-to-hire metrics
- Placement rate analytics
- Offer acceptance rate tracking
- Post-placement follow-up scheduling
- Revenue tracking (for agency model)

### 14. Analytics & Reporting
**Responsibilities:** Platform performance and recruitment metrics
**Key Features:**
- Pipeline health visualization
- Recruiter performance metrics
- Candidate funnel analysis
- Revenue and placement tracking
- Source effectiveness analytics
- Time-in-stage analysis
- Custom report builder
- Executive dashboard
- Scheduled report delivery

### 15. Talnora Orchestrator (AI Agent System)
**Responsibilities:** Central AI coordination and workflow execution
**Key Features:**
- LangGraph-based agent orchestration
- Task routing to appropriate agents
- Workflow execution management
- Agent communication via events
- Retry logic with exponential backoff
- Short-term and long-term memory
- Human-in-the-loop escalation
- Natural language command interface (Talnora Command Center)

## Technical Architecture

### Modular Monolith Structure
```
talnora/
├── apps/
│   ├── web/                  # Next.js frontend
│   └── api/                  # FastAPI backend
├── packages/
│   ├── shared/               # TypeScript/JavaScript shared utilities
│   ├── sdk/                  # Generated API client SDK
│   └── ui/                   # Shared UI component library
├── modules/                  # Bounded contexts as modules
│   ├── iam/
│   ├── organization/
│   ├── job/
│   ├── candidate/
│   ├── resume_intelligence/
│   ├── matching/
│   ├── headhunter/
│   ├── outreach/
│   ├── scheduling/
│   ├── interview/
│   ├── screening/
│   ├── submission/
│   ├── placement/
│   ├── analytics/
│   └── orchestrator/
├── infra/                    # Infrastructure as code
│   ├── docker/
│   ├── kubernetes/           # Future
│   └── terraform/            # Future
├── docs/
├── tests/
└── scripts/
```

### Database Schema (Supabase PostgreSQL)
**Multi-Tenant Approach:** Each organization gets isolated data via Row Level Security (RLS) policies on `organization_id` column.

**Core Tables:**
- `organizations`: id, name, domain, settings, created_at, updated_at
- `organization_users`: id, organization_id, user_id, role, invited_at, accepted_at
- `users`: Supabase Auth users table (extended with profile fields)
- `jobs`: id, organization_id, title, description, location, salary_range, status, created_at, updated_at
- `candidates`: id, organization_id, first_name, last_name, email, phone, current_title, current_company, created_at, updated_at
- `candidate_profiles`: id, candidate_id, parsed_resume_json, resume_embedding_id (Qdrant), skills_array, experience_years, education_array, certifications_array
- `job_embeddings`: id, job_id, embedding_vector_id (Qdrant)
- `applications`: id, job_id, candidate_id, status, applied_at, updated_at
- `interviews`: id, application_id, type, scheduled_at, conducted_at, status, transcript, summary, score, recommendation
- `workflow_executions`: id, workflow_type, entity_id (job/candidate), status, started_at, completed_at, steps_json
- `agent_tasks`: id, agent_type, task_description, status, priority, created_at, assigned_at, completed_at, result_json
- `communications`: id, application_id, channel (email/linkedin/sms), direction (in/out), content, sent_at, opened_at, clicked_at
- `notes`: id, entity_type, entity_id, author_id, content, created_at
- `talent_pools`: id, organization_id, name, description, created_at
- `talent_pool_candidates`: id, talent_pool_id, candidate_id, added_at
- `audit_logs`: id, organization_id, user_id, action, resource_type, resource_id, changes_json, ip_address, user_agent, timestamp

**Indexes:** Organization_id on all tenant-scoped tables, foreign key indexes, full-text search on relevant text fields, GIN indexes on array fields.

### Qdrant Vector Database Design
**Collections:**
1. `candidate_embeddings`: Stores resume embeddings for semantic search
   - Vector size: 1536 (OpenAI ada-002) or 768 (depending on model choice via LiteLLM)
   - Payload: candidate_id, organization_id, skills_array, experience_years, current_title
   - Indexing: HNSW for efficient similarity search

2. `job_embeddings`: Stores job description embeddings
   - Same vector size as candidate embeddings
   - Payload: job_id, organization_id, title, location, salary_range, required_skills_array

3. `interview_embeddings`: (Future) Stores interview transcript embeddings for analysis

**Search Capabilities:**
- Candidate-to-job: Find candidates similar to a job embedding
- Job-to-candidate: Find jobs similar to a candidate embedding
- Candidate-to-candidate: Find similar candidates (for talent pooling)
- Hybrid search: Combine vector similarity with metadata filtering (location, experience, etc.)

### LangGraph Agent Architecture
**Agent Types:**
1. **JobAgent**: Handles job creation, parsing, optimization
2. **ResumeAgent**: Handles resume processing, embedding generation
3. **MatchingAgent**: Performs candidate-job matching with explainability
4. **HeadhunterAgent**: Proactive talent search and recommendation
5. **OutreachAgent**: Generates and sends personalized communications
6. **SchedulingAgent**: Manages interview scheduling and reminders
7. **InterviewAgent**: Conducts chat interviews and generates analysis
8. **ScreeningAgent**: Makes pass/hold/reject decisions with reasoning
9. **ReportingAgent**: Generates analytics and reports
10. **TalnoraOrchestrator**: Master coordinator

**Communication Pattern:**
- Agents communicate via internal event bus (using Redis or PostgreSQL NOTIFY/LISTEN initially)
- Each agent exposes tools/functions that the orchestrator can call
- LangGraph manages state, memory, and workflow execution
- Human-in-the-loop checkpoints for critical decisions

**Memory System:**
- Short-term: Conversation context within a workflow
- Long-term: Entity memories (candidates, jobs) stored in database
- Semantic memory: Vector embeddings for similarity recall

### API Contracts (Backend - FastAPI)
**API Design Principles:**
- RESTful resource-oriented design
- JSON:API specification compliance
- Comprehensive OpenAPI 3.0 documentation
- Versioned API (/api/v1/)
- Standard HTTP status codes
- Pagination, filtering, sorting on list endpoints
- WebSocket endpoints for real-time updates

**Key Endpoints Examples:**
```
GET /api/v1/organizations/{org_id}/jobs
POST /api/v1/organizations/{org_id}/jobs
GET /api/v1/jobs/{job_id}/matches?limit=50&min_score=0.8
POST /api/v1/candidates/{candidate_id}/screen
POST /api/v1/outreach/sequences
POST /api/v1/agent/headhunter/search
GET /api/v1/analytics/pipeline/{org_id}
WS /api/v1/realtime/{org_id}/activities
```

### Frontend Architecture (Next.js 15)
**Structure:**
```
apps/web/
├── app/                    # App Router
│   ├── (dashboard)/        # Authenticated routes
│   │   ├── dashboard/
│   │   ├── jobs/
│   │   ├── candidates/
│   │   ├── analytics/
│   │   └── settings/
│   ├── auth/               # Public auth routes
│   │   ├── sign-in/
│   │   └── sign-up/
│   ├── api/                # API routes (proxy to backend)
│   └── components/         # Shared components
├── components/             # Reusable UI components
├── lib/                    # Utilities, hooks, services
├── styles/                 # Global styles, Tailwind config
├── public/                 # Static assets
└── tailwind.config.js
```

**State Management:**
- Zustand for global application state (user, org, preferences)
- TanStack Query for server state (data fetching, caching, mutations)
- Form state managed by React Hook Form with Zod validation

**UI Library:**
- ShadCN UI primitives (built on Radix UI)
- Custom component library extending ShadCN
- Framer Motion for animations
- Lucide icons
- Recharts for data visualization

### Design System & UI Components
**Foundations:**
- **Tokens:** Color, spacing, typography, shadow, radius (defined in Tailwind config)
- **Primitives:** Button, Input, Textarea, Select, Checkbox, Radio, Toggle, Avatar, Badge, Toast, Tooltip, Dropdown Menu
- **Components:** Data Table, Kanban Board, Card, Timeline, Progress Bar, Skeleton Loader, Empty State
- **AI-Specific Components:** 
  - AI Chat Interface (for Talnora Command Center)
  - Agent Status Panel
  - Workflow Visualization
  - Match Score Breakdown
  - Candidate Summary Card
  - Job Overview Card
  - Analytics Dashboard Widgets

**Theme:**
- Dark mode first with light mode support
- Premium, minimal, executive-grade aesthetic
- Inter/Geist font pairing
- Thoughtful spacing and elevation
- Smooth transitions and micro-interactions

### Security Model
**Authentication:**
- Supabase Auth with JWT
- Session management with refresh tokens
- OAuth providers: Google, GitHub
- Email/password with secure password policies

**Authorization:**
- RBAC with fine-grained permissions
- Resource-based access control (organization-scoped)
- Role hierarchy: Super Admin > Agency Admin > Recruiter/Hiring Manager/Client/Candidate
- Permission checking at API gateway and service layers

**Data Protection:**
- TLS 1.2+ for all transit
- Encryption at rest for sensitive fields (PII) using Supabase encryption
- Secure file storage (Supabase Storage) with signed URLs
- Regular security scanning and dependency updates

**Compliance:**
- GDPR/PIPEDA readiness: data export, deletion, consent tracking
- Audit logging of all privileged actions
- Data retention policies
- Input validation and sanitization to prevent injection
- CSRF protection
- Rate limiting and DDoS protection

### Observability
**Logging:**
- Structured JSON logging with correlation IDs
- Log levels: DEBUG, INFO, WARN, ERROR
- Centralized logging (future: ELK stack or similar)
- Audit logs for compliance

**Metrics:**
- Prometheus-compatible metrics endpoint
- Key metrics: API latency, error rates, agent execution times, LLM token usage/costs, database query performance
- Business metrics: placements per month, time-to-hire, conversion funnel

**Tracing:**
- OpenTelemetry instrumentation for distributed tracing
- Trace ID propagation across services
- Future: Jaeger or Tempo backend

**Health Checks:**
- Liveness and readiness probes
- Dependency health (database, Qdrant, external APIs)
- Custom business health metrics

### Technology Choices Justification

#### Why This Stack?
- **Next.js 15:** Industry standard for React SSR, excellent DX, App Router
- **FastAPI:** High performance, automatic OpenAPI, Python ecosystem for AI/ML
- **Supabase:** Open-source Firebase alternative, built-in Postgres, Auth, Storage
- **Qdrant:** Purpose-built vector database, excellent performance, open-source
- **LangGraph:** State-of-the-art for agent orchestration, deterministic workflows
- **LiteLLM:** Unified interface to 100+ LLMs, enables model switching/fallback
- **Tailwind/ShadCN/Radix:** Modern, accessible, customizable UI components
- **Zustand/TanStack Query:** Excellent state management solutions
- **Docker Compose:** Simple local/dev deployment, production-ready containers

#### Why Modular Monolith?
- **Simplicity:** Single deployable unit, easier debugging/refactoring initially
- **Performance:** No network latency between modules
- **Development Speed:** Faster iteration without distributed system complexity
- **Clear Boundaries:** Well-defined interfaces enable future microservice extraction
- **Operational Simplicity:** Single logging, monitoring, deployment pipeline
- **Cost-Effective:** Minimal infrastructure overhead for startup

## MVP Roadmap (Phase 1 - 3 Months)
**Goal:** Launchable core platform with AI matching and basic workflow

**Month 1: Foundation & Core Modules**
- Week 1-2: Setup repos, CI/CD, DevOps (Docker Compose)
- Week 3-4: IAM module (auth, roles, permissions)
- Week 5-6: Organization module (multi-tenant foundation)
- Week 7-8: Job module (CRUD, basic JD parsing)
- Week 9-10: Candidate module (CRUD, resume upload)
- Week 11-12: Resume Intelligence Engine (parsing, structuring)

**Month 2: AI Core & Matching**
- Week 1-3: AI Matching Engine (vector search, scoring)
- Week 4-5: Headhunter Agent (internal search)
- Week 6-7: Outreach Agent (basic email templates)
- Week 8-9: Screening Agent (rule-based pass/hold/reject)
- Week 10-12: Submission Agent (basic report generation)

**Month 3: Workflow & Polish**
- Week 1-2: Scheduling Agent (Calendar integration)
- Week 3-4: AI Interview Agent (chat-based)
- Week 5-6: Placement Management
- Week 7-8: Analytics Dashboard (core metrics)
- Week 9-10: Talnora Orchestrator (basic workflow orchestration)
- Week 11-12: UI/UX polish, testing, bug fixing, beta prep

## Implementation Roadmap (Post-MVP)
**Phase 2 (Months 4-6): Scaling & Intelligence**
- Enhanced AI models (fine-tuning, domain-specific)
- LinkedIn Recruiter integration (Phase 1)
- Advanced analytics and predictive features
- Mobile responsiveness optimization
- Performance optimization and load testing
- SOC 2 Type 1 preparation

**Phase 3 (Months 7-9): Enterprise Features**
- Advanced workflow automation
- Custom AI model training (organization-specific)
- Comprehensive reporting and BI export
- SSO (SAML, Azure AD)
- Advanced security features (DLP, IRM)
- SOC 2 Type 2 and ISO 27001 preparation

**Phase 4 (Months 10-12): Platform & Ecosystem**
- Public API and webhooks
- Marketplace for integrations
- Advanced customization (white-labeling)
- Kubernetes deployment readiness
- Global multi-region deployment
- Partner and agency portal

## Success Metrics (Post-Launch)
- **Technical:** 99.9% uptime, <200ms API p95 latency, <5% error rate
- **Business:** Time-to-hire reduction of 40% for users, placement rate increase of 25%
- **Adoption:** 70% feature usage rate, <10% churn in first 90 days
- **AI Effectiveness:** Match score correlation with successful placements >0.7

## Next Steps
1. Review this architecture document
2. Begin implementation with foundational modules (IAM, Organization)
3. Set up development environment with Docker Compose
4. Create initial database schema in Supabase
5. Begin building the Next.js frontend with authentication flows

---
*Document Version: 1.0*
*Date: 2026-05-31*
*Prepared for: Talnora AI Recruitment Agency Platform Development*