from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import ENTITY_ID

# TODO: Add functions to handle page importing, and page updated by import (see C++ version)

class CPageTitleList(QtWidgets.QListWidget):
  pageSelected = QtCore.Signal(ENTITY_ID)

  def __init__(self, parent):
    super(CPageTitleList, self).__init__(parent)
    self.setSortingEnabled(True)
    self.itemClicked.connect(self.onItemClicked)

  def findItem(self, pageId: ENTITY_ID) -> QtWidgets.QListWidgetItem | None:
    for i in range(self.count()):
      item = self.item(i)
      if item.data(QtCore.Qt.ItemDataRole.UserRole) == pageId:
        return item
    return None

  def addItems(self, pageDict):
    for pageId, pageObj in pageDict.items():
      self.addPageTitleItem(pageId, pageObj.m_title)

  def addPageTitleItem(self, pageId: ENTITY_ID, pageTitle: str):
	  # Add to the list
    newItem = QtWidgets.QListWidgetItem(pageTitle)

    newItem.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)
    self.addItem(newItem)

  def onNewPageCreated(self, pageId: ENTITY_ID, pageTitle: str):
    self.addPageTitleItem(pageId, pageTitle)

  def onPageTitleUpdated(self, pageId: ENTITY_ID, pageTitle: str):
    item = self.findItem(pageId)
    if item is not None:
      item.setText(pageTitle)

  def onPageDeleted(self, pageId: ENTITY_ID):
    item = self.findItem(pageId)
    if item is not None:
      self.takeItem(self.row(item))

  def onItemClicked(self, item: QtWidgets.QListWidgetItem):
    pageId = item.data(QtCore.Qt.ItemDataRole.UserRole)
    self.pageSelected.emit(pageId)
