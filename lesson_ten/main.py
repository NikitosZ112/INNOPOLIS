# Интерфейс старого сервиса (OldService)
class OldService:
    def fetch_data(self): # Метод старого сервиса, возвращающий данные о расходах
        return {"fuel_costs": [52373985, 1417389, 8193]}  # Общий, среднесуточный, на единицу

# Интерфейс нового сервиса (NewService)
class NewService:
    def get_data(self): # Метод нового сервиса, который должен возвращать данные в виде отчета
        pass  # Абстрактный метод

# Адаптер, который преобразует OldService к NewService
class ServiceAdapter(NewService):
    def __init__(self, old_service): #  Конструктор адаптера принимает экземпляр старого сервиса
        self.old_service = old_service

    def get_data(self): # Преобразует данные в отчет
        old_data = self.old_service.fetch_data()
        # Отчет
        report = {
            "Общий расход": f"{old_data['fuel_costs'][0]:,} ₽",
            "Среднесуточный расход": f"{old_data['fuel_costs'][1]:,} ₽",
            "Среднесуточный расход на единицу": f"{old_data['fuel_costs'][2]:,} ₽",
        }
        return report

# Клиентский код
def client_code(service: NewService):
    report = service.get_data()
    print("Отчет о расходах:")
    for key, value in report.items():
        print(f"{key}: {value}")

# Тестирование адаптера
if __name__ == "__main__":
    # Создаем экземпляр старого сервиса
    old_service = OldService()

    # Создаем адаптер для старого сервиса
    adapter = ServiceAdapter(old_service)

    # Клиентский код использует адаптер как новый сервис
    client_code(adapter)
