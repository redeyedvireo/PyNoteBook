from copy import deepcopy
from PySide6 import QtCore, QtGui, QtWidgets
from preferences import Preferences

from ui_prefs_dialog import Ui_PrefsDialog

from constants import kStartupLoadPreviousNoteBook, \
                      kStartupEmptyWorkspace

class PrefsDialog(QtWidgets.QDialog):
  def __init__(self, preferences: Preferences, parent: QtWidgets.QWidget) -> None:
    super(PrefsDialog, self).__init__(parent)

    self.ui = Ui_PrefsDialog()
    self.ui.setupUi(self)

    self.accepted.connect(self.onAccept)

    self.preferences = deepcopy(preferences)
    self.curFont = QtGui.QFont(self.preferences.editorDefaultFontFamily, self.preferences.editorDefaultFontSize)

    self.ui.listWidget.setCurrentRow(0)
    self.populateDialog()

  def populateDialog(self):
    # Application prefs
    if self.preferences.onStartupLoad == kStartupLoadPreviousNoteBook:
      self.ui.loadPreviousNotebookRadio.setChecked(True)
    else:
      self.ui.emptyWorkspaceRadio.setChecked(True)

    # Text Editor
    self.populatePointSizesCombo()
    self.setDefaultFont(self.curFont)

  def populatePointSizesCombo(self):
    fontDatabase = QtGui.QFontDatabase()

    curFontFamily = self.ui.fontCombo.currentText()
    self.ui.fontSizeCombo.clear()

    fontSizeList = fontDatabase.pointSizes(curFontFamily)

    for fontSize in fontSizeList:
      self.ui.fontSizeCombo.addItem(f'{fontSize}')

  def getDefaultFont(self) -> QtGui.QFont:
    return self.ui.fontCombo.currentFont()

  def setDefaultFont(self, font: QtGui.QFont):
    self.ui.fontCombo.setCurrentFont(font)

    # Find closest point size for font combo
    closestPointSize = self.findClosestFontSize(font.pointSize())

    index = self.ui.fontSizeCombo.findText(f'{closestPointSize}')

    self.ui.fontSizeCombo.setCurrentIndex(index if index != -1 else 0)

  def findClosestFontSize(self, fontSize: int) -> int:
    currentFontSize = -1

    index = self.ui.fontSizeCombo.findText(f'{fontSize}')

    if index != -1:
      return fontSize

    # The given font size was not found, so search for the first size that is larger
    # than the given font size
    numFonts = self.ui.fontCombo.count()

    for i in range(numFonts):
      fontSizeStr = self.ui.fontSizeCombo.itemText(i)

      if len(fontSizeStr) == 0:
        continue

      currentFontSize = int(fontSizeStr)

      if currentFontSize >= fontSize:
        return currentFontSize

    # fontSize is larger than any font in the combo box.  In this case,
    # return the largest font in the combo box.
    return currentFontSize

  def onAccept(self):
    # Application prefs
    self.preferences.onStartupLoad = kStartupLoadPreviousNoteBook if self.ui.loadPreviousNotebookRadio.isChecked() \
                                                                  else kStartupEmptyWorkspace

    # Text Editor
    font = self.getDefaultFont()
    fontSize = int(self.ui.fontSizeCombo.currentText())
    self.preferences.editorDefaultFontFamily = font.family()
    self.preferences.editorDefaultFontSize = fontSize
