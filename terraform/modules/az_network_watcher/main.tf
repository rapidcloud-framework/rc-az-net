resource "azurerm_network_watcher" "nw" {
  name                = local.nw_name
  location            = local.location
  resource_group_name = local.resource_group_name

  tags = {
    managed = "rc"
  }
}