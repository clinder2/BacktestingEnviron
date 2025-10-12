import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.insert(1, '/Users/christopherlinder/Desktop/CLBranch/BacktestingEnviron/Environ/While.py')
sys.path.insert(1, '/../BacktestingEnviron/Environ/While.py')
import Environ.While as W

class window(QWidget):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        self.resize(200,50)

def main():
    #W.While(['AAPL', 'NVDA'], 'MA', '2024-02-01', '2025-02-05', 1000)
    app = QApplication(sys.argv)
    ex=window()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    print(sys.path)
    main()