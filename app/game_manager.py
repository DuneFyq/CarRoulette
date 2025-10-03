from typing import Optional, List, Dict, Tuple
from datetime import datetime


class GameManager:
    def __init__(self):
        self.games: List[Dict] = []
        self.next_games_id = 1

    def get_game_by_id(self, game_id: int) -> Optional[Dict]:
        for game in self.games:
            if game["id_game"] == game_id:
                return game
        return None

    def get_game_by_room(self, room_id: int) -> Optional[Dict]:
        for game in self.games:
            if game["room_id"] == room_id and game["status"] == "active":
                return game
        return None

    def start_game(self, room_id: int, user_id: int, room_manager) -> Tuple[bool, str]:
        """Запускает игру из комнаты. Меняет статус комнаты на 'started'."""
        room = room_manager.get_room_by_id(room_id)
        if not room:
            return False, "Комната не найдена"
        if room["owner_id"] != user_id:
            return False, "Запустить игру может только владелец комнаты"
        if room["status"] == "closed":
            return False, "Комната закрыта"
        if room["status"] == "started":
            return False, "Игра уже запущена"

        game = {
            "id_game": self.next_games_id,
            "room_id": room_id,
            "owner_id": user_id,
            "participants_id": list(room.get("participants_id", [])),
            "created_at": datetime.now().strftime("%H:%M:%S"),
            "status": "active",
        }
        self.games.append(game)
        self.next_games_id += 1

        room["status"] = "started"
        return True, f"Игра #{game['id_game']} в комнате #{room_id} запущена"

    def close_game(self, game_id: int, user_id: int, room_manager) -> Tuple[bool, str]:
        """Завершает игру и закрывает связанную комнату."""
        game = self.get_game_by_id(game_id)
        if not game:
            return False, "Игра не найдена"
        if game["owner_id"] != user_id:
            return False, "Завершить игру может только владелец"
        if game["status"] != "active":
            return False, "Игра уже завершена"

        game["status"] = "ended"
        game["ended_at"] = datetime.now().strftime("%H:%M:%S")

        # Закрываем комнату
        ok, msg = room_manager.room_end(game["room_id"], user_id)
        if not ok:
            # Комната может быть уже закрыта; возвращаем статус игры как завершенной
            return True, f"Игра #{game_id} завершена, но комнату закрыть не удалось: {msg}"
        return True, f"Игра #{game_id} завершена и комната #{game['room_id']} закрыта"