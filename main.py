import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QListWidget, QShortcut, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QPalette, QKeySequence

class ListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-do List")
        self.setGeometry(100, 400, 400, 400)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 128, 40))  # Background
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # White text
        self.setPalette(palette)

        self.label = QLabel("What tasks need finishing?")
        self.entry = QLineEdit()
        self.entry = QLineEdit()
        self.entry.returnPressed.connect(self.save_list)  # Connect Enter key press to save_list function

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_list)  # Connect the button to the save_list function
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.delete_selected_item)

        # Create a vertical layout to hold the components
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.save_button)
        layout.addWidget(self.list_widget)

        # Style the buttons
        button_style = "QPushButton { background-color: #007ACC; color: white; border: none; padding: 5px; }"
        self.save_button.setStyleSheet(button_style)

        # Style the list widget
        list_style = "QListWidget { background-color: #282828; color: white; border: none; }"
        list_item_style = "QListWidget::item:selected { background-color: #007ACC; color: white; }"
        self.list_widget.setStyleSheet(list_style + list_item_style)

        # Create the central widget and set the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        shortcut.activated.connect(self.close)

        instruction_label = QLabel("Instructions:\n- Enter your tasks and click 'Save' or hit 'Enter' to add them to the list.\n- Click on a task to delete it from the list.\n- Close the app and come back anytime to see your tasks.")
        instruction_label.setStyleSheet("color: white;")

        # Add the instructions label to the layout
        layout.addWidget(instruction_label)

        self.list_items_saved = []
        self.load_list()

    def save_list(self):
        list_items = self.entry.text().split("\n")

        try:
            with open("list.json", "w") as f:
                json.dump(list_items, f)
        except Exception as e:
            print(e)

        self.list_items_saved.extend(list_items)
        self.update_list_widget()

    def load_list(self):
        try:
            with open("list.json", "r") as f:
                self.list_items_saved = json.load(f)
        except FileNotFoundError:
            self.list_items_saved = []

        self.update_list_widget()

    def update_list_widget(self):
        self.list_widget.clear()
        self.list_widget.addItems(self.list_items_saved)

        with open("list.json", "w") as f:
            json.dump(self.list_items_saved, f)

    def delete_selected_item(self, item):
        removed_item = self.list_items_saved.pop(self.list_widget.row(item))
        self.update_list_widget()
        print(f"Deleted: {removed_item}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    list_app = ListApp()
    list_app.show()
    sys.exit(app.exec_())