import sys
import pymysql
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, \
    QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QListWidget, QComboBox
from PyQt6.QtCore import pyqtSignal


def create_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            db='kursovoy'
        )
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
    return connection


class TeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Преподаватель')
        self.setFixedSize(1066, 800)

        title_label = QLabel('Преподаватель')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.teacher_table = QTableWidget()
        self.teacher_table.setColumnCount(6)
        self.teacher_table.setHorizontalHeaderLabels(['Фамилия', 'Имя', 'Отчество', 'Номер телефона', 'Почта', 'Рабочая почта'])

        self.load_teachers_from_db()

        header = self.teacher_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        add_teacher_button = QPushButton('Добавить преподавателя')
        add_teacher_button.clicked.connect(self.open_add_teacher_window)
        delete_teacher_button = QPushButton('Удалить преподавателя')
        delete_teacher_button.clicked.connect(self.delete_selected_teacher)
        edit_teacher_button = QPushButton('Редактировать преподавателя')
        edit_teacher_button.clicked.connect(self.open_edit_teacher_window)
        return_button = QPushButton('Вернуться на вторую форму')
        return_button.clicked.connect(self.return_to_second_window)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.teacher_table)

        button_layout = QVBoxLayout()
        button_layout.addWidget(add_teacher_button)
        button_layout.addWidget(delete_teacher_button)
        button_layout.addWidget(edit_teacher_button)
        button_layout.addWidget(return_button)
        button_layout.addStretch()

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        # Центрирование окна
        self.center()

    def center(self):
        # Центрирование окна на экране
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def load_teachers_from_db(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT COD_Teacher, Surname, Name, Midlname, Phone_number, Work_email FROM teachers"
                    cursor.execute(sql)
                    teachers = cursor.fetchall()

                    self.teacher_table.setRowCount(len(teachers))
                    for row, teacher in enumerate(teachers):
                        self.teacher_table.setItem(row, 0, QTableWidgetItem(str(teacher[0])))
                        for column, data in enumerate(teacher[1:], start=1):
                            self.teacher_table.setItem(row, column, QTableWidgetItem(data))
                    self.teacher_table.setColumnHidden(0, True)
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке данных: {e}")
            finally:
                connection.close()

    def delete_selected_teacher(self):
        selected_row = self.teacher_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Удаление преподавателя", "Пожалуйста, выберите преподавателя для удаления.")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить выбранного преподавателя?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Get the teacher's COD_Teacher from the hidden column
            teacher_id = self.teacher_table.item(selected_row, 0).text()

            connection = create_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        # SQL query to delete the teacher by COD_Teacher
                        sql = "DELETE FROM teachers WHERE COD_Teacher = %s"
                        cursor.execute(sql, (teacher_id,))
                    connection.commit()
                    QMessageBox.information(self, "Удаление", "Преподаватель удален.")
                    self.teacher_table.removeRow(selected_row)
                except pymysql.MySQLError as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении: {e}")
                finally:
                    connection.close()

    def return_to_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()
        self.close()

    def open_add_teacher_window(self):
        self.add_teacher_window = AddTeacherWindow()
        self.add_teacher_window.show()
        self.add_teacher_window.closeEvent = self.reload_teachers

    def open_edit_teacher_window(self):
        selected_row = self.teacher_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Редактирование преподавателя", "Пожалуйста, выберите преподавателя для редактирования.")
            return

        # Get the current data from the selected row, including the hidden COD_Teacher
        teacher_data = [self.teacher_table.item(selected_row, column).text() for column in range(self.teacher_table.columnCount())]
        self.edit_teacher_window = EditTeacherWindow(teacher_data)
        self.edit_teacher_window.show()
        self.edit_teacher_window.closeEvent = self.reload_teachers

    def reload_teachers(self, event):
        self.load_teachers_from_db()
        event.accept()


class EditTeacherWindow(QWidget):
    def __init__(self, teacher_data):
        super().__init__()
        self.setWindowTitle('Редактировать преподавателя')
        self.setFixedSize(400, 300)

        self.teacher_id = teacher_data[0]  # Store the COD_Teacher

        layout = QVBoxLayout()

        self.surname_input = QLineEdit(teacher_data[1])
        self.name_input = QLineEdit(teacher_data[2])
        self.patronymic_input = QLineEdit(teacher_data[3])
        self.phone_input = QLineEdit(teacher_data[4])
        self.email_input = QLineEdit(teacher_data[5])

        button_layout = QHBoxLayout()

        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_teacher)

        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(save_button)
        button_layout.addWidget(exit_button)

        layout.addWidget(self.surname_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.patronymic_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_teacher(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # SQL query to update teacher information using COD_Teacher
                    sql = """
                    UPDATE teachers
                    SET Surname=%s, Name=%s, Midlname=%s, Phone_number=%s, Work_email=%s
                    WHERE COD_Teacher=%s
                    """
                    cursor.execute(sql, (
                        self.surname_input.text(),
                        self.name_input.text(),
                        self.patronymic_input.text(),
                        self.phone_input.text(),
                        self.email_input.text(),
                        self.teacher_id
                    ))
                connection.commit()
                QMessageBox.information(self, "Сохранение", "Изменения сохранены.")
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении: {e}")
            finally:
                connection.close()
        self.close()


class AddTeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить преподавателя')
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText('Фамилия')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Имя')
        self.patronymic_input = QLineEdit()
        self.patronymic_input.setPlaceholderText('Отчество')
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('Номер телефона')
        self.phone_input.setMaxLength(12)  # Set maximum length to 12 characters
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Почта')

        button_layout = QHBoxLayout()

        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_teacher)

        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(save_button)
        button_layout.addWidget(exit_button)

        layout.addWidget(self.surname_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.patronymic_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_teacher(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # SQL-запрос для добавления нового преподавателя
                    sql = """
                    INSERT INTO teachers (Surname, Name, Midlname, Phone_number, Work_email)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        self.surname_input.text(),
                        self.name_input.text(),
                        self.patronymic_input.text(),
                        self.phone_input.text(),
                        self.email_input.text()
                    ))
                connection.commit()
                QMessageBox.information(self, "Сохранение", "Преподаватель добавлен.")
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении: {e}")
            finally:
                connection.close()
        self.close()


# Continue with the rest of your classes and methods...
class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ученики')
        self.setFixedSize(1066, 800)

        title_label = QLabel('Ученики')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создание таблицы для отображения характеристик учеников
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)  # Включая скрытую колонку для COD_Student
        self.student_table.setHorizontalHeaderLabels(['Фамилия', 'Имя', 'Отчество', 'Телефон', 'ID'])

        self.load_students_from_db()

        # Установка режима растяжения столбцов
        header = self.student_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        add_student_button = QPushButton('Добавить ученика')
        add_student_button.clicked.connect(self.open_add_student_window)
        delete_student_button = QPushButton('Удалить ученика')
        delete_student_button.clicked.connect(self.delete_selected_student)
        edit_student_button = QPushButton('Редактировать ученика')
        edit_student_button.clicked.connect(self.open_edit_student_window)
        return_button = QPushButton('Вернуться на вторую форму')
        return_button.clicked.connect(self.return_to_second_window)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.student_table)

        button_layout = QVBoxLayout()
        button_layout.addWidget(add_student_button)
        button_layout.addWidget(delete_student_button)
        button_layout.addWidget(edit_student_button)
        button_layout.addWidget(return_button)
        button_layout.addStretch()

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        # Центрирование окна
        self.center()

    def center(self):
        # Центрирование окна на экране
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def load_students_from_db(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT COD_Student, Surname, Name, Midlname, Phone_number FROM student"
                    cursor.execute(sql)
                    students = cursor.fetchall()

                    self.student_table.setRowCount(len(students))
                    for row, student in enumerate(students):
                        self.student_table.setItem(row, 0, QTableWidgetItem(str(student[1])))  # Фамилия
                        self.student_table.setItem(row, 1, QTableWidgetItem(student[2]))  # Имя
                        self.student_table.setItem(row, 2, QTableWidgetItem(student[3]))  # Отчество
                        self.student_table.setItem(row, 3, QTableWidgetItem(student[4]))  # Телефон
                        self.student_table.setItem(row, 4, QTableWidgetItem(str(student[0])))  # ID
                    self.student_table.setColumnHidden(4, True)  # Скрываем колонку COD_Student
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке данных: {e}")
            finally:
                connection.close()


    def delete_selected_student(self):
        selected_row = self.student_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Удаление ученика", "Пожалуйста, выберите ученика для удаления.")
            return

        # Подтверждение удаления
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить выбранного ученика?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Получаем COD_Student из скрытой колонки
            student_id = self.student_table.item(selected_row, 4).text()

            connection = create_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        # SQL-запрос для удаления ученика по COD_Student
                        sql = "DELETE FROM student WHERE COD_Student = %s"
                        cursor.execute(sql, (student_id,))
                    connection.commit()
                    QMessageBox.information(self, "Удаление", "Ученик удален.")
                    self.student_table.removeRow(selected_row)
                except pymysql.MySQLError as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении: {e}")
                finally:
                    connection.close()

    def return_to_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()
        self.close()

    def open_add_student_window(self):
        self.add_student_window = AddStudentWindow()
        self.add_student_window.show()
        self.add_student_window.closeEvent = self.reload_students

    def open_edit_student_window(self):
        selected_row = self.student_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Редактирование ученика", "Пожалуйста, выберите ученика для редактирования.")
            return

        # Get the current data from the selected row, including the hidden COD_Student
        student_data = [self.student_table.item(selected_row, column).text() for column in range(self.student_table.columnCount())]
        self.edit_student_window = EditStudentWindow(student_data)
        self.edit_student_window.show()
        self.edit_student_window.closeEvent = self.reload_students


    def reload_students(self, event):
        self.load_students_from_db()
        event.accept()


class EditStudentWindow(QWidget):
    def __init__(self, student_data):
        super().__init__()
        self.setWindowTitle('Редактировать ученика')
        self.setFixedSize(400, 300)

        self.student_id = student_data[4]  # Store the COD_Student

        layout = QVBoxLayout()

        self.surname_input = QLineEdit(student_data[0])
        self.name_input = QLineEdit(student_data[1])
        self.patronymic_input = QLineEdit(student_data[2])
        self.phone_input = QLineEdit(student_data[3])

        button_layout = QHBoxLayout()

        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_student)

        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(save_button)
        button_layout.addWidget(exit_button)

        layout.addWidget(self.surname_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.patronymic_input)
        layout.addWidget(self.phone_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)


    def save_student(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # SQL query to update student information using COD_Student
                    sql = """
                    UPDATE student
                    SET Surname=%s, Name=%s, Midlname=%s, Phone_number=%s
                    WHERE COD_Student=%s
                    """
                    cursor.execute(sql, (
                        self.surname_input.text(),
                        self.name_input.text(),
                        self.patronymic_input.text(),
                        self.phone_input.text(),
                        self.student_id
                    ))
                connection.commit()
                QMessageBox.information(self, "Сохранение", "Изменения сохранены.")
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении: {e}")
            finally:
                connection.close()
        self.close()

class AddStudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить ученика')
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText('Фамилия')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Имя')
        self.patronymic_input = QLineEdit()
        self.patronymic_input.setPlaceholderText('Отчество')
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('Телефон')

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_student)

        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)

        # Add buttons to the horizontal layout
        button_layout.addWidget(save_button)
        button_layout.addWidget(exit_button)

        # Add widgets to the main layout
        layout.addWidget(self.surname_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.patronymic_input)
        layout.addWidget(self.phone_input)
        layout.addLayout(button_layout)  # Add the button layout to the main layout

        self.setLayout(layout)

    def save_student(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # SQL-запрос для добавления нового ученика
                    sql = """
                    INSERT INTO student (Surname, Name, Midlname, Phone_number)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        self.surname_input.text(),
                        self.name_input.text(),
                        self.patronymic_input.text(),
                        self.phone_input.text()
                    ))
                connection.commit()
                QMessageBox.information(self, "Сохранение", "Ученик добавлен.")
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении: {e}")
            finally:
                connection.close()
        self.close()

class AddGroupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить группу')
        self.setFixedSize(400, 400)

        main_layout = QVBoxLayout()

        # Title label
        title_label = QLabel('Добавление группы')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Button to add a new student
        add_student_button = QPushButton('Добавить ученика')
        add_student_button.clicked.connect(self.add_student)
        main_layout.addWidget(add_student_button)

        # List of students in the group
        self.student_list = QListWidget()
        self.load_students()
        main_layout.addWidget(self.student_list)

        # Buttons for actions
        button_layout = QHBoxLayout()

        delete_student_button = QPushButton('Удалить ученика')
        delete_student_button.clicked.connect(self.delete_selected_student)

        save_group_button = QPushButton('Сохранить группу')
        save_group_button.clicked.connect(self.save_group)

        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(delete_student_button)
        button_layout.addWidget(save_group_button)
        button_layout.addWidget(exit_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def load_students(self):
        # Logic to load students from the database
        # For demonstration, adding dummy data
        self.student_list.addItem("Ученик 1")
        self.student_list.addItem("Ученик 2")
        self.student_list.addItem("Ученик 3")

    def add_student(self):
        # Logic to add a new student
        # For demonstration, adding a dummy student
        self.student_list.addItem("Новый ученик")

    def delete_selected_student(self):
        selected_row = self.student_list.currentRow()
        if selected_row != -1:
            self.student_list.takeItem(selected_row)
        else:
            QMessageBox.warning(self, "Удаление ученика", "Пожалуйста, выберите ученика для удаления.")

    def save_group(self):
        # Logic to save the group
        QMessageBox.information(self, "Сохранение", "Группа сохранена.")
        self.close()

class ThirdWindow(QWidget):
    course_added = pyqtSignal()  # Define a signal for when a course is added

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить курс')
        self.setFixedSize(600, 400)

        main_layout = QVBoxLayout()

        title_label = QLabel('Добавление курса')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        content_layout = QHBoxLayout()

        group_layout = QVBoxLayout()

        add_group_button = QPushButton('Добавить новую группу')
        add_group_button.clicked.connect(self.open_add_group_window)
        group_layout.addWidget(add_group_button)

        self.group_list = QListWidget()
        self.load_existing_groups()
        group_layout.addWidget(self.group_list)

        content_layout.addLayout(group_layout)

        course_layout = QVBoxLayout()

        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText('Наименование курса')
        course_layout.addWidget(self.course_name_input)

        self.teacher_combo = QComboBox()
        self.load_teachers()
        course_layout.addWidget(self.teacher_combo)

        self.language_input = QLineEdit()
        self.language_input.setPlaceholderText('Язык')
        course_layout.addWidget(self.language_input)

        button_layout = QHBoxLayout()
        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_course)
        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(save_button)
        button_layout.addWidget(exit_button)

        course_layout.addLayout(button_layout)
        content_layout.addLayout(course_layout)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def load_existing_groups(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    SELECT COD_Groups, COD_Courses, COD_Student
                    FROM groups
                    """
                    cursor.execute(sql)
                    groups = cursor.fetchall()
                    for group in groups:
                        self.group_list.addItem(f"Group ID: {group[0]}, Course ID: {group[1]}, Student ID: {group[2]}")
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке групп: {e}")
            finally:
                connection.close()

    def open_add_group_window(self):
        self.add_group_window = AddGroupWindow()
        self.add_group_window.show()

    def load_teachers(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT COD_Teacher, Surname FROM teachers"
                    cursor.execute(sql)
                    teachers = cursor.fetchall()
                    for teacher in teachers:
                        self.teacher_combo.addItem(teacher[1], teacher[0])
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке преподавателей: {e}")
            finally:
                connection.close()

    def save_course(self):
        course_name = self.course_name_input.text()
        teacher_id = self.teacher_combo.currentData()
        language = self.language_input.text()

        if not course_name or not teacher_id or not language:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    INSERT INTO courses (Course_Name, COD_Teacher, Language)
                    VALUES (%s, %s, %s)
                    """
                    cursor.execute(sql, (course_name, teacher_id, language))
                connection.commit()
                QMessageBox.information(self, "Сохранение", f"Курс '{course_name}' добавлен.")
                self.course_added.emit()  # Emit the signal to indicate a course was added
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении курса: {e}")
            finally:
                connection.close()
        self.close()


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Курсы')
        self.setFixedSize(1066, 800)

        title_label = QLabel('Курсы')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.course_table = QTableWidget()
        self.course_table.setColumnCount(3)
        self.course_table.setHorizontalHeaderLabels(['Наименование курса', 'Преподаватель', 'Язык'])

        self.load_courses_from_db()

        header = self.course_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        teacher_button = QPushButton('Преподаватель')
        teacher_button.clicked.connect(self.open_teacher_window)
        student_button = QPushButton('Ученика')
        student_button.clicked.connect(self.open_student_window)
        add_course_button = QPushButton('Добавить курс')
        add_course_button.clicked.connect(self.open_third_window)
        delete_courses_button = QPushButton('Удалить курс')
        delete_courses_button.clicked.connect(self.delete_selected_course)
        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.course_table)

        button_layout = QVBoxLayout()
        button_layout.addWidget(teacher_button)
        button_layout.addWidget(student_button)
        button_layout.addWidget(add_course_button)
        button_layout.addWidget(delete_courses_button)
        button_layout.addWidget(exit_button)
        button_layout.addStretch()

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        self.center()

    def center(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def load_courses_from_db(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    SELECT c.Course_Name, t.Surname, c.Language
                    FROM courses c
                    JOIN teachers t ON c.COD_Teacher = t.COD_Teacher
                    """
                    cursor.execute(sql)
                    courses = cursor.fetchall()

                    self.course_table.setRowCount(len(courses))
                    for row, course in enumerate(courses):
                        self.course_table.setItem(row, 0, QTableWidgetItem(course[0]))
                        self.course_table.setItem(row, 1, QTableWidgetItem(course[1]))
                        self.course_table.setItem(row, 2, QTableWidgetItem(course[2]))
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке данных: {e}")
            finally:
                connection.close()

    def delete_selected_course(self):
        selected_row = self.course_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Удаление курса", "Пожалуйста, выберите курс для удаления.")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить выбранный курс?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            course_name = self.course_table.item(selected_row, 0).text()

            connection = create_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = "DELETE FROM courses WHERE Course_Name = %s"
                        cursor.execute(sql, (course_name,))
                    connection.commit()
                    QMessageBox.information(self, "Удаление", "Курс удален.")
                    self.course_table.removeRow(selected_row)
                except pymysql.MySQLError as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении: {e}")
                finally:
                    connection.close()

    def open_third_window(self):
        self.third_window = ThirdWindow()
        self.third_window.course_added.connect(self.load_courses_from_db)  # Connect the signal to reload courses
        self.third_window.show()

    def open_teacher_window(self):
        self.teacher_window = TeacherWindow()
        self.teacher_window.show()
        self.close()

    def open_student_window(self):
        self.student_window = StudentWindow()
        self.student_window.show()
        self.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Установка заголовка окна
        self.setWindowTitle('Авторизация')

        # Установка фиксированного размера окна
        self.setFixedSize(533, 400)

        # Создание виджетов
        self.login_label = QLabel('Логин:')
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_input = QLineEdit()
        self.login_input.setFixedWidth(400)  # Увеличение фиксированной ширины

        self.password_label = QLabel('Пароль:')
        self.password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(400)  # Увеличение фиксированной ширины

        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.handle_login)

        # Установка компоновки
        layout = QVBoxLayout()

        # Центрирование полей ввода
        login_layout = QHBoxLayout()
        login_layout.addStretch()
        login_layout.addWidget(self.login_input)
        login_layout.addStretch()

        password_layout = QHBoxLayout()
        password_layout.addStretch()
        password_layout.addWidget(self.password_input)
        password_layout.addStretch()

        layout.addWidget(self.login_label)
        layout.addLayout(login_layout)
        layout.addWidget(self.password_label)
        layout.addLayout(password_layout)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Центрирование окна
        self.center()

    def center(self):
        # Центрирование окна на экране
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def handle_login(self):
    # Получаем введенные логин и пароль
        login = self.login_input.text()
        password = self.password_input.text()

        # Устанавливаем соединение с базой данных
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Запрос для проверки существования учетных данных в таблице authorization
                    sql = "SELECT * FROM authorization WHERE Name_Admin=%s AND Password_Admin=%s"
                    cursor.execute(sql, (login, password))
                    result = cursor.fetchone()

                    if result:
                        # Если учетные данные верны, открываем второе окно
                        self.second_window = SecondWindow()
                        self.second_window.show()
                        self.close()  # Закрываем окно авторизации
                    else:
                        # Если учетные данные неверны, показываем сообщение об ошибке
                        QMessageBox.warning(self, "Ошибка входа", "Неверный логин или пароль.")
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при подключении к базе данных: {e}")
            finally:
                connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())