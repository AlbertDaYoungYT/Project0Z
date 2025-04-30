import requests, json


server_url = "http://192.168.1.2:24898"

# STEP 1
res = requests.post(server_url + "/auth/hello", data=json.dumps({
    "client_version": [0, 0, 1]
}))
client_id = res.json()["id"]
print(f"ID={client_id}")

# STEP 2
res = requests.post(server_url + "/auth/ack", data=json.dumps({
    "id": client_id
}))
public_key = res.json()["public_key"]
print(f"PUBLIC_KEY={public_key}")