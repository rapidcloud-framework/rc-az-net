locals {
  firewall_name        = var.name
  location             = var.location
  resource_group_name  = var.resource_group
  sku_name             = var.sku_name
  sku_tier             = var.sku_tier
  subnet_id            = var.subnet_id
  public_ip_address_id = var.public_ip_address_id
}
