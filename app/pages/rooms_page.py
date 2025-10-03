import customtkinter as ctk

from ..ui.ui_components import TextBoxHelper
from ..dialogs.create_room_dialog import CreateRoomDialog

class RoomsPage:
    """Класс для управления страницей комнат."""
    
    def __init__(self, parent_frame, data_manager, room_manager, current_user_id):
        self.parent_frame = parent_frame
        self.data_manager = data_manager
        self.room_manager = room_manager
        self.current_user_id = current_user_id
        
        # UI элементы
        self.list_rooms = None
        self.filter_frame = None
        self.button_frame = None
        self.log_text = None
        
        self.setup_page()
        self.refresh_rooms_list()

    def setup_page(self):
        """Настройка интерфейса страницы комнат"""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(2, weight=1)

        # Заголовок
        title_label = ctk.CTkLabel(
            self.parent_frame,
            text="Управление комнатами",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        """Фрейм с кнопками управления"""
        self.button_frame = ctk.CTkFrame(self.parent_frame)
        self.button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Кнопка создания комнаты
        create_btn = ctk.CTkButton(
            self.button_frame,
            text="Создать комнату",
            command=self.create_room,
            fg_color="#2AA876",
            hover_color="#207A54"
        )
        create_btn.grid(row=0, column=0, padx=10, pady=5)

        # Кнопка обновления списка
        refresh_btn = ctk.CTkButton(
            self.button_frame,
            text="Обновить список",
            command=self.refresh_rooms_list,
            fg_color="#3B8ED0",
            hover_color="#366AB3"
        )
        refresh_btn.grid(row=0, column=1, padx=10, pady=5)

        """Список комнат"""
        self.list_rooms = ctk.CTkScrollableFrame(
            self.parent_frame,
            height=200,
            label_text="Доступные комнаты"
        )
        self.list_rooms.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.list_rooms.grid_columnconfigure(0, weight=1)

        # Словарь для хранения кнопок комнат
        self.room_buttons = {}

        """Поле для логов"""
        self.log_text = TextBoxHelper(
            self.parent_frame,
            width=400,
            height=150,
            label_text="Лог операций"
        )
        self.log_text.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

    def refresh_rooms_list(self):
        """Обновление списка комнат"""
        self.log_text.add_text("Обновление списка комнат...")
        
        # Очистка существующих кнопок
        for button in self.room_buttons.values():
            button.destroy()
        self.room_buttons.clear()
        
        try:
            rooms_data = self.get_rooms_data()
            
            if not rooms_data:
                empty_label = ctk.CTkLabel(
                    self.list_rooms,
                    text="Нет доступных комнат",
                    text_color="gray"
                )
                empty_label.grid(row=0, column=0, padx=10, pady=20)
                self.room_buttons["empty"] = empty_label
                return

            for i, room in enumerate(rooms_data):
                self.create_room_button(room, i)
                
            self.log_text.add_text(f"Загружено комнат: {len(rooms_data)}")
            
        except Exception as e:
            self.log_text.add_text(f"Ошибка загрузки комнат: {str(e)}")

    def create_room_button(self, room_data, index):
        """Создание кнопки для комнаты"""
        room_name = self.format_room_display(room_data)
        
        # Определяем цвет кнопки в зависимости от статуса
        if self.is_user_in_room(room_data):
            fg_color = "#2AA876"  # Зеленый если пользователь в комнате
        elif room_data['participants_count'] >= room_data['maxplayers']:
            fg_color = "#B32B2B"  # Красный если комната заполнена
        else:
            fg_color = "#3B8ED0"  # Синий по умолчанию

        room_button = ctk.CTkButton(
            self.list_rooms,
            text=room_name,
            command=lambda r=room_data: self.on_room_select(r),
            height=45,
            font=("Arial", 12),
            fg_color=fg_color,
            hover_color=self.get_hover_color(fg_color)
        )
        room_button.grid(row=index, column=0, padx=10, pady=5, sticky="ew")
        self.room_buttons[room_data['id_room']] = room_button

    def get_rooms_data(self):
        """Получение данных о комнатах"""

        rooms = self.room_manager.get_active_rooms()
        
        # Преобразуем данные в нужный формат
        formatted_rooms = []
        for room in rooms:
            formatted_room = {
                'id_room': room.get('id_room', room.get('id', 'unknown')),
                'name': room.get('name', f"Комната {room.get('id_room', '')}"),
                'participants_count': len(room.get('participants_id', [])),
                'participants_id': room.get('participants_id', []),
                'maxplayers': room.get('maxplayers', 4),
                'status': room.get('status', 'waiting'),
                'creator_id': room.get('creator_id', 'unknown')
            }
            formatted_rooms.append(formatted_room)
            
        return formatted_rooms

    def format_room_display(self, room_data):
        """Форматирование отображения комнаты"""
        base_name = f"{room_data['name']}"
        participants = room_data['participants_count']
        max_players = room_data['maxplayers']
        status = room_data['status']
        
        # Добавляем индикатор участия текущего пользователя
        user_status = " ✓" if self.is_user_in_room(room_data) else ""
        
        return f"{base_name} ({participants}/{max_players}) {status}{user_status}"

    def is_user_in_room(self, room_data):
        """Проверка, находится ли текущий пользователь в комнате"""
        return self.current_user_id in room_data.get('participants_id', [])

    def get_hover_color(self, base_color):
        """Получение цвета при наведении на основе базового"""
        color_map = {
            "#2AA876": "#207A54",  # Темно-зеленый
            "#B32B2B": "#8A2222",  # Темно-красный  
            "#3B8ED0": "#366AB3"   # Темно-синий
        }
        return color_map.get(base_color, "#366AB3")

    def on_room_select(self, room_data):
        """Обработчик выбора комнаты"""
        room_id = room_data['id_room']
        room_name = room_data['name']
        
        self.log_text.add_text(f"Выбрана комната: {room_name} (ID: {room_id})")
        
        # Если владелец выбирает свою комнату в ожидании — предложим старт
        is_owner = self.current_user_id == room_data.get('creator_id') or self.current_user_id == room_data.get('owner_id')
        if is_owner and room_data.get('status') == 'waiting':
            self.try_start_game(room_id)
            return
        
        # Проверяем, находится ли пользователь уже в комнате
        if self.is_user_in_room(room_data):
            self.log_text.add_text("Вы уже находитесь в этой комнате")
            return
            
        # Проверяем, не заполнена ли комната
        if room_data['participants_count'] >= room_data['maxplayers']:
            self.log_text.add_text("Комната заполнена, невозможно присоединиться")
            return
        
        # Приватная комната требует пароль (упрощенно: пока без отдельного ввода)
        password = None
        if room_data.get('access') == 'private':
            self.log_text.add_text("Для приватной комнаты требуется пароль (ввод не реализован)")
            return
            
        # Пытаемся присоединиться к комнате
        try:
            success, message = self.room_manager.room_join(room_id, self.current_user_id, password=password)
            
            if success:
                self.log_text.add_text(f"Успешно присоединились к комнате: {message}")
                # Обновляем список комнат
                self.refresh_rooms_list()
            else:
                self.log_text.add_text(f"Ошибка присоединения: {message}")
                
        except Exception as e:
            self.log_text.add_text(f"Ошибка при присоединении к комнате: {str(e)}")

    def try_start_game(self, room_id):
        try:
            # Старт игры должен выполняться через GameManager, доступ к которому получим через app
            app = self.parent_frame.winfo_toplevel()
            if hasattr(app, 'game_manager'):
                ok, msg = app.game_manager.start_game(room_id, self.current_user_id, self.room_manager)
            else:
                ok, msg = False, "Системная ошибка: GameManager недоступен"
            if ok:
                self.log_text.add_text(msg)
                self.refresh_rooms_list()
            else:
                self.log_text.add_text(msg)
        except Exception as e:
            self.log_text.add_text(f"Не удалось запустить игру: {str(e)}")

    def create_room(self):
        """Создание новой комнаты"""
        # Проверка регистрации
        if not isinstance(self.current_user_id, int) or self.current_user_id is None:
            self.log_text.add_text("Создание комнаты доступно только зарегистрированным пользователям")
            return

        dialog = CreateRoomDialog(self.parent_frame)
        dialog.show()
        params = dialog.get_result()

        if not params:
            self.log_text.add_text("Создание комнаты отменено")
            return

        self.log_text.add_text("Создание новой комнаты...")
        try:
            room = self.room_manager.room_create(
                owner_id=self.current_user_id,
                access=params["access"],
                password=params.get("password"),
                maxplayers=params["maxplayers"],
                name=params["name"],
            )
            
            if room and 'id_room' in room:
                self.log_text.add_text(f"Комната создана: {room.get('name', '')} (ID {room['id_room']}) и ожидает старта")
                # Обновляем список комнат
                self.refresh_rooms_list()
            else:
                self.log_text.add_text("Ошибка создания комнаты: возможно у вас уже есть активная комната")
                
        except Exception as e:
            self.log_text.add_text(f"Ошибка создания комнаты: {str(e)}")

    def update_user_id(self, new_user_id):
        """Обновление ID текущего пользователя"""
        self.current_user_id = new_user_id
        self.refresh_rooms_list()