from PySide6 import QtCore, QtWidgets, QtGui
from database import Database
from notebook_types import ENTITY_ID

kDefaultMaxHistory = 20

class CPageHistoryWidget(QtWidgets.QListWidget):
  PHW_PageSelected = QtCore.Signal(ENTITY_ID)

  def __init__(self, parent):
    super(CPageHistoryWidget, self).__init__(parent)
    self.db = None
    self.maxHistory = kDefaultMaxHistory

  def initialize(self, db: Database):
    self.db = db

    self.setConnections()

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
    newItem.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)

    if addAtEnd:
      self.addItem(newItem)
    else:
      self.insertItem(0, newItem)

  def findItem(self, pageId: ENTITY_ID) -> QtWidgets.QListWidgetItem | None:
    for i in range(self.count()):
      item = self.item(i)

      if item.data(QtCore.Qt.ItemDataRole.UserRole) == pageId:
        return item

    return None   # Not found

  def getPageHistory(self):
    """Returns a comma-separated list of page IDs that comprise the page history (most-recent first).
    """
    pageIdList = []

    for i in range(self.count()):
      item = self.item(i)

      pageIdList.append(item.data(QtCore.Qt.ItemDataRole.UserRole))

    return ','.join(map(str, pageIdList))


# *************************** SLOTS ***************************

  def onItemClicked(self, item):
    pageId = item.data(QtCore.Qt.ItemDataRole.UserRole)
    self.PHW_PageSelected.emit(pageId)

