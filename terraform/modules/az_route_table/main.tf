
resource "azurerm_route_table" "route_table" {
  name                          = local.route_table_name
  location                      = local.location
  resource_group_name           = local.resource_group_name

  tags = {
    managed = "rc"
  }
}