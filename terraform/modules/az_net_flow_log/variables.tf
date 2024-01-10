
variable "name" {
  type        = string
  description = "The name of the virtual network peering"
}

variable "location" {
  type = string
}

variable "network_watcher_name" {
  type = string
}
variable "resource_group" {
  type = string
}

variable "network_security_group_id" {
  type = string
}

variable "storage_account_id" {
  type = string
}

variable "enabled" {
  type    = bool
  default = true

}

variable "retention_days" {
  type    = number
  default = 7
}

variable "workspace_id" {
  type = string
}



