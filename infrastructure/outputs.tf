output "function_app_name" {
  value       = azurerm_linux_function_app.function_app.name
  description = "Deployed function app name"
}

output "function_app_default_hostname" {
  value       = azurerm_linux_function_app.function_app.default_hostname
  description = "Deployed function app hostname"
}

output "cosmosdb_endpoint" {
    value = "https://${data.azurerm_cosmosdb_account.cosmosdb_account.endpoint}.documents.azure.com:443/"
    description = "Azure CosmosDB endpooint"
}

output "cosmosdb_key" {
    value = "${data.azurerm_cosmosdb_account.cosmosdb_account.primary_master_key}"
    description = "Azure CosmosDB endpooint"
}
