import sys
import os.path
import logging
from logging.handlers import RotatingFileHandler
from PySide6 import QtCore, QtWidgets, QtGui
from qt_util import loadUi
from util import getScriptPath
from ui_pynotebookwindow import Ui_PyNoteBookWindow
from database import Database
from page_data import PageData
from page_recovery import PageRecovery

from notebook_types import PAGE_TYPE, PAGE_ADD, PAGE_ADD_WHERE, ENTITY_ID, kInvalidPageId

kLogFile = 'PyNoteBook.log'
kAppName = 'PyNoteBook'

kMaxLogileSize = 1024 * 1024

# ---------------------------------------------------------------
class PyNoteBookWindow(QtWidgets.QMainWindow):
  MW_PageDeleted = QtCore.Signal(ENTITY_ID)

  def __init__(self):
    super(PyNoteBookWindow, self).__init__()

    self.db = Database()

    self.notebookFileName = ''      # TODO: Get most-recently-used name from ini file
    self.lastUsedDirectory = getScriptPath()    # TODO: First check ini file, and if not there, use getScriptPath()
    self.currentNoteBookPath = ''   # TODO: Get from ini file

    self.ui = Ui_PyNoteBookWindow()
    self.ui.setupUi(self)

    self.currentPageId = kInvalidPageId
    self.currentPageData = None
    self.tagsModified = False

    self.enableDataEntry(False)
    self.ui.savePageButton.setEnabled(False)
    self.ui.editorStackedWidget.setEnabled(True)

    self.setConnections()


  def initialize(self):
    # TODO: Load settings from INI file
    # TODO: From INI file, determine the previously open notebook open (if any) and re-open it.
    self.ui.pageTree.initialize(self.db)


  # *************************** SLOTS ***************************

  def setConnections(self):
    # Page Tree signals
    self.ui.pageTree.pageSelectedSignal.connect(self.onPageSelected)
    self.ui.pageTree.pageTitleChangedSignal.connect(self.onPageTitleChanged)
    self.ui.pageTree.PT_PageDeleted.connect(self.onPageDeleted)

    # Editor signals
    self.ui.pageTextEdit.editorTextChangedSignal.connect(self.onPageModified)

  @QtCore.Slot()
  def on_actionOpen_Notebook_triggered(self):
    self.checkSavePage()          # First check if a notebook page is open, and if so, prompt the user to save it.

    tempDbPathname, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self,
      "NoteBook - Open NoteBook File",
      self.lastUsedDirectory,
      "NoteBook files (*.nbk)");

    if len(tempDbPathname) > 0:
      print(f'DB filename: {tempDbPathname}, selected filter: {selectedFilter}')
      self.currentNoteBookPath = tempDbPathname
      self.OpenNotebookFile()
      self.checkForMissingPages()

  @QtCore.Slot()
  def on_savePageButton_clicked(self):
    # Get ID of the log entry from the list control.  If it is a new log entry,
    # the ID will be kTempItemId.

    if self.currentPageData is not None:
      self.currentPageData.m_title = self.ui.titleLabelWidget.getPageTitleLabel()
      self.currentPageData.m_tags = self.ui.tagsEdit.text()
      self.currentPageData.m_contentString = self.ui.pageTextEdit.toHtml()

      success = self.db.updatePage(self.currentPageData)

      if not success:
        logging.error(f'[on_savePageButton_clicked] Error saving page ID {self.currentPageData.m_pageId} ({self.currentPageData.m_title})')
        return

      self.tagsModified = False
      self.ui.pageTextEdit.setDocumentModified(False)

      # TODO: Emit PageSaved signal (see who needs this.  It might not be necessary.)

      self.setAppTitle()
      self.ui.savePageButton.setEnabled(False)
    else:
      # Should never get here: self.currentPageData should always be a valid object.
      logging.error('[on_savePageButton_clicked] currentPageData is non-existent')

  @QtCore.Slot()
  def on_actionNew_Page_triggered(self):
    self.createNewPage(PAGE_TYPE.kPageTypeUserText)

  @QtCore.Slot()
  def on_actionNew_Top_Level_Page_triggered(self):
    self.createNewPage(PAGE_TYPE.kPageTypeUserText, topLevel=True)

  @QtCore.Slot()
  def on_actionNew_Folder_triggered(self):
    self.createNewPage(PAGE_TYPE.kPageFolder)

  @QtCore.Slot()
  def on_actionNew_Top_Level_Folder_triggered(self):
    self.createNewPage(PAGE_TYPE.kPageFolder, topLevel=True)

  @QtCore.Slot()
  def on_actionClose_triggered(self):
    self.closeNotebookFile()
    self.clearAllControls()
    self.enableDataEntry(False)

  def onPageSelected(self, pageId: ENTITY_ID):
    self.checkSavePage()        # Check if the current page is unsaved, and if so, ask user if he wants to save it.

    self.currentPageData = self.db.getPage(pageId)

    if self.currentPageData is not None:
      self.currentPageId = pageId

      # TODO: Get images for page
      imageNames = []

      self.tagsModified = False

      self.displayPage(self.currentPageData, imageNames, False)

      # Add page to the page history
      # TODO: Add page to the page history (will eventually be in a menu, not in a widget)
    else:
      # Page does not exist.  Blank out editors.
      logging.error(f'[PyNoteBookWindow.onPageSelected] Page ID {pageId} does not exist')
      self.clearPageEditControls()
      self.enableDataEntry(False)

      QtWidgets.QMessageBox.critical(self, kAppName, "Page does not exist")

  def onPageTitleChanged(self, pageId: ENTITY_ID, newTitle: str, isModification: bool):
    self.db.changePageTitle(pageId, newTitle, isModification)
    self.ui.titleLabelWidget.setPageTitleLabel(newTitle)
    if self.currentPageData is not None:
      self.currentPageData.m_title = newTitle

  def onPageDeleted(self, pageId: ENTITY_ID):
    # self.db.deleteAllImagesForPage(pageId)      # TODO: Implement this
    self.db.deletePage(pageId)

    self.clearPageEditControls()

    self.ui.pageTree.removePage(pageId)

    # TODO: Rethink this - instead of emitting a signal, just call the page removal member functions of each widget
    self.MW_PageDeleted.emit(pageId)


