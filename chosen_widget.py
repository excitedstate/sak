from PyQt5.QtWidgets import  QListWidget
from PyQt5.QtGui import QFont, QIcon,QKeyEvent
from PyQt5.QtCore import Qt,pyqtSignal


class ChosenDialog(QListWidget):
    signal = pyqtSignal(str)
    def __init__(self, title, position,alternatives, parent=None):
        super().__init__(parent)
        self.title = title
        self.position = position
        self.alternatives = alternatives
        self.setup()

    def setup(self):
        self.setWindowIcon(QIcon(r"..\src\app.png"))
        self.setWindowTitle(self.title)
        self.setWindowOpacity(0.5)
        self.setFont(QFont('SimHei', 30))
        self.setStyleSheet("color:white")
        self.setStyleSheet("background:grey")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setGeometry(self.position[0], self.position[1], self.position[2], self.position[3]*len(self.alternatives))
        self.addItems(self.alternatives)
        self.itemClicked.connect(self.send_chosen_company)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Escape:
            self.close()

    def send_chosen_company(self):
        chosen_company = self.currentItem().text()
        self.signal.emit(chosen_company)
        self.close()
