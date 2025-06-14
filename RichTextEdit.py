from PySide6 import QtCore, QtGui, QtWidgets
import logging

from select_style_dlg import SelectStyleDialog
from switchboard import Switchboard
from table_format_dlg import TableFormatDialog
from style_manager import StyleManager
from text_table import TextTable
from utility import formatDateTime
from textformatter import TextFormatter, TextInserter
from database import Database

from ui_RichTextEdit import Ui_RichTextEditWidget

from notebook_types import ENTITY_ID

class RichTextEditWidget(QtWidgets.QWidget):
  editorTextChangedSignal = QtCore.Signal()

  def __init__(self):
    super(RichTextEditWidget, self).__init__()
    self.ui = Ui_RichTextEditWidget()
    self.ui.setupUi(self)

    self.styleManager = None
    self.bulletStyleMenu = QtWidgets.QMenu()
    self.numberStyleMenu = QtWidgets.QMenu()

    self.ui.textColorButton.color = QtGui.QColor('Black')

    # Disable style button and style shortcut buttons at first.  These will be enabled whenever there is a selection.
    self.onSelectionChanged()

    self.styleMenu = QtWidgets.QMenu()

    # Style shortcut menus
    self.styleShortCutMenus = []

    # Connect signals
    self.setConnections()

  def initialize(self, styleManager: StyleManager, messageLabel: QtWidgets.QLabel, database: Database, switchboard: Switchboard):
    self.styleManager = styleManager
    self.db = database
    self.messageLabel = messageLabel
    self.switchboard = switchboard
    self.ui.textEdit.initialize(self.styleManager, messageLabel, self.db)
    self.initStyleButton()
    self.initStyleShortcutButtons()
    self.populatePointSizesCombo()
    self.initBulletStyleButton()
    self.initNumberStyleButton()

    # Hide the search widgets to start
    self.ui.richTextEditSearchWidget.hide()

  def setConnections(self):
    self.ui.textEdit.selectionChanged.connect(self.onSelectionChanged)
    self.ui.textEdit.textChanged.connect(self.onTextChanged)
    self.ui.textEdit.cursorPositionChanged.connect(self.onCursorPositionChanged)
    self.ui.textEdit.CTE_TableFormat.connect(self.on_tableButton_clicked)
    self.ui.textEdit.CTE_GotoPage.connect(lambda pageId: self.switchboard.emitPageSelected(pageId))

  def populatePointSizesCombo(self):
    fontDatabase = QtGui.QFontDatabase()
    curFontFamily = self.ui.fontCombo.currentText()

    self.ui.sizeCombo.clear()
    fontSizeList = fontDatabase.pointSizes(curFontFamily)
    for curFontSize in fontSizeList:
      fontSizeString = f'{curFontSize}'
      self.ui.sizeCombo.addItem(fontSizeString)

  def initStyleButton(self):
    # TODO: Should add a way for the user to import/export the style settings.
    self.styleMenu.clear()

    # The action will have the style ID stored as its data item.
    if self.styleManager is not None:
      for style in self.styleManager.styles.items():
        styleName = style[1].strName
        styleId = style[0]

        action = self.styleMenu.addAction(styleName)
        action.setData(styleId)

      self.ui.styleButton.setMenu(self.styleMenu)

  def initStyleShortcutButtons(self):
    if self.styleManager is not None:
      self.styleShortCutMenus = [ QtWidgets.QMenu() for _ in range(self.styleManager.numShortcuts()) ]

      self.initStyleShortcutButon(self.ui.styleShortcut1, 1)
      self.initStyleShortcutButon(self.ui.styleShortcut2, 2)
      self.initStyleShortcutButon(self.ui.styleShortcut3, 3)
      self.initStyleShortcutButon(self.ui.styleShortcut4, 4)

      # Connect the style shortcut buttons to their respective slots
      self.ui.styleShortcut1.clicked.connect(lambda: self.on_styleShortcut_clicked(1))
      self.ui.styleShortcut2.clicked.connect(lambda: self.on_styleShortcut_clicked(2))
      self.ui.styleShortcut3.clicked.connect(lambda: self.on_styleShortcut_clicked(3))
      self.ui.styleShortcut4.clicked.connect(lambda: self.on_styleShortcut_clicked(4))

  def initStyleShortcutButon(self, styleButton: QtWidgets.QToolButton, styleNumber: int):
    styleButtonMenu = self.styleShortCutMenus[styleNumber - 1]
    styleButtonMenu.clear()
    styleButton.setMenu(styleButtonMenu)
    action = styleButtonMenu.addAction('Configure...')
    action.triggered.connect(lambda: self.configureStyleShortcut(styleButton, styleNumber))

  def initBulletStyleButton(self):
    self.bulletStyleMenu.clear()
    self.bulletStyleMenu.addAction('Solid circle', self.onSolidCircleTriggered)
    self.bulletStyleMenu.addAction('Hollow circle', self.onHollowCircleTriggered)
    self.bulletStyleMenu.addAction('Solid square', self.onSolidSquareTriggered)

    self.ui.bulletTableInsertButton.setMenu(self.bulletStyleMenu)

  def initNumberStyleButton(self):
    self.numberStyleMenu.clear()
    self.numberStyleMenu.addAction('Decimal numbers', self.onDecimalNumbersTriggered)
    self.numberStyleMenu.addAction('Lower-case Latin characters', self.onLowerCaseLatinCharactersTriggered)
    self.numberStyleMenu.addAction('Upper-case Latic characters', self.onUpperCaseLatinCharactersTriggered)
    self.numberStyleMenu.addAction('Lower-case Roman numerals', self.onLowerCaseRomanNumeralsTriggered)
    self.numberStyleMenu.addAction('Upper-case Roman numerals', self.onUpperCaseRomanNumeralsTriggered)

    self.ui.numberTableInsertButton.setMenu(self.numberStyleMenu)

  def clear(self):
    self.ui.textEdit.clear()

  def newDocument(self, fontFamily, fontSize):
    self.ui.textEdit.clear()
    self.setDocumentModified(False)

    # Set global font size
    self.setGlobalFont(fontFamily, fontSize)

  def toHtml(self):
    return self.ui.textEdit.document().toHtml()

  def isModified(self):
    doc = self.ui.textEdit.document()
    return doc.isModified()

  def enableEditing(self, enableFlag):
    self.ui.textEdit.setEnabled(enableFlag)
    self.setEnabled(enableFlag)

  def setDocumentModified(self, modified):
    doc = self.ui.textEdit.document()
    doc.setModified(modified)

  def setDocumentText(self, content: str) -> None:
    self.ui.textEdit.setHtml(content)

  def setPageContents(self, contents: str, imageNames: list[str], pageId: ENTITY_ID) -> None:
    self.ui.textEdit.clear()

    # Set default font
    self.setGlobalFont(self.switchboard.preferences.editorDefaultFontFamily, self.switchboard.preferences.editorDefaultFontSize)

    # Load images
    self.loadImagesIntoDocument(imageNames)

    self.ui.textEdit.setHtml(contents)      # The C++ version uses insertHtml()
    self.ui.textEdit.currentPageId = pageId
    self.setDocumentModified(False)

  def loadImagesIntoDocument(self, imageNames: list[str]):
    for imageName in imageNames:
      pixmap = self.db.getImage(imageName)

      if pixmap is not None:
        self.ui.textEdit.document().addResource(QtGui.QTextDocument.ResourceType.ImageResource, QtCore.QUrl(imageName), pixmap)

  def setGlobalFont(self, fontFamily, fontSize):
    selectionCursor = self.ui.textEdit.textCursor()

    if fontSize > 3 or len(fontFamily) > 0:
      tempCharFormat = QtGui.QTextCharFormat()

      # Select entire document
      selectionCursor.select(QtGui.QTextCursor.SelectionType.Document)
      selectionFormat = selectionCursor.charFormat()

      fontSizeToUse = self.findClosestSize(fontSize)

      tempCharFormat.setFontPointSize(fontSizeToUse)
      tempCharFormat.setFontFamily(fontFamily)
      selectionCursor.mergeCharFormat(tempCharFormat)

      self.ui.textEdit.setTextCursor(selectionCursor)

      tempFont = QtGui.QFont(fontFamily, fontSizeToUse)
      doc = self.ui.textEdit.document()

      doc.setDefaultFont(tempFont)

      self.updateControls()

  def findClosestSize(self, fontSize):
    index = self.ui.sizeCombo.findText(f'{fontSize}')
    maxFontSize = 0

    if index < 0:
      return fontSize

    for i in range(self.ui.fontCombo.count()):
      fontSizeStr = self.ui.sizeCombo.itemText(i)

      if len(fontSizeStr) > 0:
        curFontSize = int(fontSizeStr)
        maxFontSize = max(maxFontSize, curFontSize)

        if curFontSize >= fontSize:
          return curFontSize

    # fontSize is larger than any font in the combo box.  In this
    # case, return the largest font in the combo box
    return maxFontSize

  def updateControls(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    fontFamilies = selectionFormat.fontFamilies()     # Returns an array of strings (font families)

    if fontFamilies is None:
      # There is no selection, so use the default font families
      # This condition generally happens after pasting plain text into the document
      doc = self.ui.textEdit.document()
      font = doc.defaultFont()
      fontFamilies = font.families()

    if fontFamilies is not None:
      index = self.ui.fontCombo.findText(fontFamilies[0])
      if index != -1:
        self.ui.fontCombo.setCurrentIndex(index)
      else:
        logging.error(f'[RichTextEditWidget.updateControls] Font family "{fontFamilies[0]}" not found in font combo box.')
    else:
      logging.error('[RichTextEditWidget.updateControls] No font families found in selection format.')

    fontSize = selectionFormat.fontPointSize()

    if fontSize <= 0:
      # If the font size is 0, use the default font size
      # This typically happens after pasting plain text into the document
      doc = self.ui.textEdit.document()
      fontSize = doc.defaultFont().pointSize()

    fontSizeStr = f'{int(fontSize)}'
    index = self.ui.sizeCombo.findText(fontSizeStr)
    if index != -1:
      self.ui.sizeCombo.setCurrentIndex(index)

    self.ui.boldButton.setChecked(selectionFormat.fontWeight() == QtGui.QFont.Weight.Bold)
    self.ui.italicButton.setChecked(selectionFormat.fontItalic())
    self.ui.underlineButton.setChecked(selectionFormat.fontUnderline())

    curBlockFormat = selectionCursor.blockFormat()
    alignmentVal = curBlockFormat.alignment()

    alignmentVal &= 0x0000000f    # Mask off other flags

    if alignmentVal == QtCore.Qt.AlignmentFlag.AlignLeft:
      self.ui.leftAlignButton.setChecked(True)
    elif alignmentVal == QtCore.Qt.AlignmentFlag.AlignHCenter:
      self.ui.centerAlignButton.setChecked(True)
    elif alignmentVal == QtCore.Qt.AlignmentFlag.AlignRight:
      self.ui.rightAlignButton.setChecked(True)
    else:
      self.ui.leftAlignButton.setChecked(True)

    textBrush = selectionFormat.foreground()
    if textBrush.isOpaque():
      self.ui.textColorButton.color = textBrush.color()
    else:
      self.ui.textColorButton.hasColor = False

    bgBrush = selectionFormat.background()
    if bgBrush.isOpaque():
      self.ui.textBackgroundButton.color = bgBrush.color()
    else:
      self.ui.textBackgroundButton.hasColor = False

  def getCursorAndSelectionFormat(self) -> tuple[QtGui.QTextCursor, QtGui.QTextCharFormat]:
    selectionCursor = self.ui.textEdit.textCursor()
    selectionFormat = selectionCursor.charFormat()
    return (selectionCursor, selectionFormat)


  # Slots

  @QtCore.Slot()
  def onTextChanged(self):
    self.editorTextChangedSignal.emit()

  @QtCore.Slot()
  def onCursorPositionChanged(self):
    self.updateControls()

  @QtCore.Slot(QtGui.QColor)
  def on_textColorButton_colorChangedSignal(self, color: QtGui.QColor):
    TextFormatter.setTextColor(self.ui.textEdit, color)

  @QtCore.Slot()
  def on_textColorButton_noColorSignal(self):
    TextFormatter.noTextColor(self.ui.textEdit)

  @QtCore.Slot(QtGui.QColor)
  def on_textBackgroundButton_colorChangedSignal(self, color: QtGui.QColor):
    TextFormatter.setBackgroundColor(self.ui.textEdit, color)

  @QtCore.Slot()
  def on_textBackgroundButton_noColorSignal(self):
    TextFormatter.noBackgroundColor(self.ui.textEdit)

  @QtCore.Slot()
  def onSelectionChanged(self):
    selectionCursor = self.ui.textEdit.textCursor()
    self.ui.styleButton.setEnabled(selectionCursor.hasSelection())

    # Note: we're keeping the style shortcut buttons enabled all the time, so that the user can configure them

  @QtCore.Slot(QtGui.QAction)
  def on_styleButton_triggered(self, action):
    """ A 'triggered' event happens when the user changes
        the current item in the style button. """
    styleId = action.data()
    self.applyStyleToSelection(styleId)

  @QtCore.Slot()
  def on_styleButton_clicked(self):
    defaultFontFamily = self.switchboard.preferences.editorDefaultFontFamily
    defaultFontSize = self.switchboard.preferences.editorDefaultFontSize

    if self.styleManager is not None:
      styleDlg = SelectStyleDialog(self, self.styleManager, defaultFontFamily, defaultFontSize)
      if styleDlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        styleId = styleDlg.getSelectedStyle()

        if styleId is not None:
          self.styleManager.applyStyle(self.ui.textEdit, styleId)
          self.updateControls()
          self.initStyleButton()
          self.switchboard.emitStylesChanged()

  def configureStyleShortcut(self, styleButton: QtWidgets.QToolButton, styleNumber: int):
    """ Configure the style shortcut button. """
    if self.styleManager is not None:
      defaultFontFamily = self.switchboard.preferences.editorDefaultFontFamily
      defaultFontSize = self.switchboard.preferences.editorDefaultFontSize

      styleDlg = SelectStyleDialog(self, self.styleManager, defaultFontFamily, defaultFontSize)

      if styleDlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        styleId = styleDlg.getSelectedStyle()
        if styleId is not None:
          self.styleManager.setShortcutStyleId(styleNumber - 1, styleId)    # Update the style shortcut with the selected style ID
          styleButton.setText(self.styleManager.styles[styleId].strName)
          styleButton.setToolTip(self.styleManager.styles[styleId].strName)

  def on_styleShortcut_clicked(self, styleNumber: int):
    selectionCursor = self.ui.textEdit.textCursor()
    if selectionCursor.hasSelection():
      if self.styleManager is not None:
        if not self.styleManager.styleShortcutIsValid(styleNumber - 1):
          QtWidgets.QMessageBox.warning(self, 'Style Button Not Configured', f'This style button is not configured.  Use the "Configure" option to set it up.')
        else:
          styleId = self.styleManager.getShortcutStyleId(styleNumber - 1)
          if styleId > -1:
            self.applyStyleToSelection(styleId)

  def applyStyleToSelection(self, styleId: int):
    """ Apply a style to the current selection. """
    if self.styleManager is not None:
      self.styleManager.applyStyle(self.ui.textEdit, styleId)
      self.updateControls()

  @QtCore.Slot()
  def on_boldButton_clicked(self):
    TextFormatter.toggleBold(self.ui.textEdit)

  @QtCore.Slot()
  def on_italicButton_clicked(self):
    TextFormatter.toggleItalic(self.ui.textEdit)

  @QtCore.Slot()
  def on_underlineButton_clicked(self):
    TextFormatter.toggleUnderline(self.ui.textEdit)

  @QtCore.Slot()
  def on_strikethroughButton_clicked(self):
    TextFormatter.toggleStrikethrough(self.ui.textEdit)

  @QtCore.Slot()
  def on_leftAlignButton_clicked(self):
    TextFormatter.leftAlign(self.ui.textEdit)

  @QtCore.Slot()
  def on_centerAlignButton_clicked(self):
    TextFormatter.centerAlign(self.ui.textEdit)

  @QtCore.Slot()
  def on_rightAlignButton_clicked(self):
    TextFormatter.rightAlign(self.ui.textEdit)

  @QtCore.Slot()
  def on_bulletTableInsertButton_clicked(self):
    TextInserter.insertBullet(self.ui.textEdit)

  @QtCore.Slot()
  def on_numberTableInsertButton_clicked(self):
    TextInserter.insertNumberList(self.ui.textEdit)

  @QtCore.Slot(int)
  def on_fontCombo_activated(self, index):
    self.populatePointSizesCombo()

    text = self.ui.fontCombo.itemText(index)
    TextFormatter.setFont(self.ui.textEdit, text)

  @QtCore.Slot(int)
  def on_sizeCombo_activated(self, index):
    text = self.ui.sizeCombo.itemText(index)
    newFontSize = int(text)

    TextFormatter.setFontSize(self.ui.textEdit, newFontSize)

  @QtCore.Slot()
  def on_tableButton_clicked(self):
    selectionCursor = self.ui.textEdit.textCursor()
    dlg = TableFormatDialog(self)
    textTable = None

    if TextTable.isCursorInTable(selectionCursor):
      textTable = TextTable.fromCursor(selectionCursor)
      if textTable is not None:
        tableFormat = textTable.textTableFormat()

        # Initialize dialog controls with data from the table
        frameFormat = textTable.textFrameFormat()
        tableWidth = frameFormat.width()

        # Background color
        dlg.setBackgroundColor(textTable.background())

    else:
      # The cursor is not in a table
      if selectionCursor.hasSelection():
        # Convert the selected text to a table
        TextTable.selectionToTable(selectionCursor)
        return

      else:
        # New Table
        dlg.setBackgroundColor(None)

    dlg.setTable(textTable)
    result = dlg.exec()

    if result == QtWidgets.QDialog.DialogCode.Accepted:
      rows = dlg.rows()
      columns = dlg.columns()
      bgColor = dlg.backgroundColor()

      if textTable is None:
        # The cursor is not within a table - insert a new one
        textTable = TextTable.createAtCursor(selectionCursor, rows, columns)
      else:
        # The cursor is within a table - allow the user to change its formatting
        if rows != textTable.rows() or columns != textTable.columns():
          textTable.resize(rows, columns)

      columnConstraints = dlg.getColumnConstraints()
      textTable.setColumnConstraints(columnConstraints)

      textTable.setBackground(bgColor)

      # DEBUG - dump the table
      # textTable.dump()


  @QtCore.Slot()
  def on_insertHLineButton_clicked(self):
    # Note: Inserting a horizontal line is apparently a very tricky operation.  It's not as simple as just
    # inserting a line and advancing the cursor position.  Here's an answer on Stack Overflow that alludes
    # to the complexity of performing this operation:
    # https://stackoverflow.com/questions/76710833/how-do-i-add-a-full-width-horizontal-line-in-qtextedit
    #
    # For now, an acceptable solution is the following.  The problem with this approach is that it inserts a
    # blank line before inserting the horizontal line, but at least it allows the cursor to be advanced afterwards.
    selectionCursor = self.ui.textEdit.textCursor()
    curBlockFormat = selectionCursor.blockFormat()      # Get current block format, before inserting the line
    selectionCursor.insertHtml('<hr />')

    # Advance cursor to after the line
    selectionCursor.insertBlock(curBlockFormat)         # Create a new block, with the previous block's format (ie, without the line)
    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onSolidCircleTriggered(self):
    TextInserter.setBulletStyle(self.ui.textEdit, QtGui.QTextListFormat.Style.ListDisc)

  @QtCore.Slot()
  def onHollowCircleTriggered(self):
    TextInserter.setBulletStyle(self.ui.textEdit, QtGui.QTextListFormat.Style.ListCircle)

  @QtCore.Slot()
  def onSolidSquareTriggered(self):
    TextInserter.setBulletStyle(self.ui.textEdit, QtGui.QTextListFormat.Style.ListSquare)

  @QtCore.Slot()
  def onDecimalNumbersTriggered(self):
    TextInserter.setBulletStyle(self.ui.textEdit, QtGui.QTextListFormat.Style.ListDecimal)

  @QtCore.Slot()
  def onLowerCaseLatinCharactersTriggered(self):
    TextInserter.setBulletStyle(self.ui.textEdit, QtGui.QTextListFormat.Style.ListLowerAlpha)

  @QtCore.Slot()
  def onUpperCaseLatinCharactersTriggered(self):
    TextInserter.setBulletStyle(self.ui.textEdit, QtGui.QTextListFormat.Style.ListUpperAlpha)

  @QtCore.Slot()
  def onLowerCaseRomanNumeralsTriggered(self):
    TextInserter.setBulletStyle(self.ui.textEdit, QtGui.QTextListFormat.Style.ListLowerRoman)

  @QtCore.Slot()
  def onUpperCaseRomanNumeralsTriggered(self):
    TextInserter.setBulletStyle(self.ui.textEdit, QtGui.QTextListFormat.Style.ListUpperRoman)

  @QtCore.Slot()
  def on_clearFormattingButton_clicked(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    currentBlockFormat = selectionCursor.blockFormat()

    # Ensure lines are single-spaced

    # There is a problem with Pyside's implementation of QTextBlockFormat.setLineHeight().  The second parameter
    # should be able ta take QtGui.QTextBlockFormat.LineHeightTypes.SingleHeight, but it throws an error about the
    # enum being incompatible with type int.  I determined from experimentation that the value of this enum is 0,
    # so we'll use 0 for the second parameter.
    # currentBlockFormat.setLineHeight(0.0, QtGui.QTextBlockFormat.LineHeightTypes.SingleHeight)  # This should work, but throws an exception
    currentBlockFormat.setLineHeight(0.0, 0)  # The second parameter is the value of QtGui.QTextBlockFormat.LineHeightTypes.SingleHeight
    currentBlockFormat.setTopMargin(0)
    currentBlockFormat.setBottomMargin(0)
    selectionCursor.setBlockFormat(currentBlockFormat)

    defaultFont = self.ui.textEdit.document().defaultFont()

    tempCharFormat = QtGui.QTextCharFormat()
    tempCharFormat.setFont(defaultFont)

    # Clear colors
    selectionFormat.clearBackground()
    selectionFormat.clearForeground()

    selectionCursor.setCharFormat(tempCharFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)
    self.updateControls()   # So the font and font size widgets show the correct thing after the font was changed here

  @QtCore.Slot()
  def on_indentLeftButton_clicked(self):
    self.ui.textEdit.reduceSelectionIndent()

  @QtCore.Slot()
  def on_indentRightButton_clicked(self):
    self.ui.textEdit.increaseSelectionIndent()

  @QtCore.Slot()
  def on_searchButton_clicked(self):
    self.ui.richTextEditSearchWidget.show()
    self.ui.searchEdit.setFocus(QtCore.Qt.FocusReason.MouseFocusReason)

  @QtCore.Slot()
  def on_searchHideButton_clicked(self):
    self.ui.richTextEditSearchWidget.hide()
    self.ui.textEdit.setFocus(QtCore.Qt.FocusReason.MouseFocusReason)

  @QtCore.Slot()
  def on_searchEdit_returnPressed(self):
    # Return was pressed while the search edit widget had the focus.  In this case, move the cursor
    # to the top of the document, and begin the search.
    # TODO: Is this the best approach?  It seems most editors start searching from the cursor's current position.
    self.ui.textEdit.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
    self.onSearchNext()

  @QtCore.Slot()
  def on_nextButton_clicked(self):
    self.onSearchNext()

  @QtCore.Slot()
  def on_prevButton_clicked(self):
    self.onSearchPrevious()

  def onSearchNext(self):
    self.search(True)

  def onSearchPrevious(self):
    self.search(False)

  def search(self, searchForward: bool):
    searchFlags = QtGui.QTextDocument.FindFlag() if searchForward else QtGui.QTextDocument.FindFlag.FindBackward
    wrapPosition = QtGui.QTextCursor.MoveOperation.Start if searchForward else QtGui.QTextCursor.MoveOperation.End

    if self.ui.wholeWordCheckBox.isChecked():
      searchFlags = searchFlags | QtGui.QTextDocument.FindFlag.FindWholeWords

    if self.ui.matchCaseCheckBox.isChecked():
      searchFlags = searchFlags | QtGui.QTextDocument.FindFlag.FindCaseSensitively

    searchText = self.ui.searchEdit.text()

    self.ui.textEdit.setFocus(QtCore.Qt.FocusReason.MouseFocusReason)
    if not self.ui.textEdit.find(searchText, searchFlags):   # Find forward, case-insensitively
      # If didn't find the text, wrap around to the beginning
      self.ui.textEdit.moveCursor(wrapPosition)
      self.ui.textEdit.find(searchText, searchFlags)