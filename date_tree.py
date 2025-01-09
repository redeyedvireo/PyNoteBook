from PySide6 import QtCore, QtWidgets, QtGui
from datetime import datetime, date
from page_data import PageData, PageDataDict
from switchboard import Switchboard
from utility import formatDate, datesEqual
from notebook_types import ENTITY_ID, PAGE_TYPE, kInvalidPageId
import logging


#************************************************************************
#* CDateWidgetItem                                                      *
#************************************************************************

class CDateWidgetItem(QtWidgets.QTreeWidgetItem):
  def __init__(self, parent, date: date):
    super(CDateWidgetItem, self).__init__(parent)
    self.date = date
    self.setText(0, formatDate(self.date))

  def __lt__(self, other):
    return self.date < other.date

  def __eq__(self, other):
    return self.date == other.date

  def __ne__(self, other):
    return self.date != other.date


class CDateTree(QtWidgets.QTreeWidget):
  def __init__(self, parent):
    super(CDateTree, self).__init__(parent)
    self.setContextMenuPolicy(QtGui.Qt.ContextMenuPolicy.CustomContextMenu)

    self.initMenus()

  def initialize(self, switchboard: Switchboard):
    self.switchboard = switchboard
    switchboard.newPageCreated.connect(self.onNewPageCreated)
    switchboard.pageSaved.connect(self.onPageSaved)
    switchboard.pageTitleUpdated.connect(self.onPageTitleUpdated)
    switchboard.pageDeleted.connect(self.onPageDeleted)

    # TODO: Connect signals for PageImported and PageUpdatedByImport

    self.itemClicked.connect(self.onItemClicked)
    self.itemChanged.connect(self.onItemChanged)

    self.customContextMenuRequested.connect(self.onContextMenu)

  def initMenus(self):
    self.contextMenu = QtWidgets.QMenu()
    self.contextMenu.addAction('ExpandAll', self.expandAll)
    self.contextMenu.addAction('CollapseAll', self.collapseAll)

  def getItemPageId(self, item: QtWidgets.QTreeWidgetItem) -> ENTITY_ID:
    return item.data(0, QtCore.Qt.ItemDataRole.UserRole)

  def addItems(self, pageDict: PageDataDict) -> None:
    self.setSortingEnabled(False)

    for pageId, pageData in pageDict.items():
      if pageData.m_pageType == PAGE_TYPE.kPageTypeUserText.value:
        self.addItem(pageData)

    self.sortDateItems()
    self.sortPageTitles()

  def addItem(self, pageData: PageData) -> None:
    dateItem = self.findDate(pageData.m_modifiedDateTime.date())

    if dateItem is None:
      dateItem = self.addDate(pageData.m_modifiedDateTime.date())

    newItem = QtWidgets.QTreeWidgetItem()
    newItem.setText(0, pageData.m_title)
    newItem.setData(0, QtCore.Qt.ItemDataRole.UserRole, pageData.m_pageId)
    dateItem.addChild(newItem)

  def pageItemParent(self, pageItem: QtWidgets.QTreeWidgetItem) -> CDateWidgetItem | None:
    parent = pageItem.parent()

    return parent if type(parent) is CDateWidgetItem else None

  def findPageItem(self, pageId: ENTITY_ID) -> QtWidgets.QTreeWidgetItem | None:
    """Returns the top-level tree widget item that contains the given page ID.

    Args:
        pageId (ENTITY_ID): Page ID of the page to find

    Returns:
        QtWidgets.QTreeWidgetItem | None: Tree widget item containing the given page, or None if not found
    """
    if pageId == kInvalidPageId:
      return None

    # Iterate over the children of the date items.  The date items are the
    # first level of children in the tree.

    tliCount = self.topLevelItemCount()

    for dateItemNum in range(tliCount):
      dateItem = self.topLevelItem(dateItemNum)

      for i in range(dateItem.childCount()):
        treeItem = dateItem.child(i)

        if treeItem is not None and self.getItemPageId(treeItem) == pageId:
          return treeItem

    # If get here, the page was not found
    return None

  def findDate(self, inDate: date) -> CDateWidgetItem | None:
    tliCount = self.topLevelItemCount()
    for i in range(tliCount):
      dateItem = self.topLevelItem(i)

      if dateItem is not None and type(dateItem) is CDateWidgetItem:
        if dateItem.date == inDate:
          return dateItem

    return None

  def addDate(self, inDate: date) -> CDateWidgetItem:
    dateItem = CDateWidgetItem(self, inDate)
    self.addTopLevelItem(dateItem)
    return dateItem

  def sortPageTitles(self):
    # Since the dates are sorted in descending order, it is necessary
    # to resort the page titles in ascending order.
    tliCount = self.topLevelItemCount()
    for i in range(tliCount):
      pItem = self.topLevelItem(i)
      self.sortTitlesWithinDate(pItem)

  def sortTitlesWithinDate(self, item: QtWidgets.QTreeWidgetItem) -> None:
    item.sortChildren(0, QtCore.Qt.SortOrder.AscendingOrder)

  def sortDateItems(self):
  	# This will end up sorting all of column 0, which would include
	  # the page titles.  The page titles will have to be sorted individually
	  # after this function is called.

    rootItem = self.invisibleRootItem()
    rootItem.sortChildren(0, QtCore.Qt.SortOrder.DescendingOrder)

  def onContextMenu(self, pos: QtCore.QPoint):
    self.contextMenu.popup(self.mapToGlobal((pos)))

  def onItemClicked(self, item: QtWidgets.QTreeWidgetItem, column: int):
    pageId = self.getItemPageId(item)
    self.switchboard.emitPageSelected(pageId)

  def onItemChanged(self, item: QtWidgets.QTreeWidgetItem, column: int):
    # Since the dates are sorted in descending order, it is necessary
    # to resort the page titles in ascending order, whenever an item
    # is changed.  Whenever the tree is touched, Qt will resort the tree,
    # thus, it is necessary to resort the titles within each date.
    self.sortPageTitles()

  def onNewPageCreated(self, pageData: PageData):
    self.addItem(pageData)
    self.sortPageTitles()

  def onPageSaved(self, pageData: PageData):
    # Determine if the page needs to be moved to a different date parent.
    item = self.findPageItem(pageData.m_pageId)

    if item is not None:
      dateItem = self.pageItemParent(item)

      if dateItem is not None:
        childIndex = dateItem.indexOfChild(item)

        if not datesEqual(dateItem.date, pageData.m_modifiedDateTime):
          # The page now has a different modification date.  It needs to be moved.
				  # Find the date under which this page should be created.
          newDateItem = self.findDate(pageData.m_modifiedDateTime.date())

          if newDateItem is None:
            # The date does not exist, so add it
            newDateItem = self.addDate(pageData.m_modifiedDateTime.date())

            # Must re-soert the date items, since a new date was added
            self.sortDateItems()

            # Sorting the date items will require all page titles to be resorted
            self.sortPageTitles()

          # DEBUG: verify that the original item is still at the same childindex
          childIndexVerify = dateItem.indexOfChild(item)
          if childIndexVerify != childIndex:
            logging.debug(f'[onPageSaved] childIndexVerify ({childIndexVerify}) does not equal childIndex ({childIndex})')
          # END DEBUG

          # Remote page item from its current date, and add it to the new date
          removedItem = dateItem.takeChild(childIndex)
          newDateItem.addChild(removedItem)

          # If the old date has no more children, remove it
          if dateItem.childCount() == 0:
            index = self.indexOfTopLevelItem(dateItem)
            self.takeTopLevelItem(index)

          self.sortTitlesWithinDate(newDateItem)

  def onPageTitleUpdated(self, pageId: int, pageTitle: str, isModification: bool):
    item = self.findPageItem(pageId)

    if item is not None:
      itemDate = self.pageItemParent(item)

      if itemDate is not None:
        item.setText(0, pageTitle)

        self.sortTitlesWithinDate(itemDate)     # Maintain sort order within the date

        # Changing the title constitutes a "change"??

  def onPageDeleted(self, pageId: ENTITY_ID):
    item = self.findPageItem(pageId)

    if item is not None:
      itemDate = self.pageItemParent(item)

      if itemDate is not None:
        itemDate.removeChild(item)

        # If the date widget has no more children, remove the date widget item
        if itemDate.childCount() == 0:
          index = self.indexOfTopLevelItem(itemDate)
          self.takeTopLevelItem(index)