# *************************** FILE ***************************

  def OpenNotebookFile(self) -> bool:
    if len(self.currentNoteBookPath) > 0 and os.path.exists(self.currentNoteBookPath):
      self.db.openDatabase(self.currentNoteBookPath)

      # TODO: If the database is password protected, get password from the user

      # Read the page order for the notebook, if one exists
      pageOrderStr = self.db.getPageOrder()

      if pageOrderStr is not None:
        print(f'Page order string: {pageOrderStr}')
        self.populateNavigationControls(pageOrderStr)
      return True
    else:
      logging.error(f'NoteBook {self.currentNoteBookPath} does not exist')
      return False

  def closeNotebookFile(self):
    if self.db.isDatabaseOpen():
      self.checkSavePage()        # check if user wants to save the page if it hasn't been saved

      # TODO: Save page history

      # Save page order
      pageOrderStr = self.ui.pageTree.getPageOrderString()
      self.db.setPageOrder(pageOrderStr)

      self.db.closeDatabase()

      self.currentNoteBookPath = ''

      self.setAppTitle()          # Remove the Notebook name from the app title

  def checkForMissingPages(self):
    """Checks if there are any pages in the database that are not in the page tree.  If so, these pages
    need to be reloaded.
    """
    pagesAndParentsList, success = self.db.getAllPageIdsAndParents()

    if success:
      pageRecovery = PageRecovery(pagesAndParentsList, self.ui.pageTree.getTreeIdList())

      if pageRecovery.thereAreLostPages():
        QtWidgets.QMessageBox.information(self, kAppName, "The list of pages need to be rescanned from the database")
        pagesToInsert = pageRecovery.recoverPages()
        pagesToInsertStr = ','.join(map(str, pagesToInsert))
        self.populateNavigationControls(pagesToInsertStr)


