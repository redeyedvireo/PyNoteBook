from enum import Enum

import logging
from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import kInvalidPageId, PAGE_TYPE, PAGE_ADD, PAGE_ADD_WHERE, ENTITY_ID, ENTITY_LIST
from database import Database
from switchboard import Switchboard

class PageWidgetItemType(Enum):
  eItemPage = 0
  eItemFolder = 1
  eItemToDoList = 2


#************************************************************************
#* CPageWidgetItem                                                      *
#************************************************************************

class CPageWidgetItem(QtWidgets.QTreeWidgetItem):
  def __init__(self, parent, pageId, itemType: PageWidgetItemType):
    super(CPageWidgetItem, self).__init__(parent)
    self.pageId = pageId
    self.itemType = itemType

    self.setText(0, 'Untitled Page')
    self.setFlags(self.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

    # Set icon based on item type
    match self.itemType:
      case PageWidgetItemType.eItemPage:
        self.setIcon(0, QtGui.QIcon(':/NoteBook/Resources/Page.png'))

      case PageWidgetItemType.eItemFolder:
        self.setIcon(0, QtGui.QIcon(':/NoteBook/Resources/Folder Closed.png'))

      case PageWidgetItemType.eItemToDoList:
        self.setIcon(0, QtGui.QIcon(':/NoteBook/Resources/ToDoList.png'))

  def SetPageId(self, pageId):
    self.pageId = pageId

	#*	Updates the icon depending on whether it is expanded or collapsed.
  def UpdateIcon(self):
    if self.itemType == PageWidgetItemType.eItemFolder:
      if self.isExpanded():
        self.setIcon(0, QtGui.QIcon(':/NoteBook/Resources/Folder Open.png'))
      else:
        self.setIcon(0, QtGui.QIcon(':/NoteBook/Resources/Folder Closed.png'))


# Alias for a list of CPageWidgetItems
PageItemList = list[CPageWidgetItem]

#************************************************************************
#* CPageTree                                                            *
#************************************************************************

class CPageTree(QtWidgets.QTreeWidget):
  PT_OnCreateNewPage = QtCore.Signal()
  PT_OnCreateNewFolder = QtCore.Signal()

  def __init__(self, parent):
    super(CPageTree, self).__init__(parent)
    self.db = None

    self.pageContextMenu = QtWidgets.QMenu()
    self.folderListSubmenu = QtWidgets.QMenu()
    self.folderContextMenu = QtWidgets.QMenu()
    self.blankAreaContextMenu = QtWidgets.QMenu()

    # This is a brute-force way to determine if a new page is being created.  It is used when
    # changing an item's title.  The on_itemChange_triggered function has no way of knowing whether
    # the item is being edited as the result of the initial title being set, or whether the title
    # is being changed deliberately by the user after the page has been created.
    self.newPageBeingCreated = False

    # This is used when loading a Notebook: the itemChanged signal will be triggered for each new
    # page that is being set.  This is to prevent it from being handled.
    self.loading = False

    self.lastClickedPage = None

    self.setContextMenuPolicy(QtGui.Qt.ContextMenuPolicy.CustomContextMenu)
    self.setAcceptDrops(True)
    self.setDragEnabled(True)
    self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)

  def initialize(self, db: Database, switchboard: Switchboard):
    self.db = db
    self.switchboard = switchboard
    self.setConnections()
    self.initMenus()

  def setConnections(self):
    self.itemClicked.connect(self.onItemClicked)
    self.itemChanged.connect(self.onItemChanged)
    self.itemExpanded.connect(self.onItemExpanded)
    self.itemCollapsed.connect(self.onItemCollapsed)
    self.customContextMenuRequested.connect(self.onContextMenu)

    # Switchboard signals
    self.switchboard.pageSelected.connect(self.selectPage)
    self.switchboard.pageDeleted.connect(self.removePage)

    # TODO: Connect signals for PageImported and PageUpdatedByImport

  def initMenus(self):
    # Page context menu
    self.pageContextMenu.addAction('Rename Page', self.onRenamePageTriggered)
    self.pageContextMenu.addAction('Delete Page', self.onDeletePageTriggered)
    self.pageContextMenu.addSeparator()
    self.folderListSubmenu.setTitle('Move to Folder')
    self.pageContextMenu.addMenu(self.folderListSubmenu)
    self.pageContextMenu.addAction('Move to top-level', self.onMoveToTopLevel)

    # Folder context menu
    self.folderContextMenu.addAction('New Page', self.onAddNewPageTriggered)
    self.folderContextMenu.addAction('New To Do List', self.onNewToDoListTriggered)
    self.folderContextMenu.addAction('New Folder', self.onNewFolderTriggered)
    self.folderContextMenu.addAction('Rename Folder', self.onRenamePageTriggered)

    # For now, deleting non-empty folders is not supported.  This could be a very involved operation, as child pages and folders
    # will have to be deleted also.  A recursive function will be needed to delete a folder.  The UI should not be
    # updated until all children of the folder have been deleted.
    self.folderContextMenu.addAction('Delete Empty Folder', self.onDeleteFolderTriggered)
    self.folderContextMenu.addSeparator()
    self.folderContextMenu.addAction('Expand All', self.expandAll)
    self.folderContextMenu.addAction('Collapse All', self.collapseAll)

  def itemToCPageWidgetItem(self, item: QtWidgets.QTreeWidgetItem) -> CPageWidgetItem | None:
    if item is not None and type(item) is CPageWidgetItem:
      return item
    else:
      return None

  def getParentId(self, item: CPageWidgetItem) -> ENTITY_ID:
    parent = item.parent()
    pageWidgetItem = self.itemToCPageWidgetItem(parent)
    if pageWidgetItem is not None:
      return pageWidgetItem.pageId
    else:
      return kInvalidPageId

  def addTopLevelPageTreeItem(self, pageTitle: str, pageId: ENTITY_ID, itemType: PageWidgetItemType):
    newItem = CPageWidgetItem(0, pageId, itemType)
    newItem.setText(0, pageTitle)
    self.addTopLevelItem(newItem)

  def newItem(self, pageId: ENTITY_ID, pageType: PAGE_TYPE, pageAddWhere: PAGE_ADD_WHERE, title: str) -> tuple[bool, str, int]:
    """ Adds a new item to the tree.  If title is empty, the user will be given the chance to enter a title.
        Returns:
        - success
        - title (in case the user changed it)
        - parent ID, or kInvalidPageId if it is a top-level item
    """
    newPageId = pageId
    parentId = kInvalidPageId

    match pageType:
      case PAGE_TYPE.kPageTypeUserText:
        newItemType = PageWidgetItemType.eItemPage

      case PAGE_TYPE.kPageFolder:
        newItemType = PageWidgetItemType.eItemFolder

      case PAGE_TYPE.kPageTypeToDoList:
        newItemType = PageWidgetItemType.eItemToDoList

      case _:
        newItemType = PageWidgetItemType.eItemPage

    newItem = CPageWidgetItem(0, newPageId, newItemType)

    currentItem = self.currentItem()

    # - if there is no current item in the page tree, then add a new top-level item
    # - if the current item is a page (not a folder), then add a sibling item
    # - if the current item is a folder, then add a child

    if currentItem is None or pageAddWhere == PAGE_ADD_WHERE.kPageAddTopLevel:
      # Add a new top-level item
      self.addTopLevelItem(newItem)
    else:
      if type(currentItem) is CPageWidgetItem:
        if currentItem.itemType == PageWidgetItemType.eItemPage:
          parent = currentItem.parent()
          if parent is not None:
            parent.addChild(newItem)
            if type(parent) is CPageWidgetItem:
              parentId = parent.pageId
          else:
            # currentItem is a top-level (ie, no parent)
            currentItemIndex = self.indexOfTopLevelItem(currentItem)
            if currentItemIndex != -1:
              self.insertTopLevelItem(currentItemIndex + 1, newItem)

        elif currentItem.itemType == PageWidgetItemType.eItemFolder:
          # The current item is a folder, so add a child item
          # TODO: Currently, the new page is placed at the end of the folder items.  Maybe it should go after the current one?
          currentItem.addChild(newItem)
          currentItem.setExpanded(True)
          parentId = currentItem.pageId
      else:
        # Error - all items in the tree should be of type CPageWidgetItem
        logging.error(f'CPageTree.newItem: currentItem is not a CPageWidgetItem')
        return (False, title, kInvalidPageId)

    self.scrollToItem(newItem)

    if len(title) == 0:
      # The title parameter was empty, so make the item editable so the user can enter the page title
      self.newPageBeingCreated = True     # To ensure that this doesn't count as a page modification
      self.editItem(newItem, 0)
    else:
      # Use the title parameter as the item's title
      newItem.setText(0, title)

    return (True, newItem.text(0), parentId)

  def addItemsNew(self, pageDict, pageOrderStr):
    pageIdList = pageOrderStr.split(',')

    self.loading = True

    for pageIdStr in pageIdList:
      pageId = int(pageIdStr)

      if pageId != kInvalidPageId and pageId in pageDict:
        pageData = pageDict[pageId]

        pageType = PageWidgetItemType.eItemPage

        if pageData is not None:
          match pageData.m_pageType:
            case PAGE_TYPE.kPageTypeUserText.value:
              pageType = PageWidgetItemType.eItemPage

            case PAGE_TYPE.kPageTypeToDoList.value:
              pageType = PageWidgetItemType.eItemToDoList

            case PAGE_TYPE.kPageFolder.value:
              pageType = PageWidgetItemType.eItemFolder

            case _:
              pageType = PageWidgetItemType.eItemPage

        success = self.addItem(pageData.m_pageId, pageData.m_parentId, pageType, pageData.m_title)

        if not success:
          logging.error(f'CPageTree.addItemsNew: Error adding item')

    self.loading = False

  def addItem(self, pageId: int, parentId: int, pageType: PageWidgetItemType, pageTitle: str) -> bool:
    if pageId == kInvalidPageId:
      logging.error(f'CPageTree.addItem: pageId is invalid')
      return False

    parent = None

    if parentId != kInvalidPageId:
      # Add as child.  Make sure the parent exists in the tree
      parent = self.findItem(parentId)

      if parent is None:
        # Parent not found
        logging.error(f'CPageTree.addItem: For pageId {pageId}, parentId {parentId} is not found in the tree')
        return False

    newTreeWidgetItem = CPageWidgetItem(parent, pageId, pageType)
    newTreeWidgetItem.setText(0, pageTitle)

    if parent is not None:
      parent.addChild(newTreeWidgetItem)
    else:
      self.addTopLevelItem(newTreeWidgetItem)

    return True

  def findItem(self, pageId: ENTITY_ID) -> CPageWidgetItem | None:
    if pageId == kInvalidPageId:
      return None

    return self.findItemInSubTree(self.invisibleRootItem(), pageId)

  def findItemInSubTree(self, pageWidgetItem: QtWidgets.QTreeWidgetItem | CPageWidgetItem, pageId) -> CPageWidgetItem | None:
    if pageWidgetItem is not None:
      # Note that pageWidgetItem might be a QTreeWidgetItem in the case where it is the invisibleRootItem.  In all other
      # cases, it should be a CPageTreeWidgetItem.
      if type(pageWidgetItem) is CPageWidgetItem and pageWidgetItem.pageId == pageId:
        return pageWidgetItem

      for i in range(pageWidgetItem.childCount()):
        pTreeItem = pageWidgetItem.child(i)

        if type(pTreeItem) is CPageWidgetItem:
          if pTreeItem.pageId == pageId:
            return pTreeItem

          # Search pTreeItem's children
          pFoundItem = self.findItemInSubTree(pTreeItem, pageId)

          if pFoundItem is not None and pFoundItem.pageId == pageId:
            return pFoundItem
        else:
          # Should never get here
          logging.error(f'CPageTree.findItemInSubTree: pTreeItem is not a CPageWidgetItem')
          return None

      # Not found
      return None

    else:
      logging.error(f'CPageTree.findItemInSubTree: pageWidgetItem is not a CPageWidgetItem')
      return None

  def moveItem(self, item: CPageWidgetItem, newParent: CPageWidgetItem | None) -> bool:
    """Moves a page to a new parent

    Args:
        item (CPageWidgetItem): Page to move
        newParent (CPageWidgetItem): Parent in which to move the item, or None to insert at top-level

    Returns:
        bool: True if successful, False otherwise.
    """
    if item is None:
      return False

    # Get item's parent
    parentOfItem = item.parent()

    tempItem = None

    if parentOfItem is not None:
      childIndex = parentOfItem.indexOfChild(item)

      if childIndex != -1:
        tempItem = parentOfItem.takeChild(childIndex)
        # tempItem should be the same as item
    else:
      # item is a top-level item
      index = self.indexOfTopLevelItem(item)

      if index != -1:
        tempItem = self.takeTopLevelItem(index)

    if tempItem is not None:
      # Insert at new location
      if newParent is not None:
        newParent.addChild(tempItem)
      else:
        # If newParent is None, move item to the top-level
        self.addTopLevelItem(tempItem)

      return True
    else:
      return False

  def selectPage(self, pageId: ENTITY_ID):
    selectedItem = self.findItem(pageId)

    if selectedItem is not None:
      # Need to set the loading flag, because the scrollToItem() function, called below,
      # causes various subtrees to expand, which trigger onItemChanged() to be called.
      self.loading = True

      self.scrollToItem(selectedItem)
      self.setCurrentItem(selectedItem)
      self.loading = False

  def removePage(self, pageId: ENTITY_ID):
    item = self.findItem(pageId)

    if item is not None:
      # Determine which item to select next
      #  - First try to select the item below.
      #  - If that item does not exist, try to select the item above
      #  - If that item does not exist, try to select the parent
      newItem = self.itemBelow(item)

      if newItem is None:
        # Try item above
        newItem = self.itemAbove(item)

        if newItem is None:
          # Try parent
          newItem = item.parent()

      if newItem is not None:
        self.setCurrentItem(newItem)

      # Remove the item from the tree
      if item.parent() is not None:
        item.parent().removeChild(item)
      else:
        index = self.indexOfTopLevelItem(item)
        self.takeTopLevelItem(index)

      self.writePageOrderToDatabase()

      if newItem is not None and type(newItem) is CPageWidgetItem:
        self.switchboard.emitPageSelected(newItem.pageId)

  def getPageOrderString(self) -> str:
    idList = self.getTreeIdList()
    return ','.join(map(str, idList))

  def getTreeIdList(self) -> ENTITY_LIST:
    return self.getTreeListForSubfolder(self.invisibleRootItem())

  def getTreeListForSubfolder(self, treeWidgetItem: QtWidgets.QTreeWidgetItem) -> ENTITY_LIST:
    entityList = []

    numChildren = treeWidgetItem.childCount()

    for i in range(numChildren):
      subPageItem = treeWidgetItem.child(i)

      if type(subPageItem) is CPageWidgetItem:
        entityList.append(subPageItem.pageId)

        if subPageItem.itemType == PageWidgetItemType.eItemFolder:
          # Search folder's children
          subList = self.getTreeListForSubfolder(subPageItem)
          entityList.extend(subList)

    return entityList

  def writePageOrderToDatabase(self):
    pageOrderStr = self.getPageOrderString()
    if self.db is not None:
      self.db.setPageOrder(pageOrderStr)

  def updateParent(self, pageId: ENTITY_ID, newParentId: ENTITY_ID):
    if self.db is not None:
      self.db.updatePageParent(pageId, newParentId)
      self.writePageOrderToDatabase()

  def getFolderList(self) -> PageItemList:
    """Returns a list of folders in the tree.

    Returns:
        ENTITY_LIST: List of folders found in the tree.
    """
    return self.getFolderListFromSubTree(self.invisibleRootItem())

  def getFolderListFromSubTree(self, root: QtWidgets.QTreeWidgetItem) -> PageItemList:
    """Returns a list of all folders under the root item.

    Args:
        root (QtWidgets.QTreeWidgetItem): Element from which to return the child folders

    Returns:
        PageItemList: List of folders, as a list of CPageWidgetItems.
    """
    entityList = []

    numChildren = root.childCount()

    for i in range(numChildren):
      subPageItem = root.child(i)

      if type(subPageItem) is CPageWidgetItem:
        if subPageItem.itemType == PageWidgetItemType.eItemFolder:
          entityList.append(subPageItem)
          subList = self.getFolderListFromSubTree(subPageItem)
          entityList.extend(subList)

    return entityList

  def deletePage(self, pageId):
    self.switchboard.emitPageDeleted(pageId)

  def deleteFolder(self):
    if self.lastClickedPage is not None and self.lastClickedPage.itemType == PageWidgetItemType.eItemFolder:
      if self.isFolderEmpty(self.lastClickedPage):
        self.deletePage(self.lastClickedPage.pageId)

  def isFolderEmpty(self, item: CPageWidgetItem) -> bool:
    if item is None:
      return True
    else:
      return item.childCount == 0

  def isPointOnPage(self, pt) -> bool:
    item = self.itemAt(pt)

    if item is not None and type(item) is CPageWidgetItem:
      return item.itemType == PageWidgetItemType.eItemPage or item.itemType == PageWidgetItemType.eItemToDoList

    return False

  def isPointOnFolder(self, pt) -> bool:
    item = self.itemAt(pt)
    if item is not None and type(item) is CPageWidgetItem:
      return item.itemType == PageWidgetItemType.eItemFolder

    return False

  def constructFolderSubmenu(self):
    self.folderListSubmenu.clear()

    pageList = self.getFolderList()

    for item in pageList:
      newAction = QtGui.QAction(item.text(0), self)
      newAction.setData(item.pageId)
      self.folderListSubmenu.addAction(newAction)

      newAction.triggered.connect(self.onMoveFolder)


