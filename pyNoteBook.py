import sys
import os.path
import datetime
from pathlib import Path
import logging
import platform
from logging.handlers import RotatingFileHandler
from PySide6 import QtCore, QtWidgets, QtGui
from qt_util import loadUi
from util import getScriptPath
from ui_pynotebookwindow import Ui_PyNoteBookWindow
from database import Database
from page_data import PageData
from page_recovery import PageRecovery
from preferences import Preferences
from page_info_dlg import CPageInfoDlg
from prefs_dialog import PrefsDialog
from about_dlg import AboutDialog
from favorites_dialog import FavoritesDialog
from favorites_manager import FavoritesManager
from search_dialog import SearchDialog
from style_manager import StyleManager

from notebook_types import PAGE_TYPE, PAGE_ADD, PAGE_ADD_WHERE, ENTITY_ID, kInvalidPageId

kLogFile = 'PyNoteBook.log'
kAppName = 'PyNoteBook'

from constants import kPrefsFileName, \
                      kStyleDefsFileName, \
                      kStartupLoadPreviousNoteBook

kMaxLogileSize = 1024 * 1024
kMaxRecentFiles = 20

# ---------------------------------------------------------------
class PyNoteBookWindow(QtWidgets.QMainWindow):
  MW_PageDeleted = QtCore.Signal(ENTITY_ID)

  def __init__(self):
    super(PyNoteBookWindow, self).__init__()

    prefsFilePath = self.getPrefsPath()
    self.prefs = Preferences(prefsFilePath)

    self.db = Database()

    self.notebookFileName = ''      # Current notebook file name (name only)
    self.lastUsedDirectory: str = getScriptPath()
    self.currentNoteBookPath = ''   # Current notebook path (complete path)
    self.recentFileList = []        # List of recent files (complete paths)

    self.ui = Ui_PyNoteBookWindow()
    self.ui.setupUi(self)

    self.currentPageId = kInvalidPageId
    self.currentPageData = None
    self.tagsModified = False

    self.enableDataEntry(False)
    self.ui.savePageButton.setEnabled(False)
    self.ui.editorStackedWidget.setEnabled(True)

    self.favoritesManager = FavoritesManager()

    self.styleManager = StyleManager()
    self.styleManager.loadStyleDefs(self.getStyleDefsPath())

    self.ui.pageTextEdit.initialize(self.styleManager)

    self.setConnections()

  def initialize(self):
    self.ui.pageTree.initialize(self.db)
    self.ui.recentlyViewedList.initialize(self.db)
    self.ui.titleLabelWidget.initialize()

    self.prefs.readPrefsFile()

    pos = self.prefs.windowPos
    size = self.prefs.windowSize

    if pos is not None:
      self.move(pos)

    if size is not None:
      self.resize(size)

    self.recentFileList = self.prefs.recentFiles

    if len(self.recentFileList) > 0:
      self.updateRecentFilesMenu()

    previousFilepath = self.prefs.lastFile

    self.ui.navigationTabWidget.setCurrentIndex(self.prefs.selectedNavigationTab)

    if previousFilepath is not None and len(previousFilepath) > 0:
      if self.prefs.onStartupLoad == kStartupLoadPreviousNoteBook:
        # Reopen previously opened notebook.
        self.OpenNotebookFile(previousFilepath)


  # *************************** SLOTS ***************************

  def setConnections(self):
    # Page Tree signals
    self.ui.pageTree.pageSelectedSignal.connect(self.onPageSelected)
    self.ui.pageTree.pageTitleChangedSignal.connect(self.onPageTitleChanged)
    self.ui.pageTree.PT_PageDeleted.connect(self.onPageDeleted)
    self.ui.pageTree.PT_OnCreateNewPage.connect(self.on_actionNew_Page_triggered)
    self.ui.pageTree.PT_OnCreateNewFolder.connect(self.on_actionNew_Folder_triggered)

    # Editor signals
    self.ui.pageTextEdit.editorTextChangedSignal.connect(self.onPageModified)

    # Page History Widget
    self.ui.recentlyViewedList.PHW_PageSelected.connect(self.onPageSelected)

    # Title Label Widget
    self.ui.titleLabelWidget.TLW_SetPageAsFavorite.connect(self.onAddPageToFavorites)
    self.ui.titleLabelWidget.TLW_SetPageAsNonFavorite.connect(self.onRemovePageFromFavorites)

  @QtCore.Slot()
  def on_actionOpen_Notebook_triggered(self):
    self.checkSavePage()          # First check if a notebook page is open, and if so, prompt the user to save it.

    tempDbPathname, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self,
      "NoteBook - Open NoteBook File",
      self.lastUsedDirectory,
      "NoteBook files (*.nbk)");

    if len(tempDbPathname) > 0:
      print(f'DB filename: {tempDbPathname}, selected filter: {selectedFilter}')
      self.OpenNotebookFile(tempDbPathname)

  @QtCore.Slot()
  def on_savePageButton_clicked(self):
    # Get ID of the log entry from the list control.  If it is a new log entry,
    # the ID will be kTempItemId.

    if self.currentPageData is not None:
      self.currentPageData.m_title = self.ui.titleLabelWidget.getPageTitleLabel()
      self.currentPageData.m_tags = self.ui.tagsEdit.text()
      self.currentPageData.m_contentString = self.ui.pageTextEdit.toHtml()
      self.currentPageData.m_modifiedDateTime = datetime.datetime.now()

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

  @QtCore.Slot()
  def on_actionSearch_triggered(self):
    dlg = SearchDialog(self.db, self.ui.pageTree, self)
    dlg.show()

    dlg.pageSelectedSignal.connect(self.onPageSelected)

  @QtCore.Slot()
  def on_actionManage_Favorites_triggered(self):
    dlg = FavoritesDialog(self.favoritesManager.favoritesList, self)
    result = dlg.exec_()

    if result == QtWidgets.QDialog.DialogCode.Accepted:
      newFavoritesList = dlg.favoritesList
      removedPageIds = self.favoritesManager.getRemovedItems(newFavoritesList)

      # Update all removed pages to have their favorite flag turned off
      for pageId in removedPageIds:
        self.db.setPageFavoriteStatus(pageId, False)

      self.favoritesManager.setFavoriteItems(newFavoritesList)
      self.rebuildFavoritesMenu()

  @QtCore.Slot()
  def on_actionPage_Info_triggered(self):
    if self.currentPageData is not None:
      dlg = CPageInfoDlg(self, self.currentPageData)
      dlg.exec_()

  @QtCore.Slot()
  def on_actionSettings_triggered(self):
    dlg = PrefsDialog(self.prefs, self)
    result = dlg.exec_()

    if result == QtWidgets.QDialog.DialogCode.Accepted:
      self.prefs = dlg.preferences
      self.prefs.writePrefsFile()

  @QtCore.Slot()
  def on_actionAbout_NoteBook_triggered(self):
    dlg = AboutDialog(self.getAppDataDir(), self)
    dlg.exec()

  @QtCore.Slot()
  def on_actionAbout_Qt_triggered(self):
    app = QtWidgets.QApplication.instance()
    if type(app) is QtWidgets.QApplication:
      app.aboutQt()

  def onFavoriteSelected(self):
    sender = self.sender()

    if type(sender) is QtGui.QAction:
      pageId = sender.data()
      if pageId != kInvalidPageId:
        self.onPageSelected(pageId)

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
      self.ui.recentlyViewedList.addHistoryItem(pageId, self.currentPageData.m_title)

      # TODO: Notify child components that a new page has been selected?
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

  def onPageDefavorited(self, pageId: ENTITY_ID):
    self.db.setPageFavoriteStatus(pageId, False)

    if self.currentPageId == pageId:
      self.ui.titleLabelWidget.setFavoritesIcon(False)

  def onAddPageToFavorites(self):
    if self.currentPageIsValid() and self.currentPageData is not None and not self.currentPageData.m_bIsFavorite:
      self.favoritesManager.addFavoriteItem(self.currentPageId, self.currentPageData.m_title)
      self.rebuildFavoritesMenu()
      self.db.setPageFavoriteStatus(self.currentPageId, True)
      self.ui.titleLabelWidget.setFavoritesIcon(True)
      self.currentPageData.m_bIsFavorite = True

  def onRemovePageFromFavorites(self):
    if self.currentPageIsValid() and self.currentPageData is not None and self.currentPageData.m_bIsFavorite:
      self.onPageDefavorited(self.currentPageId)
      self.favoritesManager.removeFavoriteItem(self.currentPageId)
      self.rebuildFavoritesMenu()
      self.currentPageData.m_bIsFavorite = False

  def onRecentFileSelected(self):
    sender = self.sender()

    if type(sender) is QtGui.QAction:
      print(f'Recent file selected: {sender.text()}')

      self.closeNotebookFile()
      self.clearAllControls()
      self.OpenNotebookFile(sender.text())


