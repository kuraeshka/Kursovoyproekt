import sys
import pymysql
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QMessageBox, QListWidget, QComboBox, QListWidgetItem, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import pyqtSignal


def apply_styles(widget):
    # Основной стиль для окна
    widget.setStyleSheet("""
        QWidget {
            background-color: #E3F2FD;
        }
        QLabel {
            color: #1976D2;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        QLineEdit {
            padding: 8px;
            border: 2px solid #BBDEFB;
            border-radius: 4px;
            background-color: white;
        }
        QLineEdit:focus {
            border: 2px solid #2196F3;
        }
        QTableWidget {
            background-color: white;
            border: 2px solid #BBDEFB;
            border-radius: 4px;
        }
        QTableWidget::item:selected {
            background-color: #BBDEFB;
        }
        QHeaderView::section {
            background-color: #2196F3;
            color: white;
            padding: 6px;
            border: none;
        }
        QListWidget {
            background-color: white;
            border: 2px solid #BBDEFB;
            border-radius: 4px;
        }
        QListWidget::item:selected {
            background-color: #BBDEFB;
            color: #0D47A1;
        }
        QComboBox {
            padding: 8px;
            border: 2px solid #BBDEFB;
            border-radius: 4px;
            background-color: white;
        }
        QComboBox:drop-down {
            border: none;
        }
        QComboBox:down-arrow {
            background-color: #2196F3;
        }
    """)


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
        apply_styles(self)
        self.setWindowTitle('Преподаватель')
        self.setFixedSize(1066, 800)

        title_label = QLabel('Преподаватель')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.teacher_table = QTableWidget()
        self.teacher_table.setColumnCount(6)
        self.teacher_table.setHorizontalHeaderLabels(
            ['Фамилия', 'Имя', 'Отчество', 'Номер телефона', 'Почта', 'Рабочая почта'])

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
            QMessageBox.warning(self, "Редактирование преподавателя",
                                "Пожалуйста, выберите преподавателя для редактирования.")
            return

        # Get the current data from the selected row, including the hidden COD_Teacher
        teacher_data = [self.teacher_table.item(selected_row, column).text() for column in
                        range(self.teacher_table.columnCount())]
        self.edit_teacher_window = EditTeacherWindow(teacher_data)
        self.edit_teacher_window.show()
        self.edit_teacher_window.closeEvent = self.reload_teachers

    def reload_teachers(self, event):
        self.load_teachers_from_db()
        event.accept()


class EditTeacherWindow(QWidget):
    def __init__(self, teacher_data):
        super().__init__()
        apply_styles(self)
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
        apply_styles(self)
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
        apply_styles(self)
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
        student_data = [self.student_table.item(selected_row, column).text() for column in
                        range(self.student_table.columnCount())]
        self.edit_student_window = EditStudentWindow(student_data)
        self.edit_student_window.show()
        self.edit_student_window.closeEvent = self.reload_students

    def reload_students(self, event):
        self.load_students_from_db()
        event.accept()


class EditStudentWindow(QWidget):
    def __init__(self, student_data):
        super().__init__()
        apply_styles(self)
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
        apply_styles(self)
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


