from PySide6 import QtCore, QtWidgets, QtGui

class CPageTree(QtWidgets.QTreeWidget):
  def __init__(self, parent):
    super(CPageTree, self).__init__(parent)