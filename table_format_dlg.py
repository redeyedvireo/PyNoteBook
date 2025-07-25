from PySide6 import QtCore, QtWidgets, QtGui

from column_type_combo_box import ColumnTypeComboBox
from text_table import TextTable
from ui_table_format_dlg import Ui_TableFormatDlg

from text_table_defs import kDefaultColumnWidth

kTableColumns = 2
kWidthColumn =  0
kTypeColumn =   1

kDefaultNumRows = 2
kDefaultNumColumns = 2

class TableFormatDialog(QtWidgets.QDialog):
  def __init__(self, textTable: TextTable | None, parent):
    super(TableFormatDialog, self).__init__(parent)

    self.ui = Ui_TableFormatDlg()
    self.ui.setupUi(self)

    self.textTable = textTable

    self.ui.backgroundColorButton.setColorSwatchFillsButton(True)
    self.ui.backgroundColorButton.hasColor = False

    # Set background color
    if self.textTable is not None:
      self.setBackgroundColor(self.textTable.background())
    else:
      self.setBackgroundColor(None)

    self.setUpTable()

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
      columnType = self.getColumnType(i)
      textLength = QtGui.QTextLength(columnType, colWidth)

      columnConstraints.append(textLength)

    return columnConstraints

  @QtCore.Slot(int)
  def on_columnsSpin_valueChanged(self, i: int):
    self.adjustTableColumns(i)

  def setUpTable(self):
    self.populateColumns()

    if self.textTable is not None:
      self.ui.rowsSpin.setValue(self.textTable.rows())
      self.ui.columnsSpin.setValue(self.textTable.columns())
    else:
      # No table exists; set to default values
      self.ui.rowsSpin.setValue(kDefaultNumRows)
      self.ui.columnsSpin.setValue(kDefaultNumColumns)

  def populateColumns(self):
    columnWidths: list[QtGui.QTextLength] = []
    numColumns = kDefaultNumColumns

    if self.textTable is None:
      # No table exists; a new table will be created.  By default, make columns fixed width.
      for _ in range(numColumns):
        textLength = QtGui.QTextLength(QtGui.QTextLength.Type.FixedLength, kDefaultColumnWidth)
        columnWidths.append(textLength)
    else:
      numColumns = self.textTable.columns()
      tableFormat = self.textTable.textTableFormat()
      columnWidths = tableFormat.columnWidthConstraints()

    self.ui.tableWidget.setColumnCount(kTableColumns)

    # Set the number of rows in the table widget to the number of columns in the text table.
    # There is one table widget row per column in the text table.
    self.ui.tableWidget.setRowCount(numColumns)

    # Set Header labels
    self.ui.tableWidget.setHorizontalHeaderLabels(['Width', 'Type'])

    # Set the column widths and types in the table widget to match the text table.
    for column, textLength in enumerate(columnWidths):
      self.setTableValue(column, kWidthColumn, textLength.rawValue())
      self.setColumnType(column, textLength.type())

    horizHeader = self.ui.tableWidget.horizontalHeader()
    horizHeader.setStretchLastSection(True)

  def adjustTableColumns(self, numRows: int):
    """Adjusts the number of columns in the text table.
       Recall that each column in the text table corresponds to a row in the table widget.

    Args:
        numRows (int): Number of rows to set in the table widget.
    """
    currentNumRows = self.ui.tableWidget.rowCount()

    if numRows == currentNumRows:
      return    # Nothing to do

    self.ui.tableWidget.setRowCount(numRows)

    if numRows > currentNumRows:
      # Add rows and set table column constraints to default values

      for row in range(numRows):
        if row >= currentNumRows:
          # New row; set type to Fixed
          self.setTableValue(row, kWidthColumn, kDefaultColumnWidth)

          comboBox  = self.createColumnTypeComboBox()
          self.ui.tableWidget.setCellWidget(row, kTypeColumn, comboBox)

  def createColumnTypeComboBox(self):
    comboBox = ColumnTypeComboBox(self.ui.tableWidget)
    return comboBox

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

  def setColumnType(self, row: int, columnType: QtGui.QTextLength.Type):
    """ Sets the column type for the specified row and column. """
    comboBox = self.ui.tableWidget.cellWidget(row, kTypeColumn)

    if comboBox is None:
      # Create a new combo box if it doesn't exist
      comboBox = self.createColumnTypeComboBox()
      comboBox.type = columnType  # Set the type using the property setter
      self.ui.tableWidget.setCellWidget(row, kTypeColumn, comboBox)

    elif isinstance(comboBox, ColumnTypeComboBox):
      comboBox.type = columnType  # Set the type using the property setter

  def getColumnType(self, row: int) -> QtGui.QTextLength.Type:
    """ Returns the column type for the specified row. """
    comboBox = self.ui.tableWidget.cellWidget(row, kTypeColumn)

    if comboBox is None:
      return QtGui.QTextLength.Type.FixedLength  # Default to Fixed if no combo box exists

    if isinstance(comboBox, ColumnTypeComboBox):
      return comboBox.type  # Use the property getter

    return QtGui.QTextLength.Type.FixedLength  # Default to Fixed if not a ColumnTypeComboBox
