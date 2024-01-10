resource "azurerm_network_watcher_flow_log" "main" {
  network_watcher_name      = var.network_watcher_name
  resource_group_name       = var.resource_group
  name                      = var.name
  location                  = var.location
  network_security_group_id = var.network_security_group_id
  storage_account_id        = var.storage_account_id
  enabled                   = var.enabled

  retention_policy {
    enabled = var.enabled
    days    = var.retention_days
  }

  traffic_analytics {
    enabled               = var.enabled
    workspace_id          = data.azurerm_log_analytics_workspace.main.workspace_id
    workspace_region      = data.azurerm_log_analytics_workspace.main.location
    workspace_resource_id = data.azurerm_log_analytics_workspace.main.id
  }
}

data "azurerm_log_analytics_workspace" "main" {
  name                = var.workspace_id
  resource_group_name = var.resource_group
}
