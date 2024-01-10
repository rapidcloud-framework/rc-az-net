resource "azurerm_route" "route" {
  name                = local.route_name
  resource_group_name = local.resource_group_name
  route_table_name    = local.route_table_name
  address_prefix      = local.address_prefix
  next_hop_type       = local.next_hop_type
}