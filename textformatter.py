from PySide6 import QtCore, QtGui, QtWidgets

class TextFormatter:
  def __init__(self, textEdit: QtWidgets.QTextEdit) -> None:
    self.textEdit = textEdit
    self.selectionCursor = self.textEdit.textCursor()
    self.selectionFormat = self.selectionCursor.charFormat()
    self.blockFormat = self.selectionCursor.blockFormat()
    self.tempCharFormat = QtGui.QTextCharFormat()

  def mergeCharFormatAndfinalize(self):
    self.selectionCursor.mergeCharFormat(self.tempCharFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def setBlockFormatAndFinalize(self):
    self.selectionCursor.setBlockFormat(self.blockFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def setCharFormatAndFinalize(self):
    self.selectionCursor.setCharFormat(self.selectionFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def _toggleStrikethrough(self):
    self.tempCharFormat.setFontStrikeOut(not self.selectionFormat.fontStrikeOut())
    self.mergeCharFormatAndfinalize()

  def _toggleUnderline(self):
    self.tempCharFormat.setFontUnderline(not self.selectionFormat.fontUnderline())
    self.mergeCharFormatAndfinalize()

  def _toggleItalic(self):
    self.tempCharFormat.setFontItalic(not self.selectionFormat.fontItalic())
    self.mergeCharFormatAndfinalize()

  def _toggleBold(self):
    if self.selectionFormat.fontWeight() != QtGui.QFont.Weight.Bold:
      self.tempCharFormat.setFontWeight(QtGui.QFont.Weight.Bold)
    else:
      self.tempCharFormat.setFontWeight(QtGui.QFont.Weight.Normal)

    self.mergeCharFormatAndfinalize()

  def _leftAlign(self):
    self.blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    self.setBlockFormatAndFinalize()

  def _centerAlign(self):
    self.blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    self.setBlockFormatAndFinalize()

  def _rightAlign(self):
    self.blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    self.setBlockFormatAndFinalize()

  def _setTextColor(self, color: QtGui.QColor):
    self.tempCharFormat = QtGui.QTextCharFormat()
    self.tempCharFormat.setForeground(QtGui.QBrush(color))
    self.mergeCharFormatAndfinalize()

  def _noTextColor(self):
    # NOTE: This approach will cause all text in the selection to take on
    # all characteristics of the selectionFormat.  It has the effect of
    # removing formatting changes within the block.  Unfortunately,
    # mergeCharFormat does not work when clearing a property.
    self.selectionFormat.clearForeground()
    self.setCharFormatAndFinalize()

  def _setBackgroundColor(self, color: QtGui.QColor):
    self.tempCharFormat = QtGui.QTextCharFormat()
    self.tempCharFormat.setBackground(QtGui.QBrush(color))
    self.mergeCharFormatAndfinalize()

  def _noBackgroundColor(self):
    # NOTE: This approach will cause all text in the selection to take on
    # all characteristics of the selectionFormat.  It has the effect of
    # removing formatting changes within the block.  Unfortunately,
    # mergeCharFormat does not work when clearing a property.
    self.selectionFormat.clearBackground()
    self.setCharFormatAndFinalize()

  def _setFont(self, fontFamily: str):
    self.selectionFormat.setFontFamily(fontFamily)
    self.setCharFormatAndFinalize()

  def _setFontSize(self, fontSize: int):
    self.tempCharFormat.setFontPointSize(fontSize)
    self.mergeCharFormatAndfinalize()

  @staticmethod
  def toggleStrikethrough(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._toggleStrikethrough()

  @staticmethod
  def toggleUnderline(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._toggleUnderline()

  @staticmethod
  def toggleItalic(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._toggleItalic()

  @staticmethod
  def toggleBold(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._toggleBold()

  @staticmethod
  def leftAlign(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._leftAlign()

  @staticmethod
  def centerAlign(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._centerAlign()

  @staticmethod
  def rightAlign(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._rightAlign()

  @staticmethod
  def setTextColor(textEdit: QtWidgets.QTextEdit, color: QtGui.QColor):
    TextFormatter(textEdit)._setTextColor(color)

  @staticmethod
  def noTextColor(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._noTextColor()

  @staticmethod
  def setBackgroundColor(textEdit: QtWidgets.QTextEdit, color: QtGui.QColor):
    TextFormatter(textEdit)._setBackgroundColor(color)

  @staticmethod
  def noBackgroundColor(textEdit: QtWidgets.QTextEdit):
    TextFormatter(textEdit)._noBackgroundColor()

  @staticmethod
  def setFont(textEdit: QtWidgets.QTextEdit, fontFamily: str):
    TextFormatter(textEdit)._setFont(fontFamily)

  @staticmethod
  def setFontSize(textEdit: QtWidgets.QTextEdit, fontSize: int):
    TextFormatter(textEdit)._setFontSize(fontSize)

class TextInserter:
  def __init__(self, textEdit: QtWidgets.QTextEdit) -> None:
    self.textEdit = textEdit
    self.selectionCursor = self.textEdit.textCursor()

  def _insertBullet(self):
    newListFormat = QtGui.QTextListFormat()
    newListFormat.setIndent(1)
    newListFormat.setStyle(QtGui.QTextListFormat.Style.ListDisc)

    self.selectionCursor.createList(newListFormat)

  def _insertNumberList(self):
    newListFormat = QtGui.QTextListFormat()
    newListFormat.setIndent(1)
    newListFormat.setStyle(QtGui.QTextListFormat.Style.ListDecimal)

    self.selectionCursor.createList(newListFormat)

  def _setBulletStyle(self, bulletStyle: QtGui.QTextListFormat.Style):
    list = self.selectionCursor.currentList()

    if list is not None:
      listFormat = list.format()
      listFormat.setStyle(bulletStyle)
      list.setFormat(listFormat)

  @staticmethod
  def insertBullet(textEdit: QtWidgets.QTextEdit):
    TextInserter(textEdit)._insertBullet()

  @staticmethod
  def insertNumberList(textEdit: QtWidgets.QTextEdit):
    TextInserter(textEdit)._insertNumberList()

  @staticmethod
  def setBulletStyle(textEdit: QtWidgets.QTextEdit, bulletStyle: QtGui.QTextListFormat.Style):
    TextInserter(textEdit)._setBulletStyle(bulletStyle)
