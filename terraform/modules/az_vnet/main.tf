resource "azurerm_virtual_network" "vnet" {
  name                = local.vnet_name
  location            = local.location
  resource_group_name = local.resource_group_name
  address_space       = local.address_space
  dns_servers         = local.dns_servers
  tags = {
    managed = "rc"
  }
}
