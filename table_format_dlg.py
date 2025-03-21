from PySide6 import QtCore, QtWidgets, QtGui

from text_table import TextTable
from ui_table_format_dlg import Ui_TableFormatDlg

from text_table_defs import kDefaultColumnWidth

kTableColumns = 2
kWidthColumn =  0
kTypeColumn =   1

class TableFormatDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    super(TableFormatDialog, self).__init__(parent)

    self.ui = Ui_TableFormatDlg()
    self.ui.setupUi(self)

    self.textTable = None

    self.ui.backgroundColorButton.setColorSwatchFillsButton(True)
    self.ui.backgroundColorButton.hasColor = False

  def rows(self) -> int:
    return self.ui.rowsSpin.value()

  def columns(self) -> int:
    return self.ui.columnsSpin.value()

  def backgroundColor(self):
    return self.ui.backgroundColorButton.color

  def backgroundHasColor(self) -> bool:
    return self.ui.backgroundColorButton.hasColor

  def setBackgroundColor(self, color: QtGui.QColor | None):
    self.ui.backgroundColorButton.color = color

  def getColumnConstraints(self) -> list[QtGui.QTextLength]:
    columnConstraints = []
    numColumns = self.ui.tableWidget.rowCount()

    for i in range(numColumns):
      colWidth = self.getTableValue(i, 0, kDefaultColumnWidth)
      constraintType = self.getTableStringValue(i, 1, 'Fixed')

      match constraintType:
        case 'Fixed':
          textLength = QtGui.QTextLength(QtGui.QTextLength.Type.FixedLength, colWidth)

        case 'Percentage':
          textLength = QtGui.QTextLength(QtGui.QTextLength.Type.PercentageLength, colWidth)

        case 'Variable':
          textLength = QtGui.QTextLength(QtGui.QTextLength.Type.VariableLength, colWidth)

        case _:  # Default to Fixed
          textLength = QtGui.QTextLength(QtGui.QTextLength.Type.FixedLength, colWidth)

      columnConstraints.append(textLength)

    return columnConstraints

  @QtCore.Slot(int)
  def on_columnsSpin_valueChanged(self, i: int):
    self.adjustTableRows(i)

  def populateColumns(self):
    colWidths = []

    if self.textTable is None:
      # No table exists; a new table will be created.  Create a default table format.
      numColumns = 1
      textLength = QtGui.QTextLength(QtGui.QTextLength.Type.FixedLength, kDefaultColumnWidth)
      colWidths.append(textLength)
    else:
      numColumns = self.textTable.columns()
      tableFormat = self.textTable.textTableFormat()
      colWidths = tableFormat.columnWidthConstraints()

    self.ui.tableWidget.setColumnCount(kTableColumns)
    self.ui.tableWidget.setRowCount(numColumns)

    # Set Header labels
    self.ui.tableWidget.setHorizontalHeaderLabels(['Width', 'Type'])

    for col in range(numColumns):
      # Get column width for column
      textLength = colWidths[col]
      self.setTableValue(col, kWidthColumn, textLength.rawValue())

      # For now, make all columns "fixed"
      match textLength.type():
        case QtGui.QTextLength.Type.FixedLength:
          self.setTableText(col, kTypeColumn, 'Fixed')

        case QtGui.QTextLength.Type.PercentageLength:
          self.setTableText(col, kTypeColumn, 'Percentage')

        case QtGui.QTextLength.Type.VariableLength:
          self.setTableText(col, kTypeColumn, 'Variable')

        case _:  # Default to Fixed
          self.setTableText(col, kTypeColumn, 'Fixed')

    horizHeader = self.ui.tableWidget.horizontalHeader()
    horizHeader.setStretchLastSection(True)


  def adjustTableRows(self, numRows: int):
    currentNumRows = self.ui.tableWidget.rowCount()

    if numRows == currentNumRows:
      return    # Nothing to do

    self.ui.tableWidget.setRowCount(numRows)

    if numRows > currentNumRows:
      # Add rows and set table column constraints to default values
      rowsToAdd = numRows - currentNumRows

      for row in range(numRows):
        if row >= currentNumRows:
          # New row; set type to Fixed
          self.setTableText(row, kTypeColumn, 'Fixed')
          self.setTableValue(row, kWidthColumn, kDefaultColumnWidth)

  def setTable(self, textTable: TextTable | None):
    self.textTable = textTable

    self.populateColumns()

    if self.textTable is not None:
      self.ui.rowsSpin.setValue(self.textTable.rows())
      self.ui.columnsSpin.setValue(self.textTable.columns())


  def getTableValue(self, row: int, col: int, defaultValue: float) -> float:
    retVal = defaultValue
    item = self.ui.tableWidget.item(row, col)

    if item is not None:
      cellText = item.text()
      retVal = float(cellText)

    return retVal

  def getTableStringValue(self, row: int, col: int, defaultValue: str) -> str:
    retVal = defaultValue
    item = self.ui.tableWidget.item(row, col)

    if item is not None:
      retVal = item.text()

    return retVal

  def setTableValue(self, row: int, col: int, value: float):
    self.setTableText(row, col, str(value))

  def setTableText(self, row: int, col: int, text: str):
    item = self.ui.tableWidget.item(row, col)

    if item is None:
      # Need to create a new item for this position
      item = QtWidgets.QTableWidgetItem()
      self.ui.tableWidget.setItem(row, col, item)

    item.setText(text)

