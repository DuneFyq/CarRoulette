from typing import Dict

from ..user_manager import UserManager
from ..room_manager import RoomManager

from ..network.client import Client
from ..network.server import Server
from ..network.network_manager import NetworkManager


class GameServerSystem:
    def __init__(self):
        self.user_manager = UserManager()
        self.network_manager = NetworkManager()
        self.room_manager = RoomManager()
        self.server = Server(self.network_manager, self.user_manager, self.game_manager)

    def create_client(self) -> Client:
        return Client(self.network_manager, self.user_manager)

    def get_system_status(self) -> Dict:
        return {
            "users_count": len(self.user_manager.list_users()),
            "active_connections": len(self.network_manager.active_connections),
            "active_networks": len(self.server.active_networks),
            "active_rooms": len(self.room_manager.get_active_rooms()),
            "server_info": {
                "networks": self.server.list_active_networks(),
                "rooms": self.room_manager.get_active_rooms(),
            },
        }

    def shutdown_system(self):
        print("Система безопасно отключается...")

        for nid in list(self.server.active_networks.keys()):
            net = self.server.active_networks[nid]
            self.server.close_server(nid, net["owner_id"])
            
        for room in list(self.room_manager.get_active_rooms()):
            self.room_manager.room_end(room["id_room"], room["owner_id"])
            
        print("Система отключена")