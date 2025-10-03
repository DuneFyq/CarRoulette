import customtkinter as ctk

from ..random_tools import RandomCar
from ..ui.ui_components import TextBoxHelper


class CarPage:
    """Класс для управления страницей с машинами."""
    
    def __init__(self, parent_frame, data_manager):
        self.parent_frame = parent_frame
        self.data_manager = data_manager
        
        self.count = 2
        self.mode = "forza 5"

        self.result_text = None
        self.setup_page()
    
    def setup_page(self):
        """Настраивает элементы страницы машин."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(4, weight=1)
        
        self.result_text = TextBoxHelper(
            self.parent_frame, 
            width=400,
            height=150,
            label_text=None
        )
        self.result_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Информация игры
        self.info = ctk.CTkFrame(self.parent_frame)
        self.info.grid_rowconfigure(2, weight=1)
        self.info.grid(row=1, column=0, padx=20, pady=10, sticky="new")

        self.count_scroll = ctk.CTkLabel(
            self.info,
            text=f"Доступно: {self.count}"
        )
        self.count_scroll.grid(row=1, column=0, padx=20, pady=10, sticky="new")
        
        self.create_button()
        
        # Кнопка очистки
        self.clear_btn = ctk.CTkButton(
            self.parent_frame, 
            text="🧹 Очистить", 
            command=self.clear_results
        )
        self.clear_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    def create_button(self):
        if self.mode == "forza 5":
            self.btn_forza5 = ctk.CTkButton(
                self.parent_frame, 
                text="Случайная машина Forza 5",
                command=lambda: self._generate_car('forza5', "Forza 5:")
            )
            self.btn_forza5.grid(row=2, column=0, padx=20, pady=10, sticky="new")
        elif self.mode == "forza 4":
            self.btn_forza4 = ctk.CTkButton(
                self.parent_frame, 
                text="Случайная машина Forza 4",
                command=lambda: self._generate_car('forza4', "Forza 4:")
            )
            self.btn_forza4.grid(row=2, column=0, padx=20, pady=10, sticky="new")
    
    def _generate_car(self, key, header):
        """Универсальный метод генерации машины."""
        try:
            if self.count <= 0:
                print("0 доступных прокруток")
                return

            data = self.data_manager.get_data(key)
            if not data:
                raise ValueError("Данные не найдены")
            
            car = RandomCar(data)
            if not car or 'brand' not in car:
                raise ValueError("Неверный формат данных")

            self.count -= 1
            self.count_scroll.configure(text=f"Доступно: {self.count}")
            
            result = f"{header} \n {car['brand']} - {car['model']} ({car.get('year', '—')})\n\n"
            self.result_text.add_text(result)
            
        except Exception as e:
            self.result_text.add_text(f"❌ Ошибка: {e}\n")

    def clear_results(self):
        """Очищает результаты."""
        # Use the 'clear' method on the 'result_text' instance
        self.result_text.clear()