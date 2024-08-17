from PySide6 import QtCore, QtWidgets, QtGui
import re

from text_table_defs import kDefaultColumnWidth

class TextTable:
  def __init__(self) -> None:
    self.textTable: QtGui.QTextTable | None = None

  @staticmethod
  def isCursorInTable(cursor: QtGui.QTextCursor) -> bool:
    """Indicates whether the given cursor is currently within a table.

    Args:
        cursor (QtGui.QTextCursor): _description_

    Returns:
        bool: True if the cursor is within a table
    """
    return cursor.currentTable() is not None

  @staticmethod
  def fromCursor(cursor: QtGui.QTextCursor) -> 'TextTable | None':
    """Returns a CTextTable object corresponding to the QTextTable located at the
       cursor position.  Returns None if the cursor is not within a QTextTable.

    Args:
        cursor (QtGui.QTextCursor): _description_

    Returns:
        TextTable: TextTable containing the cursor
    """
    if TextTable.isCursorInTable(cursor):
      table = TextTable()
      table.textTable = cursor.currentTable()
      return table
    else:
      return None

  @staticmethod
  def currentTableRow(cursor: QtGui.QTextCursor) -> int:
    """Returns the row of the table that the cursor is currently occupying

    Args:
        cursor (QtGui.QTextCursor): _description_

    Returns:
        int: Row number
    """
    table = cursor.currentTable()

    if table is not None:
      curCell = table.cellAt(cursor)
      return curCell.row()
    else:
      return -1

  @staticmethod
  def insertRow(cursor: QtGui.QTextCursor, above: bool):
    """Inserts a row in the table containing the cursor.

    Args:
        cursor (QtGui.QTextCursor): _description_
        above (bool): True for above, False for below
    """
    table = cursor.currentTable()

    if table is not None:
      curCell = table.cellAt(cursor)

      if above:
        table.insertRows(curCell.row(), 1)
      else:
        # Below
        if curCell.row() == table.rows() - 1:
          # This is the last row.  Use appendRows to add a row at the end.
          table.appendRows(1)
        else:
          table.insertRows(curCell.row() + 1, 1)

  @staticmethod
  def deleteRowAtCursor(cursor: QtGui.QTextCursor):
    """Deletes the row in which the cursor currently resides.

    Args:
        cursor (QtGui.QTextCursor): _description_
    """
    table = cursor.currentTable()

    if table is not None:
      table.removeRows(table.cellAt(cursor).row(), 1)

  @staticmethod
  def copyRow(cursor: QtGui.QTextCursor, sourceRow: int):
    """Copies source row to the row containing the cursor.  Table's size remains the same.

    Args:
        cursor (QtGui.QTextCursor): _description_
        sourceRow (int): _description_
    """
    table = cursor.currentTable()

    if table is not None:
      destRow = table.cellAt(cursor).row()

      # Copy the contents of each column from sourceRow to this row
      numColumns = table.columns()

      for columnNum in range(numColumns):
        TextTable.copyCell(table, sourceRow, columnNum, destRow, columnNum)

  @staticmethod
  def copyCell(table: QtGui.QTextTable, sourceRow: int, sourceColumn: int, destRow: int, destColumn: int):
    """Copies a cell.

    Args:
        table (QtGui.QTextTable): _description_
        sourceRow (int): _description_
        sourceColumn (int): _description_
        destRow (int): _description_
        destColumn (int): _description_
    """
    sourceCell = table.cellAt(sourceRow, sourceColumn)
    destCell = table.cellAt(destRow, destColumn)

    # Select the contents of the source cell
    sourceCellStart = sourceCell.firstCursorPosition()
    sourceCellEnd = sourceCell.lastCursorPosition()

    sourceCellStart.setPosition(sourceCellEnd.position(), QtGui.QTextCursor.MoveMode.KeepAnchor)

    # The source cell should now be selected
    textFragment = sourceCellStart.selection()

    # Copy to destination
    destCellStart = destCell.firstCursorPosition()
    destCellStart.insertFragment(textFragment)

  @staticmethod
  def selectionToTable(selectionCursor: QtGui.QTextCursor):
    """Converts a selection to a QTextTable.

    Args:
        cursor (QtGui.QTextCursor): _description_
    """
    # It would be nice to be able to preserve the formatting, but QTextCursor::toHtml()
    # returns a rather involved block of HTML, which would be tricky to parse, so we'll
    # just work with the plain text.
    allText = selectionCursor.selectedText()

    # Determine the column delimiter.  The default will be a space, but it might be a
    # tab character.  If a tab character is found in the selected text, we'll assume
    # the fields are tab-delimited.
    columnDelimiter = '\\s'

    if '\\t' in allText:
      columnDelimiter = '\\t'

    allText.replace('\u8233', '\\n')    # Replace Unicode paragraph separators with \n
    lines = allText.split('\\n')

    numRows = 0
    numColumns = 0

    # Determine the number of rows and columns in the table
    for line in lines:
      tempLine = ''
      if columnDelimiter == '\\s':
        tempLine = line.strip()   # Remove whitespace at the beginning and end of line
        tempLine = re.sub(' +', ' ', tempLine)    # Replace multiple spaces with a single space
      else:
        tempLine = line.strip()

      if len(tempLine) > 0:
        numRows += 1
        lineElements = tempLine.split(columnDelimiter)
        numColumns = max(numColumns, len(lineElements))

    # Remove the text from the document
    selectionCursor.removeSelectedText()

    # Insert the table
    table = selectionCursor.insertTable(numRows, numColumns)

    # Add the text
    curRow = 0
    for line in lines:
      tempLine = ''
      if columnDelimiter == '\\s':
        tempLine = line.strip()   # Remove whitespace at the beginning and end of line
        tempLine = re.sub(' +', ' ', tempLine)    # Replace multiple spaces with a single space
      else:
        tempLine = line.strip()

      if len(tempLine) > 0:
        curCol = 0
        lineElements = tempLine.split(columnDelimiter)

        for cellText in lineElements:
          cell = table.cellAt(curRow, curCol)
          cursor = cell.firstCursorPosition()
          cursor.insertText(cellText)

        curCol += 1

    # Set some formatting parameters
    tableFormat = table.format()
    columnConstraints = []

    for i in range(numColumns):
      textLength = QtGui.QTextLength(QtGui.QTextLength.Type.FixedLength, kDefaultColumnWidth)
      columnConstraints.append(textLength)

    tableFormat.setColumnWidthConstraints(columnConstraints)
    tableFormat.setBackground(QtGui.QBrush('white'))
    table.setFormat(tableFormat)

  @staticmethod
  def createAtCursor(cursor: QtGui.QTextCursor, rows: int, columns: int) -> 'TextTable':
    """Creates a new text table and returns it

    Args:
        cursor (QtGui.QTextCursor): _description_
        rows (int): _description_
        columns (int): _description_

    Returns:
        TextTable: _description_
    """
    textTable = TextTable()
    textTable.textTable = cursor.insertTable(rows, columns)
    return textTable

  def rows(self) -> int:
    if self.textTable is not None:
      return self.textTable.rows()
    else:
      return -1

  def columns(self) -> int:
    if self.textTable is not None:
      return self.textTable.columns()
    else:
      return -1

  def resize(self, rows: int, columns: int):
    if self.textTable is not None:
      self.textTable.resize(rows, columns)

  def textTableFormat(self) -> QtGui.QTextTableFormat:
    if self.textTable is not None:
      return self.textTable.format()
    else:
      return QtGui.QTextTableFormat()

  def textFrameFormat(self) -> QtGui.QTextFrameFormat:
    if self.textTable is not None:
      return self.textTable.frameFormat()
    else:
      return QtGui.QTextFrameFormat()

  def background(self) -> QtGui.QBrush:
    if self.textTable is not None:
      tableFormat = self.textTable.format()
      return tableFormat.background()
    else:
      return QtGui.QBrush()

  def setBackground(self, brush: QtGui.QBrush):
    if self.textTable is not None:
      ttFormat = self.textTable.format()
      ttFormat.setBackground(brush)
      self.textTable.setFormat(ttFormat)

  def setColumnConstraints(self, columnConstraints: list[QtGui.QTextLength]):
    if self.textTable is not None:
      ttFormat = self.textTable.format()
      ttFormat.setColumnWidthConstraints(columnConstraints)
      self.textTable.setFormat(ttFormat)