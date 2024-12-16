from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, 
    QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, 
    QHeaderView, QMessageBox, QInputDialog, QDialog, QFormLayout, QLineEdit, 
    QAbstractItemView, QLabel, QDateEdit, QTimeEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
import sys
import pg8000
import os

import pg8000


class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить сотрудника")
        self.layout = QFormLayout(self)

        self.surname_edit = QLineEdit(self)
        self.name_edit = QLineEdit(self)
        self.otchestvo_edit = QLineEdit(self)
        self.resident_edit = QComboBox(self)
        self.resident_edit.addItems(["Да", "Нет"])
        self.distant_work_format_edit = QComboBox(self)
        self.distant_work_format_edit.addItems(["Да", "Нет"])
        self.add_button = QPushButton("Добавить", self)

        self.layout.addRow("Фамилия", self.surname_edit)
        self.layout.addRow("Имя", self.name_edit)
        self.layout.addRow("Отчество", self.otchestvo_edit)
        self.layout.addRow("Резидент", self.resident_edit)
        self.layout.addRow("Удалённый формат работы", self.distant_work_format_edit)
        self.layout.addRow(self.add_button)

        self.add_button.clicked.connect(self.accept)

    def get_values(self):
        return self.surname_edit.text(), self.name_edit.text(), self.otchestvo_edit.text(), self.resident_edit.currentText() == "Да", self.distant_work_format_edit.currentText() == "Да"



