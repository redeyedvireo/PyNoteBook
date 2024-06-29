from PySide6 import QtCore, QtWidgets, QtGui

ICON_MAP = dict[int, QtGui.QPixmap]

class CClickableLabel(QtWidgets.QLabel):
  def __init__(self, parent):
    super(CClickableLabel, self).__init__(parent)
    self.iconMap: ICON_MAP = {}

  def loadIconForIndex(self, index: int, iconPath: str):
    self.iconMap[index] = QtGui.QPixmap(iconPath)

  def setIcon(self, index: int):
    if index in self.iconMap:
      pixmap = self.iconMap[index]
      self.setPixmap(pixmap)

