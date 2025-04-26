import inspect
import json
import time
from aiohttp import web
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)
from dataclasses import fields
import requests

def get_server_region():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        res = {
            "SHORT": f"{data.get('timezone').split('/')[0].capitalize()}-{data.get('country')}",
            "COUNTRY": f"{data.get('country')}-{data.get('region').lowercase().replace(' ', '_')}"
        }
        return res
    except Exception as e:
        print(f"Error getting region: {e}")
        return None


async def status_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    region = get_server_region()
    
    prefix = "SERVER_FEATURES_"
    server_features = {
        f.name.removeprefix(prefix).lower(): getattr(services.game_constants, f.name)
        for f in fields(services.game_constants)
        if f.name.startswith(prefix)
    }

    res = {
        "release_candidate": services.game_constants.VERSION, #TODO: Create a release candidate system
        "server": {
            "version": services.game_constants.VERSION,
            "region": region["SHORT"],
            "uptime": time.strftime("%-Hh %-Mm %-Ss", time.gmtime(time.time()-services.uptime)),
            "timestamp": time.time()
        },
        "game": {
            "max_players": services.game_constants.MAX_PLAYERS,
            "online_players": None, #TODO: Make the server track the amount of online players
            "min_client_version": services.game_constants.MIN_CLIENT_VERSION,
            "maintenance_mode": False,
            "features": server_features
        },
        "network": { #TODO: Create a pinging program to calculate latency (same with packet loss)
            "latency_ms": {
                "avg": 32, 
                "max": 88,
                "min": 12
            },
            "packet_loss_percent": 0.2
        },
        "meta": { #TODO: Add server verification
            "official": True,
            "server_type": "dedicated",
            "hosted_by": "Project Z0",
            "signature": "YjFjZ...==",
            "verified": True
        }
    }

    return web.json_response(res)


if __name__ == "__main__":
    print(get_server_region())
