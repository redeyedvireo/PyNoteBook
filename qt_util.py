from PySide6 import QtCore
from PySide6.QtUiTools import QUiLoader

def loadUi(uiFilename):
  uiFile = QtCore.QFile('pynotebookwindow.ui')
  uiFile.open(QtCore.QFile.ReadOnly)

  loader = QUiLoader()
  return loader.load(uiFile)
