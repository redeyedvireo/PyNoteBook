from PySide6 import QtCore, QtGui, QtWidgets
import datetime

from select_style_dlg import SelectStyleDialog
from table_format_dlg import TableFormatDialog
from style_manager import StyleManager
from text_table import TextTable
from utility import formatDateTime
from textformatter import TextFormatter, TextInserter

from ui_RichTextEdit import Ui_RichTextEditWidget
class RichTextEditWidget(QtWidgets.QWidget):
  editorTextChangedSignal = QtCore.Signal()

  # def __init__(self, parent):
  def __init__(self):

    super(RichTextEditWidget, self).__init__()
    self.ui = Ui_RichTextEditWidget()
    self.ui.setupUi(self)

    self.styleManager = None
    self.bulletStyleMenu = QtWidgets.QMenu()
    self.numberStyleMenu = QtWidgets.QMenu()

    self.ui.textColorButton.setColor(QtGui.QColor('Black'))

    # Disable style button at first.  It will be enabled whenever there is a selection.
    self.ui.styleButton.setEnabled(False)

    self.styleMenu = QtWidgets.QMenu()

    # Connect signals
    self.setConnections()

  def initialize(self, styleManager: StyleManager):
    self.styleManager = styleManager
    self.initStyleButton()
    self.populatePointSizesCombo()
    self.initBulletStyleButton()
    self.initNumberStyleButton()

  def setConnections(self):
    self.ui.textEdit.selectionChanged.connect(self.onSelectionChanged)
    self.ui.textEdit.textChanged.connect(self.onTextChanged)
    self.ui.textEdit.cursorPositionChanged.connect(self.onCursorPositionChanged)

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

  def setPageContents(self, contents: str, imageNames: list[str]) -> None:
    self.ui.textEdit.clear()

    # TODO: Load images

    self.ui.textEdit.setHtml(contents)      # The C++ version uses insertHtml()

    self.setDocumentModified(False)

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

      tempFont = QtGui.QFont(fontFamily, fontSize)
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

        if curFontSize > fontSize:
          return curFontSize

    # fontSize is larger than any font in the combo box.  In this
    # case, return the largest font in the combo box
    return maxFontSize

  def updateControls(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    fontFamilies = selectionFormat.fontFamilies()     # Returns an array of strings (font families)
    if fontFamilies is not None:
      index = self.ui.fontCombo.findText(fontFamilies[0])
      if index != -1:
        self.ui.fontCombo.setCurrentIndex(index)

    fontSize = selectionFormat.fontPointSize()
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
      self.ui.textColorButton.setColor(textBrush.color())
    else:
      self.ui.textColorButton.setNoColor()

    bgBrush = selectionFormat.background()
    if bgBrush.isOpaque():
      self.ui.textBackgroundButton.setColor(bgBrush.color())
    else:
      self.ui.textBackgroundButton.setNoColor()

  def getCursorAndSelectionFormat(self) -> tuple[QtGui.QTextCursor, QtGui.QTextCharFormat]:
    selectionCursor = self.ui.textEdit.textCursor()
    selectionFormat = selectionCursor.charFormat()
    return (selectionCursor, selectionFormat)

  def addAddendum(self):
    textCursor = self.ui.textEdit.textCursor()

    textCursor.movePosition(QtGui.QTextCursor.MoveOperation.End, QtGui.QTextCursor.MoveMode.MoveAnchor)

    self.ui.textEdit.insertHtml(f'<br><hr />Addendum {formatDateTime(datetime.datetime.now())}<br>')


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

  @QtCore.Slot(QtGui.QAction)
  def on_styleButton_triggered(self, action):
    """ A 'triggered' event happens when the user changes
        the current item in the style button. """
    styleId = action.data()
    if self.styleManager:
      self.styleManager.applyStyle(self.ui.textEdit, styleId)

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

        # Header color
        bgBrush = textTable.background()

        dlg.setBackgroundColor(bgBrush.color())

    else:
      # The cursor is not in a table
      if selectionCursor.hasSelection():
        # Convert the selected text to a table
        TextTable.selectionToTable(selectionCursor)
        return

      else:
        # New Table
        dlg.setBackgroundColor(QtGui.QColor('white'))

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
      textTable.setBackground(QtGui.QBrush(bgColor))

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
  def on_styleButton_clicked(self):
    if self.styleManager is not None:
      styleDlg = SelectStyleDialog(self, self.styleManager)
      if styleDlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        styleId = styleDlg.getSelectedStyle()

        if styleId is not None:
          self.styleManager.applyStyle(self.ui.textEdit, styleId)
          self.initStyleButton()

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
