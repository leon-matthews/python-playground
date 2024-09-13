"""

Installation:

    $ pip install pyside6
    $ sudo apt install libxcb-cursor0

See:
    https://doc.qt.io/qtforpython-6/tutorials/index.html
"""
import sys
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QPushButton


@Slot()
def say_hello():
    print("Thanks!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    button = QPushButton("Push Me")
    button.clicked.connect(say_hello)
    button.show()

    sys.exit(app.exec())
