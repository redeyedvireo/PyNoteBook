from PySide6 import QtCore, QtWidgets, QtGui
from database import Database
from notebook_types import ENTITY_ID, ID_TITLE_LIST

from ui_favorites_widget import Ui_CFavoritesWidget

class CFavoritesWidget(QtWidgets.QWidget):
  FW_PageSelected = QtCore.Signal(ENTITY_ID)
  FW_PageDefavorited = QtCore.Signal(ENTITY_ID)

  def __init__(self, parent):
    super(CFavoritesWidget, self).__init__(parent)
    self.ui = Ui_CFavoritesWidget()
    self.ui.setupUi(self)

    self.db = None
    self.selectedItem = None

  def initialize(self, db: Database):
    self.db = db

    self.setConnections()

  def setConnections(self):
    self.ui.favoritesListWidget.itemClicked.connect(self.onItemClicked)
    self.ui.clearButton.clicked.connect(self.onRemoveAllClicked)
    self.ui.removeSelectedButton.clicked.connect(self.onRemoveSelectedClicked)

  def clear(self):
    self.ui.favoritesListWidget.clear()

  def addPage(self, pageId: ENTITY_ID, pageTitle: str):
    newItem = QtWidgets.QListWidgetItem(pageTitle)
    newItem.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)
    self.ui.favoritesListWidget.addItem(newItem)

  def removePage(self, pageId: ENTITY_ID):
    foundItem = self.findFavoriteItem(pageId)

    if foundItem is not None:
      row = self.getItemRow(foundItem)
      self.ui.favoritesListWidget.takeItem(row)

  def addPages(self, pages: ID_TITLE_LIST):
    for page in pages:
      self.addFavoriteItem(page[0], page[1])

  def addFavoriteItem(self, pageId: ENTITY_ID, pageTitle: str):
    # Check if this page already exists
    foundItem = self.findFavoriteItem(pageId)

    if foundItem is None:
      self.addPage(pageId, pageTitle)

  def findFavoriteItem(self, pageId: ENTITY_ID) -> QtWidgets.QListWidgetItem | None:
    numItems = self.ui.favoritesListWidget.count()

    for i in range(numItems):
      item = self.ui.favoritesListWidget.item(i)
      itemPageId = self.getItemPageId(item)

      if itemPageId == pageId:
        return item

    return None   # Not found

  def getNthItemPageId(self, n) -> ENTITY_ID:
    """Gets the page ID for the Nth item in the list

    Args:
        n (int): Index into page ID list

    Returns:
        ENTITY_ID: Page ID of the given item
    """
    item = self.ui.favoritesListWidget.item(n)
    return self.getItemPageId(item)

  def getItemPageId(self, item: QtWidgets.QListWidgetItem) -> ENTITY_ID:
    return item.data(QtCore.Qt.ItemDataRole.UserRole)

  def getItemRow(self, item: QtWidgets.QListWidgetItem) -> int:
    return self.ui.favoritesListWidget.row(item)


# *************************** SLOTS ***************************

  def onItemClicked(self, item):
    self.selectedItem = item
    pageId = item.data(QtCore.Qt.ItemDataRole.UserRole)
    self.FW_PageSelected.emit(pageId)

  def onRemoveAllClicked(self):
    numItems = self.ui.favoritesListWidget.count()

    for i in range(numItems):
      item = self.ui.favoritesListWidget.item(0)    # Always take the first one, as the list will be shrinking
      pageId = self.getItemPageId(item)
      self.ui.favoritesListWidget.takeItem(self.getItemRow(item))
      self.FW_PageDefavorited.emit(pageId)

  def onRemoveSelectedClicked(self):
    if self.selectedItem is not None:
      pageId = self.getItemPageId(self.selectedItem)
      self.ui.favoritesListWidget.takeItem(self.getItemRow(self.selectedItem))
      self.selectedItem = None
      self.FW_PageDefavorited.emit(pageId)
