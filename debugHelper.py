from PySide6 import QtCore, QtWidgets, QtGui
import logging

def dumpTextTable(textTable: QtGui.QTextTable):
  textTableFormat = textTable.format()
  textFrameFormat = textTable.frameFormat()

  dumpTextTableFormat(textTableFormat)
  dumpFrameFormat(textFrameFormat)

  logging.debug(f'Text Table:')
  logging.debug(f'  Columns: {textTable.columns()}')
  logging.debug(f'  Rows: {textTable.rows()}')
  for i in range(textTable.rows()):
    logging.debug(f'Row {i}:')
    for j in range(textTable.columns()):
      cell = textTable.cellAt(i, j)
      logging.debug(f'  Column {j}:')
      dumpTableCell(cell)

def dumpTextTableFormat(textTableFormat: QtGui.QTextTableFormat):
  logging.debug(f'Text Table Format:')
  logging.debug(f'  Header row count: {textTableFormat.headerRowCount()}')
  logging.debug(f'  Border collapse: {textTableFormat.borderCollapse()}')
  logging.debug(f'  Cell spacing: {textTableFormat.cellSpacing()}')
  logging.debug(f'  Cell padding: {textTableFormat.cellPadding()}')
  logging.debug(f'  Is table cell format: {textTableFormat.isTableCellFormat()}')
  logging.debug(f'  Is format valid: {textTableFormat.isValid()}')
  logging.debug(f'  Background:{dumpBrush(textTableFormat.background())}')
  logging.debug(f'  Foreground:{dumpBrush(textTableFormat.foreground())}')
  logging.debug(f'  Column width constraints: {textTableFormat.columnWidthConstraints()}')
  logging.debug(f'  Width: {textTableFormat.width()}')

def dumpTextFormat(textFormat: QtGui.QTextFormat):
  logging.debug(f'Text format:')
  logging.debug(f'  Background: {dumpBrush(textFormat.background())}')
  logging.debug(f'  Foreground: {dumpBrush(textFormat.foreground())}')

def dumpFrameFormat(frameFormat: QtGui.QTextFrameFormat):
  logging.debug(f'Frame format:')
  logging.debug(f'  Border thickness: {frameFormat.border()}')
  logging.debug(f'  Border brush: {dumpBrush(frameFormat.borderBrush())}')
  logging.debug(f'  Border style: {frameFormat.borderStyle()}')
  logging.debug(f'  Frame height: {frameFormat.height()}')
  logging.debug(f'  Frame width: {frameFormat.width()}')
  logging.debug(f'  Frame margin: {frameFormat.margin()}')
  logging.debug(f'  Frame padding: {frameFormat.padding()}')
  logging.debug(f'  Foreground: {frameFormat.foreground()}')
  logging.debug(f'  Background: {frameFormat.background()}')

def dumpTextBlockFormat(blockFormat: QtGui.QTextBlockFormat):
  logging.debug(f'Text block format:')
  logging.debug(f'  Bottom margin: {blockFormat.bottomMargin()}')
  logging.debug(f'  Top margin: {blockFormat.topMargin()}')
  logging.debug(f'  Left margin: {blockFormat.leftMargin()}')
  logging.debug(f'  Right margin: {blockFormat.rightMargin()}')
  logging.debug(f'  Line height: {blockFormat.lineHeight()}')
  logging.debug(f'  Line height type: {blockFormat.lineHeightType()}')
  logging.debug(f'  Text indent: {blockFormat.textIndent()}')

def dumpBrush(brush: QtGui.QBrush):
  brushDump = f'Brush: Color: {brush.color()}, Style: {brush.style()}'
  return brushDump

def dumpTableCell(tableCell: QtGui.QTextTableCell):
  cellFormat = tableCell.format()
  logging.debug(f'    Background: {dumpBrush(cellFormat.background())}')
  logging.debug(f'    Foreground: {dumpBrush(cellFormat.foreground())}')

  iterator = tableCell.begin()
  while iterator != tableCell.end():
    frame = iterator.currentFrame()

    # I think the iterator either points to a frame or a block, but not both
    if frame is not None:
      currentIteratorFormat = frame.format()
      logging.debug(f'  {dumpTextFormat(currentIteratorFormat)}')
    else:
      currentIteratorFormat = iterator.currentBlock().blockFormat()
      dumpTextBlockFormat(currentIteratorFormat)

    iterator += 1

