resource "azurerm_network_security_group" "ns_group" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  tags = {
    managed = "rc"
  }
}

resource "azurerm_network_security_rule" "nsg_rules" {
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.ns_group.name
  for_each                    = { for sg in var.security_rule : sg.name => sg }
  name                        = each.value.name
  description                 = each.value.description
  source_port_range           = each.value.source_port_range
  destination_port_range      = each.value.destination_port_range
  source_address_prefix       = each.value.source_address_prefix
  destination_address_prefix  = each.value.destination_address_prefix
  access                      = each.value.access
  protocol                    = each.value.protocol
  priority                    = each.value.priority
  direction                   = each.value.direction
}
