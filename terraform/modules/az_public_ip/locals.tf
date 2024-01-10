locals {
  public_ip_name         = var.public_ip_name
  resource_group_name    = var.resource_group_name
  location               = var.location
  allocation_method      = var.sku == "Standard" ? "Static" : var.allocation_method
}