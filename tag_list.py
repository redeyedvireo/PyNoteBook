from PySide6 import QtCore, QtWidgets, QtGui

class CTagList(QtWidgets.QListWidget):
  def __init__(self, parent):
    super(CTagList, self).__init__(parent)