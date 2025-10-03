import random

def RandomCar(data):
    """Функция для выбора случайного автомобиля из данных"""
    try:
        # Проверяем что data - список и в нем есть элементы
        if data and isinstance(data, list) and len(data) > 0:
            return random.choice(data)
        return {}
    except:
        # Возвращаем пустой словарь при любой ошибке
        return {}

def RandomCard(data):
    """Функция для выбора случайной карточки из данных"""
    try:
        # Такая же простая логика как в RandomCar
        if data and isinstance(data, list) and len(data) > 0:
            return random.choice(data)
        return {}
    except:
        return {}