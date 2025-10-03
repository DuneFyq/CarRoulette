from typing import Optional, Dict
from datetime import datetime

class NetworkManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict] = {}  # user_id -> info
        self.connection_counter = 0

    def simulate_connection(self, user_id: int) -> Dict:
        self.connection_counter += 1
        
        info = {
            "connection_id": self.connection_counter,
            "user_id": user_id,
            "status": "connected",
            "connected_at": datetime.now().strftime("%H:%M:%S"),
            "ip": f"192.168.1.{user_id}",
            "port": 8080 + user_id,
        }
        self.active_connections[user_id] = info

        return info

    def disconnect_user(self, user_id: int) -> bool:
        return self.active_connections.pop(user_id, None) is not None

    def is_user_connected(self, user_id: int) -> bool:
        return user_id in self.active_connections

    def get_connection_info(self, user_id: int) -> Optional[Dict]:
        return self.active_connections.get(user_id)