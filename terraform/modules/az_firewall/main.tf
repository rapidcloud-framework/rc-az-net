resource "azurerm_firewall" "firewall" {
  name                = local.firewall_name
  location            = local.location
  resource_group_name = local.resource_group_name
  sku_name            = local.sku_name
  sku_tier            = local.sku_tier
  # ip_configuration {
  #   name                 = local.firewall_name
  #   subnet_id            = local.subnet_id
  #   public_ip_address_id = local.public_ip_address_id
  # }
}

