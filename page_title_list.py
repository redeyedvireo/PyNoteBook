from PySide6 import QtCore, QtWidgets, QtGui

class CPageTitleList(QtWidgets.QListWidget):
  def __init__(self, parent):
    super(CPageTitleList, self).__init__(parent)