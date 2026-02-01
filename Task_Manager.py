import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"


def load_tasks():
    """
    Загружает задачи из файла JSON.
    Если файл не существует — возвращает пустой список.
    """
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    """
    Сохраняет список задач в файл JSON.
    """
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def show_tasks(tasks):
    """
    Выводит все задачи на экран, отсортированные по приоритету и дедлайну.
    """
    if not tasks:
        print("\n📭 Список задач пуст\n")
        return

    tasks.sort(key=lambda x: (x["priority"], x["deadline"]))  # Сортируем по приоритету и дедлайну

    print("\n📋 Ваши задачи:")
    for index, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        print(f"{index}. {task['title']} [{status}] - Приоритет: {task['priority']} - Дедлайн: {deadline}")
    print()


def add_task(tasks):
    """
    Добавляет новую задачу с дедлайном и приоритетом.
    """
    title = input("Введите название задачи: ")
    deadline = input("Введите дедлайн задачи (формат YYYY-MM-DD): ")
    
    # Проверяем, что дедлайн введён правильно
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        print("❌ Неверный формат даты, используйте YYYY-MM-DD")
        return

    # Выбираем приоритет
    print("Выберите приоритет задачи (1 - низкий, 2 - средний, 3 - высокий):")
    priority_input = input("Приоритет: ")
    
    # Преобразуем в текстовый приоритет
    if priority_input == "1":
        priority = "низкий"
    elif priority_input == "2":
        priority = "средний"
    elif priority_input == "3":
        priority = "высокий"
    else:
        print("❌ Неверный приоритет")
        return

    tasks.append({
        "title": title,
        "done": False,
        "priority": priority,
        "deadline": deadline_date.strftime("%Y-%m-%d")
    })

    save_tasks(tasks)
    print("✅ Задача успешно добавлена\n")


def complete_task(tasks):
    """
    Отмечает задачу как выполненную.
    """
    show_tasks(tasks)

    if not tasks:
        return

    number = int(input("Введите номер выполненной задачи: ")) - 1

    if 0 <= number < len(tasks):
        tasks[number]["done"] = True
        save_tasks(tasks)
        print("🎉 Задача отмечена как выполненная\n")
    else:
        print("❌ Неверный номер задачи\n")


def delete_task(tasks):
    """
    Удаляет выбранную задачу.
    """
    show_tasks(tasks)

    if not tasks:
        return

    number = int(input("Введите номер задачи для удаления: ")) - 1

    if 0 <= number < len(tasks):
        removed_task = tasks.pop(number)
        save_tasks(tasks)
        print(f"🗑️ Задача '{removed_task['title']}' удалена\n")
    else:
        print("❌ Неверный номер задачи\n")


def search_task(tasks):
    """
    Поиск задачи по названию.
    """
    search_query = input("Введите часть названия задачи для поиска: ").lower()
    found_tasks = [task for task in tasks if search_query in task["title"].lower()]

    if not found_tasks:
        print("❌ Задачи не найдены\n")
        return

    print("\n🔍 Результаты поиска:")
    for index, task in enumerate(found_tasks, start=1):
        status = "✅" if task["done"] else "❌"
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        print(f"{index}. {task['title']} [{status}] - Приоритет: {task['priority']} - Дедлайн: {deadline}")
    print()


def main():
    """
    Главная функция программы.
    Здесь работает основное меню.
    """
    tasks = load_tasks()

    while True:
        print("📌 МЕНЕДЖЕР ЗАДАЧ")
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Отметить задачу выполненной")
        print("4. Удалить задачу")
        print("5. Поиск задачи")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            search_task(tasks)
        elif choice == "6":
            print("👋 Программа завершена")
            break
        else:
            print("❌ Неверный ввод, попробуйте снова\n")


# Точка входа в программу
if __name__ == "__main__":
    main()
