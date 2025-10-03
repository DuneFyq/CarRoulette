from datetime import datetime
from typing import Dict, Optional, List

from ..room_manager import RoomManager
from ..user_manager import UserManager
from .network_manager import NetworkManager

class Server:
    def __init__(self, network_manager: NetworkManager, user_manager: UserManager, room_manager: RoomManager):
        self.network_manager = network_manager
        self.user_manager = user_manager
        self.room_manager = room_manager
        self.active_networks: Dict[int, Dict] = {}
        self.next_network_id = 1

    def create_server(self, owner_id: int, name: str = "Новая сеть", password: str = None) -> Optional[Dict]:
        owner = self.user_manager.get_user(owner_id)
        if not owner:
            print("Владелец не найден")
            return None
        network = {
            "id": self.next_network_id,
            "name": name,
            "owner_id": owner_id,
            "participants_id": [owner_id],
            "password": password,
            "status": "active",
            "created_at": datetime.now().strftime("%H:%M:%S"),
            "max_participants": 10,
        }
        self.active_networks[self.next_network_id] = network
        self.next_network_id += 1
        print(f"Новая сеть создана: {name} (ID: {network['id']})")
        return network

    def close_server(self, network_id: int, user_id: int) -> bool:
        if network_id not in self.active_networks:
            print("Сеть не найдена")
            return False
        network = self.active_networks[network_id]
        if network["owner_id"] != user_id:
            print("Только владелец может закрыть сеть")
            return False
        for pid in list(network["participants_id"]):
            self.network_manager.disconnect_user(pid)
        network["status"] = "closed"
        del self.active_networks[network_id]
        print(f"Сеть {network['name']} закрылась")
        return True

    def add_participant(self, network_id: int, user_id: int, password: str = None) -> bool:
        if network_id not in self.active_networks:
            print("Сеть не найдена")
            return False
        network = self.active_networks[network_id]
        if network["password"] and network["password"] != password:
            print("Неверный пароль")
            return False
        if user_id in network["participants_id"]:
            print("Пользователь уже в сети")
            return False
        if len(network["participants_id"]) >= network["max_participants"]:
            print("Сеть переполнена")
            return False
        network["participants_id"].append(user_id)
        user = self.user_manager.get_user(user_id)
        uname = user["name"] if user else f"User_{user_id}"
        print(f"Пользователь {uname} присоединился к сети {network['name']}")
        self.notify_all_participants(network_id, f"Пользователь {uname} присоединился")
        return True

    def remove_participant(self, network_id: int, user_id: int) -> bool:
        if network_id not in self.active_networks:
            print("Сеть не найдена")
            return False
        network = self.active_networks[network_id]
        if user_id not in network["participants_id"]:
            print("Пользователь не в сети")
            return False
        network["participants_id"].remove(user_id)
        self.network_manager.disconnect_user(user_id)
        user = self.user_manager.get_user(user_id)
        uname = user["name"] if user else f"User_{user_id}"
        print(f"Пользователь {uname} покинул сеть")
        self.notify_all_participants(network_id, f"Пользователь {uname} покинул сеть")
        return True

    def fireserver(self, user_id: int, network_id: int, message: str = ""):
        if network_id in self.active_networks and user_id in self.active_networks[network_id]["participants_id"]:
            user = self.user_manager.get_user(user_id)
            uname = user["name"] if user else f"User_{user_id}"
            print(f"Сервер получил сообщение от {uname} в сети {network_id}: {message}")
        else:
            print("Недействительное подключение")

    def notify_participant(self, user_id: int, message: str):
        if self.network_manager.is_user_connected(user_id):
            print(f"Участник {user_id} уведомлён: {message}")

    def notify_all_participants(self, network_id: int, message: str = ""):
        if network_id not in self.active_networks:
            return

        network = self.active_networks[network_id]
        connected = sum(1 for uid in network["participants_id"] if self.network_manager.is_user_connected(uid))

        print(f"Все участники сети {network['name']} уведомлены ({connected} подключено): {message}")

    def get_network_info(self, network_id: int) -> Optional[Dict]:
        return self.active_networks.get(network_id)

    def list_active_networks(self) -> List[Dict]:
        return list(self.active_networks.values())