# *************************** UI ***************************

  def populateNavigationControls(self, pageOrderStr: str):
    pageDict, success = self.db.getPageList()   # Retrieve all pages, regardless of whether they appear in the pageOrderStr

    self.ui.pageTree.addItemsNew(pageDict, pageOrderStr)

    self.ui.pageTitleList.addItems(pageDict)
    self.ui.dateTree.addItems(pageDict)

    pageIdDict, success = self.db.getTagList()

    self.ui.tagList.addItems(pageIdDict)

  def enableDataEntry(self, enable):
    self.ui.pageTextEdit.setEnabled(enable)
    self.ui.pageTextEdit.enableEditing(enable)
    self.ui.tagsEdit.setEnabled(enable)

  def createNewPage(self, pageType: PAGE_TYPE, pageTitle = '', topLevel = False):
    """Creates a new Notebook page.

    Args:
        pageType (PAGE_TYPE): Type of page to create (ie, user text, folder, todo)
        pageTitle (str, optional): Title of page. Defaults to ''.
        topLevel (bool, optional): Whether this should be a top-level page. Defaults to False.
    """
    self.checkSavePage()      # Check if the current page is unsaved

    # Create new page
    newPageId = self.db.nextPageId()      # Get an unused ID to use for this new page

    self.currentPageData = PageData()
    self.currentPageData.m_pageId = newPageId
    self.currentPageData.m_pageType = pageType

    self.clearPageEditControls()

    pageAddWhere = PAGE_ADD_WHERE.kPageAddTopLevel if topLevel else PAGE_ADD_WHERE.kPageAddDefault

    success, title, parentId = self.ui.pageTree.newItem(newPageId, pageType, pageAddWhere, pageTitle)

    if success:
      self.currentPageData.m_parentId = parentId      # This might be kInvalidPageId, which is OK
      self.currentPageData.m_title = title

      # Currently, addNewBlankPage applies for creating both pages and folders.
      self.db.addNewBlankPage(self.currentPageData)

      if pageType == PAGE_TYPE.kPageTypeUserText:
        # TODO: Should a 'new page created' event be emitted here?
        pass

      elif pageType == PAGE_TYPE.kPageFolder:
        # TODO: Should a 'new folder created' event be emitted here?
        pass

      # Write the page order to the database.
      pageOrderStr = self.ui.pageTree.getPageOrderString()
      self.db.setPageOrder(pageOrderStr)

  def displayPage(self, pageData: PageData, imageNames: list[str], isNewPage: bool):
    self.ui.titleLabelWidget.setPageTitleLabel(pageData.m_title)

    # TODO: Once there are multiple editor types, activate the appropriate editor

    if pageData.m_pageType == PAGE_TYPE.kPageTypeUserText:
      if isNewPage:
        # TODO: Create new document
        pass
      else:
        self.ui.pageTextEdit.setPageContents(pageData.m_contentString, imageNames)

    # Set tags
    if len(pageData.m_tags) == 0:
      self.ui.tagsEdit.clear()
    else:
      self.ui.tagsEdit.setText(pageData.m_tags)

    self.setAppTitle()

    self.enableDataEntry(True)

    # Disable the Save button (until an edit is made)
    self.ui.savePageButton.setEnabled(False)

  def clearAllControls(self):
    self.clearPageEditControls()
    self.ui.pageTree.clear()
    self.ui.pageTitleList.clear()
    self.ui.dateTree.clear()
    self.ui.tagList.clear()
    self.ui.recentlyViewedList.clear()
    self.ui.searchWidget.clear()
    self.ui.favoritesWidget.clear()

  def checkSavePage(self):
    # TODO: Implement checkSavePage
    pass

  def onPageModified(self):
    self.setAppTitle()
    self.ui.savePageButton.setEnabled(True)

  def setAppTitle(self):
    windowTitle = ''

    if len(self.notebookFileName) > 0:
      windowTitle = f'Notebook - {self.currentNoteBookPath}'

      if self.pageIsModified():
        windowTitle += '*'
    else:
      windowTitle = 'Notebook'

    self.setWindowTitle(windowTitle)

  def pageIsModified(self) -> bool:
    return self.ui.pageTextEdit.isModified()

  def clearPageEditControls(self):
    self.ui.titleLabelWidget.clear()

    fontSize = 12
    fontFamily = 'Arial'

    # TODO: When prefs are implemented, uncomment this
    # fontSize = self.prefs.getEditorDefaultFontSize()

    # if fontSize < 0:
    #   fontSize = 10

    # fontFamily = self.prefs.getEditorDefaultFontFamily()

    self.ui.pageTextEdit.newDocument(fontFamily, fontSize)

    self.ui.tagsEdit.clear()

# *************************** SHUTDOWN ***************************

  def closeEvent(self, event):
    print('closeEvent called')
    self.closeAppWindow()

  def closeAppWindow(self):
    logging.info('Closing app window...')
    self.closeNotebookFile()
    # self.prefs.setWindowPos(self.pos())
    # self.prefs.setWindowSize(self.size())
    # self.prefs.writePrefsFile()

def shutdownApp():
  logging.info("Shutting down...")
  logging.shutdown()

def getLogfilePath():
  return os.path.join(getScriptPath(), kLogFile)

def main():
  console = logging.StreamHandler()
  rotatingFileHandler = RotatingFileHandler(getLogfilePath(), maxBytes=kMaxLogileSize, backupCount=9)
  logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                          handlers=[ rotatingFileHandler, console ])

  app = QtWidgets.QApplication([])

  window = PyNoteBookWindow()
  window.initialize()

  # widget.resize(800, 600)
  window.show()

  returnValue = app.exec()
  shutdownApp()

  sys.exit(returnValue)

# ---------------------------------------------------------------
if __name__ == "__main__":
  main()
