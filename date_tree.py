from PySide6 import QtCore, QtWidgets, QtGui

class CDateTree(QtWidgets.QTreeWidget):
  def __init__(self, parent):
    super(CDateTree, self).__init__(parent)