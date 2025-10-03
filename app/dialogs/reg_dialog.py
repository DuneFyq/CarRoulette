import customtkinter as ctk
from ..ui.ui_components import Box

class RegDialog(Box):
    """Всплывающее окно регистрации."""

    def __init__(self, parent, user_manager=None):
        super().__init__(
            parent,
            title="Регистрация",
            width=400,
            height=300,
            min_size=(350, 250),
            center=True,
            modal=True,
            resizable=(False, False),
            on_close=None
        )

        self.user_manager = user_manager
        self.submit_btn = None
        self.result = None

    def create_content(self, container):
        # Настройка сетки
        container.grid_columnconfigure(1, weight=1)
        for i in range(3):
            container.grid_rowconfigure(i, weight=1)
        
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
            placeholder_text="Не менее 6 символов"
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

        # Кнопка «Зарегистрироваться»
        self.submit_btn = ctk.CTkButton(
            container,
            text="Зарегистрироваться",
            command=self.on_submit,
            width=140,
            height=32
        )
        self.submit_btn.configure(
            text_color="#FFFFFF",
            fg_color="#2E8B57",
            hover_color="#276749"
        )
        self.submit_btn.pack(side="right", padx=5, pady=10)
        self.default_button = self.submit_btn

    def validate_form(self):
        """Проверка заполнения полей"""
        errors = []
        
        if not self.nickname_entry.get().strip():
            errors.append("Никнейм не может быть пустым")
        
        if len(self.password_entry.get()) < 6:
            errors.append("Пароль должен содержать не менее 6 символов")
        
        return errors

    def on_submit(self):
        """Обработчик отправки формы"""
        errors = self.validate_form()
        
        if errors:
            error_text = "\n".join(f"• {error}" for error in errors)
            self.status_label.configure(text=error_text)
            return

        # Сбор данных формы
        self.result = {
            'nickname': self.nickname_entry.get().strip(),
            'password': self.password_entry.get()
        }

        if self.user_manager is not None:
            print(f"Регистрация пользователя: {self.result['nickname']}")
            self.user_manager.create_user(self.result['nickname'], self.result['password'])
        else:
            print("Не удалось создать пользователя")

        self._on_close()

    def get_result(self):
        """Возвращает результат работы диалога"""
        return self.result