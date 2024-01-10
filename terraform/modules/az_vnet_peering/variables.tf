variable "resource_group" {
  type        = string
  description = "Name of resource group to deploy virtual network in."
}

variable "virtual_network_name" {
  type = string
}

variable "remote_virtual_network_id" {
  type = string

}

variable "name" {
  type        = string
  description = "The name of the virtual network peering"
}

variable "allow_forwarded_traffic" {
  type    = bool
  default = false
}

variable "allow_virtual_network_access" {
  type    = bool
  default = true
}
