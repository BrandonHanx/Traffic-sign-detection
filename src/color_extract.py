from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon


class ColorDialog(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        color = QColor(0, 0, 0)
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Color Dialog')
        self.setWindowIcon(QIcon("images/button/pallet.jpg"))
        self.button = QPushButton('Dialog', self)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.move(20, 20)
        self.button.clicked.connect(self.showDialog)
        self.setFocus()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setStyleSheet('QWidget{background-color:%s}' % color.name())
        self.widget.setGeometry(100, 100, 100, 100)

    def showDialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.widget.setStyleSheet('QWidget {background-color:%s}' % col.name())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    qb = ColorDialog()
    qb.show()
    sys.exit(app.exec_())
