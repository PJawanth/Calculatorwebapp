// ============================================================================
// Calculator WebApp Infrastructure
// Deploys: Linux App Service Plan + Python Web App + Application Insights
// ============================================================================

@description('Base name for all resources')
param baseName string = 'calculator-webapp'

@description('Environment name')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('App Service Plan SKU')
param appServicePlanSku string = 'B1'

@description('Python version')
param pythonVersion string = '3.11'

// ============================================================================
// Variables
// ============================================================================

var resourceSuffix = '${baseName}-${environment}'
var appServicePlanName = 'asp-${resourceSuffix}'
var webAppName = 'app-${resourceSuffix}'
var appInsightsName = 'ai-${resourceSuffix}'
var logAnalyticsName = 'log-${resourceSuffix}'

// ============================================================================
// Log Analytics Workspace (required for App Insights)
// ============================================================================

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// ============================================================================
// Application Insights
// ============================================================================

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// ============================================================================
// App Service Plan (Linux)
// ============================================================================

resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: appServicePlanSku
  }
  properties: {
    reserved: true // Required for Linux
  }
}

// ============================================================================
// Web App
// ============================================================================

resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|${pythonVersion}'
      alwaysOn: true
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      http20Enabled: true
      appCommandLine: 'python -m uvicorn app.main:app --host 0.0.0.0 --port 8000'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'APP_NAME'
          value: baseName
        }
        {
          name: 'ENV'
          value: environment
        }
      ]
    }
  }
}

// ============================================================================
// Outputs
// ============================================================================

@description('The name of the deployed web app')
output webAppName string = webApp.name

@description('The default hostname of the web app')
output webAppHostname string = webApp.properties.defaultHostName

@description('The URL of the web app')
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'

@description('Application Insights Instrumentation Key')
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey

@description('Application Insights Connection String')
output appInsightsConnectionString string = appInsights.properties.ConnectionString
