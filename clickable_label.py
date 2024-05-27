from PySide6 import QtCore, QtWidgets, QtGui

class CClickableLabel(QtWidgets.QLabel):
  def __init__(self, parent):
    super(CClickableLabel, self).__init__(parent)