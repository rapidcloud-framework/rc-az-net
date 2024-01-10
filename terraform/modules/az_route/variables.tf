variable "name" {
  description = "The name of the Azure Route resource to create."
  type        = string
}

variable "resource_group" {
  description = "The name of the Azure Resource Group in which to create the Route resource."
  type        = string
}

variable "route_table_name" {
  description = "The name of the Azure Route Table that the Route resource should associate with."
  type        = string
}

variable "address_prefix" {
  description = "The IP address prefix for the destination that this Route resource applies to."
  type        = string
}

variable "next_hop_type" {
  description = "The type of the next hop for the Route resource. Valid values are VirtualNetworkGateway, VnetLocal, Internet, VirtualAppliance, and None."
  type        = string
}