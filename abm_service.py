import time
import jwt
import requests

TEAM_ID = 'TU_TEAM_ID'
KEY_ID = 'TU_KEY_ID'
PRIVATE_KEY_PATH = 'AuthKey_KEYID.p8'
API_ISSUER = 'VENDOR_ID'
TOKEN_URL = 'https://api.cds.apple.com/v1/oauth/token'
API_BASE_URL = 'https://api-business.apple.com/v1'

def create_jwt():
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()
    now = int(time.time())
    payload = {
        'iss': TEAM_ID,
        'iat': now,
        'exp': now + 20*60,
        'aud': 'appstoreconnect-v1'
    }
    headers = {'alg': 'ES256', 'kid': KEY_ID, 'typ': 'JWT'}
    return jwt.encode(payload, private_key, algorithm='ES256', headers=headers)

def get_abm_access_token():
    jwt_token = create_jwt()
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': API_ISSUER,
        'client_secret': jwt_token,
        'grant_type': 'client_credentials',
        'scope': 'business.api'
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def assign_device_to_mdm(access_token, device_serial, mdm_server_id):
    url = f"{API_BASE_URL}/orgDeviceActivities"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "data": {
            "type": "orgDeviceAssignments",
            "attributes": {
                "serialNumbers": [device_serial],
                "action": "assign"
            },
            "relationships": {
                "deviceManagementService": {
                    "data": {
                        "type": "deviceManagementServices",
                        "id": mdm_server_id
                    }
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.ok, response.text
