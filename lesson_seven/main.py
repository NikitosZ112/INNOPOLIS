import asyncio

async def increment_counter(counter, lock, num_increment, task_id):
    async with lock:
        for _ in range(num_increment):
            counter[0] += 1
            print(f"Task: {task_id}, Counter: {counter}")
        await asyncio.sleep(0.5)

async def main():
    num_tasks = 3 # Количество параллельных задач
    num_increments = 10 # Количество инкрементов каждой задачей
    counter = [0] # Общий счетчик (хранится в списке, чтобы передавать по ссылке)
    lock = asyncio.Lock() # Объект блокировки
    # Создание задач
    tasks = [increment_counter(counter, lock, num_increments, i) for i in range(num_tasks)]
    # Запуск задач параллельно
    await asyncio.gather(*tasks)
    # Вывод конечного значения счетчика
    print(f"Final counter value: {counter[0]}")
    # Проверка корректности значения счетчика
    expected_value = num_tasks * num_increments
    print(f"Expected counter value: {expected_value}")
    assert counter[0] == expected_value, "The final counter value does not match the expected value!"


if __name__ == "__main__":
    asyncio.run(main())