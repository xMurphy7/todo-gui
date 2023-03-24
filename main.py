import datetime
import sys

from PySide6 import QtCore, QtWidgets, QtGui


class App(QtWidgets.QMainWindow):
    tasks = []
    checkboxes = []

    def __init__(self):
        super().__init__()

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
            task_id = len(self.tasks)
            self.tasks.append(task_text)

            self.task_tab.insertRow(task_id)
            self.checkbox = QtWidgets.QTableWidgetItem()
            self.checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)
            self.checkboxes.append(self.checkbox)
            desc = QtWidgets.QTableWidgetItem(task_text)
            desc.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            time_val = QtWidgets.QTableWidgetItem(str(time_created))
            time_val.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            self.task_tab.setItem(task_id, 0, self.checkbox)  # Column 1 - Checkbox
            self.task_tab.setItem(task_id, 1, desc)  # Column 2 - Task description
            # Column 3 - Task comments
            self.task_tab.setItem(task_id, 3, time_val)  # Column 4 - Start date
            # Column 5 - End date

            self.main_widget.update()

    @QtCore.Slot()
    def remove_task(self):
        if self.tasks:
            for i, val in enumerate(self.checkboxes):
                if val.checkState() == QtCore.Qt.CheckState.Checked:
                    self.checkboxes.pop(i)
                    self.tasks.pop(i)
                    self.task_tab.removeRow(i)
            self.main_widget.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = App()
    widget.show()
    sys.exit(app.exec())
