terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "resource_group" {
  name     = "${var.project}-${var.environment}-resource-group"
  location = var.location
}

resource "azurerm_network_security_group" "vnet_nsg" {
  name                = "${var.project}-${var.environment}-vnet-nsg"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.project}-${var.environment}-vnet"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name

  address_space = ["10.0.0.0/16"]
  subnet {
    name           = "default"
    address_prefix = "10.0.0.0/24"
    security_group = azurerm_network_security_group.vnet_nsg.id
  }
}

resource "azurerm_storage_account" "storage_account" {
  name                = "${var.project}${var.environment}storage"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name

  account_replication_type = "LRS"
  account_tier             = "Standard"
}

resource "azurerm_service_plan" "app_service_plan" {
  name                = "${var.project}-${var.environment}-app-service-plan"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name

  os_type  = "Linux"
  sku_name = "Y1" # https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/service_plan#sku_name
}

resource "azurerm_linux_function_app" "function_app" {
  name                = "${var.project}-${var.environment}-function-app"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name

  service_plan_id      = azurerm_service_plan.app_service_plan.id
  storage_account_name = azurerm_storage_account.storage_account.name

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = ""
  }

  site_config {
    application_stack {
      python_version = 3.9
    }
    use_32_bit_worker = false
  }

  lifecycle {
    ignore_changes = [
      app_settings["WEBSITE_RUN_FROM_PACKAGE"]
    ]
  }
}

data "azurerm_cosmosdb_account" "cosmosdb_account" {
  name                = "${var.project}-${var.environment}-cosmosdb-account"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name

  consistency_policy {
    consistency_level = "Strong"
  }
  enable_free_tier = true
  geo_location {
    location          = var.geo_location
    failover_priority = 0
  }
  offer_type = "Standard"
  virtual_network_rule {
    id = azurerm_virtual_network.vnet.id
  }
}

resource "azurerm_cosmosdb_sql_database" "cosmosdb_sql" {
  account_name        = data.azurerm_cosmosdb_account.cosmosdb_account
  name                = "${var.project}-${var.environment}-cosmosdb-sql"
  resource_group_name = azurerm_resource_group.resource_group.name

  throughput = 400
}

resource "azurerm_cosmosdb_sql_container" "cosmosdb_sql_container" {
  account_name        = data.azurerm_cosmosdb_account.cosmosdb_account
  name                = "${var.project}-${var.environment}-cosmosdb-sql-container"
  resource_group_name = azurerm_resource_group.resource_group.name

  database_name      = azurerm_cosmosdb_sql_database.cosmosdb_sql.name
  partition_key_path = "/message_type"
  throughput         = 400
}
