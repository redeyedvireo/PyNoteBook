import sys
from PySide6 import QtCore, QtWidgets, QtGui
from qt_util import loadUi
from ui_pynotebookwindow import Ui_NoteBookClass

# ---------------------------------------------------------------
class PyNoteBookWindow(QtWidgets.QMainWindow):
    def __init__(self):
      super(PyNoteBookWindow, self).__init__()

      # self.ui = loadUi('pynotebookwindow.ui')
      # window.show()

      self.ui = Ui_NoteBookClass()
      self.ui.setupUi(self)

def main():
  app = QtWidgets.QApplication([])

  window = PyNoteBookWindow()
  # widget.resize(800, 600)
  window.show()

  sys.exit(app.exec())

# ---------------------------------------------------------------
if __name__ == "__main__":
  main()
