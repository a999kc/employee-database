import sys
from database import Database
from employee import Employee
import random
import string
import time  # Для замера времени

def generate_random_name():
    # Генерируем случайную фамилию и имя
    first_names = ['Ivan', 'Anna', 'Sergey', 'Polina', 'Maria', 'Dmitry', 'Ekaterina', 'Igor', 'Olga', 'Andrey']
    last_names = ['Petrov', 'Ivanov', 'Sidorov', 'Volkov', 'Kuznetsov', 'Fedorov', 'Mikhailov', 'Alekseev', 'Pavlov', 'Smirnov']

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # Возвращаем ФИО в формате "Фамилия Имя"
    return f"{last_name} {first_name}"

def generate_random_birth_date():
    # Генерируем случайную дату рождения (между 1950 и 2000 годом)
    year = random.randint(1950, 2010)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Ограничиваем до 28, чтобы избежать некорректных дат
    return f"{day:02d}-{month:02d}-{year}"

def generate_random_gender():
    # Генерируем случайный пол
    return random.choice(['Male', 'Female'])

def main():
    db = None

    if len(sys.argv) > 1:
        mode = int(sys.argv[1])
        
        # Режим 1: Создание таблицы
        if mode == 1:
            db = Database()  # Вызываем метод для создания таблицы
            print("Таблица сотрудников успешно создана.")
            db.close()  # Закрываем соединение после создания таблицы

        # Режим 2: Добавление нового сотрудника
        elif mode == 2:
            if len(sys.argv) != 5:
                print("Неверное количество аргументов для добавления сотрудника.")
                print('Пример использования: python main.py 2 "ФИО" "ДД-ММ-ГГГГ" "Пол"')
            else:
                db = Database()  # Подключаемся к базе данных
                full_name = sys.argv[2]
                birth_date = sys.argv[3]
                gender = sys.argv[4]

                # Создаем объект Employee и добавляем его в базу данных
                employee = Employee(full_name, birth_date, gender)
                db.add_employee(employee)
                print(f"Сотрудник {full_name} успешно добавлен в базу данных.")
                db.close()  # Закрываем соединение после добавления

        # Режим 3: Вывод всех сотрудников
        elif mode == 3:
            db = Database()  # Подключаемся к базе данных
            employees = db.get_all_employees()  # Получаем список всех сотрудников

            if employees:
                print(f"{'ФИО':<30} {'Дата рождения':<12} {'Пол':<6} {'Возраст':<6}")
                print("-" * 60)
                for employee in employees:
                    full_name, birth_date, gender = employee
                    # Используем метод calculate_age из класса Employee
                    employee_obj = Employee(full_name, birth_date, gender)
                    age = employee_obj.calculate_age()
                    print(f"{full_name:<30} {birth_date:<12} {gender:<6} {age:<6}")
            else:
                print("Список сотрудников пуст.")

            db.close()  # Закрываем соединение после вывода

        # Режим 4: Автоматическое заполнение 10,000 сотрудников
        elif mode == 4:
            db = Database()  # Подключаемся к базе данных
            
            # Создаем список сотрудников
            employees = []
            for _ in range(9900):
                full_name = generate_random_name()
                birth_date = generate_random_birth_date()
                gender = generate_random_gender()
                employee = Employee(full_name, birth_date, gender)
                employees.append(employee)

            # Добавляем 100 сотрудников с фамилиями на "F"
            for _ in range(100):
                full_name = generate_random_name()
                full_name = f"F{full_name[1:]}"  # Заменяем первую букву фамилии на "F"
                birth_date = generate_random_birth_date()
                gender = "Male"  # Мужской пол
                employee = Employee(full_name, birth_date, gender)
                employees.append(employee)

            # Добавляем сотрудников в базу данных пакетно
            db.add_multiple_employees(employees)
            print("10,000 сотрудников успешно добавлены в базу данных.")
            db.close()  # Закрываем соединение после добавления сотрудников

        # Режим 5: Выборка по критерию "пол мужской, фамилия начинается с F"
        elif mode == 5:
            db = Database()  # Подключаемся к базе данных
            
            # Замер времени выполнения запроса
            start_time = time.time()
            employees = db.get_male_employees_with_F()  # Получаем выборку сотрудников
            end_time = time.time()

            # Вывод результатов
            if employees:
                print(f"{'ФИО':<30} {'Дата рождения':<12} {'Пол':<6}")
                print("-" * 60)
                for employee in employees:
                    full_name, birth_date, gender = employee
                    print(f"{full_name:<30} {birth_date:<12} {gender:<6}")
                print(f"Время выполнения: {end_time - start_time:.4f} секунд")
            else:
                print("Сотрудники, соответствующие критериям, не найдены.")

            db.close()  # Закрываем соединение после выполнения запроса

        # Режим 6: Оптимизация базы данных (создание индексов)
        elif mode == 6:
            db = Database()  # Подключаемся к базе данных
            
            # Замер времени до оптимизации
            start_time = time.time()
            employees_before = db.get_male_employees_with_F()  # Выборка до оптимизации
            end_time = time.time()
            print(f"Время выполнения до оптимизации: {end_time - start_time:.4f} секунд")

            # Создаем индексы на столбцы 'gender' и 'full_name'
            db.create_indexes()
            print("Индексы успешно созданы.")

            # Замер времени после создания индексов
            start_time = time.time()
            employees_after = db.get_male_employees_with_F()  # Выборка после оптимизации
            end_time = time.time()
            print(f"Время выполнения после оптимизации: {end_time - start_time:.4f} секунд")

            db.close()  # Закрываем соединение после оптимизации

if __name__ == "__main__":
    main()