terraform {
  required_version = ">=v1.5.0, <2.0.0"

  required_providers {
    conductorone = {
      source  = "ConductorOne/conductorone"
      version = "0.1.1"
    }
  }
}


provider "conductorone" {
  server_url    = "https://<your-tenant>.conductor.one/"
  client_id     = "abc"
  client_secret = "abc"
}


# Example for setting a new alias
resource "conductorone_app_entitlement" "<your-entitlement>" {
  id     = data.external.c1_entitlements.result.<your-entitlement>
  app_id = data.conductorone_app.<your-app>.id
  alias  = "Set Alias by TF via dynamic data source"
}