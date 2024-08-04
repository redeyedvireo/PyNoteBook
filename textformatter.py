from PySide6 import QtCore, QtGui, QtWidgets

class TextFormatter:
  def __init__(self, textEdit: QtWidgets.QTextEdit) -> None:
    self.textEdit = textEdit
    self.selectionCursor = self.textEdit.textCursor()
    self.selectionFormat = self.selectionCursor.charFormat()
    self.blockFormat = self.selectionCursor.blockFormat()
    self.tempCharFormat = QtGui.QTextCharFormat()

  def finalize(self):
    self.textEdit.setTextCursor(self.selectionCursor)

  def _toggleStrikethrough(self):
    self.tempCharFormat.setFontStrikeOut(not self.selectionFormat.fontStrikeOut())
    self.selectionCursor.mergeCharFormat(self.tempCharFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def _toggleUnderline(self):
    self.tempCharFormat.setFontUnderline(not self.selectionFormat.fontUnderline())
    self.selectionCursor.mergeCharFormat(self.tempCharFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def _toggleItalic(self):
    self.tempCharFormat.setFontItalic(not self.selectionFormat.fontItalic())
    self.selectionCursor.mergeCharFormat(self.tempCharFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def _toggleBold(self):
    if self.selectionFormat.fontWeight() != QtGui.QFont.Weight.Bold:
      self.tempCharFormat.setFontWeight(QtGui.QFont.Weight.Bold)
    else:
      self.tempCharFormat.setFontWeight(QtGui.QFont.Weight.Normal)
    self.selectionCursor.mergeCharFormat(self.tempCharFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def _leftAlign(self):
    self.blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    self.selectionCursor.setBlockFormat(self.blockFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def _centerAlign(self):
    self.blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    self.selectionCursor.setBlockFormat(self.blockFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

  def _rightAlign(self):
    self.blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    self.selectionCursor.setBlockFormat(self.blockFormat)
    self.textEdit.setTextCursor(self.selectionCursor)

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

  @staticmethod
  def insertBullet(textEdit: QtWidgets.QTextEdit):
    TextInserter(textEdit)._insertBullet()

  @staticmethod
  def insertNumberList(textEdit: QtWidgets.QTextEdit):
    TextInserter(textEdit)._insertNumberList()
