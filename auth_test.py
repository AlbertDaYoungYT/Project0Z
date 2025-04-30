import requests, json


server_url = "http://192.168.1.2:24898"

res = requests.post(server_url + "/auth/hello", data={
    "client_version": [0, 0, 1]
})
client_id = res.json()["id"]
print(f"ID={client_id}")