# *************************** SETTINGS ***************************

  def getScriptPath(self):
    if getattr(sys, 'frozen', False):
      # If the application is run as a bundle, the PyInstaller bootloader
      # extends the sys module by a flag frozen=True and sets the app
      # path into variable _MEIPASS'.
      application_path, executable = os.path.split(sys.executable)
    else:
      application_path = os.path.dirname(os.path.abspath(__file__))

    return application_path

  def getAppDataDir(self) -> str:
    """Returns the directory used for app data.  The prefs file and styles def file are stored here.

    Returns:
        str: App data directory.
    """
    if platform.system() == 'Windows':
      # This attempts to use whatever directory is in the APPDATA environment variable, if it exists.
      # If the APPDATA environment variable doesn't exist, the application directory is used.
      return os.getenv('APPDATA', self.getScriptPath())
    elif platform.system() == 'Linux':
      # On Linux, use "~/.pylogbook"
      homeDirObj = Path.home()
      appDataDir = homeDirObj / '.pylogbook'
      return os.fspath(appDataDir)
    else:
      print('The application data directory is currently only supported on Windows and Linux')
      return ''

  def getPrefsPath(self) -> str:
    """ Returns the full path to the prefs file. """
    appDataDir = self.getAppDataDir()
    prefsPath = os.path.normpath(os.path.join(appDataDir, kAppName, kPrefsFileName))
    print(f'Prefs path: {prefsPath}')
    return prefsPath

  def getStyleDefsPath(self) -> str:
    """ Returns the full path to the style defs file.
        For now, this will be in the same directory as the prefs file (ie, the app data directory), but
        eventually, this will be user locatable, so that other apps (such as PyLogBook) can use the same styles.
    """
    appDataDir = self.getAppDataDir()
    styleDefsPath = os.path.normpath(os.path.join(appDataDir, kAppName, kStyleDefsFileName))
    print(f'Style defs path: {styleDefsPath}')
    return styleDefsPath


