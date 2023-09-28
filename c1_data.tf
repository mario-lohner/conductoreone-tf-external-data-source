data "external" "c1_entitlements" {
  program = ["python3", "c1_entitlements.py"]

  query = {
    client_id = "abc"                               # ConductoreOne Client ID
    client_secret = "abc"                           # ConductoreOne Client Secret
    okta_app_id = "2USyZXqzTbgLUENL2sPK63KOWPr"     # ConductoreOne AppId for query entitlements
    c1_url = "https://<your-tenant>.conductor.one"  # ConductoreOne Base URL 
  }
}