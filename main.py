from PyQt5 import QtWidgets
from gui import MainWindow
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
