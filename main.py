import datetime
import os.path
import sys
import csv
from PySide6 import QtCore, QtWidgets, QtGui


class App(QtWidgets.QMainWindow):
    checkboxes = []
    FILENAME = 'tasks_db.csv'

    def __init__(self):
        super().__init__()

        # Make sure that the csv file exists.
        if not os.path.exists(self.FILENAME):
            open(self.FILENAME, 'x').close()

        self.setWindowTitle('To-do')
        self.setFixedSize(800, 500)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.add_menu()
        self.add_entry()
        self.add_todo_list()
        self.add_remove()

        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.read_db()

    def read_db(self):
        """Read tasks from csv file and create the file if it doesn't exist."""
        with open(self.FILENAME, 'r', newline='') as csvfile:
            tasks_reader = csv.reader(csvfile)
            for task_id, row in enumerate(tasks_reader):
                self.task_tab.insertRow(task_id)
                checkbox = QtWidgets.QTableWidgetItem()
                checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                checkbox.setCheckState(QtCore.Qt.Unchecked)
                self.checkboxes.append(checkbox)
                desc = QtWidgets.QTableWidgetItem(row[0])
                desc.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                time_val = QtWidgets.QTableWidgetItem(str(row[2]))
                time_val.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                self.task_tab.setItem(task_id, 0, checkbox)  # Column 1 - Checkbox
                self.task_tab.setItem(task_id, 1, desc)  # Column 2 - Task description
                # Column 3 - Task comments
                self.task_tab.setItem(task_id, 3, time_val)  # Column 4 - Start date
                # Column 5 - End date
                self.main_widget.update()

    def add_menu(self):
        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction('&Info')
        help_menu.addAction('&Credits')

    def add_entry(self):
        entry_layout = QtWidgets.QHBoxLayout()
        self.entry = QtWidgets.QLineEdit()
        self.entry.returnPressed.connect(self.add_task)
        add_btn = QtWidgets.QPushButton('Add')
        add_btn.clicked.connect(self.add_task)
        entry_layout.addWidget(self.entry)
        entry_layout.addWidget(add_btn)

        self.main_layout.addLayout(entry_layout)

    def add_remove(self):
        remove_layout = QtWidgets.QHBoxLayout()
        remove_btn = QtWidgets.QPushButton('Remove')
        remove_btn.clicked.connect(self.remove_task)
        remove_layout.addWidget(remove_btn)

        self.main_layout.addLayout(remove_layout)

    def add_todo_list(self):
        list_box = QtWidgets.QGroupBox('To-do')
        list_layout = QtWidgets.QHBoxLayout()

        self.task_tab = QtWidgets.QTableWidget(0, 5)
        self.task_tab.setHorizontalHeaderLabels(['Done', 'Task', 'Comments', 'Start date', 'End date'])
        h_header = self.task_tab.horizontalHeader()
        h_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        h_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        h_header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.task_tab.verticalHeader().hide()
        list_layout.addWidget(self.task_tab)
        list_box.setLayout(list_layout)

        self.main_layout.addWidget(list_box)

    @QtCore.Slot()
    def add_task(self):
        task_text = self.entry.text().strip()
        self.entry.clear()
        if task_text:
            time_created = datetime.datetime.now().strftime('%d/%m/%y')
            task_id = len(self.checkboxes)

            # Add task to csv file
            with open(self.FILENAME, 'a', newline='') as csvfile:
                tasks_writer = csv.DictWriter(csvfile, fieldnames=['Task', 'Comments', 'Start date', 'End date'])
                tasks_writer.writerow({'Task': task_text, 'Start date': time_created})

            self.task_tab.insertRow(task_id)
            checkbox = QtWidgets.QTableWidgetItem()
            checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            checkbox.setCheckState(QtCore.Qt.Unchecked)
            self.checkboxes.append(checkbox)
            desc = QtWidgets.QTableWidgetItem(task_text)
            desc.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            time_val = QtWidgets.QTableWidgetItem(str(time_created))
            time_val.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            self.task_tab.setItem(task_id, 0, checkbox)  # Column 1 - Checkbox
            self.task_tab.setItem(task_id, 1, desc)  # Column 2 - Task description
            # Column 3 - Task comments
            self.task_tab.setItem(task_id, 3, time_val)  # Column 4 - Start date
            # Column 5 - End date

            self.main_widget.update()

    @QtCore.Slot()
    def remove_task(self):
        if self.checkboxes:
            for i, val in reversed(list(enumerate(self.checkboxes))):
                if val.checkState() == QtCore.Qt.CheckState.Checked:
                    with open(self.FILENAME, 'r', newline='') as csvfile:
                        rows = [row for row in csv.reader(csvfile)]

                    rows.pop(i)
                    with open(self.FILENAME, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(rows)
                    self.checkboxes.pop(i)
                    self.task_tab.removeRow(i)
            self.main_widget.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = App()
    widget.show()
    sys.exit(app.exec())
