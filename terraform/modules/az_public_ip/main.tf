resource "azurerm_public_ip" "publicIP" {
  name                = local.public_ip_name
  resource_group_name = local.resource_group_name
  location            = local.location
  allocation_method   = local.allocation_method
  sku                 = var.sku

  tags = {
    managed = "rc"
  }
}