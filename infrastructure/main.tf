terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "resource_group" {
  name = "${var.project}-${var.environment}-resource-group"
  location = var.location
}

resource "azurerm_storage_account" "storage_account" {
  name = "${var.project}${var.environment}storage"
  resource_group_name = azurerm_resource_group.resource_group.name
  location = var.location

  account_tier = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "app_service_plan" {
  name                = "${var.project}-${var.environment}-app-service-plan"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = var.location

  os_type             = "Linux"
  sku_name            = "Y1" # https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/service_plan#sku_name
}

resource "azurerm_linux_function_app" "example" {
  name                = "${var.project}-${var.environment}-function-app"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = var.location

  storage_account_name = azurerm_storage_account.storage_account.name
  service_plan_id      = azurerm_service_plan.app_service_plan.id

  site_config {
      application_stack = {
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