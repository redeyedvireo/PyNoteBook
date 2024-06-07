from enum import Enum

import logging
from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import kInvalidPageId, PAGE_TYPE, PAGE_ADD, PAGE_ADD_WHERE, ENTITY_ID, ENTITY_LIST

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

  def SetPageId(self, pageId):
    self.pageId = pageId

	#*	Updates the icon depending on whether it is expanded or collapsed.
  def UpdateIcon(self):
    pass


#************************************************************************
#* CPageTree                                                            *
#************************************************************************

class CPageTree(QtWidgets.QTreeWidget):
  pageSelectedSignal = QtCore.Signal(ENTITY_ID)
  pageTitleChangedSignal = QtCore.Signal(ENTITY_ID, str, bool)

  def __init__(self, parent):
    super(CPageTree, self).__init__(parent)
    self.db = None

    # This is a brute-force way to determine if a new page is being created.  It is used when
    # changing an item's title.  The on_itemChange_triggered function has no way of knowing whether
    # the item is being edited as the result of the initial title being set, or whether the title
    # is being changed deliberately by the user after the page has been created.
    self.newPageBeingCreated = False

    # This is used when loading a Notebook: the itemChanged signal will be triggered for each new
    # page that is being set.  This is to prevent it from being handled.
    self.loading = False

  def initialize(self, db):
    self.db = db
    self.setConnections()

  def setConnections(self):
    # TODO: Set signal/slot connections
    self.itemClicked.connect(self.onItemClicked)
    self.itemChanged.connect(self.onItemChanged)

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

  def newItem(self, pageId: ENTITY_ID, pageAdd: PAGE_ADD, pageAddWhere: PAGE_ADD_WHERE, title: str) -> tuple[bool, str, int]:
    """ Adds a new item to the tree.  If title is empty, the user will be given the chance to enter a title.
        Returns:
        - success
        - title (in case the user changed it)
        - parent ID, or kInvalidPageId if it is a top-level item
    """
    newPageId = pageId

    newItemType = PageWidgetItemType.eItemPage

    parentId = kInvalidPageId

    match pageAdd:
      case PAGE_ADD.kNewPage:
        newItemType = PageWidgetItemType.eItemPage

      case PAGE_ADD.kNewFolder:
        newItemType = PageWidgetItemType.eItemFolder

      case PAGE_ADD.kNewToDoListPage:
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
          parentId = self.getParentId(currentItem)
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

  def findItem(self, pageId) -> CPageWidgetItem | None:
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


# *************************** SLOTS ***************************

  def onItemClicked(self, item, column):
    if type(item) is CPageWidgetItem:
      pageId = item.pageId
      self.pageSelectedSignal.emit(pageId)

  def onItemChanged(self, item, column: int):
    if self.loading:
      # If loading a Notebook file, do nothing here
      return

    if type(item) is CPageWidgetItem:
      self.setCurrentItem(item)
      self.pageTitleChangedSignal.emit(item.pageId, item.text(0), not self.newPageBeingCreated)

    # Reset this flag.
    self.newPageBeingCreated = False
