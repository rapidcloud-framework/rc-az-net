resource "azurerm_subnet" "azure_subnets" {
  name                 = local.azure_subnet_name
  resource_group_name  = local.resource_group_name
  virtual_network_name = local.vnet_name
  address_prefixes     = local.address_prefix
  service_endpoints    = length(var.service_endpoints) > 0 ? var.service_endpoints : null
}
