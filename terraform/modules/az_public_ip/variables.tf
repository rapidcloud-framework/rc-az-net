variable "public_ip_name" {
  description = "The name of the public IP address."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group where the public IP address should be created."
  type        = string
}

variable "location" {
  description = "The location where the public IP address should be created."
  type        = string
}

variable "sku" {
  description = "The SKU Tier that should be used for the Public IP."
  type        = string
}

variable "allocation_method" {
  description = "The allocation method to use for the public IP address."
  type        = string
  default     = "Dynamic"
}
