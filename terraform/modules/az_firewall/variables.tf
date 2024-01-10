variable "name" {
  description = "Name of the Azure Firewall"
  type        = string
}

variable "location" {
  description = "Location where the Azure Firewall will be deployed"
  type        = string
}

variable "resource_group" {
  description = "Name of the Azure resource group where the Azure Firewall will be deployed"
  type        = string
}

variable "sku_name" {
  description = "Name of the Azure Firewall SKU"
  type        = string
}

variable "sku_tier" {
  description = "Tier of the Azure Firewall SKU"
  type        = string
}

variable "subnet_id" {
  description = "ID of the subnet where the Azure Firewall will be deployed"
  type        = string
  default     = null
}

variable "public_ip_address_id" {
  description = "ID of the public IP address to associate with the Azure Firewall"
  type        = string
  default     = null
}
