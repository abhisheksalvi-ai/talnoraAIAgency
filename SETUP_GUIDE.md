# Talnora AI Recruitment Agency - Setup Guide

## Resolving scikit-learn Installation Issues on Windows

The error you encountered is a common issue when installing scikit-learn from source on Windows due to missing build dependencies or compiler compatibility issues.

### Solutions:

#### Option 1: Use Pre-compiled Wheels (Recommended)
Instead of building from source, install a pre-compiled wheel:

```bash
# First uninstall any partially installed version
pip uninstall scikit-learn

# Install from official wheel repository
pip install scikit-learn==1.5.0 --only-binary :all:
```

Or use the conda package manager (if you have Anaconda/Miniconda installed):
```bash
conda install scikit-learn=1.5.0
```

#### Option 2: Install Build Dependencies
If you prefer to build from source, install the required build tools:

1. Install Microsoft C++ Build Tools:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Select "Desktop development with C++" workload

2. Install Rust (needed for some dependencies):
   - https://www.rust-lang.org/tools/install

3. Then try installing scikit-learn again:
   ```bash
   pip install scikit-learn==1.3.2
   ```

#### Option 3: Use a Newer Version
Newer versions of scikit-learn have better Windows support:
```bash
pip install scikit-learn>=1.5.0
```

Note: I've temporarily commented out scikit-learn in requirements.txt. You'll need to install it separately after setting up the environment.

## Complete Setup Instructions

### 1. Environment Setup
```bash
# Copy environment templates
cd apps/api
cp .env.example .env
cd ../web
cp .env.example .env.local

# Edit the .env files with your configuration
# See the examples in the files for what to set
```

### 2. Install Dependencies

#### Backend
```bash
cd apps/api
pip install -r requirements.txt

# Install scikit-learn separately (using one of the methods above)
# Example using wheels:
pip install scikit-learn==1.5.0 --only-binary :all:
```

#### Frontend
```bash
cd apps/web
npm install
```

### 3. Set Up External Services

#### Option A: Using Docker Compose (Recommended)
```bash
# From project root
docker-compose up --build

# Wait for services to start, then:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

#### Option B: Manual Setup
If you prefer to run services locally:

1. **PostgreSQL**: 
   - Install PostgreSQL 15+
   - Create database 'talnora' 
   - Create user 'talnora' with password 'talnora_pass'
   - Or modify the .env file to match your local setup

2. **Qdrant**:
   - Download from: https://qdrant.tech/documentation/quick-start/
   - Or run with Docker: `docker run -p 6333:6333 qdrant/qdrant`

3. **Redis**:
   - Install Redis or run with Docker: `docker run -p 6379:6379 redis:7-alpine`

### 4. Database Setup

If using Docker Compose, the database will be initialized automatically.

If setting up manually:
```bash
# Apply the Supabase schema to your PostgreSQL database
psql -h localhost -U talnora -d talnora < infra/supabase/schema.sql
```

### 5. Running the Application

#### With Docker Compose
```bash
docker-compose up
# Services available at:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
```

#### Local Development
```bash
# Backend (in one terminal)
cd apps/api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
cd apps/web
npm run dev
```

## Troubleshooting

### "int_t is not a type identifier" error with scikit-learn
This is a known issue with older scikit-learn versions on Windows. Use one of the solutions above.

### Module not found errors
Make sure you're installing packages in the correct environment and that your PATH is set correctly.

### Port conflicts
If ports 3000, 8000, 5432, 6333, or 6379 are in use, either:
- Change the port in the configuration files
- Stop the conflicting services
- Use different ports in docker-compose.yml

## Getting Started with Development

Once the environment is running, you can begin implementing features following the MVP roadmap:

1. **Complete IAM module**: Add email verification, password reset, and MFA preparation
2. **Organization module**: Implement team structures and cross-organization permissions
3. **Job module**: Build CRUD operations and basic job description parsing
4. **Candidate module**: Implement resume upload and basic profile management
5. **Resume Intelligence Agent**: Create your first AI agent for resume parsing

Refer to the architecture documents in the project root for detailed guidance on each module.

## Important Notes

- The project uses a modular monolith architecture designed for easy migration to microservices later
- All AI agents will be built using LangGraph for orchestration
- Vector search is powered by Qdrant for semantic matching capabilities
- Multi-tenancy is implemented using Row Level Security in PostgreSQL
- The frontend uses Next.js 15 with Tailwind CSS and ShadCN UI for a modern, responsive interface

For any questions, refer to the architecture documents or check the GitHub repository for updates.