# *************************** EVENTS ***************************

  def mousePressEvent(self, event: QtGui.QMouseEvent):
    super().mousePressEvent(event)
    item = self.itemAt(event.pos())
    if item is not None and type(item) is CPageWidgetItem:
      self.lastClickedPage = item

  def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
    super().dragEnterEvent(event)
    if self.lastClickedPage is not None:
      event.acceptProposedAction()

  def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
    super().dragMoveEvent(event)
    event.accept()

  def dropEvent(self, event: QtGui.QDropEvent):
    super().dropEvent(event)
    event.acceptProposedAction()
    if self.lastClickedPage is not None:
      self.updateParent(self.lastClickedPage.pageId, self.getParentId(self.lastClickedPage))

# *************************** SLOTS ***************************

  def onItemClicked(self, item, column):
    if type(item) is CPageWidgetItem:
      pageId = item.pageId
      self.switchboard.emitPageSelected(pageId)

  def onItemChanged(self, item, column: int):
    if self.loading:
      # If loading a Notebook file, do nothing here
      return

    if type(item) is CPageWidgetItem:
      self.setCurrentItem(item)
      self.switchboard.emitPageTitleUpdated(item.pageId, item.text(0), not self.newPageBeingCreated)

    # Reset this flag.
    self.newPageBeingCreated = False

  def onItemExpanded(self, item):
    if type(item) is CPageWidgetItem:
      item.UpdateIcon()

  def onItemCollapsed(self, item):
    if type(item) is CPageWidgetItem:
      item.UpdateIcon()

  def onContextMenu(self, pos):
    item = self.itemAt(pos)

    if item is not None:
      if type(item) is CPageWidgetItem:
        self.lastClickedPage = item

        self.constructFolderSubmenu()

        if self.isPointOnPage(pos):
          self.pageContextMenu.popup(self.mapToGlobal(pos))
        else:
          # For now, deleting non-empty folders is not supported.  So,
          # check if the folder is empty, and if not, hide the "Delete Empty Folder"
          # menu item.
          self.folderContextMenu.popup(self.mapToGlobal(pos))
    else:
      # User clicked on white space
      self.blankAreaContextMenu.popup(self.mapToGlobal(pos))

  def onRenamePageTriggered(self):
    if self.lastClickedPage is not None:
      self.editItem(self.lastClickedPage, 0)

  def onDeletePageTriggered(self):
    if self.lastClickedPage is not None:
      message = f'Do you want to delete the page {self.lastClickedPage.text(0)}'

      if QtWidgets.QMessageBox.question(self, 'NoteBook - Delete Page', message) == QtWidgets.QMessageBox.StandardButton.Yes:
        self.deletePage(self.lastClickedPage.pageId)

  def onDeleteFolderTriggered(self):
    # TODO: Implement this
    pass

  def onMoveToTopLevel(self):
    if self.lastClickedPage is not None:
      success = self.moveItem(self.lastClickedPage, None)
      if success:
        self.updateParent(self.lastClickedPage.pageId, kInvalidPageId)

  def onMoveFolder(self):
    if self.lastClickedPage is not None:
      sender = self.sender()

      if type(sender) is QtGui.QAction:
        print(f'Data: {sender.data()}')
        pageId = sender.data()
        destinationItem = self.findItem(pageId)

        if destinationItem is not None and type(destinationItem) is CPageWidgetItem:
          if destinationItem.itemType == PageWidgetItemType.eItemFolder:
            success = self.moveItem(self.lastClickedPage, destinationItem)

            if success:
              self.updateParent(self.lastClickedPage.pageId, destinationItem.pageId)

  def onAddNewPageTriggered(self):
    self.PT_OnCreateNewPage.emit()

  def onNewToDoListTriggered(self):
    # TODO: Implement this
    pass

  def onNewFolderTriggered(self):
    self.PT_OnCreateNewFolder.emit()

