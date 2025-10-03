import json

class DataManager:
    """Класс для управления данными приложения"""
    
    def __init__(self):
        self.data_sources = {
            'forza5': "app/data/cars_forza5.json",
            'forza4': "app/data/cars_forza4.json", 
            'cards': "app/data/cards.json"
        }
    
    def get_data(self, source_key):
        """Получение данных по ключу из JSON-файла"""
        print(f"Получение данных по ключу: {source_key}")
        try:
            if source_key in self.data_sources:
                with open(self.data_sources[source_key], 'r', encoding='utf-8') as file:
                    return json.load(file)
            return []
        except Exception as e:
            print(f"Ошибка при чтении данных: {e}")
            return []