variable "resource_group" {
  type        = string
  description = "Name of resource group to deploy virtual network in."
}

variable "vnet_name" {
  type        = string
  description = "The name of the virtual network that is to be added to the subnet"
}

variable "address_prefix" {
  type        = list(string)
  description = "The address space of the virtual network"
}


variable "name" {
  type        = string
  description = "the unique name for the subnet being created"
}

variable "service_endpoints" {
  type    = list(string)
  default = []
}
