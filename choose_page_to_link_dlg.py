from PySide6 import QtCore, QtGui, QtWidgets

from database import Database
from notebook_types import ENTITY_ID

from ui_choose_page_to_link_dlg import Ui_ChoosePageToLinkDlg

from notebook_types import PAGE_TYPE

class ChoosePageToLinkDlg(QtWidgets.QDialog):
  def __init__(self, database: Database, parent: QtWidgets.QWidget) -> None:
    super(ChoosePageToLinkDlg, self).__init__(parent)

    self.ui = Ui_ChoosePageToLinkDlg()
    self.ui.setupUi(self)

    self.db = database

    self.loadPageTitles()

  def loadPageTitles(self):
    pageDict, success = self.db.getPageList()

    if success:
      for pageId, pageObj in pageDict.items():
        # Only want to show pages, not folders
        if pageObj.m_pageType == PAGE_TYPE.kPageTypeUserText.value:
          newItem = QtWidgets.QListWidgetItem(pageObj.m_title, self.ui.listWidget)
          newItem.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)

      self.ui.listWidget.sortItems()

  def getSelectedPage(self) -> ENTITY_ID:
    item = self.ui.listWidget.currentItem()
    return item.data(QtCore.Qt.ItemDataRole.UserRole)

  @QtCore.Slot()
  def on_clearFilterButton_clicked(self):
    self.showAllRows()

  @QtCore.Slot()
  def on_filterEdit_returnPressed(self):
    self.filterContents()

  @QtCore.Slot(str)
  def on_filterEdit_textChanged(self, text):
    self.filterContents()

  @QtCore.Slot(QtWidgets.QListWidgetItem)
  def on_listWidget_itemDoubleClicked(self, item: QtWidgets.QListWidgetItem):
    self.accept()

  def itemText(self, row: int) -> str:
    item = self.ui.listWidget.item(row)
    return item.text()

  def setRowVisibility(self, row: int, visible: bool):
    item = self.ui.listWidget.item(row)
    item.setHidden(not visible)

  def filterContents(self):
    filterString = self.ui.filterEdit.text()

    if len(filterString) > 0:
      numItems = self.ui.listWidget.count()
      filterStringLowerCase = filterString.lower()

      for row in range(numItems):
        self.setRowVisibility(row, filterStringLowerCase in self.itemText(row).lower())

  def showAllRows(self):
    self.ui.filterEdit.setText('')

    numItems = self.ui.listWidget.count()
    for row in range(numItems):
        self.setRowVisibility(row, True)
