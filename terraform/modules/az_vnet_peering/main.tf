resource "azurerm_virtual_network_peering" "vnet_peering" {
  name                         = local.name
  resource_group_name          = local.resource_group
  virtual_network_name         = local.virtual_network_name
  remote_virtual_network_id    = local.remote_virtual_network_id
  allow_forwarded_traffic      = local.allow_forwarded_traffic
  allow_virtual_network_access = local.allow_forwarded_traffic
}
