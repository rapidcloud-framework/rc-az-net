resource "azurerm_network_ddos_protection_plan" "ddos" {
  name                = local.ddos_plan_name
  location            = local.location
  resource_group_name = local.resource_group_name

  tags = {
    managed = "rc"
  }
}