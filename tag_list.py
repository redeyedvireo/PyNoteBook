from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import ENTITY_ID
from pageCache import PageCache
from switchboard import Switchboard
from tagCache import TagCache

class CTagList(QtWidgets.QListWidget):
  def __init__(self, parent):
    super(CTagList, self).__init__(parent)
    self.setContextMenuPolicy(QtGui.Qt.ContextMenuPolicy.CustomContextMenu)
    self.customContextMenuRequested.connect(self.onContextMenu)
    self.contextMenu = QtWidgets.QMenu(self)

  def initialize(self, tagCache: TagCache, pageCache: PageCache, switchboard: Switchboard) -> None:
    self.tagCache = tagCache
    self.pageCache = pageCache
    self.switchboard = switchboard

    self.switchboard.pageTitleUpdated.connect(self.updateTags)
    self.switchboard.pageDeleted.connect(self.onPageIdDeleted)

  def addItems(self) -> None:
    """Adds items from the tag cache to the list.  It is assumed that the tag cache has
       been populated.
    """
    for tag in self.tagCache.tagDict.keys():
      self.addTag(tag)

  def addTag(self, tag: str) -> None:
	  # Add to the list
    newItem = QtWidgets.QListWidgetItem(tag)

    self.addItem(newItem)

  def updateTags(self) -> None:
    rowsToDelete = []
    numRows = self.count()

    # Scan the list and remove any tags that are no longer in the tag cache
    for row in range(numRows):
      item = self.item(row)
      if item is not None:
        tag = item.text()
        if tag not in self.tagCache.tagDict:
          rowsToDelete.append(row)

    # Remove the rows
    for row in reversed(rowsToDelete):
      self.takeItem(row)

    # Add any new tags
    for tag, pageIds in self.tagCache.tagDict.items():
      if self.findTag(tag) is None:
        self.addTag(tag)

  def findTag(self, tag: str) -> QtWidgets.QListWidgetItem | None:
    foundItems = self.findItems(tag, QtCore.Qt.MatchFlag.MatchFixedString)
    return foundItems[0] if len(foundItems) > 0 else None

  def onContextMenu(self, pos):
    self.contextMenu.clear()

    item = self.itemAt(pos)
    if item is None:
      return

    tagStr = item.text()

    pagesUsingTag = self.tagCache.pagesUsingTag(tagStr)

    pageTitleIdDict = {}
    for pageId in pagesUsingTag:
      pageTitle = self.pageCache.pageTitle(pageId)
      pageTitleIdDict[pageTitle] = pageId

    sortedPageTitles = dict(sorted(pageTitleIdDict.items()))

    for pageTitle, pageId in sortedPageTitles.items():
      action = self.contextMenu.addAction(f'{pageTitle}')
      action.setData(pageId)
      action.triggered.connect(self.onPageIdSelected)

    self.contextMenu.exec(self.mapToGlobal(pos))

  def onPageIdSelected(self):
    sender = self.sender()

    if type(sender) is QtGui.QAction:
      pageId = sender.data()

      self.switchboard.emitPageSelected(pageId)

  def onPageIdDeleted(self, pageId: ENTITY_ID):
    self.updateTags()