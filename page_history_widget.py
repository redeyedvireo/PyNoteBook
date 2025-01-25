from PySide6 import QtCore, QtWidgets, QtGui
from database import Database
from switchboard import Switchboard
from notebook_types import ENTITY_ID, kInvalidPageId

kDefaultMaxHistory = 20

class CPageHistoryWidget(QtWidgets.QListWidget):
  def __init__(self, parent):
    super(CPageHistoryWidget, self).__init__(parent)
    self.db = None
    self.maxHistory = kDefaultMaxHistory

  def initialize(self, db: Database, switchboard: Switchboard):
    self.db = db
    self.switchboard = switchboard

    self.setConnections()

  def pageIdForItem(self, item: QtWidgets.QListWidgetItem) -> ENTITY_ID:
    return item.data(QtCore.Qt.ItemDataRole.UserRole)

  def setPageIdForItem(self, item, pageId):
    item.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)

  def setConnections(self):
    self.itemClicked.connect(self.onItemClicked)

  def setPageHistory(self, pageHistoryStr: str):
    if self.db is not None:
      pageIdStrList = pageHistoryStr.split(',')
      pageIdList = [int(idStr) for idStr in pageIdStrList]

      for pageId in pageIdList:
        title = self.db.getPageTitle(pageId)
        if title is not None:
          self.addHistoryItem(pageId, title, True)

  def getMostRecentlyViewedPage(self) -> ENTITY_ID:
    return self.pageIdForItem(self.item(0)) if self.count() > 0 else kInvalidPageId

  def addHistoryItem(self, pageId: ENTITY_ID, title: str, addAtEnd: bool = False):
    item = self.findItem(pageId)

    if item is not None:
      # This page already exists.  If it is not the first element,
      # remove it, and place it at the top.  If it is the first element,
      # there is nothing to do.
      itemRow = self.row(item)

      if itemRow > 0:
        self.takeItem(itemRow)
      else:
        return      # The item is already the first item in the list

    if self.count() == self.maxHistory:
      # The list is full.  Remove the last item before adding a new one
      self.takeItem(self.count() - 1)

    newItem = QtWidgets.QListWidgetItem(title)
    self.setPageIdForItem(newItem, pageId)

    if addAtEnd:
      self.addItem(newItem)
    else:
      self.insertItem(0, newItem)

  def findItem(self, pageId: ENTITY_ID) -> QtWidgets.QListWidgetItem | None:
    for i in range(self.count()):
      item = self.item(i)

      if self.pageIdForItem(item) == pageId:
        return item

    return None   # Not found

  def getPageHistory(self):
    """Returns a comma-separated list of page IDs that comprise the page history (most-recent first).
    """
    pageIdList = []

    for i in range(self.count()):
      item = self.item(i)

      pageIdList.append(self.pageIdForItem(item))

    return ','.join(map(str, pageIdList))


# *************************** SLOTS ***************************

  def onItemClicked(self, item):
    pageId = self.pageIdForItem(item)
    self.switchboard.emitPageSelected(pageId)