class EditEmployeeDialog(QDialog):
    def __init__(self, employee, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать сотрудника")
        self.layout = QFormLayout(self)

        self.surname_edit = QLineEdit(self)
        self.surname_edit.setText(employee[0])
        self.name_edit = QLineEdit(self)
        self.name_edit.setText(employee[1])
        self.otchestvo_edit = QLineEdit(self)
        self.otchestvo_edit.setText(employee[2])
        self.resident_edit = QComboBox(self)
        self.resident_edit.addItems(["Да", "Нет"])
        self.resident_edit.setCurrentText("Да" if employee[3] else "Нет")
        self.distant_work_format_edit = QComboBox(self)
        self.distant_work_format_edit.addItems(["Да", "Нет"])
        self.distant_work_format_edit.setCurrentText("Да" if employee[4] else "Нет")
        self.edit_button = QPushButton("Изменить", self)
        self.remove_button = QPushButton("Удалить", self)

        self.layout.addRow("Фамилия", self.surname_edit)
        self.layout.addRow("Имя", self.name_edit)
        self.layout.addRow("Отчество", self.otchestvo_edit)
        self.layout.addRow("Резидент", self.resident_edit)
        self.layout.addRow("Удалённый формат работы", self.distant_work_format_edit)
        self.layout.addRow(self.edit_button)
        self.layout.addRow(self.remove_button)

        self.edit_button.clicked.connect(self.edit)
        self.remove_button.clicked.connect(self.remove)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def edit(self):
        self.button_clicked = "Изменить"
        self.accept()

    def remove(self):
        self.button_clicked = "Удалить"
        self.done(QDialog.Rejected)

    def buttonClicked(self):
        return self.button_clicked

    def get_values(self):
        return self.surname_edit.text(), self.name_edit.text(), self.otchestvo_edit.text(), self.resident_edit.currentText() == "Да", self.distant_work_format_edit.currentText() == "Да"



# диалоговые окна вкладки ТИМЛИДЫ
class AddTeamLeadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить тимлида")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.surname_edit = QLineEdit(self)
        self.otchestvo_edit = QLineEdit(self)
        self.max_hours_edit = QLineEdit(self)
        self.add_button = QPushButton("Добавить", self)

        self.layout.addRow("Имя", self.name_edit)
        self.layout.addRow("Фамилия", self.surname_edit)
        self.layout.addRow("Отчество", self.otchestvo_edit)
        self.layout.addRow("Максимальное количество часов", self.max_hours_edit)
        self.layout.addRow(self.add_button)

        self.add_button.clicked.connect(self.accept)

    def get_values(self):
        if not (str.isnumeric(self.max_hours_edit.text())):
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверный формат ввода часов!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return []

        return self.name_edit.text(), self.surname_edit.text(), self.otchestvo_edit.text(), int(self.max_hours_edit.text())



class EditTeamLeadDialog(QDialog):
    def __init__(self, team_lead, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать тимлида")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(team_lead[1])
        self.surname_edit = QLineEdit(self)
        self.surname_edit.setText(team_lead[2])
        self.otchestvo_edit = QLineEdit(self)
        self.otchestvo_edit.setText(team_lead[3])
        self.max_hours_edit = QLineEdit(self)
        self.max_hours_edit.setText(str(team_lead[4]))
        self.edit_button = QPushButton("Изменить", self)
        self.remove_button = QPushButton("Удалить", self)

        self.layout.addRow("Имя", self.name_edit)
        self.layout.addRow("Фамилия", self.surname_edit)
        self.layout.addRow("Отчество", self.otchestvo_edit)
        self.layout.addRow("Максимальное количество часов", self.max_hours_edit)
        self.layout.addRow(self.edit_button)
        self.layout.addRow(self.remove_button)

        self.edit_button.clicked.connect(self.edit)
        self.remove_button.clicked.connect(self.remove)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def edit(self):
        self.button_clicked = "Изменить"
        self.accept()

    def remove(self):
        self.button_clicked = "Удалить"
        self.done(QDialog.Rejected)

    def buttonClicked(self):
        return self.button_clicked

    def get_values(self):
        if not(str.isnumeric(self.max_hours_edit.text())):
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверный формат ввода часов!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return []

        return self.name_edit.text(), self.surname_edit.text(), self.otchestvo_edit.text(), int(self.max_hours_edit.text())




# диалоговые окна вкладки АУДИТОРИИ
class AddRoomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить комнату")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)

        self.type_edit = QComboBox(self)
        self.type_edit.addItems(["lecture hall", "meeting room", "gym", "recreation room"])
        self.capacity_edit = QLineEdit(self)
        self.add_button = QPushButton("Добавить", self)

        self.layout.addRow("Название комнаты", self.name_edit)
        self.layout.addRow("Тип", self.type_edit)
        self.layout.addRow("Вместимость", self.capacity_edit)
        self.layout.addRow(self.add_button)

        self.add_button.clicked.connect(self.accept)

    def get_values(self):
        capacity = self.capacity_edit.text()
        if not(str.isnumeric(capacity)) or int(capacity) <= 0:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверный формат ввода вместимости комнаты!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return []

        return self.name_edit.text(), self.type_edit.currentText(), int(capacity)


class EditRoomDialog(QDialog):
    def __init__(self, room, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать комнату")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(room[1])
        self.type_edit = QComboBox(self)
        self.type_edit.addItems(["lecture hall", "meeting room", "gym", "recreation room"])
        self.type_edit.setCurrentText(room[2])  
        self.capacity_edit = QLineEdit(self)
        self.capacity_edit.setText(str(room[3]))  
        self.edit_button = QPushButton("Изменить", self)
        self.remove_button = QPushButton("Удалить", self)

        self.layout.addRow("Название комнаты", self.name_edit)
        self.layout.addRow("Тип", self.type_edit)
        self.layout.addRow("Вместимость", self.capacity_edit)
        self.layout.addRow(self.edit_button)
        self.layout.addRow(self.remove_button)

        self.edit_button.clicked.connect(self.edit)
        self.remove_button.clicked.connect(self.remove)

    def edit(self):
        self.button_clicked = "Изменить"
        self.accept()

    def remove(self):
        self.button_clicked = "Удалить"
        self.done(QDialog.Rejected)

    def buttonClicked(self):
        return self.button_clicked

    def get_values(self):
        capacity = self.capacity_edit.text()
        if not (str.isnumeric(capacity)) or int(capacity) <= 0:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверный формат ввода вместимости комнаты!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return []

        return self.name_edit.text(), self.type_edit.currentText(), int(capacity)

# диалоговые окна вкладки РАСПИСАНИЕ
class AddMeetingDialog(QDialog):  # Заменено на AddMeetingDialog
    def __init__(self, connection, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить встречу")
        self.layout = QFormLayout(self)

        self.date_edit = QDateEdit(self)
        self.time_edit = QTimeEdit(self)
        self.room_edit = QComboBox(self)
        self.team_edit = QComboBox(self)

        self.type_edit = QComboBox(self)
        self.team_lead_edit = QComboBox(self)
        self.type_edit.addItems(["small talk", "daily meeting", "conference"])
        self.add_button = QPushButton("Добавить", self)

        self.layout.addRow("Дата", self.date_edit)
        self.layout.addRow("Время", self.time_edit)
        self.layout.addRow("Комната", self.room_edit)
        self.layout.addRow("Команда", self.team_edit)

        self.layout.addRow("Тип", self.type_edit)
        self.layout.addRow("Организатор", self.team_lead_edit)
        self.layout.addRow(self.add_button)

        self.connection = connection
        self.cursor = self.connection.cursor()

        self.load_rooms()
        self.load_teams()
        self.load_team_leads()

        self.add_button.clicked.connect(self.accept)

    def load_rooms(self):
        self.cursor.execute("SELECT room_name, room_id FROM rooms")  
        rooms = self.cursor.fetchall()
        for room in rooms:
            self.room_edit.addItem(f"{room[0]} ({room[1]})")

    def load_teams(self):
        self.cursor.execute("SELECT team_name FROM teams")  
        teams = self.cursor.fetchall()
        for team in teams:
            self.team_edit.addItem(team[0])

    def load_team_leads(self):
        self.cursor.execute(
            "SELECT team_lead_surname, team_lead_name, team_lead_otchestvo, team_lead_id FROM team_leads ORDER BY team_lead_id")  
        team_leads = self.cursor.fetchall()
        for team_lead in team_leads:
            team_lead_info = f"{team_lead[0]} {team_lead[1][0]}. {team_lead[2][0]}. ({team_lead[3]})"
            self.team_lead_edit.addItem(team_lead_info)

    def get_values(self):
        return (
            self.date_edit.date(),
            self.time_edit.time(),
            self.room_edit.currentText(),
            self.team_edit.currentText(),
            self.type_edit.currentText(),
            self.team_lead_edit.currentText()
        )

# главное окно
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Schedule")
        self.setGeometry(0, 0, 300, 200)
        self.setMinimumSize(900, 700)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.tabs = ["Команды", "Тимлиды", "Аудитории", "Расписание"]
        for tab_name in self.tabs:
            tab = QWidget()
            if tab_name == "Команды":
                self.teams_tab = tab
            elif tab_name == "Тимлиды":
                self.team_leads_tab = tab
            elif tab_name == "Аудитории":
                self.rooms_tab = tab
            elif tab_name == "Расписание":
                self.schedule_tab = tab
            self.tab_widget.addTab(tab, tab_name)

        self.connect_to_database()

        self.teams_layout = QVBoxLayout(self.teams_tab)
        self.combo_layout = QHBoxLayout()
        self.teams_combo = QComboBox()
        self.teams_combo.setStyleSheet("font-size: 14px; color: blue")
        self.add_team_button = QPushButton("Добавить команду")
        self.add_team_button.setStyleSheet("font-size: 14px")
        self.combo_layout.addWidget(self.teams_combo)
        self.combo_layout.addWidget(self.add_team_button)
        self.teams_layout.addLayout(self.combo_layout)

        self.add_employee_button = QPushButton("Добавить сотрудника")
        self.remove_team_button = QPushButton("Удалить команду")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.add_employee_button)
        self.buttons_layout.addWidget(self.remove_team_button)
        self.teams_layout.addLayout(self.buttons_layout)

        self.add_employee_button.setStyleSheet("font-size: 14px")
        self.remove_team_button.setStyleSheet("font-size: 14px")

        self.teams_table = QTableWidget()
        self.teams_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.teams_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.teams_layout.addWidget(self.teams_table)

        self.teams_combo.currentIndexChanged.connect(self.update_table)
        self.add_team_button.clicked.connect(self.add_team)
        self.remove_team_button.clicked.connect(self.remove_team)
        self.add_employee_button.clicked.connect(self.add_employee)
        self.teams_table.itemDoubleClicked.connect(self.edit_or_remove_employee)

        self.load_teams()

        self.team_leads_layout = QVBoxLayout(self.team_leads_tab)
        self.team_leads_table = QTableWidget()
        self.team_leads_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.team_leads_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.team_leads_layout.addWidget(self.team_leads_table)
        self.add_team_lead_button = QPushButton("Добавить тимлида")
        self.add_team_lead_button.setStyleSheet("font-size: 14px")
        self.team_leads_layout.addWidget(self.add_team_lead_button)

        self.add_team_lead_button.clicked.connect(self.add_team_lead)
        self.team_leads_table.itemDoubleClicked.connect(self.edit_or_remove_team_lead)

        self.load_team_leads()

        self.rooms_layout = QVBoxLayout(self.rooms_tab)
        self.rooms_table = QTableWidget()
        self.rooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rooms_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.rooms_layout.addWidget(self.rooms_table)
        self.add_room_button = QPushButton("Добавить аудиторию")
        self.add_room_button.setStyleSheet("font-size: 14px")
        self.rooms_layout.addWidget(self.add_room_button)

        self.add_room_button.clicked.connect(self.add_room)
        self.rooms_table.itemDoubleClicked.connect(self.edit_or_remove_room)

        self.load_rooms()

        # вкладка РАСПИСАНИЕ
        self.schedule_layout = QVBoxLayout(self.schedule_tab)

        self.team_layout = QVBoxLayout()
        self.team_label = QLabel("Команда:")
        self.team_label.setStyleSheet("font-size: 14px;")
        self.teams_combo_schedule = QComboBox()
        self.teams_combo_schedule.setStyleSheet("font-size: 14px; color: blue")
        self.team_layout.addWidget(self.team_label)
        self.team_layout.addWidget(self.teams_combo_schedule)

        self.team_lead_layout = QVBoxLayout()
        self.team_lead_label = QLabel("Организатор:")
        self.team_lead_label.setStyleSheet("font-size: 14px;")
        self.team_leads_combo_schedule = QComboBox()
        self.team_leads_combo_schedule.setStyleSheet("font-size: 14px; color: blue")
        self.team_lead_layout.addWidget(self.team_lead_label)
        self.team_lead_layout.addWidget(self.team_leads_combo_schedule)

        self.combo_layout_schedule = QHBoxLayout()
        self.combo_layout_schedule.addLayout(self.team_layout)
        self.combo_layout_schedule.addLayout(self.team_lead_layout)
        self.schedule_layout.addLayout(self.combo_layout_schedule)

        self.schedule_table = QTableWidget()
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.schedule_layout.addWidget(self.schedule_table)

        self.add_meeting_button = QPushButton("Добавить встречу")
        self.add_meeting_button.setStyleSheet("font-size: 14px")
        self.schedule_layout.addWidget(self.add_meeting_button)

        self.teams_combo_schedule.currentIndexChanged.connect(self.update_schedule)
        self.team_leads_combo_schedule.currentIndexChanged.connect(self.update_schedule)
        self.add_meeting_button.clicked.connect(self.add_meeting)

        self.schedule_table.itemDoubleClicked.connect(self.delete_meeting)

        self.load_teams_schedule()
        self.load_team_leads_schedule()
        self.update_schedule()


    # Подключение к БД
    def connect_to_database(self):
        connection_params = {
            "host": "localhost",
            "port": 5433,
            "database": "postgres",
            "user": "postgres",
            "password": "2919",
        }
        try:
            self.connection = pg8000.connect(**connection_params)
            print("Успешное подключение к базе данных")
        except Exception as e:
            print(f"Произошла ошибка при подключении к базе данных: {e}")


    # Функции вкладки КОМАНДЫ
    def load_teams(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT team_name FROM teams")
        teams = cursor.fetchall()
        for team in teams:
            self.teams_combo.addItem(team[0])

    def add_team(self):
        team_name, ok = QInputDialog.getText(self, 'Добавить команду', 'Введите имя команды:')
        if ok:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(team_id) FROM teams")
            max_team_id = cursor.fetchone()[0]
            new_team_id = max_team_id + 1 if max_team_id is not None else 1
            cursor.execute(f"INSERT INTO teams (team_id, team_name) VALUES ({new_team_id}, '{team_name}')")
            self.connection.commit()
            self.teams_combo.addItem(team_name)

    def update_table(self):
        team_name = self.teams_combo.currentText()
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT employee_id, employee_surname, employee_name, employee_otchestvo FROM employees WHERE team_id = (SELECT team_id FROM teams WHERE team_name = '{team_name}') ORDER BY employee_id")
        employees = cursor.fetchall()

        self.teams_table.setRowCount(len(employees))
        self.teams_table.setColumnCount(4)
        self.teams_table.setHorizontalHeaderLabels(["Id", "Фамилия", "Имя", "Отчество"])

        for i, employee in enumerate(employees):
            for j in range(4):
                self.teams_table.setItem(i, j, QTableWidgetItem(str(employee[j])))

    def remove_team(self):
        team_name = self.teams_combo.currentText()

        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Question)
        confirm_box.setWindowTitle("Подтверждение удаления")
        confirm_box.setText(f"Вы уверены, что хотите удалить команду '{team_name}' и всех ее сотрудников?")
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.No)

        if confirm_box.exec_() == QMessageBox.Yes:
            cursor = self.connection.cursor()
            cursor.execute(
                f"DELETE FROM employees WHERE team_id = (SELECT team_id FROM teams WHERE team_name = '{team_name}')")
            cursor.execute(f"DELETE FROM teams WHERE team_name = '{team_name}'")
            self.connection.commit()
            self.teams_combo.removeItem(self.teams_combo.currentIndex())

    def add_employee(self):
        dialog = AddEmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            surname, name, otchestvo, resident, distant_work_format = dialog.get_values()
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(employee_id) FROM employees")
            max_employee_id = cursor.fetchone()[0]
            new_employee_id = max_employee_id + 1 if max_employee_id is not None else 1
            team_name = self.teams_combo.currentText()
            cursor.execute(f"SELECT team_id FROM teams WHERE team_name = '{team_name}'")
            team_id = cursor.fetchone()[0]
            cursor.execute(
                f"INSERT INTO employees (employee_id, employee_name, employee_surname, employee_otchestvo, distant_work_format, resident, team_id) VALUES ({new_employee_id}, '{name}', '{surname}', '{otchestvo}', {distant_work_format}, {resident}, {team_id})")
            self.connection.commit()
            self.update_table()

    def edit_or_remove_employee(self):
        current_row = self.teams_table.currentRow()
        employee_id = self.teams_table.item(current_row, 0).text()
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT employee_surname, employee_name, employee_otchestvo, resident, distant_work_format FROM employees WHERE employee_id = {employee_id}")
        employee = cursor.fetchone()
        dialog = EditEmployeeDialog(employee, self)
        result = dialog.exec_()
        if dialog.buttonClicked() == "Изменить" and result == QDialog.Accepted:
            surname, name, otchestvo, resident, distant_work_format = dialog.get_values()
            cursor.execute(
                f"UPDATE employees SET employee_surname = '{surname}', employee_name = '{name}', employee_otchestvo = '{otchestvo}', resident = {resident}, distant_work_format = {distant_work_format} WHERE employee_id = {employee_id}")
        elif dialog.buttonClicked() == "Удалить":
            cursor.execute(f"DELETE FROM employees WHERE employee_id = {employee_id}")
        self.connection.commit()
        self.update_table()

    def load_team_leads(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT team_lead_id, team_lead_surname, team_lead_name, team_lead_otchestvo, max_hours FROM team_leads ORDER BY team_lead_id")
        team_leads = cursor.fetchall()

        self.team_leads_table.setRowCount(len(team_leads))
        self.team_leads_table.setColumnCount(5)
        self.team_leads_table.setHorizontalHeaderLabels(["Id", "Фамилия", "Имя", "Отчество", "Занятость"])

        for i, team_lead in enumerate(team_leads):
            team_lead = list(team_lead)
            cursor.execute(f"SELECT public.get_team_lead_hours({team_lead[0]})")
            team_lead_busy_hours = cursor.fetchone()[0]
            team_lead[-1] = f"{team_lead_busy_hours}/{team_lead[-1]}"
            for j in range(5):
                self.team_leads_table.setItem(i, j, QTableWidgetItem(str(team_lead[j])))

    def add_team_lead(self):
        dialog = AddTeamLeadDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            values = dialog.get_values()
            if not values:
                return
            name, surname, otchestvo, max_hours = values
            cursor = self.connection.cursor()

            cursor.execute("SELECT MAX(team_lead_id) FROM team_leads")
            last_team_lead_id = cursor.fetchone()[0]

            if last_team_lead_id is None:
                last_team_lead_id = 0
            new_team_lead_id = last_team_lead_id + 1

            try:
                cursor.execute(
                    f"INSERT INTO team_leads (team_lead_id, team_lead_name, team_lead_surname, team_lead_otchestvo, max_hours) VALUES ({new_team_lead_id}, '{name}', '{surname}', '{otchestvo}', {max_hours})")
                self.connection.commit()
            except pg8000.DatabaseError as e:
                error_message = e.args[0].get('M')
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText(error_message)
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.connection.rollback()

            self.load_team_leads()

    def edit_or_remove_team_lead(self):
        current_row = self.team_leads_table.currentRow()
        team_lead_id = self.team_leads_table.item(current_row, 0).text()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM team_leads WHERE team_lead_id = {team_lead_id}")
        team_lead = cursor.fetchone()
        dialog = EditTeamLeadDialog(team_lead, self)
        result = dialog.exec_()
        if dialog.buttonClicked() == "Изменить" and result == QDialog.Accepted:
            values = dialog.get_values()
            if not values:
                return
            name, surname, otchestvo, max_hours = values
            try:
                cursor.execute(
                    f"UPDATE team_leads SET team_lead_name = '{name}', team_lead_surname = '{surname}', team_lead_otchestvo = '{otchestvo}', max_hours = {max_hours} WHERE team_lead_id = {team_lead_id}")
            except pg8000.DatabaseError as e:
                error_message = e.args[0].get('M')
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText(error_message)
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.connection.rollback()

        elif dialog.buttonClicked() == "Удалить":
            cursor.execute(f"DELETE FROM team_leads WHERE team_lead_id = {team_lead_id}")

        self.connection.commit()
        self.load_team_leads()

    def load_rooms(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rooms ORDER BY room_id")
        rooms = cursor.fetchall()

        self.rooms_table.setRowCount(len(rooms))
        self.rooms_table.setColumnCount(4)
        self.rooms_table.setHorizontalHeaderLabels(["Id", "Название комнаты", "Тип", "Вместимость"])

        for i, room in enumerate(rooms):
            for j in range(4):
                self.rooms_table.setItem(i, j, QTableWidgetItem(str(room[j])))

    def add_room(self):
        dialog = AddRoomDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            values = dialog.get_values()
            if not values:
                return
            name, room_type, capacity = values

            cursor = self.connection.cursor()

            cursor.execute("SELECT MAX(room_id) FROM rooms")
            last_room_id = cursor.fetchone()[0]

            if last_room_id is None:
                last_room_id = 0
            new_room_id = last_room_id + 1

            cursor.execute(
                f"INSERT INTO rooms (room_id, room_name, room_type, room_capacity) VALUES ({new_room_id}, '{name}', '{room_type}', {capacity})")
            self.connection.commit()
            self.load_rooms()

    def edit_or_remove_room(self):
        current_row = self.rooms_table.currentRow()
        room_id = self.rooms_table.item(current_row, 0).text()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM rooms WHERE room_id = {room_id}")
        room = cursor.fetchone()
        dialog = EditRoomDialog(room, self)
        result = dialog.exec_()
        if dialog.buttonClicked() == "Изменить" and result == QDialog.Accepted:
            values = dialog.get_values()
            if not values:
                return
            name, room_type, capacity = values
            cursor.execute(
                f"UPDATE rooms SET room_name = '{name}', room_type = '{room_type}', room_capacity = {capacity} WHERE room_id = {room_id}")
        elif dialog.buttonClicked() == "Удалить":
            cursor.execute(f"DELETE FROM rooms WHERE room_id = {room_id}")
        self.connection.commit()
        self.load_rooms()

    # Функции вкладки Расписание
    def load_teams_schedule(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT team_name FROM teams")
        teams = cursor.fetchall()
        self.teams_combo_schedule.addItem("all")
        for team in teams:
            self.teams_combo_schedule.addItem(team[0])

    def load_team_leads_schedule(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT team_lead_surname, team_lead_name, team_lead_otchestvo, team_lead_id FROM team_leads ORDER BY team_lead_id")
        team_leads = cursor.fetchall()
        self.team_leads_combo_schedule.addItem("all")
        for team_lead in team_leads:
            team_lead_info = f"{team_lead[0]} {team_lead[1]} {team_lead[2]} ({team_lead[3]})"
            self.team_leads_combo_schedule.addItem(team_lead_info)

    def update_schedule(self):
        team_value = self.teams_combo_schedule.currentText()
        team_lead_id = self.team_leads_combo_schedule.currentText()

        if team_lead_id != "all":
            team_lead_id = team_lead_id.split('(')[-1].split(')')[0]

        cursor = self.connection.cursor()
        if team_value == "all" and (team_lead_id == "all" or team_lead_id == ""):
            cursor.execute("SELECT * FROM schedule ORDER BY date, time")
        elif team_value != "all" and (team_lead_id == "all" or team_lead_id == ""):
            cursor.execute(
                f"SELECT * FROM schedule WHERE team_id = (SELECT team_id FROM teams WHERE team_name = '{team_value}') ORDER BY date, time")
        elif team_value == "all" and team_lead_id != "all":
            cursor.execute(f"SELECT * FROM schedule WHERE team_lead_id = {team_lead_id} ORDER BY date, time")
        else:
            cursor.execute(
                f"SELECT * FROM schedule WHERE team_id = (SELECT team_id FROM teams WHERE team_name = '{team_value}') AND team_lead_id = {team_lead_id} ORDER BY date, time")

        rows = cursor.fetchall()

        self.schedule_table.setRowCount(0)

        self.schedule_table.setRowCount(len(rows))
        self.schedule_table.setColumnCount(8)
        self.schedule_table.setHorizontalHeaderLabels(
            ["Дата", "Время", "Комната", "Тимлид", "Команда", "Тип", "team_lead_id", "room_id"])

        # self.schedule_table.setColumnHidden(7, True)
        # self.schedule_table.setColumnHidden(8, True)
        self.schedule_table.setColumnHidden(6, True)
        self.schedule_table.setColumnHidden(7, True)

        if team_value == "all" and (team_lead_id == "all" or team_lead_id == ""):
            cursor.execute(f"""
                SELECT schedule.date, schedule.time, rooms.room_name,
                CONCAT(team_leads.team_lead_surname, ' ', SUBSTRING(team_leads.team_lead_name FROM 1 FOR 1), '. ', SUBSTRING(team_leads.team_lead_otchestvo FROM 1 FOR 1), '.'),
                teams.team_name, schedule.type, schedule.team_lead_id, schedule.room_id
                FROM schedule
                INNER JOIN rooms ON schedule.room_id = rooms.room_id
                INNER JOIN team_leads ON schedule.team_lead_id = team_leads.team_lead_id
                INNER JOIN teams ON schedule.team_id = teams.team_id
                ORDER BY schedule.date, schedule.time
            """)
        elif team_value != "all" and (team_lead_id == "all" or team_lead_id == ""):
            cursor.execute(f"""
                SELECT schedule.date, schedule.time, rooms.room_name,
                CONCAT(team_leads.team_lead_surname, ' ', SUBSTRING(team_leads.team_lead_name FROM 1 FOR 1), '. ', SUBSTRING(team_leads.team_lead_otchestvo FROM 1 FOR 1), '.'),
                teams.team_name, schedule.type, schedule.team_lead_id, schedule.room_id
                FROM schedule
                INNER JOIN rooms ON schedule.room_id = rooms.room_id
                INNER JOIN team_leads ON schedule.team_lead_id = team_leads.team_lead_id
                INNER JOIN teams ON schedule.team_id = teams.team_id
                WHERE teams.team_name = '{team_value}'
                ORDER BY schedule.date, schedule.time
            """)
        elif team_value == "all" and team_lead_id != "all":
            cursor.execute(f"""
                SELECT schedule.date, schedule.time, rooms.room_name,
                CONCAT(team_leads.team_lead_surname, ' ', SUBSTRING(team_leads.team_lead_name FROM 1 FOR 1), '. ', SUBSTRING(team_leads.team_lead_otchestvo FROM 1 FOR 1), '.'),
                teams.team_name, schedule.type, schedule.team_lead_id, schedule.room_id
                FROM schedule
                INNER JOIN rooms ON schedule.room_id = rooms.room_id
                INNER JOIN team_leads ON schedule.team_lead_id = team_leads.team_lead_id
                INNER JOIN teams ON schedule.team_id = teams.team_id
                WHERE team_leads.team_lead_id = {team_lead_id}
                ORDER BY schedule.date, schedule.time
            """)
        else:
            cursor.execute(f"""
                SELECT schedule.date, schedule.time, rooms.room_name,
                CONCAT(team_leads.team_lead_surname, ' ', SUBSTRING(team_leads.team_lead_name FROM 1 FOR 1), '. ', SUBSTRING(team_leads.team_lead_otchestvo FROM 1 FOR 1), '.'),
                teams.team_name, schedule.type, schedule.team_lead_id, schedule.room_id
                FROM schedule
                INNER JOIN rooms ON schedule.room_id = rooms.room_id
                INNER JOIN team_leads ON schedule.team_lead_id = team_leads.team_lead_id
                INNER JOIN teams ON schedule.team_id = teams.team_id
                WHERE teams.team_name = '{team_value}' AND team_leads.team_lead_id = {team_lead_id}
                ORDER BY schedule.date, schedule.time
            """)

        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            for j in range(8):
                self.schedule_table.setItem(i, j, QTableWidgetItem(str(row[j])))

        cursor.close()

    def add_meeting(self):
        self.add_meeting_dialog = AddMeetingDialog(self.connection, self)
        result = self.add_meeting_dialog.exec_()
        if result == QDialog.Accepted:
            date, time, room, team, meeting_type, team_lead = self.add_meeting_dialog.get_values()
            cursor = self.connection.cursor()

            cursor.execute(f"SELECT team_id FROM teams WHERE team_name = '{team}'")
            team_id = cursor.fetchone()[0]

            try:
                cursor.execute('CALL public.add_to_schedule(\'{}\', \'{}\', {}, {}, {}, \'{}\')'.format(
                date.toString("yyyy-MM-d"),
                    time.toString('HH:mm:ss'),
                    room.split('(')[-1].split(')')[0],
                    team_lead.split('(')[-1].split(')')[0],
                    team_id,
                    meeting_type,
                ))
                self.connection.commit()

            except pg8000.DatabaseError as e:
                error_message = e.args[0].get('M')
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText(error_message)
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.connection.rollback()


        self.update_schedule()
        self.load_team_leads()

    def delete_meeting(self):
        current_row = self.schedule_table.currentRow()
        team_lead_id = self.schedule_table.item(current_row, 6).text()
        room_id = self.schedule_table.item(current_row, 7).text()
        date = self.schedule_table.item(current_row, 0).text()
        time = self.schedule_table.item(current_row, 1).text()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Вы уверены, что хотите удалить это собрание?")
        msg.setWindowTitle("Подтверждение удаления")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            cursor = self.connection.cursor()
            cursor.execute(
                f"DELETE FROM schedule WHERE team_lead_id = {team_lead_id} AND room_id = {room_id} AND date = '{date}' AND time = '{time}'")
            self.connection.commit()

        self.update_schedule()
        self.load_team_leads()


if __name__ == "__main__":
    os.environ["QT_PLUGIN_PATH"] = r"C:\Users\Ксения\AppData\Local\Programs\Python\Python312\Lib\site-packages\PyQt5\Qt5\plugins"
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
