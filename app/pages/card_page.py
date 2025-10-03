import re
import customtkinter as ctk

from ..random_tools import RandomCard
from ..ui.ui_components import TextBoxHelper


class CardPage:
    """Класс для управления страницей с карточками."""
    
    def __init__(self, parent_frame, data_manager):
        self.parent_frame = parent_frame
        self.data_manager = data_manager

        self.count = 10

        self.card_result_text = None
        self.setup_page()
    
    def setup_page(self):
        """Настраивает элементы страницы карточек."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(3, weight=1)
        
        self.card_result_text = TextBoxHelper(
            self.parent_frame, 
            width=400,
            height=150,
            label_text=None
        )
        self.card_result_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Информация игры
        self.info = ctk.CTkFrame(self.parent_frame)
        self.info.grid_rowconfigure(2, weight=1)
        self.info.grid(row=1, column=0, padx=20, pady=10, sticky="new")

        self.count_scroll = ctk.CTkLabel(
            self.info,
            text=f"Доступно: {self.count}"
        )
        self.count_scroll.grid(row=1, column=0, padx=20, pady=10, sticky="new")
        
        # Кнопка генерации карточки
        self.btn_card = ctk.CTkButton(
            self.parent_frame, 
            text="Случайная карточка",
            command=self.generate_card
        )
        self.btn_card.grid(row=2, column=0, padx=20, pady=10, sticky="new")
        
        # Кнопка очистки
        self.card_clear_btn = ctk.CTkButton(
            self.parent_frame, 
            text="🧹 Очистить", 
            command=self.clear_card_results
        )
        self.card_clear_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
    
    def generate_card(self):
        """Генерирует случайную карточку."""
        try:
            if self.count <= 0:
                print("0 доступных прокруток")
                return

            data = self.data_manager.get_data('cards')
            if not data:
                raise ValueError("Данные не найдены")
            
            card = RandomCard(data)
            if not card or 'name' not in card:
                raise ValueError("Неверный формат данных")

            self.count -= 1
            self.count_scroll.configure(text=f"Доступно: {self.count}")
            
            result = f"Карточка:\n{card['name']}\n{card['description']}\n{'-'*30}\n"
            self.card_result_text.add_text(result)
            
        except Exception as e:
            self.card_result_text.add_text(f"❌ Ошибка: {e}\n")
    
    def clear_card_results(self):
        """Очищает результаты карточек."""
        self.card_result_text.clear()