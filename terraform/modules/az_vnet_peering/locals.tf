locals {
  name                         = var.name
  resource_group               = var.resource_group
  virtual_network_name         = var.virtual_network_name
  remote_virtual_network_id    = var.remote_virtual_network_id
  allow_forwarded_traffic      = var.allow_forwarded_traffic
  allow_virtual_network_access = var.allow_virtual_network_access
}
