from PySide6 import QtCore, QtWidgets, QtGui

class CPageHistoryWidget(QtWidgets.QListWidget):
  def __init__(self, parent):
    super(CPageHistoryWidget, self).__init__(parent)