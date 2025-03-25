from PySide6 import QtCore, QtWidgets, QtGui
from page_tree import CPageTree
from database import Database

from notebook_types import ENTITY_ID

from switchboard import Switchboard
from ui_search_dialog import Ui_searchDialog

class SearchDialog(QtWidgets.QDialog):
  def __init__(self, db: Database, pageTree: CPageTree, switchboard: Switchboard, parent):
    super(SearchDialog, self).__init__(parent)

    self.ui = Ui_searchDialog()
    self.ui.setupUi(self)

    self.db = db
    self.pageTree = pageTree
    self.switchboard = switchboard

    self.setConnections()

  def setConnections(self):
    self.ui.searchEdit.returnPressed.connect(self.search)

  @QtCore.Slot()
  def on_closeButton_clicked(self):
    self.done(True)

  @QtCore.Slot()
  def on_searchButton_clicked(self):
    self.search()

  @QtCore.Slot(str)
  def on_searchEdit_textChanged(self, newText):
    searchTerm = self.ui.searchEdit.text()

    self.ui.searchButton.setEnabled(len(searchTerm) > 0)

  @QtCore.Slot(QtWidgets.QListWidgetItem)
  def on_resultsListWidget_itemClicked(self, item):
    pageId = item.data(QtCore.Qt.ItemDataRole.UserRole)
    self.switchboard.emitPageSelected(pageId)

  def search(self):
    searchTerm = self.ui.searchEdit.text()
    self.doSearch(searchTerm)

  def doSearch(self, searchText):
    self.setWaitCursor()
    self.ui.resultsListWidget.clear()

    pageIds = self.pageTree.getTreeIdList()

    # Scan each page, and check its title and contents for the search term
    for pageId in pageIds:
      results = self.db.getPageTextItems(pageId)

      if results is not None:
        pageTitle = results[0]
        pageContentsHtml = results[1]
        tags = results[2]

        if searchText in pageTitle:
          self.addItem(pageId, pageTitle)

        else:
          # Since pages are stored as HTML, it is necessary to create a QTextDocument
          # with the text, then pull out the text with plainText.  Then, the plain text
          # can be searched.
          textDoc = QtGui.QTextDocument()

          textDoc.setHtml(pageContentsHtml)
          textContents = textDoc.toPlainText()

          if searchText in textContents:
            self.addItem(pageId, pageTitle)
          elif searchText in tags:
            self.addItem(pageId, pageTitle)

    self.restoreCursor()

  def addItem(self, pageId: ENTITY_ID, title: str):
    newItem = QtWidgets.QListWidgetItem(title)
    newItem.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)
    self.ui.resultsListWidget.addItem(newItem)

  def setWaitCursor(self):
    app = self.getApp()
    if app is not None:
      app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))

  def restoreCursor(self):
    app = self.getApp()
    if app is not None:
      app.restoreOverrideCursor()

  def getApp(self) -> QtWidgets.QApplication | None:
    app = QtWidgets.QApplication.instance()
    if type(app) is QtWidgets.QApplication:
      return app
    return None