# *************************** FILE ***************************

  def OpenNotebookFile(self, filepath) -> bool:
    if len(filepath) > 0 and os.path.exists(filepath):
      directory, filename = os.path.split(filepath)
      self.notebookFileName = filename
      self.lastUsedDirectory = directory
      self.currentNoteBookPath = filepath

      self.db.openDatabase(self.currentNoteBookPath)

      # TODO: If the database is password protected, get password from the user

      # Read the page order for the notebook, if one exists
      pageOrderStr = self.db.getPageOrder()

      if pageOrderStr is not None:
        print(f'Page order string: {pageOrderStr}')
        self.populateNavigationControls(pageOrderStr)

        # Read page history
        pageHistoryStr = self.db.getPageHistory()

        if pageHistoryStr is not None:
          self.ui.recentlyViewedList.setPageHistory(pageHistoryStr)

        self.addFavoritesToFavoritesMenu()

        self.addFileToRecentFilesList()
        self.checkForMissingPages()

        self.displayLastEntry()
      return True
    else:
      logging.error(f'NoteBook {self.currentNoteBookPath} does not exist')
      return False

  def addFavoritesToFavoritesMenu(self):
    favoritePages = self.db.getFavoritePages()
    self.favoritesManager.setFavoriteItems(favoritePages)

    self.rebuildFavoritesMenu()

  def rebuildFavoritesMenu(self):
    """ Rebuilds the favorites menu from the contents of the favorites Manager. """
    self.removeExistingFavorites()
    favoritesSubmenu = self.getFavoritesSubmenu()

    for page in self.favoritesManager.favoritesList:
      action = QtGui.QAction(page[1], self)
      action.setData(page[0])     # Set pageId as the data element
      favoritesSubmenu.addAction(action)
      action.triggered.connect(self.onFavoriteSelected)

  def removeExistingFavorites(self):
    favoritesSubmenu = self.getFavoritesSubmenu()
    favoritesSubmenu.clear()

  def getFavoritesSubmenu(self) -> QtWidgets.QMenu:
    favoritesSubmenu = self.ui.actionFavorites.menu()

    if favoritesSubmenu is None:
      favoritesSubmenu = QtWidgets.QMenu()
      self.ui.actionFavorites.setMenu(favoritesSubmenu)

    if favoritesSubmenu is not None and type(favoritesSubmenu) is QtWidgets.QMenu:
      return favoritesSubmenu
    else:
      # Should never get here
      logging.error(f'[MainWindow.getFavoritesSubmenu] Returning a detached empty menu')
      return QtWidgets.QMenu()

  def addFileToRecentFilesList(self):
    if self.currentNoteBookPath in self.recentFileList:
      # The file is there, so remove it, and add it to the top
      self.recentFileList.remove(self.currentNoteBookPath)

    if len(self.recentFileList) == kMaxRecentFiles:
      self.recentFileList.pop()     # Remove last item

    # Add file to the top of the list
    self.recentFileList.insert(0, self.currentNoteBookPath)

    self.updateRecentFilesMenu()

  def updateRecentFilesMenu(self):
    recentMenu = self.ui.actionRecent_Notebooks.menu()

    if recentMenu is None:
      recentMenu = QtWidgets.QMenu()

      self.ui.actionRecent_Notebooks.setMenu(recentMenu)

    if recentMenu is not None and type(recentMenu) is QtWidgets.QMenu:
      recentMenu.clear()

      for recentFile in self.recentFileList:
        action = recentMenu.addAction(recentFile, self.onRecentFileSelected)

  def closeNotebookFile(self):
    if self.db.isDatabaseOpen():
      self.checkSavePage()        # check if user wants to save the page if it hasn't been saved

      # Save page history
      pageHistoryStr = self.ui.recentlyViewedList.getPageHistory()
      self.db.setPageHistory(pageHistoryStr)

      # Save page order
      pageOrderStr = self.ui.pageTree.getPageOrderString()
      self.db.setPageOrder(pageOrderStr)

      self.favoritesManager.clear()
      self.rebuildFavoritesMenu()

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

  def displayLastEntry(self):
    """Display the entry that was displayed when the database was last closed
    """
    pageId = self.ui.recentlyViewedList.getMostRecentlyViewedPage()

    if pageId == kInvalidPageId:
      pageId = self.db.getFirstPageId()
      pageId = pageId if type(pageId) == int else None

    if pageId is not None:
      self.onPageSelected(pageId)

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

    self.ui.titleLabelWidget.setFavoritesIcon(pageData.m_bIsFavorite)

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
    self.favoritesManager.clear()

  def checkSavePage(self):
    if self.pageModified():
      result = QtWidgets.QMessageBox.question(self, "PyNoteBook - Save Entry?", \
                                              'The current page has not been saved.  Would you like to save it?',\
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

      if result == QtWidgets.QMessageBox.StandardButton.Yes:
        self.on_savePageButton_clicked()

  def pageModified(self) -> bool:
    return self.ui.pageTextEdit.isModified() or self.tagsModified

  def onPageModified(self):
    self.setAppTitle()
    self.ui.savePageButton.setEnabled(True)

  def setAppTitle(self):
    windowTitle = ''

    if len(self.notebookFileName) > 0:
      windowTitle = f'Notebook - {self.currentNoteBookPath}'

      if self.pageModified():
        windowTitle += '*'
    else:
      windowTitle = 'Notebook'

    self.setWindowTitle(windowTitle)

  def clearPageEditControls(self):
    self.ui.titleLabelWidget.clear()

    fontSize = self.prefs.editorDefaultFontSize

    if fontSize <= 0:
      fontSize = 10

    fontFamily = self.prefs.editorDefaultFontFamily

    self.ui.pageTextEdit.newDocument(fontFamily, fontSize)

    self.ui.tagsEdit.clear()

  def currentPageIsValid(self) -> bool:
    return self.currentPageId != kInvalidPageId


# *************************** SHUTDOWN ***************************

  def closeEvent(self, event):
    self.closeAppWindow()

  def closeAppWindow(self):
    logging.info('Closing app window...')

    self.prefs.windowPos = self.pos()
    self.prefs.windowSize = self.size()
    self.prefs.lastFile = self.currentNoteBookPath
    self.prefs.recentFiles = self.recentFileList
    self.prefs.selectedNavigationTab = self.ui.navigationTabWidget.currentIndex()

    self.prefs.writePrefsFile()

    self.closeNotebookFile()

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
