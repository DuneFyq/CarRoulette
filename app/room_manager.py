from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from .game_manager import GameManager

class RoomManager:
    def __init__(self):
        self.rooms: List[Dict] = []
        self.next_room_id = 1

    def _validate_room(self, room_id: int, check_active: bool = False) -> Tuple[Optional[Dict], Optional[str]]:
        room = self.get_room_by_id(room_id)
        if not room:
            return None, "Комната не найдена"

        # Для присоединения допускаем только комнаты в статусе "waiting"
        if check_active and room["status"] != "waiting":
            return None, "Комната недоступна для присоединения"

        return room, None

    def room_list(self) -> List[Dict]:
        return self.rooms

    def get_active_rooms(self) -> List[Dict]:
        # Отображаем все комнаты, которые не закрыты
        return [room for room in self.rooms if room["status"] in ["waiting", "started"]]

    def get_room_by_id(self, room_id: int) -> Optional[Dict]:
        for room in self.rooms:
            if room["id_room"] == room_id:
                return room
        return None

    def room_create(self, owner_id: int, access: str, password: str = None, maxplayers: int = 2, name: str = None) -> Optional[Dict]:
        if access not in ["private", "public"]:
            return None

        if access == "private" and not password:
            return None

        if maxplayers < 2:
            return None

        # Один владелец не может иметь больше одной активной комнаты
        for room in self.rooms:
            if room.get("owner_id") == owner_id and room.get("status") in ["waiting", "started"]:
                print(f"Пользователь {owner_id} уже имеет активную комнату #{room.get('id_room')}")
                return None

        room_name = name.strip() if isinstance(name, str) and name.strip() else f"Комната {self.next_room_id}"

        room = {
            "id_room": self.next_room_id,
            "owner_id": owner_id,
            "access": access,
            "password": password,
            "maxplayers": maxplayers,
            "name": room_name,
            "participants_id": [owner_id],
            "status": "waiting",
            "created_at": datetime.now().strftime("%H:%M:%S"),
        }

        self.rooms.append(room)
        self.next_room_id += 1

        print(f"Создана новая комната: id={room['id_room']}, access={room['access']}, maxplayers={room['maxplayers']}, name={room['name']}")

        return room

    def room_end(self, room_id: int, user_id: int) -> Tuple[bool, str]:
        room, err = self._validate_room(room_id)

        if err:
            return False, err
        if room["owner_id"] != user_id:
            return False, "Закрывать комнату может только владелец"
        if room["status"] == "closed":
            return False, "Комната уже закрыта"
        room["status"] = "closed"
        return True, f"Комната #{room_id} закрыта"

    def room_join(self, room_id: int, user_id: int, password: str = None) -> Tuple[bool, str]:
        room, err = self._validate_room(room_id, check_active=True)

        if err:
            return False, err

        if room["access"] == "private":
            if not password:
                return False, "Для этой комнаты требуется пароль"
            if password != room["password"]:
                return False, "Неверный пароль"

        if user_id in room["participants_id"]:
            return False, "Пользователь уже в комнате"

        if len(room["participants_id"]) >= room["maxplayers"]:
            return False, "Комната переполнена"

        room["participants_id"].append(user_id)

        return True, f"Пользователь {user_id} присоединился к комнате #{room_id}"

    def room_leave(self, room_id: int, user_id: int) -> Tuple[bool, str]:
        room, err = self._validate_room(room_id, check_active=True)

        if err:
            return False, err

        if user_id == room["owner_id"]:
            return False, "Владелец не может покинуть свою комнату (закройте ее)"

        if user_id not in room["participants_id"]:
            return False, "Пользователь не в комнате"

        room["participants_id"].remove(user_id)

        return True, f"Пользователь {user_id} покинул комнату #{room_id}"

    def get_room_participants(self, room_id: int) -> Tuple[bool, Union[List[int], str]]:
        room, err = self._validate_room(room_id)

        if err:
            return False, err

        return True, room["participants_id"]

    def delete_room(self, room_id: int, user_id: int) -> Tuple[bool, str]:
        room, err = self._validate_room(room_id)

        if err:
            return False, err

        if room["owner_id"] != user_id:
            return False, "Удалять комнату может только владелец"

        self.rooms = [r for r in self.rooms if r["id_room"] != room_id]

        return True, f"Комната #{room_id} удалена"

    def get_room_info(self, room_id: int) -> Tuple[bool, Union[Dict, str]]:
        room, err = self._validate_room(room_id)

        if err:
            return False, err

        return True, room.copy()