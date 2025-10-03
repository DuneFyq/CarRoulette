from .network.game_server_system import GameServerSystem

def demo_system():
    print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ ПОДКЛЮЧЕНИЯ ===\n")
    system = GameServerSystem()

    print("1. Создание пользователей:")
    user1 = system.user_manager.create_user("Игрок1", "password123")
    user2 = system.user_manager.create_user("Игрок2", "password456")
    print()

    print("2. Создание клиентов и логин:")
    client1 = system.create_client()
    client2 = system.create_client()
    client1.login("Игрок1", "password123")
    client2.login("Игрок2", "password456")
    print()

    print("3. Создание сети и подключение:")
    network = system.server.create_server(user1["id"], "Тестовая сеть", "net123")
    client1.connect(network["id"])
    client2.connect(network["id"])
    system.server.add_participant(network["id"], user2["id"], "net123")
    print()

    print("4. Комнаты:")
    room = system.room_manager.room_create(user1["id"], "public", maxplayers=4)
    print(f"Комната создана: ID {room['id_room']}")
    ok, msg = system.room_manager.room_join(room["id_room"], user2["id"])
    print(msg)
    print()

    print("5. Сообщения и уведомления:")
    client1.send_message_to_server("Привет всем!")
    system.server.fireserver(user1["id"], network["id"], "Привет от Игрока1")
    system.server.notify_participant(user2["id"], "Добро пожаловать!")
    system.server.notify_all_participants(network["id"], "Игра начинается!")
    print()

    print("6. Статус системы:")
    st = system.get_system_status()
    print(f"Пользователей: {st['users_count']}")
    print(f"Активных подключений: {st['active_connections']}")
    print(f"Активных сетей: {st['active_networks']}")
    print(f"Активных комнат: {st['active_rooms']}")
    print()

    print("7. Отключение:")
    client1.disconnect()
    client2.disconnect()
    system.shutdown_system()
    print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")

if __name__ == "__main__":
    demo_system()