class SelectStudentWindow(QWidget):
    student_selected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Выбрать ученика')
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        # Список всех учеников
        self.student_list = QListWidget()
        self.load_students()
        layout.addWidget(self.student_list)

        # Кнопки
        button_layout = QHBoxLayout()

        select_button = QPushButton('Выбрать')
        select_button.clicked.connect(self.select_student)

        cancel_button = QPushButton('Отмена')
        cancel_button.clicked.connect(self.close)

        button_layout.addWidget(select_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_students(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    SELECT COD_Student, Surname, Name, Midlname, Phone_number 
                    FROM student 
                    ORDER BY Surname, Name
                    """
                    cursor.execute(sql)
                    students = cursor.fetchall()

                    for student in students:
                        item = QListWidgetItem(f"{student[1]} {student[2]} {student[3]}")
                        # Сохраняем все данные о студенте
                        item.setData(Qt.ItemDataRole.UserRole, {
                            'id': student[0],
                            'surname': student[1],
                            'name': student[2],
                            'patronymic': student[3],
                            'phone': student[4]
                        })
                        self.student_list.addItem(item)
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке студентов: {e}")
            finally:
                connection.close()

    def select_student(self):
        selected_item = self.student_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Выбор ученика", "Пожалуйста, выберите ученика")
            return

        student_data = selected_item.data(Qt.ItemDataRole.UserRole)
        self.student_selected.emit(student_data)
        self.close()


class AddGroupWindow(QWidget):
    group_saved = pyqtSignal()

    def __init__(self, course_id=None):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Добавить группу')
        self.setFixedSize(600, 500)
        self.course_id = course_id

        main_layout = QVBoxLayout()

        # Кнопки для добавления учеников
        buttons_layout = QHBoxLayout()

        add_new_student_button = QPushButton('Добавить нового ученика')
        add_new_student_button.clicked.connect(self.open_add_student_window)

        select_student_button = QPushButton('Выбрать из списка')
        select_student_button.clicked.connect(self.open_select_student_window)

        buttons_layout.addWidget(add_new_student_button)
        buttons_layout.addWidget(select_student_button)
        main_layout.addLayout(buttons_layout)

        # Список учеников в группе
        students_label = QLabel('Ученики в группе:')
        main_layout.addWidget(students_label)

        self.student_list = QListWidget()
        main_layout.addWidget(self.student_list)

        # Кнопки действий
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

    def open_select_student_window(self):
        self.select_student_window = SelectStudentWindow()
        self.select_student_window.student_selected.connect(self.add_student_to_list)
        self.select_student_window.show()

    # Остальные методы остаются без изменений...

    def open_add_student_window(self):
        # Получаем ID группы после её создания
        group_id = None
        if hasattr(self, 'group_id'):
            group_id = self.group_id

        self.add_student_window = AddStudentToGroupWindow(group_id=group_id)
        self.add_student_window.student_added.connect(self.add_student_to_list)
        self.add_student_window.show()

    def add_student_to_list(self, student_data):
        # Проверяем, не добавлен ли уже этот студент
        for i in range(self.student_list.count()):
            item = self.student_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == student_data['id']:
                QMessageBox.warning(self, "Добавление ученика", "Этот ученик уже добавлен в группу")
                return

        # Добавляем нового ученика в список
        item = QListWidgetItem(f"{student_data['surname']} {student_data['name']} {student_data['patronymic']}")
        item.setData(Qt.ItemDataRole.UserRole, student_data['id'])
        self.student_list.addItem(item)

    def delete_selected_student(self):
        selected_item = self.student_list.currentItem()
        if selected_item:
            self.student_list.takeItem(self.student_list.row(selected_item))
        else:
            QMessageBox.warning(self, "Удаление ученика", "Выберите ученика для удаления")

    def save_group(self):
        if self.student_list.count() == 0:
            QMessageBox.warning(self, "Сохранение группы", "Добавьте хотя бы одного ученика в группу")
            return

        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Создаем новую группу
                    sql = """
                    INSERT INTO groups (COD_Courses)
                    VALUES (%s)
                    """
                    cursor.execute(sql, (self.course_id,))
                    group_id = cursor.lastrowid

                    # Добавляем всех студентов в группу через таблицу group_students
                    for i in range(self.student_list.count()):
                        item = self.student_list.item(i)
                        student_id = item.data(Qt.ItemDataRole.UserRole)

                        sql = """
                        INSERT INTO group_students (COD_Groups, COD_Student)
                        VALUES (%s, %s)
                        """
                        cursor.execute(sql, (group_id, student_id))

                    connection.commit()
                    QMessageBox.information(self, "Сохранение", "Группа успешно создана")
                    self.group_saved.emit()
                    self.close()

            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении группы: {e}")
                connection.rollback()
            finally:
                connection.close()


class AddStudentToGroupWindow(QWidget):
    student_added = pyqtSignal(dict)

    def __init__(self, group_id=None, course_id=None):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Добавить ученика')
        self.setFixedSize(400, 300)

        # Сохраняем ID группы и курса
        self.group_id = group_id
        self.course_id = course_id

        layout = QVBoxLayout()

        # Поля ввода
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText('Фамилия')

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Имя')

        self.patronymic_input = QLineEdit()
        self.patronymic_input.setPlaceholderText('Отчество')

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('Телефон')

        # Кнопки
        button_layout = QHBoxLayout()
        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_student)

        cancel_button = QPushButton('Отмена')
        cancel_button.clicked.connect(self.close)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Добавляем виджеты в layout
        layout.addWidget(self.surname_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.patronymic_input)
        layout.addWidget(self.phone_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_student(self):
        # Проверка заполнения обязательных полей
        if not all([self.surname_input.text(), self.name_input.text(), self.patronymic_input.text()]):
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return

        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Добавляем нового ученика в таблицу student
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
                    student_id = cursor.lastrowid

                    # Добавляем связь ученика с группой в таблицу group_students
                    if self.group_id:
                        sql = """
                        INSERT INTO group_students (COD_Groups, COD_Student)
                        VALUES (%s, %s)
                        """
                        cursor.execute(sql, (self.group_id, student_id))

                connection.commit()

                # Отправляем сигнал с данными нового ученика
                self.student_added.emit({
                    'id': student_id,
                    'surname': self.surname_input.text(),
                    'name': self.name_input.text(),
                    'patronymic': self.patronymic_input.text(),
                    'phone': self.phone_input.text()
                })

                self.close()
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении: {e}")
            finally:
                connection.close()


class ThirdWindow(QWidget):
    course_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Добавить курс')
        self.setFixedSize(400, 300)  # Reduced width since we removed the group list

        main_layout = QVBoxLayout()

        title_label = QLabel('Добавление курса')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Course information layout
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

        # Buttons layout
        button_layout = QHBoxLayout()
        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_course)
        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(save_button)
        button_layout.addWidget(exit_button)

        course_layout.addLayout(button_layout)
        main_layout.addLayout(course_layout)

        self.setLayout(main_layout)

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
                QMessageBox.information(self, "Сохранение", f"Курс '{course_name}' успешно сохранен")
                self.course_added.emit()
                self.close()
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении курса: {e}")
                connection.rollback()
            finally:
                connection.close()

class EditGroupWindow(QWidget):
    group_updated = pyqtSignal()

    def __init__(self, course_id):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Редактирование группы')
        self.setFixedSize(600, 500)
        self.course_id = course_id

        main_layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel('Редактирование группы')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Кнопка добавления ученика
        add_student_button = QPushButton('Добавить ученика')
        add_student_button.clicked.connect(self.open_add_student_window)
        main_layout.addWidget(add_student_button)

        # Список учеников
        self.student_list = QListWidget()
        self.load_students()
        main_layout.addWidget(self.student_list)

        # Кнопки действий
        button_layout = QHBoxLayout()

        delete_student_button = QPushButton('Удалить ученика')
        delete_student_button.clicked.connect(self.delete_selected_student)

        save_button = QPushButton('Сохранить группу')
        save_button.clicked.connect(self.save_group)

        delete_group_button = QPushButton('Удалить группу')
        delete_group_button.clicked.connect(self.delete_group)

        button_layout.addWidget(delete_student_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(delete_group_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def load_students(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    SELECT s.COD_Student, s.Surname, s.Name, s.Midlname
                    FROM student s
                    JOIN groups g ON s.COD_Student = g.COD_Student
                    WHERE g.COD_Courses = %s
                    """
                    cursor.execute(sql, (self.course_id,))
                    students = cursor.fetchall()
                    self.student_list.clear()
                    for student in students:
                        item = QListWidgetItem(f"{student[1]} {student[2]} {student[3]}")
                        item.setData(Qt.ItemDataRole.UserRole, student[0])
                        self.student_list.addItem(item)
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке студентов: {e}")
            finally:
                connection.close()

    def open_add_student_window(self):
        self.add_student_window = AddStudentToGroupWindow(course_id=self.course_id)
        self.add_student_window.student_added.connect(self.load_students)
        self.add_student_window.show()

    def delete_selected_student(self):
        selected_item = self.student_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Удаление", "Выберите ученика для удаления")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить этого ученика из группы?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            student_id = selected_item.data(Qt.ItemDataRole.UserRole)
            connection = create_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = """
                        DELETE FROM groups 
                        WHERE COD_Student = %s AND COD_Courses = %s
                        """
                        cursor.execute(sql, (student_id, self.course_id))
                    connection.commit()
                    self.load_students()
                except pymysql.MySQLError as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении: {e}")
                finally:
                    connection.close()

    def save_group(self):
        QMessageBox.information(self, "Сохранение", "Изменения сохранены")
        self.group_updated.emit()
        self.close()

    def delete_group(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить всю группу?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            connection = create_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = """
                        DELETE FROM groups 
                        WHERE COD_Courses = %s
                        """
                        cursor.execute(sql, (self.course_id,))
                    connection.commit()
                    self.group_updated.emit()
                    self.close()
                except pymysql.MySQLError as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении группы: {e}")
                finally:
                    connection.close()


class EditGroupWindow(QWidget):
    group_updated = pyqtSignal()

    def __init__(self, group_id):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Редактирование группы')
        self.setFixedSize(600, 500)
        self.group_id = group_id

        main_layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel('Редактирование группы')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Кнопки для добавления учеников
        buttons_layout = QHBoxLayout()

        select_student_button = QPushButton('Выбрать из списка')
        select_student_button.clicked.connect(self.open_select_student_window)
        buttons_layout.addWidget(select_student_button)

        main_layout.addLayout(buttons_layout)

        # Список учеников
        self.student_list = QListWidget()
        self.load_students()
        main_layout.addWidget(self.student_list)

        # Кнопки действий
        button_layout = QHBoxLayout()

        delete_student_button = QPushButton('Удалить ученика')
        delete_student_button.clicked.connect(self.delete_selected_student)

        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_group)

        delete_group_button = QPushButton('Удалить группу')
        delete_group_button.clicked.connect(self.delete_group)

        button_layout.addWidget(delete_student_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(delete_group_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def delete_group(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить группу?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            connection = create_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        # Сначала удаляем записи из таблицы group_students
                        sql = "DELETE FROM group_students WHERE COD_Groups = %s"
                        cursor.execute(sql, (self.group_id,))

                        # Затем удаляем саму группу
                        sql = "DELETE FROM groups WHERE COD_Groups = %s"
                        cursor.execute(sql, (self.group_id,))

                    connection.commit()
                    QMessageBox.information(self, "Удаление", "Группа успешно удалена")
                    self.group_updated.emit()
                    self.close()
                except pymysql.MySQLError as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении группы: {e}")
                    connection.rollback()
                finally:
                    connection.close()

    def load_students(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    SELECT s.COD_Student, s.Surname, s.Name, s.Midlname
                    FROM student s
                    JOIN group_students gs ON s.COD_Student = gs.COD_Student
                    WHERE gs.COD_Groups = %s
                    """
                    cursor.execute(sql, (self.group_id,))
                    students = cursor.fetchall()
                    self.student_list.clear()
                    for student in students:
                        item = QListWidgetItem(f"{student[1]} {student[2]} {student[3]}")
                        item.setData(Qt.ItemDataRole.UserRole, student[0])
                        self.student_list.addItem(item)
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке студентов: {e}")
            finally:
                connection.close()

    def open_select_student_window(self):
        self.select_student_window = SelectStudentWindow()
        self.select_student_window.student_selected.connect(self.add_student_to_list)
        self.select_student_window.show()

    def add_student_to_list(self, student_data):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    INSERT INTO group_students (COD_Groups, COD_Student)
                    VALUES (%s, %s)
                    """
                    cursor.execute(sql, (self.group_id, student_data['id']))
                connection.commit()
                self.load_students()
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении студента: {e}")
            finally:
                connection.close()

    def delete_selected_student(self):
        selected_item = self.student_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Удаление", "Выберите ученика для удаления")
            return

        student_id = selected_item.data(Qt.ItemDataRole.UserRole)
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    DELETE FROM group_students 
                    WHERE COD_Groups = %s AND COD_Student = %s
                    """
                    cursor.execute(sql, (self.group_id, student_id))
                connection.commit()
                self.load_students()
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении: {e}")
            finally:
                connection.close()

    def save_group(self):
        self.group_updated.emit()
        self.close()


class EditCourseWindow(QWidget):
    course_updated = pyqtSignal()

    def __init__(self, course_id, course_name, teacher_id, language):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Редактировать курс')
        self.setFixedSize(600, 400)
        self.course_id = course_id

        main_layout = QVBoxLayout()

        title_label = QLabel('Редактирование курса')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        content_layout = QHBoxLayout()

        # Левая часть с группами
        group_layout = QVBoxLayout()

        add_group_button = QPushButton('Добавить группу')
        add_group_button.clicked.connect(self.add_group)
        group_layout.addWidget(add_group_button)

        self.groups_list = QListWidget()
        self.groups_list.itemDoubleClicked.connect(self.edit_group)
        group_layout.addWidget(self.groups_list)

        content_layout.addLayout(group_layout)

        # Правая часть с информацией о курсе
        course_layout = QVBoxLayout()

        self.course_name_input = QLineEdit(course_name)
        self.course_name_input.setPlaceholderText('Наименование курса')
        course_layout.addWidget(self.course_name_input)

        self.teacher_combo = QComboBox()
        self.load_teachers(teacher_id)
        course_layout.addWidget(self.teacher_combo)

        self.language_input = QLineEdit(language)
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

        # Загружаем группы курса
        self.load_course_groups()

    def save_course(self):
        if not self.course_name_input.text() or not self.teacher_combo.currentData() or not self.language_input.text():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    UPDATE courses 
                    SET Course_Name = %s, COD_Teacher = %s, Language = %s
                    WHERE COD_Courses = %s
                    """
                    cursor.execute(sql, (
                        self.course_name_input.text(),
                        self.teacher_combo.currentData(),
                        self.language_input.text(),
                        self.course_id
                    ))
                connection.commit()
                QMessageBox.information(self, "Сохранение", "Изменения сохранены")
                self.course_updated.emit()
                self.close()
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении курса: {e}")
                connection.rollback()
            finally:
                connection.close()

    def edit_group(self, item):
        """Открывает окно редактирования группы при двойном клике"""
        group_id = item.data(Qt.ItemDataRole.UserRole)
        self.edit_group_window = EditGroupWindow(group_id)
        self.edit_group_window.group_updated.connect(self.load_course_groups)
        self.edit_group_window.show()

        self.edit_group_window.show()

    def load_course_groups(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Получаем все группы и их студентов для данного курса
                    sql = """
                    SELECT g.COD_Groups, s.Surname, s.Name, s.Midlname
                    FROM groups g
                    JOIN group_students gs ON g.COD_Groups = gs.COD_Groups
                    JOIN student s ON gs.COD_Student = s.COD_Student
                    WHERE g.COD_Courses = %s
                    ORDER BY g.COD_Groups
                    """
                    cursor.execute(sql, (self.course_id,))
                    students = cursor.fetchall()

                    # Создаем словарь для группировки студентов по группам
                    groups = {}
                    for row in students:
                        group_id = row[0]
                        student_name = f"{row[1]} {row[2]} {row[3]}"
                        if group_id in groups:
                            groups[group_id].append(student_name)
                        else:
                            groups[group_id] = [student_name]

                    # Очищаем список групп
                    self.groups_list.clear()

                    # Добавляем группы и их студентов в список
                    for group_id, students in groups.items():
                        item_text = f"Группа {group_id}"
                        if students:
                            item_text += f": {', '.join(students)}"
                        item = QListWidgetItem(item_text)
                        item.setData(Qt.ItemDataRole.UserRole, group_id)
                        self.groups_list.addItem(item)

            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке групп: {e}")
            finally:
                connection.close()

    def add_group(self):
        self.add_group_window = AddGroupWindow(self.course_id)
        self.add_group_window.group_saved.connect(
            self.load_course_groups)  # Подключаем сигнал к обновлению списка групп
        self.add_group_window.show()

    def delete_group(self):
        selected_item = self.groups_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Удаление группы", "Выберите группу для удаления")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить группу из курса?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            group_id = selected_item.data(Qt.ItemDataRole.UserRole)
            connection = create_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = """
                        UPDATE groups 
                        SET COD_Courses = NULL 
                        WHERE COD_Groups = %s
                        """
                        cursor.execute(sql, (group_id,))
                    connection.commit()
                    self.load_course_groups()
                except pymysql.MySQLError as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении группы: {e}")
                finally:
                    connection.close()

    def load_teachers(self, current_teacher_id):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT COD_Teacher, Surname FROM teachers"
                    cursor.execute(sql)
                    teachers = cursor.fetchall()
                    for teacher in teachers:
                        self.teacher_combo.addItem(teacher[1], teacher[0])
                        if teacher[0] == current_teacher_id:
                            self.teacher_combo.setCurrentIndex(self.teacher_combo.count() - 1)
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке преподавателей: {e}")
            finally:
                connection.close()


class SelectGroupWindow(QWidget):
    group_added = pyqtSignal()

    def __init__(self, course_id):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Выбрать группу')
        self.setFixedSize(400, 300)
        self.course_id = course_id

        layout = QVBoxLayout()

        # Список доступных групп
        self.groups_list = QListWidget()
        self.load_available_groups()
        layout.addWidget(self.groups_list)

        # Кнопки
        button_layout = QHBoxLayout()
        add_button = QPushButton('Добавить')
        add_button.clicked.connect(self.add_group_to_course)
        cancel_button = QPushButton('Отмена')
        cancel_button.clicked.connect(self.close)

        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_available_groups(self):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    SELECT COD_Groups, Name_Groups 
                    FROM groups 
                    WHERE COD_Courses IS NULL
                    """
                    cursor.execute(sql)
                    groups = cursor.fetchall()
                    for group in groups:
                        item = QListWidgetItem(f"{group[1]}")  # Отображаем Name_Groups
                        item.setData(Qt.ItemDataRole.UserRole, group[0])  # Сохраняем COD_Groups
                        self.groups_list.addItem(item)
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке групп: {e}")
            finally:
                connection.close()

    def add_group_to_course(self):
        selected_item = self.groups_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Добавление группы", "Выберите группу для добавления")
            return

        group_id = selected_item.data(Qt.ItemDataRole.UserRole)
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    UPDATE groups 
                    SET COD_Courses = %s 
                    WHERE COD_Groups = %s
                    """
                    cursor.execute(sql, (self.course_id, group_id))
                connection.commit()
                self.group_added.emit()
                self.close()
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении группы: {e}")
            finally:
                connection.close()


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        apply_styles(self)
        self.setWindowTitle('Курсы')
        self.setFixedSize(1066, 800)

        main_layout = QVBoxLayout()

        title_label = QLabel('Курсы')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        content_layout = QHBoxLayout()

        # Создаем таблицу
        self.course_table = QTableWidget()
        self.course_table.setColumnCount(4)
        self.course_table.setHorizontalHeaderLabels(['Наименование курса', 'Преподаватель', 'Язык', 'ID'])
        self.course_table.hideColumn(3)
        self.course_table.cellDoubleClicked.connect(self.open_edit_course_window)

        header = self.course_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        content_layout.addWidget(self.course_table)

        # Правая панель с кнопками и фильтром
        right_panel = QVBoxLayout()

        # Добавляем ComboBox для фильтрации по языку
        self.language_filter = QComboBox()
        self.language_filter.addItem("Все языки")
        self.language_filter.currentTextChanged.connect(self.filter_by_language)
        right_panel.addWidget(self.language_filter)

        # Кнопки
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

        right_panel.addWidget(teacher_button)
        right_panel.addWidget(student_button)
        right_panel.addWidget(add_course_button)
        right_panel.addWidget(delete_courses_button)
        right_panel.addWidget(exit_button)
        right_panel.addStretch()

        content_layout.addLayout(right_panel)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)
        self.center()

        # Загружаем данные
        self.load_courses_from_db()
        self.load_languages()

    def load_languages(self):
        """Загрузка списка языков из базы данных"""
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT DISTINCT Language FROM courses ORDER BY Language"
                    cursor.execute(sql)
                    languages = cursor.fetchall()

                    # Очищаем комбобокс, оставляя только "Все языки"
                    self.language_filter.clear()
                    self.language_filter.addItem("Все языки")

                    # Добавляем языки из базы данных
                    for language in languages:
                        if language[0]:  # Проверяем, что язык не пустой
                            self.language_filter.addItem(language[0])
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке языков: {e}")
            finally:
                connection.close()

    def filter_by_language(self, selected_language):
        """Фильтрация курсов по выбранному языку"""
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    if selected_language == "Все языки":
                        sql = """
                        SELECT c.COD_Courses, c.Course_Name, t.Surname, c.Language, c.COD_Teacher
                        FROM courses c
                        JOIN teachers t ON c.COD_Teacher = t.COD_Teacher
                        """
                        cursor.execute(sql)
                    else:
                        sql = """
                        SELECT c.COD_Courses, c.Course_Name, t.Surname, c.Language, c.COD_Teacher
                        FROM courses c
                        JOIN teachers t ON c.COD_Teacher = t.COD_Teacher
                        WHERE c.Language = %s
                        """
                        cursor.execute(sql, (selected_language,))

                    courses = cursor.fetchall()
                    self.course_table.setRowCount(len(courses))
                    for row, course in enumerate(courses):
                        self.course_table.setItem(row, 0, QTableWidgetItem(course[1]))  # Course_Name
                        self.course_table.setItem(row, 1, QTableWidgetItem(course[2]))  # Teacher Surname
                        self.course_table.setItem(row, 2, QTableWidgetItem(course[3]))  # Language
                        self.course_table.setItem(row, 3, QTableWidgetItem(str(course[0])))  # COD_Courses
                        self.course_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, course[4])
            except pymysql.MySQLError as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при фильтрации курсов: {e}")
            finally:
                connection.close()

    def open_edit_course_window(self, row, column):
        course_id = self.course_table.item(row, 3).text()
        course_name = self.course_table.item(row, 0).text()
        teacher_id = self.course_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        language = self.course_table.item(row, 2).text()

        self.edit_course_window = EditCourseWindow(course_id, course_name, teacher_id, language)
        self.edit_course_window.course_updated.connect(self.load_courses_from_db)
        self.edit_course_window.show()

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
                    SELECT c.COD_Courses, c.Course_Name, t.Surname, c.Language, c.COD_Teacher
                    FROM courses c
                    JOIN teachers t ON c.COD_Teacher = t.COD_Teacher
                    """
                    cursor.execute(sql)
                    courses = cursor.fetchall()

                    self.course_table.setRowCount(len(courses))
                    for row, course in enumerate(courses):
                        self.course_table.setItem(row, 0, QTableWidgetItem(course[1]))  # Course_Name
                        self.course_table.setItem(row, 1, QTableWidgetItem(course[2]))  # Teacher Surname
                        self.course_table.setItem(row, 2, QTableWidgetItem(course[3]))  # Language
                        self.course_table.setItem(row, 3, QTableWidgetItem(str(course[0])))  # COD_Courses
                        # Сохраняем COD_Teacher как дополнительные данные
                        self.course_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, course[4])
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
            # Get the course ID from the hidden column
            course_id = self.course_table.item(selected_row, 3).text()

            connection = create_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        # SQL query to delete the course by COD_Courses
                        sql = "DELETE FROM courses WHERE COD_Courses = %s"
                        cursor.execute(sql, (course_id,))
                    connection.commit()
                    QMessageBox.information(self, "Удаление", "Курс удален.")
                    self.course_table.removeRow(selected_row)
                    # Update the language list after deleting the course
                    self.load_languages()
                except pymysql.MySQLError as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении: {e}")
                finally:
                    connection.close()


    def open_third_window(self):
        self.third_window = ThirdWindow()
        # Подключаем сигнал к обоим методам обновления
        self.third_window.course_added.connect(self.update_after_course_change)
        self.third_window.show()

    def update_after_course_change(self):
        """Обновляет и таблицу курсов, и список языков"""
        self.load_courses_from_db()
        self.load_languages()

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
        apply_styles(self)

        self.setWindowTitle('Авторизация')
        self.setFixedSize(533, 400)

        # Создание основного layout
        layout = QVBoxLayout()
        layout.setSpacing(10)  # Добавляем отступы между элементами

        # Создаем контейнер для центрирования содержимого
        center_container = QVBoxLayout()
        center_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Группа для логина
        login_group = QVBoxLayout()
        self.login_label = QLabel('Логин')
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.login_input = QLineEdit()
        self.login_input.setFixedWidth(400)
        login_group.addWidget(self.login_label)
        login_group.addWidget(self.login_input)

        # Группа для пароля
        password_group = QVBoxLayout()
        self.password_label = QLabel('Пароль')
        self.password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(400)
        password_group.addWidget(self.password_label)
        password_group.addWidget(self.password_input)

        # Кнопка входа
        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setFixedWidth(400)

        # Добавляем группы в центральный контейнер
        center_container.addLayout(login_group)
        center_container.addLayout(password_group)
        center_container.addWidget(self.login_button)

        # Добавляем центральный контейнер в основной layout
        layout.addStretch()
        layout.addLayout(center_container)
        layout.addStretch()

        self.setLayout(layout)
        self.center()

    # Остальные методы остаются без изменений
    def center(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def handle_login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM authorization WHERE Name_Admin=%s AND Password_Admin=%s"
                    cursor.execute(sql, (login, password))
                    result = cursor.fetchone()

                    if result:
                        self.second_window = SecondWindow()
                        self.second_window.show()
                        self.close()
                    else:
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