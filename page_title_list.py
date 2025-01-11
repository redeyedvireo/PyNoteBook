from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import ENTITY_ID
from page_data import PageData
from switchboard import Switchboard

# TODO: Add functions to handle page importing, and page updated by import (see C++ version)

class CPageTitleList(QtWidgets.QListWidget):
  def __init__(self, parent):
    super(CPageTitleList, self).__init__(parent)
    self.setSortingEnabled(True)
    self.itemClicked.connect(self.onItemClicked)

  def initialize(self, switchboard: Switchboard):
    self.switchboard = switchboard
    switchboard.newPageCreated.connect(self.onNewPageCreated)
    switchboard.pageTitleUpdated.connect(self.onPageTitleUpdated)
    switchboard.pageDeleted.connect(self.onPageDeleted)

    # TODO: Connect signals for PageImported and PageUpdatedByImport

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

  def onNewPageCreated(self, pageData: PageData):
    self.addPageTitleItem(pageData.m_pageId, pageData.m_title)

  def onPageTitleUpdated(self, pageId: ENTITY_ID, pageTitle: str, isModification: bool):
    item = self.findItem(pageId)
    if item is not None:
      item.setText(pageTitle)

  def onPageDeleted(self, pageId: ENTITY_ID):
    item = self.findItem(pageId)
    if item is not None:
      self.takeItem(self.row(item))

  def onItemClicked(self, item: QtWidgets.QListWidgetItem):
    pageId = item.data(QtCore.Qt.ItemDataRole.UserRole)
    self.switchboard.emitPageSelected(pageId)
