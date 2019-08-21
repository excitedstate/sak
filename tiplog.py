from PyQt5.QtWidgets import QLabel,QDialog
from PyQt5.QtGui import QFont, QIcon,QKeyEvent
from PyQt5.QtCore import Qt

class TipDialog(QDialog):
    def __init__(self, title, text, array: list):
        super().__init__()
        self.label = QLabel(self)
        self.title = title
        self.text = text
        self.array = array
        self.setup()

    def setup(self):
        self.setWindowIcon(QIcon(r"./src/app.png"))
        self.setWindowTitle(self.title)
        self.label.setFont(QFont("", 20))
        self.label.setText(self.text)
        self.setGeometry(self.array[0], self.array[1], self.array[2], self.array[3])

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Escape:
            self.close()