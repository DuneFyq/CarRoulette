import customtkinter as ctk
from typing import Callable, Optional, Tuple

class PageManager:
    """Управляет переключением между страницами и состоянием кнопок навигации."""
    
    def __init__(self, pages, navigation_buttons):
        self.pages = pages
        self.navigation_buttons = navigation_buttons
        self.current_page = None
    
    def show_page(self, name):
        """Переключает страницу и обновляет стили навигационных кнопок."""
        frame = self.pages.get(name)
        
        if not frame or self.current_page == name:
            return
        
        # Показываем страницу (поднимаем на верх)
        frame.lift()
        self.current_page = name
        
        # Сброс стиля всех кнопок
        default_color = "#FFFFFF"
        default_fg = self.navigation_buttons['rooms'].cget("fg_color")
        
        for btn in self.navigation_buttons.values():
            btn.configure(text_color=default_color, fg_color=default_fg, state="normal")
        
        # Подсвечиваем активную кнопку
        active_color = "#0078D7"
        active_text_color = "#000000"
        
        if name in self.navigation_buttons:
            self.navigation_buttons[name].configure(
                fg_color=active_color, 
                text_color=active_text_color
            )


class TextBoxHelper(ctk.CTkFrame):
    """Виджет-обёртка над CTkTextbox с заголовком и удобными методами.

    Использование:
        tb = TextBoxHelper(parent, width=400, height=150, label_text="Лог")
        tb.grid(...)
        tb.add_text("Hello")
        tb.clear()
    """

    def __init__(
        self,
        parent,
        width: int = 400,
        height: int = 150,
        label_text: Optional[str] = None,
    ):
        super().__init__(parent)

        # Заголовок (опционально)
        if label_text:
            self.label = ctk.CTkLabel(self, text=label_text)
            self.label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 6))
        else:
            self.label = None

        # Сам текстовый виджет
        self.textbox = ctk.CTkTextbox(self, width=width, height=height)
        self.textbox.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Только для чтения по умолчанию
        self.textbox.configure(state="disabled")

    # Совместимый с текущей логикой интерфейс
    def add_text(self, text: str):
        """Добавляет строку текста в конец и блокирует редактирование."""
        self.textbox.configure(state="normal")
        # Добавляем перевод строки, если текста нет или не оканчивается на него
        needs_newline = True
        try:
            last_char = self.textbox.get("end-2c")
            needs_newline = last_char != "\n"
        except Exception:
            pass
        if needs_newline:
            self.textbox.insert("end", "\n")
        self.textbox.insert("end", text)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def clear(self):
        """Очищает содержимое текстового поля."""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")


class InputHelper:
    """Вспомогательный класс для обработки пользовательского ввода."""
    
    @staticmethod
    def get_int_or_default(entry, default_value):
        """Получает целое число из поля ввода или возвращает значение по умолчанию."""
        val = entry.get().strip()
        if not val:
            return default_value
        try:
            return int(val)
        except:
            return default_value

class Box(ctk.CTkToplevel):
    """Универсальное модальное окно для наследования с расширенным функционалом."""

    def __init__(
        self,
        parent,
        title: str = "Box",
        width: int = 400,
        height: int = 300,
        min_size: Tuple[int, int] = (300, 200),
        center: bool = True,
        modal: bool = True,
        resizable: Tuple[bool, bool] = (False, False),
        on_close: Optional[Callable] = None
    ):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.minsize(*min_size)
        self.resizable(*resizable)

        self.transient(parent)
        if modal:
            self.grab_set()

        self.on_close = on_close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        if center:
            self._center_window(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()
        self._create_body()
        self._create_footer()

        self.create_content(self.body_frame)
        self.create_buttons(self.footer_frame)

        self.bind('<Escape>', lambda e: self._on_close())
        self.bind('<Return>', self._on_enter)

    def _create_header(self):
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.create_header(self.header_frame)

    def _create_body(self):
        self.body_frame = ctk.CTkFrame(self)
        self.body_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.body_frame.grid_columnconfigure(0, weight=1)

    def _create_footer(self):
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="e", padx=20, pady=(0, 20))
        self.footer_frame.grid_columnconfigure(0, weight=1)

    def create_header(self, container):
        """
        Переопределить для кастомного заголовка.
        По умолчанию рисуется текстовый заголовок.
        """
        lbl = ctk.CTkLabel(
            container,
            text=self.title(),
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl.pack(side="left", padx=20, pady=15)

    def create_content(self, container):
        """
        Переопределить для наполнения окна виджетами.
        container — CTkFrame для размещения элементов.
        """
        placeholder = ctk.CTkLabel(
            container,
            text="Переопределите create_content()",
            text_color="gray50"
        )
        placeholder.pack(expand=True, padx=10, pady=10)

    def create_buttons(self, container):
        """
        Переопределить для создания своих кнопок.
        По умолчанию одна OK-кнопка.
        """
        self.add_button("OK", command=self._on_close, default=True)

    def add_button(
        self,
        text: str,
        command: Callable,
        default: bool = False,
        side: str = "right",
        padx: Tuple[int, int] = (10, 0),
        pady: int = 5
    ):
        """
        Помогает добавить кнопку в футер.
        default — помечает «Enter»-кнопку.
        """
        btn = ctk.CTkButton(
            self.footer_frame,
            text=text,
            command=command,
            width=80,
            height=32
        )
        btn.pack(side=side, padx=padx, pady=pady)
        if default:
            self.default_button = btn

    def _center_window(self, parent):
        """Безопасное центрирование относительно родителя."""
        try:
            self.update_idletasks()
            px, py = parent.winfo_x(), parent.winfo_y()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            w, h = self.winfo_width(), self.winfo_height()
            x = px + (pw - w) // 2
            y = py + (ph - h) // 2
            self.geometry(f"+{x}+{y}")
        except Exception:
            pass

    def _on_close(self):
        """Закрывает окно и вызывает on_close, если задан."""
        if self.on_close:
            self.on_close()
        self.destroy()

    def _on_enter(self, event=None):
        """Имитация клика по default-кнопке при нажатии Enter."""
        if hasattr(self, "default_button"):
            self.default_button.invoke()

    def show(self):
        """Показывает окно модально и ждёт его закрытия."""
        self.deiconify()
        self.wait_visibility()
        self.focus_set()
        self.wait_window()