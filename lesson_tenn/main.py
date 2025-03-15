# # Интерфейс команды
class Command:
    def execute(self): # Выполнить команду
        pass

    def undo(self): # Отменить команду
        pass

# Класс для управления светом
class Light:
    def on(self):
        print("Свет включен")
        return "Свет включен"

    def off(self):
        print("Свет выключен")
        return "Свет выключен"

# Команда для включения света
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()

# Команда для выключения света
class lightOffCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()

# Класс для управления командами
class RemoteControl:
    def __init__(self):
        self.history = [] # История выполненных команд

    def set_command(self, command): # Выполняет команду и сохраняет ее в истории
        command.execute()
        self.history.append(command)

    def undo_last_command(self):
        if self.history:
            last_command = self.history.pop()
            last_command.undo()
        else:
            print("Команд для отмены нет")

# Тестирование системы
if __name__ == "__main__":
    light_room = Light() # Объект света

    # Команды для управления светом
    light_on = LightOnCommand(light_room)
    light_off = lightOffCommand(light_room)

    # Создаем пульт управления
    remote = RemoteControl()

    # Управляем светом
    remote.set_command(light_on)
    remote.set_command(light_off)

    # Отменяем последнюю команду
    remote.undo_last_command()  # Свет включается обратно