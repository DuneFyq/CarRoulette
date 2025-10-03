from typing import Optional, List, Dict

class UserManager:
    def __init__(self):
        self._users: List[Dict] = []
        self._next_id: int = 1

    def create_user(self, name: str = "Новый игрок", password: str = None) -> Optional[Dict]:

        if password is None or len(password) < 3:
            print("Пароль короткий или его нет")
            return None

        user = {
            "id": self._next_id,
            "name": name,
            "password": password
        }

        self._users.append(user)
        self._next_id += 1

        print(f"Создался новый пользователь: {user['id'], user['name']}")
        return user

    def get_user(self, user_id: int) -> Optional[Dict]:
        print(f"Получены данные пользователя:{user_id}")

        return next((user for user in self._users if user["id"] == user_id), None)

    def authenticate_user(self, name: str, password: str) -> Optional[Dict]:
        for user in self._users:
            if user["name"] == name and user["password"] == password:
                print(f"Пользовать вошёл в аккаунт: {name, password}")
                return user
        return None

    def list_users(self) -> List[Dict]:
        print("Получен список пользователей")
        return [user.copy() for user in self._users]
