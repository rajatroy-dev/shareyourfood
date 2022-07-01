variable "environment" {
  type        = string
  description = "Environment (dev / stage / prod)"
}

variable "geo_location" {
  type        = string
  description = "Geo location for CosmosDB"
}

variable "project" {
  type        = string
  description = "Project name"
}

variable "location" {
  type        = string
  description = "Azure region to deploy module to"
}

variable "subscription_id" {
  type        = string
  description = "Azure subscription id"
}

variable "tenant_id" {
  type        = string
  description = "Azure tenant id"
}
