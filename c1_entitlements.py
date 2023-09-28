import json
import requests
import sys

# Get stdin from TF
input = sys.stdin.read()
input_json = json.loads(input)

# Set variables
client_id = input_json.get('client_id')
client_secret = input_json.get('client_secret')
okta_app_id = input_json.get('okta_app_id')
c1_base_url = input_json.get('c1_url')


# Step 1: Fetch the access token
payload = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}
response = requests.post(f"{c1_base_url}/auth/v1/token", data=payload)
if response.status_code == 200:
    access_token = response.json().get("access_token")
else:
    print("Failed to fetch access token")
    exit(1)


# Step 2: Query all entitlements of the Okta App
response = requests.get(
    f"{c1_base_url}/api/v1/apps/{okta_app_id}/entitlements?page_size=100",
    headers={"Authorization": f"Bearer {access_token}"}
)

if response.status_code == 200:
    entitlements = response.json()["list"]

    # Iterate pages till nextPageToke is empty
    while len(response.json()["nextPageToken"]) != 0:
            token = response.json()["nextPageToken"]
            response = requests.get(
                f"{c1_base_url}/api/v1/apps/{okta_app_id}/entitlements?page_size=100&page_token={token}",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            entitlements = entitlements + response.json()["list"]
            token = response.json()["nextPageToken"]
else:
    print("API call failed")
    exit(1)


# Step 4: Process each entitlement and generate TF data object
result = {}
for i in entitlements:
    entry = i.get("appEntitlement")
    c1_id = entry.get("id")
    c1_name = entry.get("displayName")

    # Remove c1 postfixes
    c1_name = c1_name.replace(" Group Member", "")
    c1_name = c1_name.replace(" App Access", "")
    c1_name = c1_name.replace(" Role Member", "")

    result[str(c1_name)] = c1_id
        

# Step 5: dump results as json        
print(json.dumps(result))