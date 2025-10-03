import customtkinter as ctk
from ..ui.ui_components import Box


class CreateRoomDialog(Box):
    """Всплывающее окно создания комнаты (публичной/приватной)."""

    def __init__(self, parent):
        super().__init__(
            parent,
            title="Создание комнаты",
            width=460,
            height=340,
            min_size=(440, 320),
            center=True,
            modal=True,
            resizable=(False, False),
            on_close=None
        )

        self.result = None
        self.submit_btn = None

    def create_content(self, container):
        # Сетка
        for i in range(5):
            container.grid_rowconfigure(i, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Название комнаты
        ctk.CTkLabel(container, text="Название:", font=("Arial", 12)).grid(row=0, column=0, padx=12, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(container, font=("Arial", 14), height=32, placeholder_text="Например: Дружеский заезд")
        self.name_entry.grid(row=0, column=1, padx=12, pady=10, sticky="ew")

        # Тип доступа
        ctk.CTkLabel(container, text="Доступ:", font=("Arial", 12)).grid(row=1, column=0, padx=12, pady=10, sticky="w")
        self.access_option = ctk.CTkOptionMenu(
            container,
            values=["public", "private"],
            width=140,
            command=lambda _val: self._toggle_password()
        )
        self.access_option.set("public")
        self.access_option.grid(row=1, column=1, padx=12, pady=10, sticky="w")

        # Пароль (только для private)
        ctk.CTkLabel(container, text="Пароль:", font=("Arial", 12)).grid(row=2, column=0, padx=12, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(container, font=("Arial", 14), height=32, show="•", placeholder_text="Если комната приватная")
        self.password_entry.grid(row=2, column=1, padx=12, pady=10, sticky="ew")

        # Максимум участников
        ctk.CTkLabel(container, text="Макс. игроков:", font=("Arial", 12)).grid(row=3, column=0, padx=12, pady=10, sticky="w")
        self.maxplayers_entry = ctk.CTkEntry(container, font=("Arial", 14), height=32, placeholder_text="Например: 4")
        self.maxplayers_entry.insert(0, "4")
        self.maxplayers_entry.grid(row=3, column=1, padx=12, pady=10, sticky="w")

        # Статус ошибок
        self.status_label = ctk.CTkLabel(container, text="", text_color="#E74C3C", font=("Arial", 11))
        self.status_label.grid(row=4, column=0, columnspan=2, padx=12, pady=5, sticky="w")

        self._toggle_password()

    def _toggle_password(self):
        is_private = self.access_option.get() == "private"
        state = "normal" if is_private else "disabled"
        try:
            self.password_entry.configure(state=state)
            if not is_private:
                self.password_entry.delete(0, "end")
        except Exception:
            pass

    def create_buttons(self, container):
        cancel_btn = ctk.CTkButton(container, text="Отмена", command=self._on_close, width=100, height=32, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        cancel_btn.pack(side="right", padx=10, pady=10)

        self.submit_btn = ctk.CTkButton(container, text="Создать", command=self.on_submit, width=120, height=32)
        self.submit_btn.configure(text_color="#FFFFFF", fg_color="#2E8B57", hover_color="#276749")
        self.submit_btn.pack(side="right", padx=5, pady=10)
        self.default_button = self.submit_btn

    def validate_form(self):
        errors = []
        name = self.name_entry.get().strip()
        access = self.access_option.get()
        password = self.password_entry.get()
        maxplayers_raw = self.maxplayers_entry.get().strip() or "4"

        # Название
        if not name:
            errors.append("Название комнаты не может быть пустым")

        # Макс. игроков
        try:
            maxplayers = int(maxplayers_raw)
            if maxplayers < 2:
                errors.append("Макс. игроков должен быть не менее 2")
        except ValueError:
            errors.append("Макс. игроков должен быть числом")

        # Доступ/пароль
        if access not in ("public", "private"):
            errors.append("Некорректный тип доступа")
        if access == "private" and not password:
            errors.append("Для приватной комнаты требуется пароль")

        return errors

    def on_submit(self):
        errors = self.validate_form()
        if errors:
            self.status_label.configure(text="\n".join(f"• {e}" for e in errors))
            return

        self.result = {
            "name": self.name_entry.get().strip(),
            "access": self.access_option.get(),
            "password": self.password_entry.get() or None,
            "maxplayers": int(self.maxplayers_entry.get().strip() or "4"),
        }

        self._on_close()

    def get_result(self):
        return self.result