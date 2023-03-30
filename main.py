import webbrowser
from datetime import datetime
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
        self.setFixedSize(800, 515)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.create_menu()
        self.create_entry()
        self.create_todo_list()
        self.create_remove()

        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.read_db()

    def create_menu(self):
        """Create window's menu"""
        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu('&Help')
        info_action = help_menu.addAction('&Info')
        info_action.triggered.connect(self.menu_info)
        help_menu.addSeparator()
        credits_action = help_menu.addAction('Credits')
        credits_action.triggered.connect(self.menu_credits)

    @QtCore.Slot()
    def menu_info(self):
        """Action for 'Info' button that creates a message box with information about the program."""
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Info')
        msg.setText('''This is a simple program that lets you create a to-do list. You can add and remove them from \
the database.\nWhen adding a new task, you can specify it's description, additional comments and end date.''')
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.exec()

    @QtCore.Slot()
    def menu_credits(self):
        """Action for 'Credits' button that takes the user to developer's GitHub profile"""
        webbrowser.open('https://github.com/xMurphy7')

    def create_entry(self):
        """Create entry section which contains task description, comments, end date and button that calls add_task()."""
        entry_layout = QtWidgets.QHBoxLayout()

        info_box = QtWidgets.QGroupBox('Task info')
        info_box.setAlignment(4)
        info_layout = QtWidgets.QVBoxLayout()
        desc_label = QtWidgets.QLabel('Description')
        self.entry_desc = QtWidgets.QLineEdit()
        self.entry_desc.returnPressed.connect(self.add_task)
        comment_label = QtWidgets.QLabel('Comment')
        self.entry_comment = QtWidgets.QLineEdit()
        self.entry_comment.returnPressed.connect(self.add_task)
        add_btn = QtWidgets.QPushButton('Add')
        add_btn.clicked.connect(self.add_task)

        cal_layout = QtWidgets.QHBoxLayout()
        cal_box = QtWidgets.QGroupBox('End date')
        cal_box.setAlignment(4)
        self.entry_end = QtWidgets.QCalendarWidget()
        self.entry_end.setMinimumDate(self.entry_end.selectedDate())
        self.entry_end.setGridVisible(True)
        self.entry_end.setLocale(QtCore.QLocale.Language.English)

        info_layout.addWidget(desc_label)
        info_layout.addWidget(self.entry_desc)
        info_layout.addStretch()
        info_layout.addWidget(comment_label)
        info_layout.addWidget(self.entry_comment)
        info_layout.addStretch()
        info_layout.addWidget(add_btn)
        info_box.setLayout(info_layout)

        cal_layout.addWidget(self.entry_end)
        cal_box.setLayout(cal_layout)

        entry_layout.addWidget(info_box)
        entry_layout.addWidget(cal_box)

        self.main_layout.addLayout(entry_layout)

    def create_remove(self):
        """Create remove button, that calls remove_task() method."""
        remove_layout = QtWidgets.QHBoxLayout()
        remove_btn = QtWidgets.QPushButton('Remove')
        remove_btn.clicked.connect(self.remove_task)
        remove_layout.addWidget(remove_btn)

        self.main_layout.addLayout(remove_layout)

    def create_todo_list(self):
        """Create table widget."""
        list_box = QtWidgets.QGroupBox('To-do')
        list_layout = QtWidgets.QHBoxLayout()

        self.task_tab = QtWidgets.QTableWidget(0, 5)
        self.task_tab.setHorizontalHeaderLabels(['Done', 'Task', 'Comment', 'Start date', 'End date'])
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

    def insert_row(self, task_id, row):
        """Insert data as a row in table.
        :param task_id id number of the task
        :param row list which contains description, comment, start date and end date"""
        self.task_tab.insertRow(task_id)
        checkbox = QtWidgets.QTableWidgetItem()
        checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.checkboxes.append(checkbox)  # Append checkbox to the list, so you can check it's state while removing
        desc = QtWidgets.QTableWidgetItem(row[0])  # Task description
        comment = QtWidgets.QTableWidgetItem(row[1])  # Task comment
        start_date = QtWidgets.QTableWidgetItem(row[2])  # Start date
        end_date = QtWidgets.QTableWidgetItem(row[3])  # End date

        for cell in [desc, comment, start_date, end_date]:
            # Align text in cell to center
            cell.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            # Make the cell non-editable and non-selectable
            cell.setFlags(cell.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable & ~QtCore.Qt.ItemFlag.ItemIsSelectable)

        self.task_tab.setItem(task_id, 0, checkbox)  # Column 1 - Checkbox
        self.task_tab.setItem(task_id, 1, desc)  # Column 2 - Task description
        self.task_tab.setItem(task_id, 2, comment)  # Column 3 - Task comment
        self.task_tab.setItem(task_id, 3, start_date)  # Column 4 - Start date
        self.task_tab.setItem(task_id, 4, end_date)  # Column 5 - End date

        # Check if 'end date' has passed.
        if datetime.strptime(row[3], '%d/%m/%y').date() < datetime.now().date():
            for j in range(self.task_tab.columnCount()):
                self.task_tab.item(task_id, j).setBackground(QtGui.QColor('#F85656'))

        self.main_widget.update()

    def read_db(self):
        """Read tasks from csv file and create the file if it doesn't exist."""
        with open(self.FILENAME, 'r', newline='') as csvfile:
            tasks_reader = csv.reader(csvfile)
            for task_id, row in enumerate(tasks_reader):
                self.insert_row(task_id, row)

    @QtCore.Slot()
    def add_task(self):
        """Add the task with information written in entry boxes."""
        task_text = self.entry_desc.text().strip()  # Task's description
        self.entry_desc.clear()
        if task_text:
            task_id = len(self.checkboxes)  # Task's ID
            comment = self.entry_comment.text().strip()  # Task's comment
            self.entry_comment.clear()
            start_date = datetime.now().strftime('%d/%m/%y')  # Task's starting date
            end_date = self.entry_end.selectedDate().toString('dd/MM/yy')  # Task's end date
            row = [task_text, comment, start_date, end_date]  # List with task information

            self.insert_row(task_id, row)  # Insert row

            # Add task to csv file
            with open(self.FILENAME, 'a', newline='') as csvfile:
                tasks_writer = csv.writer(csvfile)
                tasks_writer.writerow([task_text, comment, start_date, end_date])

    @QtCore.Slot()
    def remove_task(self):
        """Remove tasks with checked checkboxes."""
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
