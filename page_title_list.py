from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import ENTITY_ID


class CPageTitleList(QtWidgets.QListWidget):
  def __init__(self, parent):
    super(CPageTitleList, self).__init__(parent)

  def addItems(self, pageDict):
    for pageId, pageObj in pageDict.items():
      self.addPageTitleItem(pageId, pageObj.m_title)

  def addPageTitleItem(self, pageId: ENTITY_ID, pageTitle: str):
	  # Add to the list
    newItem = QtWidgets.QListWidgetItem(pageTitle)

    newItem.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)
    self.addItem(newItem)