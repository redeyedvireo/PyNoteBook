from enum import Enum

import logging
from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import kInvalidPageId, PAGE_TYPE

class PageWidgetItemType(Enum):
  eItemPage = 0
  eItemFolder = 1
  eItemToDoList = 2


#************************************************************************
#* CPageWidgetItem                                                      *
#************************************************************************

class CPageWidgetItem(QtWidgets.QTreeWidgetItem):
  def __init__(self, parent, pageId, itemType):
    super(CPageWidgetItem, self).__init__(parent)
    self.pageId = pageId
    self.itemType = itemType

  def SetPageId(self, pageId):
    self.pageId = pageId

	#*	Updates the icon depending on whether it is expanded or collapsed.
  def UpdateIcon(self):
    pass

class CPageTree(QtWidgets.QTreeWidget):
  def __init__(self, parent):
    super(CPageTree, self).__init__(parent)

  def addItemsNew(self, pageDict, pageOrderStr):
    # TODO: Would like to move away from using a page order string.  It would be better to be
    #       able to just read the pages from the database.

    pageIdList = pageOrderStr.split(',')

    for pageIdStr in pageIdList:
      pageId = int(pageIdStr)

      if pageId != kInvalidPageId:
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