import sqlite3
from datetime import datetime

class Database:

    def __init__(self, connection=None, db_path="./data/employee.sqlite", query="""
        CREATE TABLE IF NOT EXISTS Employee (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        gender TEXT NOT NULL
        )
        """ ):

        self.connection = sqlite3.connect(db_path)
        # Устанавливаем соединение с базой данных
        cursor = self.connection.cursor()

        # Запрос 
        cursor.execute(query)

        # Сохраняем изменения и закрываем соединение
        self.connection.commit()

    def add_employee(self, employee):
        try:
            # SQL-запрос для вставки нового сотрудника
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO Employee (full_name, birth_date, gender) 
                VALUES (?, ?, ?)
            ''', employee.to_tuple())  # Используем метод to_tuple() объекта Employee

            # Сохранение изменений
            self.connection.commit()
            print(f"Сотрудник {employee.full_name} успешно добавлен в базу данных.")
        
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении сотрудника: {e}")

    def get_all_employees(self):
        query = """
        SELECT DISTINCT full_name, birth_date, gender
        FROM Employee
        ORDER BY full_name;
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        employees = cursor.fetchall()

        return employees

    def add_multiple_employees(self, employees):
            # Пакетное добавление сотрудников
            insert_query = '''
            INSERT INTO Employee (full_name, birth_date, gender)
            VALUES (?, ?, ?)
            '''
            # Создаем список кортежей для вставки в базу данных
            cursor = self.connection.cursor()
            employees_data = [employee.to_tuple() for employee in employees]
            cursor.executemany(insert_query, employees_data)
            self.connection.commit()

    def get_male_employees_with_F(self):
        # SQL-запрос для выборки сотрудников: пол мужской, фамилия начинается на "F"
        query = '''
        SELECT full_name, birth_date, gender
        FROM Employee
        WHERE gender = 'Male' AND full_name LIKE 'F%'
        ORDER BY full_name;
        '''
        cursor = self.connection.cursor()
        cursor.execute(query)
        employees = cursor.fetchall()

        return employees

    # Метод для создания индексов
    def create_indexes(self):
        index_query = '''
        CREATE INDEX IF NOT EXISTS idx_gender_fullname
        ON Employee (gender, full_name);
        '''
        cursor = self.connection.cursor()
        cursor.execute(index_query)
        self.connection.commit()

    def close(self):
        # Закрытие соединения с базой данных
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")



        
