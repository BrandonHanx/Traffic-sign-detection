from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from xmotor import gogo, stop, back, turn_left, turn_right


class RemoteController(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Remote Controller')
        self.setObjectName("MainWindow")
        self.setStyleSheet("#MainWindow{background-color:white}")
        self.setWindowIcon(QIcon("images/button/controller.jpg"))

        up = QIcon()
        up.addPixmap(QPixmap("images/button/up.png"), QIcon.Normal, QIcon.Off)

        down = QIcon()
        down.addPixmap(QPixmap("images/button/down.png"), QIcon.Normal, QIcon.Off)

        left = QIcon()
        left.addPixmap(QPixmap("images/button/left.png"), QIcon.Normal, QIcon.Off)

        right = QIcon()
        right.addPixmap(QPixmap("images/button/right.png"), QIcon.Normal, QIcon.Off)

        stop_button = QIcon()
        stop_button.addPixmap(QPixmap("images/button/stop.png"), QIcon.Normal, QIcon.Off)

        self.button1 = QPushButton(self)
        self.button1.setIcon(up)
        self.button1.setIconSize(QtCore.QSize(80, 80))
        self.button1.setFixedSize(80, 80)
        self.button1.setFocusPolicy(Qt.NoFocus)
        self.button1.setAutoRepeat(True)
        self.button1.move(210, 100)
        self.button1.clicked.connect(gogo)

        self.button2 = QPushButton(self)
        self.button2.setIcon(down)
        self.button2.setIconSize(QtCore.QSize(80, 80))
        self.button2.setFixedSize(80, 80)
        self.button2.setFocusPolicy(Qt.NoFocus)
        self.button2.setAutoRepeat(True)
        self.button2.move(210, 320)
        self.button2.clicked.connect(back)

        self.button3 = QPushButton(self)
        self.button3.setIcon(left)
        self.button3.setIconSize(QtCore.QSize(80, 80))
        self.button3.setFixedSize(80, 80)
        self.button3.setFocusPolicy(Qt.NoFocus)
        self.button3.setAutoRepeat(True)
        self.button3.move(100, 210)
        self.button3.clicked.connect(lambda: turn_left(0.1))

        self.button4 = QPushButton(self)
        self.button4.setIcon(right)
        self.button4.setIconSize(QtCore.QSize(80, 80))
        self.button4.setFixedSize(80, 80)
        self.button4.setFocusPolicy(Qt.NoFocus)
        self.button4.setAutoRepeat(True)
        self.button4.move(320, 210)
        self.button4.clicked.connect(lambda: turn_right(0.1))

        self.button5 = QPushButton(self)
        self.button5.setIcon(stop_button)
        self.button5.setIconSize(QtCore.QSize(80, 80))
        self.button5.setFixedSize(80, 80)
        self.button5.setFocusPolicy(Qt.NoFocus)
        self.button5.setAutoRepeat(True)
        self.button5.move(210, 210)
        self.button5.clicked.connect(stop)

        self.setFocus()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    qb = RemoteController()
    qb.show()
    sys.exit(app.exec_())
