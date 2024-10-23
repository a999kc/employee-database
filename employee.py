from datetime import datetime

class Employee:
    def __init__(self, full_name, birth_date, gender):
        # Инициализация объекта сотрудника
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def calculate_age(self):
        # Метод для расчета возраста сотрудника
        birth_date = datetime.strptime(self.birth_date, '%d-%m-%Y')
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def to_tuple(self):
        # Преобразование объекта в кортеж для передачи в SQL-запрос
        return (self.full_name, self.birth_date, self.gender)
