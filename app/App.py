import customtkinter as ctk

from .data_manager import DataManager
from .dialogs.login_dialog import LoginDialog
from .dialogs.reg_dialog import RegDialog
from .room_manager import RoomManager
from .game_manager import GameManager
from .pages.car_page import CarPage
from .pages.card_page import CardPage
from .pages.rooms_page import RoomsPage
from .ui.ui_components import PageManager
from .user_manager import UserManager

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CarApp(ctk.CTk):
    """Главное приложение CarRoulette для Forza."""
    
    def __init__(self):
        super().__init__()
        self.title("CarRoulette for Forza")
        self.geometry("1200x800")
        
        # Менеджеры
        self.data_manager = DataManager()
        self.user_manager = UserManager()
        self.current_user_id = None  # Создадим "текущего пользователя"
        self.room_manager = RoomManager()  # Менеджер комнат
        self.game_manager = GameManager()  # Менеджер игр
        
        # UI компоненты
        self.pages = {}
        self.navigation_buttons = {}
        self.page_manager = None
        self.page_container = None
        
        # Страницы
        self.car_page = None
        self.card_page = None
        self.rooms_page = None
        
        self.setup_ui()
        self.create_pages()
        self.setup_page_manager()
        
        # Показываем страницу комнат по умолчанию
        self.page_manager.show_page("rooms")
    
    def setup_ui(self):
        """Настраивает основной интерфейс приложения."""
        # UI сетка
        self.grid_columnconfigure(0, weight=0, minsize=200)  # Навигация с фиксированной шириной (например, 200 пикселей)
        self.grid_columnconfigure(1, weight=1)               # Контейнер страницы растягивается на остаток пространства
        self.grid_rowconfigure(0, weight=0)                  # Заголовок фиксированный по высоте
        self.grid_rowconfigure(1, weight=1)                  # Основное содержимое растягивается по высоте

        
        self._create_header()
        self._create_navigation()
        self._create_page_container()
    
    def _create_header(self):
        """Создает заголовок приложения с кнопками авторизации в одной строке."""
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self,
            text="Forza Horizon: CarRoulette",
            font=("Arial", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        
        # Фрейм для кнопок авторизации
        self.auth_buttons = ctk.CTkFrame(self)
        self.auth_buttons.grid(row=0, column=1, padx=10, pady=15, sticky="e")
        
        # Кнопки внутри фрейма располагаем в одну строку
        self.reg_button = ctk.CTkButton(
            self.auth_buttons, 
            text="Зарегистрироваться",
            command=self._on_register_click
        )
        self.reg_button.grid(row=0, column=0, padx=(5, 5), pady=5)
        
        self.log_button = ctk.CTkButton(
            self.auth_buttons, 
            text="Войти",
            command=self._on_login_click
        )
        self.log_button.grid(row=0, column=1, padx=(5, 5), pady=5)
    
    def _create_navigation(self):
        """Создает навигационную панель."""
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.navigation_buttons["rooms"] = ctk.CTkButton(
            self.button_frame, 
            text="Комнаты",
            command=lambda: self.page_manager.show_page("rooms")
        )
        self.navigation_buttons["rooms"].grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.navigation_buttons["cars"] = ctk.CTkButton(
            self.button_frame, 
            text="Машины",
            command=lambda: self.page_manager.show_page("cars")
        )
        self.navigation_buttons["cars"].grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.navigation_buttons["cards"] = ctk.CTkButton(
            self.button_frame, 
            text="Карточки",
            command=lambda: self.page_manager.show_page("cards")
        )
        self.navigation_buttons["cards"].grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.navigation_buttons["challenge"] = ctk.CTkButton(
            self.button_frame, 
            text="Челленджи",
            command=lambda: self.page_manager.show_page("cards")
        )
        self.navigation_buttons["challenge"].grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Пустое пространство для выравнивания
        self.empty_space = ctk.CTkLabel(self.button_frame, text="")
        self.empty_space.grid(row=4, column=0, sticky="nsew")

        # Вес для пустого пространства, чтобы занимал всё оставшееся место по вертикали
        self.button_frame.grid_rowconfigure(4, weight=1)
    
    def _create_page_container(self):
        """Создает контейнер для страниц."""
        self.page_container = ctk.CTkFrame(self)
        self.page_container.grid(
            row=1, column=1,
            padx=(5, 10), pady=10, sticky="nsew"
        )
        self.page_container.grid_columnconfigure(0, weight=1)
        self.page_container.grid_rowconfigure(0, weight=1)
    
    def create_pages(self):
        """Создает все страницы приложения."""
        # Создаем фреймы для страниц
        self.pages["cars"] = ctk.CTkFrame(self.page_container)
        self.pages["cars"].grid(row=0, column=0, sticky="nsew")
        
        self.pages["cards"] = ctk.CTkFrame(self.page_container)
        self.pages["cards"].grid(row=0, column=0, sticky="nsew")
        
        self.pages["rooms"] = ctk.CTkFrame(self.page_container)
        self.pages["rooms"].grid(row=0, column=0, sticky="nsew")
        
        # Инициализируем страницы
        self.car_page = CarPage(self.pages["cars"], self.data_manager)
        self.card_page = CardPage(self.pages["cards"], self.data_manager)
        self.rooms_page = RoomsPage(
            self.pages["rooms"], 
            self.data_manager, 
            self.room_manager, 
            self.current_user_id
        )

    def _on_login_click(self):
        dlg = LoginDialog(self, user_manager=self.user_manager)
        dlg.show()
        user = dlg.get_result()
        if user and isinstance(user, dict):
            self.current_user_id = user.get("id", self.current_user_id)
            # Обновим страницу комнат, чтобы она увидела нового пользователя
            if self.rooms_page:
                self.rooms_page.update_user_id(self.current_user_id)

    def _on_register_click(self):
        dlg = RegDialog(self, user_manager=self.user_manager)
        dlg.show()
        data = dlg.get_result()
        if data and isinstance(data, dict):
            # После регистрации можно сразу авторизовать пользователя
            new_user = None
            # Попробуем найти созданного пользователя в списке
            for u in self.user_manager.list_users():
                if u.get("name") == data.get("nickname"):
                    new_user = u
                    break
            if new_user:
                self.current_user_id = new_user.get("id")
                if self.rooms_page:
                    self.rooms_page.update_user_id(self.current_user_id)
    
    def setup_page_manager(self):
        """Настраивает менеджер страниц."""
        self.page_manager = PageManager(self.pages, self.navigation_buttons)


if __name__ == "__main__":
    # Preferred way is to run via run_app.py to avoid import issues
    app = CarApp()
    app.mainloop()