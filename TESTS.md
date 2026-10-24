# Tests README

## Test Suites

### Backend Tests (Pytest)

Location: `test_agents.py`

Tests for agent implementations:
- Job description parser
- Candidate scoring
- Embedding operations
- Workflow orchestration

**Running:**
```bash
cd apps/api
pytest test_agents.py -v
pytest test_agents.py --cov=app --cov-report=html
```

**Coverage Target:** 80%+

### Frontend Tests (Vitest)

Location: `test_components.tsx`

Tests for React components:
- KPI Cards (metrics, trends)
- Agent Control Center (status, task queues)
- Candidate Pipeline Funnel (stages, percentages)
- Copilot Chat Panel (messaging, API calls)
- Autonomy Mode Selector (level selection, persistence)

**Running:**
```bash
cd apps/web
npm run test
npm run test -- --coverage
```

## Test Structure

Each test follows the Arrange-Act-Assert pattern:

1. **Arrange** - Set up test data and mocks
2. **Act** - Execute the code being tested
3. **Assert** - Verify the results

## Mocking

### Backend
- Mock LLM clients (LiteLLM)
- Mock Qdrant vector database
- Mock external services

### Frontend
- Mock API calls with vi.fn()
- Mock React components
- Mock localStorage

## Best Practices

✅ Use descriptive test names
✅ Test both happy path and error cases
✅ Keep tests isolated and independent
✅ Mock external dependencies
✅ Maintain 80%+ code coverage
✅ Run tests before committing

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Daily scheduled runs

Build fails if coverage < 80% or tests fail.
