from  PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

