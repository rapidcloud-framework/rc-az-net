resource "azurerm_dns_zone" "dns_zone" {
  name                = local.domain_name
  resource_group_name = local.resource_group_name
  tags = {
    managed = "rc"
  }
}

output "id" {
  value = azurerm_dns_zone.dns_zone.id
}

output "name" {
  value = azurerm_dns_zone.dns_zone.name
}