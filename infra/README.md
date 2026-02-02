# Infrastructure as Code - Bicep

This folder contains the Azure Bicep templates for deploying the Calculator WebApp infrastructure.

## Resources Deployed

- **Log Analytics Workspace** - For Application Insights telemetry storage
- **Application Insights** - Application performance monitoring
- **App Service Plan** - Linux-based hosting plan
- **Azure Web App** - Python 3.11 web application

## Prerequisites

1. [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli) installed
2. [Bicep CLI](https://docs.microsoft.com/azure/azure-resource-manager/bicep/install) installed (or use Azure CLI which includes Bicep)
3. An Azure subscription

## Local Deployment

### 1. Login to Azure

```bash
az login
az account set --subscription "<your-subscription-id>"
```

### 2. Create Resource Group

```bash
az group create \
  --name rg-calculator-webapp-dev \
  --location centralindia
```

### 3. Deploy Infrastructure

```bash
az deployment group create \
  --resource-group rg-calculator-webapp-dev \
  --template-file main.bicep \
  --parameters @params.dev.json
```

### 4. Verify Deployment

```bash
az deployment group show \
  --resource-group rg-calculator-webapp-dev \
  --name main \
  --query properties.outputs
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `baseName` | Base name for all resources | `calculator-webapp` |
| `environment` | Environment (dev/staging/prod) | `dev` |
| `location` | Azure region | Resource group location |
| `appServicePlanSku` | App Service Plan SKU | `B1` |
| `pythonVersion` | Python runtime version | `3.11` |

## Web App Configuration

The deployed Web App is configured with:

- **Startup Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **SCM_DO_BUILD_DURING_DEPLOYMENT**: `true` - Enables Oryx build during ZIP deployment
- **WEBSITES_PORT**: `8000` - Tells Azure the port your app listens on
- **HTTPS Only**: Enabled
- **Minimum TLS Version**: 1.2
- **FTPS State**: Disabled (security best practice)

## Cleanup

To delete all deployed resources:

```bash
az group delete --name rg-calculator-webapp-dev --yes --no-wait
```

## CI/CD Integration

This infrastructure is deployed via GitHub Actions using the `infra-deploy.yml` workflow with:

- Azure OIDC authentication (no secrets stored)
- Manual trigger via `workflow_dispatch`
- Separate from application deployment workflow
