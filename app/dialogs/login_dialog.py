import customtkinter as ctk
from ..ui.ui_components import Box

class LoginDialog(Box):
    """Всплывающее окно входа."""

    def __init__(self, parent, user_manager=None):
        super().__init__(
            parent,
            title="Войти",
            width=400,
            height=280,
            min_size=(350, 250),
            center=True,
            modal=True,
            resizable=(False, False),
            on_close=None
        )

        self.user_manager = user_manager
        self.result = None

    def create_content(self, container):
        # Настройка сетки
        container.grid_columnconfigure(1, weight=1)
        for i in range(3):
            container.grid_rowconfigure(i, weight=1)
        
        # Поле ника
        label_nickname = ctk.CTkLabel(
            container, 
            text="Никнейм:",
            font=("Arial", 12)
        )
        label_nickname.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.nickname_entry = ctk.CTkEntry(
            container, 
            font=("Arial", 14),
            height=35,
            placeholder_text="Введите ваш никнейм"
        )
        self.nickname_entry.grid(row=0, column=1, padx=20, pady=15, sticky="ew")
        self.nickname_entry.bind("<Return>", lambda e: self.on_submit())
        
        # Устанавливаем фокус на поле ввода ника
        self.nickname_entry.focus_set()

        # Поле пароля
        label_password = ctk.CTkLabel(
            container, 
            text="Пароль:",
            font=("Arial", 12)
        )
        label_password.grid(row=1, column=0, padx=20, pady=15, sticky="w")

        self.password_entry = ctk.CTkEntry(
            container, 
            font=("Arial", 14),
            height=35,
            show="•",
            placeholder_text="Введите ваш пароль"
        )
        self.password_entry.grid(row=1, column=1, padx=20, pady=15, sticky="ew")
        self.password_entry.bind("<Return>", lambda e: self.on_submit())

        # Метка для ошибок
        self.status_label = ctk.CTkLabel(
            container,
            text="",
            text_color="#E74C3C",
            font=("Arial", 11)
        )
        self.status_label.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky="w")

    def create_buttons(self, container):
        # Кнопка «Отмена»
        cancel_btn = ctk.CTkButton(
            container,
            text="Отмена",
            command=self._on_close,
            width=100,
            height=32,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE")
        )
        cancel_btn.pack(side="right", padx=10, pady=10)

        # Кнопка «Войти»
        submit_btn = ctk.CTkButton(
            container,
            text="Войти",
            command=self.on_submit,
            width=100,
            height=32
        )
        submit_btn.configure(
            text_color="#FFFFFF",
            fg_color="#2E8B57",
            hover_color="#276749"
        )
        submit_btn.pack(side="right", padx=5, pady=10)

        # Enter-кнопка
        self.default_button = submit_btn

    def validate_form(self):
        """Проверка заполнения полей"""
        errors = []
        
        if not self.nickname_entry.get().strip():
            errors.append("Введите никнейм")
        
        if not self.password_entry.get():
            errors.append("Введите пароль")
        
        return errors

    def on_submit(self):
        """Обработчик входа"""
        errors = self.validate_form()
        
        if errors:
            error_text = "\n".join(f"• {error}" for error in errors)
            self.status_label.configure(text=error_text)
            return

        nickname = self.nickname_entry.get().strip()
        password = self.password_entry.get()

        # Если доступен user_manager, выполним проверку
        if self.user_manager is not None:
            user = self.user_manager.authenticate_user(nickname, password)
            if not user:
                self.status_label.configure(text="Неверный никнейм или пароль")
                return
            self.result = user
        else:
            self.result = {'nickname': nickname}

        print(f"Вход пользователя: {nickname}")
        self._on_close()

    def get_result(self):
        """Возвращает результат работы диалога"""
        return self.result