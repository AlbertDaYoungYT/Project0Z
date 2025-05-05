from dataclasses import dataclass
import json
import time
from typing import Any, Dict, List, Optional
from uuid import UUID
from aiohttp import web

from config.ConfigContainer import ConfigContainer

class DDOSProtectionSystem:
    def __init__(self, config: ConfigContainer):
        self.config = config
        self._TCPClientList: Dict[str, List[Dict[str, Any]]] = {}
        self._UDPClientList: Dict[str, List[Dict[str, Any]]] = {}

    def add_tcp(self, request: web.Request):
        client_info = {
            "id": request.get("id", None),
            "headers": dict(request.headers),
            "time": time.time()
        }
        if request.remote not in self._TCPClientList:
            self._TCPClientList[request.remote] = []
        self._TCPClientList[request.remote].append(client_info)

    def hit_tcp(self, request: web.Request) -> bool:
        self.add_tcp(request)

        client_ip = request.remote
        current_time = time.time()

        # Check for TCP connections from the same IP within the time window and delete old entries
        tcp_connections = self._TCPClientList.get(client_ip, [])
        
        time_window_threshold = current_time - self.config.connection_time_window_seconds
        
        valid_connections = [conn for conn in tcp_connections if conn["time"] > time_window_threshold]
        self._TCPClientList[client_ip] = valid_connections

        # Check if the number of connections exceeds the threshold per IP
        if len(valid_connections) >= self.config.max_connections_per_ip_within_time_window:
            return True
        
        return False