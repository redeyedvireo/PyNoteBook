import sys
import os.path
import logging
from logging.handlers import RotatingFileHandler
from PySide6 import QtCore, QtWidgets, QtGui
from qt_util import loadUi
from util import getScriptPath
from ui_pynotebookwindow import Ui_PyNoteBookWindow
from database import Database

kLogFile = 'PyNoteBook.log'
kAppName = 'PyNoteBook'

kMaxLogileSize = 1024 * 1024

# ---------------------------------------------------------------
class PyNoteBookWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(PyNoteBookWindow, self).__init__()

    # self.ui = loadUi('pynotebookwindow.ui')
    # window.show()

    self.db = Database()

    self.notebookFileName = ''      # TODO: Get most-recently-used name from ini file
    self.lastUsedDirectory = getScriptPath()    # TODO: First check ini file, and if not there, use getScriptPath()
    self.currentNoteBookPath = ''   # TODO: Get from ini file

    self.ui = Ui_PyNoteBookWindow()
    self.ui.setupUi(self)


  # *************************** SLOTS ***************************

  @QtCore.Slot()
  def on_actionOpen_Notebook_triggered(self):
    # TODO: First check if a notebook page is open, and if so, prompt the user to save it.

    tempDbPathname, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self,
      "NoteBook - Open NoteBook File",
      self.lastUsedDirectory,
      "NoteBook files (*.nbk)");

    if len(tempDbPathname) > 0:
      print(f'DB filename: {tempDbPathname}, selected filter: {selectedFilter}')
      self.currentNoteBookPath = tempDbPathname


# *************************** FILE ***************************

  def OpenNotebookFile(self) -> bool:
    if len(self.currentNoteBookPath) > 0 and os.path.exists(self.currentNoteBookPath):
      self.db.openDatabase(self.currentNoteBookPath)
      return True
    else:
      logging.error(f'NoteBook {self.currentNoteBookPath} does not exist')
      return False

# *************************** SHUTDOWN ***************************

  def closeEvent(self, event):
    print('closeEvent called')
    self.closeAppWindow()

  def closeAppWindow(self):
    logging.info('Closing app window...')
    # self.closeLogFile()
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
  # widget.resize(800, 600)
  window.show()

  returnValue = app.exec()
  shutdownApp()

  sys.exit(returnValue)

# ---------------------------------------------------------------
if __name__ == "__main__":
  main()
