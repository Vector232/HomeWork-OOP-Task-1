# КЛАССЫ
# Общий для всех дальнейших классов родитель
class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
    # За корректную работу можно не волноваться т к в данном задании при вызове этого метода у любого объекта чей клаcс не обладает
    # параметром grades в любом случае возникнет исключение. Т е нет разницы(в этом задании) пишем мы метод только для нужных классов (студенты и лекторы) или наследуем всеми (студенты лекторы И эксперты)
    def averageGrade(self):
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)

        if len(all_grades) != 0:
            average_grade = sum(all_grades) / len(all_grades)
        else:
            average_grade = 0

        return average_grade
    
    # Реализуем возможность сравнения через операторы: > >= == (< <= == !=)
    # Note Как я понял, в нашем случае достаточно одного одного оператора, чтобы все корректно работало.
    def __lt__(self, x):
        val1 = self.averageGrade()
        val2 = x.averageGrade()
        return True if val1 < val2 else False
    
    def __le__(self, x):
        val1 = self.averageGrade()
        val2 = x.averageGrade()
        return True if val1 <= val2 else False
    
    def __eq__(self, x):
        val1 = self.averageGrade()
        val2 = x.averageGrade()
        return True if val1 == val2 else False
    
        
class Student(Person):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname) #super() все параметры родителя запихиваем в будущий объект одной строкой
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_the_lecture(self, lecturer, course, grade = int):
        if 0 > grade > 10: return 'Неверный балл' #контролируем корректность балла.

        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'
        
    def __str__(self) -> str:
        return f'СТУДЕНТ\n'\
               f'Ими: {self.name}\n'\
               f'Фамилия: {self.surname}\n'\
               f'Средняя оценка за домашние задания: {self.averageGrade()}\n'\
               f'Курсы в прцессе изучения: {" ".join(self.courses_in_progress)}\n'\
               f'Завершенные курсы: {" ".join(self.finished_courses)}'

 
        
class Mentor(Person):
    def __init__(self, name, surname, courses_attached = []):
        super().__init__(name, surname)
        self.courses_attached = courses_attached

        

class Lecturer(Mentor):
    def __init__(self, name, surname, courses_attached = []):
        super().__init__(name, surname, courses_attached)
        self.grades = {}

    def __str__(self) -> str:
        return f'ЛЕКТОР\n'\
               f'Ими: {self.name}\n'\
               f'Фамилия: {self.surname}\n'\
               f'Средняя оценка за лекции: {self.averageGrade()}'


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            student.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'
        
    def __str__(self) -> str:
        return f'ЭКСПЕРТ\n'\
               f'Ими: {self.name}\n'\
               f'Фамилия: {self.surname}'
        

#ФУНКЦИИ
#1 - для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса (в качестве аргументов принимаем список студентов и название курса)
def аverageCourseGrade(students = list, course = str):
    all_grades = []
    for student in students:
        all_grades.extend(student.grades[course])
    
    average_grade = sum(all_grades)/len(all_grades)
    return average_grade

#2 - для подсчета средней оценки за лекции всех лекторов в рамках курса (в качестве аргумента принимаем список лекторов и название курса)
 #Функция выше универсальна т к и у студентов и у лекторов есть параметр grades одинаковой структуры


#--------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------Полевые испытания-------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------

# Создаем студентов
student_A = Student("Иван", "Иванов", "дотер")
student_B = Student("Петр", "Петров", "танкист")

# Создаем лекторов
lecturer_A = Lecturer("Илья", "Ильин")
lecturer_B = Lecturer("Алексей", "Алексеев")

# Создаем экспертов
reviewer_A = Reviewer("Семен", "Мойколлега")
reviewer_B = Reviewer("Сидор", "Ович")

# Зачисляем студентов на два курса
student_A.courses_in_progress += ['course_A']
student_A.courses_in_progress += ['course_B']
student_B.courses_in_progress += ['course_A']
student_B.courses_in_progress += ['course_B']

# Прикрепляем лекторов к двум курсам
lecturer_A.courses_attached += ['course_A']
lecturer_A.courses_attached += ['course_B']
lecturer_B.courses_attached += ['course_A']
lecturer_B.courses_attached += ['course_B']

# Закрепляем экспертов за двумя курсами
reviewer_A.courses_attached += ['course_A']
reviewer_B.courses_attached += ['course_B']
reviewer_A.courses_attached += ['course_A']
reviewer_B.courses_attached += ['course_B']

# Каждый ученик ставит одну оценку каждому лектору за каждый курс
student_A.rate_the_lecture(lecturer_A, 'course_A', 6)
student_A.rate_the_lecture(lecturer_A, 'course_B', 7)
student_A.rate_the_lecture(lecturer_B, 'course_A', 6)
student_A.rate_the_lecture(lecturer_B, 'course_B', 10)
student_B.rate_the_lecture(lecturer_A, 'course_A', 8)
student_B.rate_the_lecture(lecturer_A, 'course_B', 7)
student_B.rate_the_lecture(lecturer_B, 'course_A', 8)
student_B.rate_the_lecture(lecturer_B, 'course_B', 10)

# Каждый эксперт ставит одну оценку каждому ученику за каждый курс
reviewer_A.rate_hw(student_A, 'course_A', 10)
reviewer_A.rate_hw(student_A, 'course_B', 8)
reviewer_A.rate_hw(student_B, 'course_A', 7)
reviewer_A.rate_hw(student_B, 'course_B', 8)
reviewer_B.rate_hw(student_A, 'course_A', 10)
reviewer_B.rate_hw(student_A, 'course_B', 6)
reviewer_B.rate_hw(student_B, 'course_A', 7)
reviewer_B.rate_hw(student_B, 'course_B', 6)

# Все студенты
print(student_A)
print(student_B)

# Все лекторы
print(lecturer_A)
print(lecturer_B)

# Все эксперты
print(reviewer_A)
print(reviewer_B)

print(аverageCourseGrade([student_A, student_B], 'course_A'))
print(аverageCourseGrade([student_A, student_B], 'course_B'))

print(аverageCourseGrade([lecturer_A, lecturer_B], 'course_A'))
print(аverageCourseGrade([lecturer_A, lecturer_B], 'course_B'))

# Все сравнения в одну сторону
print(student_A.averageGrade(), student_B.averageGrade())
print(student_A > student_B)
print(student_A >= student_B)
print(student_A == student_B)
# и в другую
print(student_A.averageGrade(), student_B.averageGrade())
print(student_A < student_B)
print(student_A <= student_B)
print(student_A != student_B)

# Для лекторов аналогично
print(lecturer_A.averageGrade(), lecturer_B.averageGrade())
print(lecturer_A > lecturer_B)
print(lecturer_A >= lecturer_B)
print(lecturer_A == lecturer_B)

print(lecturer_A.averageGrade(), lecturer_B.averageGrade())
print(lecturer_A < lecturer_B)
print(lecturer_A <= lecturer_B)
print(lecturer_A != lecturer_B)
