resource "azurerm_private_dns_zone" "private_dns" {
  name                = local.private_domain_name
  resource_group_name = local.resource_group_name
  tags = {
    managed = "rc"
  }
}