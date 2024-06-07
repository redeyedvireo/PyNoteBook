from PySide6 import QtCore, QtWidgets, QtGui
from datetime import datetime, date
from page_data import PageDataDict
from utility import formatDate
from notebook_types import PAGE_TYPE


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

  def addItems(self, pageDict: PageDataDict) -> None:
    self.setSortingEnabled(False)

    for pageId, pageData in pageDict.items():
      if pageData.m_pageType == PAGE_TYPE.kPageTypeUserText.value:
        self.addItem(pageData)

    self.sortDateItems()
    self.sortPageTitles()

  def addItem(self, pageData) -> None:
    dateItem = self.findDate(pageData.m_modifiedDateTime.date())

    if dateItem is None:
      dateItem = self.addDate(pageData.m_modifiedDateTime.date())

    newItem = QtWidgets.QTreeWidgetItem()
    newItem.setText(0, pageData.m_title)
    newItem.setData(0, QtCore.Qt.ItemDataRole.UserRole, pageData.m_pageId)
    dateItem.addChild(newItem)

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
    tliCount = self.topLevelItemCount();
    for i in range(tliCount):
      pItem = self.topLevelItem(i)
      self.sortTitlesWithinDate(pItem)

  def sortTitlesWithinDate(self, item) -> None:
    item.sortChildren(0, QtCore.Qt.SortOrder.AscendingOrder)

  def sortDateItems(self):
  	# This will end up sorting all of column 0, which would include
	  # the page titles.  The page titles will have to be sorted individually
	  # after this function is called.

    rootItem = self.invisibleRootItem()
    rootItem.sortChildren(0, QtCore.Qt.SortOrder.DescendingOrder)
