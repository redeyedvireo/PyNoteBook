from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import ENTITY_ID
from pageCache import PageCache
from tagCache import TagCache

class CTagList(QtWidgets.QListWidget):
  pageSelected = QtCore.Signal(ENTITY_ID)

  def __init__(self, parent):
    super(CTagList, self).__init__(parent)
    self.setContextMenuPolicy(QtGui.Qt.ContextMenuPolicy.CustomContextMenu)
    self.customContextMenuRequested.connect(self.onContextMenu)
    self.contextMenu = QtWidgets.QMenu(self)

  def initialize(self, tagCache: TagCache, pageCache: PageCache) -> None:
    self.tagCache = tagCache
    self.pageCache = pageCache

  def addItems(self) -> None:
    """Adds items from the tag cache to the list.  It is assumed that the tag cache has
       been populated.
    """
    tagsAdded = []      # Used to prevent duplicates from being added

    for tag, pageIds in self.tagCache.tagDict.items():
      for pageId in pageIds:
        if tag not in tagsAdded:
          self.addTag(pageId, tag)
          tagsAdded.append(tag)

  def addTag(self, pageId: ENTITY_ID, tag: str) -> None:
	  # Add to the list
    newItem = QtWidgets.QListWidgetItem(tag)

    newItem.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)
    self.addItem(newItem)

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

    self.contextMenu.exec_(self.mapToGlobal(pos))

  def onPageIdSelected(self):
    sender = self.sender()

    if type(sender) is QtGui.QAction:
      pageId = sender.data()

      self.pageSelected.emit(pageId)