# An attempt at a PubSub mechanism
from PySide6 import QtCore, QtWidgets, QtGui

from page_data import PageData
from preferences import Preferences

class Switchboard(QtCore.QObject):
  pageSelected = QtCore.Signal(int)
  newPageCreated = QtCore.Signal(PageData)
  createNewToDoList = QtCore.Signal()
  pageSaved = QtCore.Signal(PageData)
  pageTitleUpdated = QtCore.Signal(int, str, bool)
  pageDeleted = QtCore.Signal(int)
  pageImported = QtCore.Signal(int, str)
  pageImportUpdated = QtCore.Signal(int, str)
  pageImportDeleted = QtCore.Signal(int)
  stylesChanged = QtCore.Signal()

  def __init__(self):
    super(Switchboard, self).__init__()
    self.preferences = Preferences('')

  def emitPageSelected(self, pageId: int):
    self.pageSelected.emit(pageId)

  def emitNewPageCreated(self, pageData: PageData):
    self.newPageCreated.emit(pageData)

  def emitCreateNewToDoList(self):
    self.createNewToDoList.emit()

  def emitPageSaved(self, pageData: PageData):
    self.pageSaved.emit(pageData)

  def emitPageTitleUpdated(self, pageId: int, pageTitle: str, isModification: bool):
    self.pageTitleUpdated.emit(pageId, pageTitle, isModification)

  def emitPageDeleted(self, pageId: int):
    self.pageDeleted.emit(pageId)

  def emitPageImported(self, pageId: int, pageTitle: str):
    self.pageImported.emit(pageId, pageTitle)

  def emitPageImportUpdated(self, pageId: int, pageTitle: str):
    self.pageImportUpdated.emit(pageId, pageTitle)

  def emitPageImportDeleted(self, pageId: int):
    self.pageImportDeleted.emit(pageId)

  def emitStylesChanged(self):
    self.stylesChanged.emit()
