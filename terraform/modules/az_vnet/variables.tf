variable "resource_group" {
  type        = string
  description = "Name of resource group to deploy virtual network in."
}

variable "location" {
  type        = string
  description = "The location where the virtual network will be created"
}

variable "name" {
  type        = string
  description = "The name of the virtual network"
}

variable "address_space" {
  type        = list(string)
  description = "The address space of the virtual network"
  default     = ["10.0.0.0/16"]
}

variable "dns_servers" {
  type        = list(string)
  description = "The list of DNS servers for the virtual network"
  default     = null
}
