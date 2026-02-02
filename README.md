# Calculator WebApp

A production-ready FastAPI calculator web application with complete CI/CD pipelines, DevSecOps scanning, Infrastructure as Code (Bicep), and a DevOps metrics dashboard.

[![CI](https://github.com/owner/calculator-webapp/actions/workflows/ci.yml/badge.svg)](https://github.com/owner/calculator-webapp/actions/workflows/ci.yml)
[![CD - Azure Web App](https://github.com/owner/calculator-webapp/actions/workflows/cd-azure-webapp.yml/badge.svg)](https://github.com/owner/calculator-webapp/actions/workflows/cd-azure-webapp.yml)
[![Security](https://github.com/owner/calculator-webapp/actions/workflows/security.yml/badge.svg)](https://github.com/owner/calculator-webapp/actions/workflows/security.yml)

## 🚀 Features

- **FastAPI Application** - Modern Python web framework with automatic OpenAPI documentation
- **RESTful Calculator API** - Add, subtract, multiply, divide operations
- **Comprehensive Testing** - Unit tests with pytest and coverage
- **CI/CD Pipelines** - GitHub Actions for continuous integration and deployment
- **DevSecOps** - Security scanning with CodeQL, Bandit, pip-audit, Gitleaks, and Checkov
- **Infrastructure as Code** - Azure Bicep templates for reproducible deployments
- **Metrics Dashboard** - DevOps/DevSecOps metrics published to GitHub Pages
- **Dependency Management** - Dependabot for automated security updates

## 📁 Project Structure

```
calculator-webapp/
├── app/                          # Application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI entry point
│   ├── calculator.py             # Business logic
│   └── config.py                 # Environment configuration
├── tests/                        # Test suite
│   ├── test_calculator.py        # Unit tests
│   └── test_api.py               # API integration tests
├── metrics/                      # Metrics dashboard generator
│   ├── main.py                   # GitHub API metrics collector
│   ├── render_dashboard.py       # Dashboard renderer
│   └── templates/
│       └── index.html            # Dashboard template
├── infra/                        # Infrastructure as Code
│   ├── main.bicep                # Azure Bicep template
│   ├── params.dev.json           # Dev environment parameters
│   └── README.md                 # Deployment instructions
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                # Continuous Integration
│   │   ├── cd-azure-webapp.yml   # Continuous Deployment
│   │   ├── security.yml          # Security scanning
│   │   ├── metrics-dashboard.yml # Metrics dashboard
│   │   └── infra-deploy.yml      # Infrastructure deployment
│   └── dependabot.yml            # Dependabot configuration
├── requirements.txt              # Runtime dependencies
├── requirements-dev.txt          # Development dependencies
├── pyproject.toml                # Project & tool configuration
├── README.md                     # This file
└── LICENSE                       # MIT License
```

## 🔧 Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/owner/calculator-webapp.git
cd calculator-webapp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run Locally

```bash
# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **OpenAPI Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Run Tests

```bash
# Run all tests with coverage
pytest tests/ --cov=app --cov-report=term-missing -v

# Run specific test file
pytest tests/test_calculator.py -v
```

### Lint Code

```bash
# Check linting
ruff check app/ tests/

# Format code
ruff format app/ tests/
```

## 🌐 API Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/health` | Health check | - |
| POST | `/add` | Add two numbers | `{"a": 5, "b": 3}` |
| POST | `/sub` | Subtract two numbers | `{"a": 10, "b": 4}` |
| POST | `/mul` | Multiply two numbers | `{"a": 6, "b": 7}` |
| POST | `/div` | Divide two numbers | `{"a": 20, "b": 4}` |

### Example Requests

```bash
# Health check
curl http://localhost:8000/health

# Add numbers
curl -X POST http://localhost:8000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 5, "b": 3}'

# Divide (with error handling)
curl -X POST http://localhost:8000/div \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 0}'
# Returns: {"detail": "Division by zero is not allowed"}
```

## ☁️ Azure Deployment

### Prerequisites

1. **Azure Subscription** with permissions to create resources
2. **Azure AD App Registration** configured for OIDC
3. **GitHub Repository** with the following configured:

#### GitHub Secrets (Repository Settings → Secrets)

| Secret Name | Description |
|-------------|-------------|
| `AZURE_CLIENT_ID` | Azure AD Application (client) ID |
| `AZURE_TENANT_ID` | Azure AD Directory (tenant) ID |
| `AZURE_SUBSCRIPTION_ID` | Azure Subscription ID |

#### GitHub Variables (Repository Settings → Variables)

| Variable Name | Description | Example |
|---------------|-------------|---------|
| `AZURE_WEBAPP_NAME` | Name of the Azure Web App | `app-calculator-webapp-dev` |
| `AZURE_RESOURCE_GROUP` | Resource group name | `rg-calculator-webapp-dev` |

### Setting Up Azure OIDC

```bash
# Create Azure AD App Registration
az ad app create --display-name "GitHub-Actions-Calculator-WebApp"

# Get the App ID
APP_ID=$(az ad app list --display-name "GitHub-Actions-Calculator-WebApp" --query "[0].appId" -o tsv)

# Create Service Principal
az ad sp create --id $APP_ID

# Add federated credential for GitHub Actions
az ad app federated-credential create \
  --id $APP_ID \
  --parameters '{
    "name": "github-main-branch",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:owner/calculator-webapp:ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'

# Assign Contributor role to subscription
az role assignment create \
  --assignee $APP_ID \
  --role "Contributor" \
  --scope "/subscriptions/<subscription-id>"
```

### Deploy Infrastructure

1. Go to **Actions** → **Infrastructure Deploy**
2. Click **Run workflow**
3. Select environment (`dev`, `staging`, `prod`)
4. Click **Run workflow**

Or deploy manually:

```bash
az group create --name rg-calculator-webapp-dev --location centralindia

az deployment group create \
  --resource-group rg-calculator-webapp-dev \
  --template-file infra/main.bicep \
  --parameters @infra/params.dev.json
```

## 📊 Enable GitHub Pages (Metrics Dashboard)

1. Go to **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Select branch: `gh-pages` and folder: `/ (root)`
4. Click **Save**
5. Manually trigger the **Metrics Dashboard** workflow or wait for scheduled run

Dashboard URL: `https://<username>.github.io/calculator-webapp/`

## 🔄 Workflow Execution

### Trigger Conditions

| Workflow | PR | Push to main | Schedule | Manual |
|----------|:--:|:------------:|:--------:|:------:|
| CI | ✅ | ✅ | ❌ | ❌ |
| CD - Azure Web App | ❌ | ✅ | ❌ | ❌ |
| Security | ✅ | ✅ | Weekly (Sun) | ❌ |
| Metrics Dashboard | ❌ | ❌ | Every 6h | ✅ |
| Infrastructure Deploy | ❌ | ❌ | ❌ | ✅ |

### Execution Sequence

**On Pull Request:**
1. CI workflow runs (lint + test)
2. Security workflow runs (all scans)

**On Push to main:**
1. CI workflow runs (lint + test)
2. CD workflow runs (test → deploy to Azure)
3. Security workflow runs (all scans)

**Scheduled:**
- Security: Weekly on Sunday at 00:00 UTC
- Metrics Dashboard: Every 6 hours

**Manual:**
- Infrastructure Deploy: Via workflow_dispatch
- Metrics Dashboard: Via workflow_dispatch

## 📈 Metrics Dashboard

The dashboard tracks comprehensive DevOps metrics:

### DORA Metrics
- Deployment frequency (total/successful/failed)
- Change failure rate
- MTTR proxy (time between failure and recovery)

### Flow/Delivery Metrics
- PR throughput (merged PRs)
- PR lead time (created → merged)

### CI/CD Health
- CI success rate
- Average CI duration
- Average deploy duration

### DevSecOps Signals
- Security workflow success rate
- Last security scan status

### Dependency Health
- Open Dependabot PRs
- Merged Dependabot PRs
- Outdated dependency count

## 🔒 Security Features

- **CodeQL** - Static application security testing (SAST)
- **Bandit** - Python-specific security linting
- **pip-audit** - Dependency vulnerability scanning
- **Gitleaks** - Secrets detection
- **Checkov** - Infrastructure as Code security scanning
- **Dependabot** - Automated dependency updates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

All PRs trigger CI and Security workflows automatically.
