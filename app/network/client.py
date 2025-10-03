from typing import Dict

from .network_manager import NetworkManager
from ..user_manager import UserManager

class Client:
    def __init__(self, network_manager: NetworkManager, user_manager: UserManager):
        self.player = {"id": None, "name": None, "password": None}
        self.network_manager = network_manager
        self.user_manager = user_manager
        self.is_connected = False
        self.current_network_id = None

    def register_player(self, name: str, password: str) -> bool:
        user = self.user_manager.create_user(name, password)

        if user:
            self.player = user
            print(f"Участник создан: {name} (ID: {user['id']})")
            return True

        print("Ошибка создания участника")
        return False

    def login(self, name: str, password: str) -> bool:
        user = self.user_manager.authenticate_user(name, password)
        if user:
            self.player = user
            print(f"Вход выполнен: {name} (ID: {user['id']})")
            return True
        print("Неверные данные для входа")
        return False

    def connect(self, network_id: int = None) -> bool:
        if not self.player["id"]:
            print("Сначала войдите в систему")
            return False
            
        if self.is_connected:
            print("Уже подключен к сети")
            return False

        info = self.network_manager.simulate_connection(self.player["id"])
        self.is_connected = True
        self.current_network_id = network_id or 1

        print(f"Участник {self.player['name']} присоединился к сети {self.current_network_id}")
        print(f"Подключение: {info['ip']}:{info['port']}")
        return True

    def disconnect(self) -> bool:
        if not self.is_connected:
            print("Не подключен к сети")
            return False
        ok = self.network_manager.disconnect_user(self.player["id"])
        if ok:
            self.is_connected = False
            self.current_network_id = None
            print(f"Участник {self.player['name']} вышел")
            return True
        print("Ошибка отключения")
        return False

    def send_message_to_server(self, message: str) -> bool:
        if not self.is_connected:
            print("Не подключен к серверу")
            return False
        print(f"Сообщение от {self.player['name']} серверу: {message}")
        return True

    def receive_notification(self, message: str):
        if self.is_connected:
            print(f"Уведомление для {self.player['name']}: {message}")

    def get_status(self) -> Dict:
        return {
            "player": self.player,
            "connected": self.is_connected,
            "network_id": self.current_network_id,
            "connection_info": self.network_manager.get_connection_info(self.player["id"])
            if self.player["id"]
            else None,
        }