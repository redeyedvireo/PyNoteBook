from PySide6 import QtCore, QtWidgets, QtGui
import logging

def debugOutput(message: str, indent = 0):
  logging.debug(f'{" " * indent}{message}')

def dumpTextTable(textTable: QtGui.QTextTable, indent = 0):
  textTableFormat = textTable.format()
  textFrameFormat = textTable.frameFormat()

  dumpTextTableFormat(textTableFormat)
  dumpFrameFormat(textFrameFormat)

  debugOutput(f'Text Table:', indent + 2)
  debugOutput(f'Columns: {textTable.columns()}', indent + 4)
  debugOutput(f'Rows: {textTable.rows()}', indent + 4)

  for i in range(textTable.rows()):
    debugOutput(f'Row {i}:', indent + 4)
    for j in range(textTable.columns()):
      cell = textTable.cellAt(i, j)
      debugOutput(f'Column {j}:', indent + 6)
      dumpTableCell(cell, indent + 6)

def dumpTextTableFormat(textTableFormat: QtGui.QTextTableFormat, indent: int = 0):
  debugOutput(f'Text Table Format:', indent)
  debugOutput(f'Header row count: {textTableFormat.headerRowCount()}', indent + 2)
  debugOutput(f'Border collapse: {textTableFormat.borderCollapse()}', indent + 2)
  debugOutput(f'Cell spacing: {textTableFormat.cellSpacing()}', indent + 2)
  debugOutput(f'Cell padding: {textTableFormat.cellPadding()}', indent + 2)
  debugOutput(f'Is table cell format: {textTableFormat.isTableCellFormat()}', indent + 2)
  debugOutput(f'Is format valid: {textTableFormat.isValid()}', indent + 2)
  debugOutput(f'Background:{dumpBrush(textTableFormat.background())}', indent + 2)
  debugOutput(f'Foreground:{dumpBrush(textTableFormat.foreground())}', indent + 2)
  debugOutput(f'Column width constraints: {textTableFormat.columnWidthConstraints()}', indent + 2)
  debugOutput(f'Width: {textTableFormat.width()}', indent + 2)

def dumpTextFormat(textFormat: QtGui.QTextFormat, indent: int = 0):
  debugOutput(f'Text format:', indent)
  debugOutput(f'Background: {dumpBrush(textFormat.background())}', indent + 2)
  debugOutput(f'Foreground: {dumpBrush(textFormat.foreground())}', indent + 2)

def dumpFrameFormat(frameFormat: QtGui.QTextFrameFormat, indent: int = 0):
  debugOutput(f'Frame format:', indent)
  debugOutput(f'Border thickness: {frameFormat.border()}', indent + 2)
  debugOutput(f'Border brush: {dumpBrush(frameFormat.borderBrush())}', indent + 2)
  debugOutput(f'Border style: {frameFormat.borderStyle()}', indent + 2)
  debugOutput(f'Frame height: {frameFormat.height()}', indent + 2)
  debugOutput(f'Frame width: {frameFormat.width()}', indent + 2)
  debugOutput(f'Frame margin: {frameFormat.margin()}', indent + 2)
  debugOutput(f'Frame padding: {frameFormat.padding()}', indent + 2)
  debugOutput(f'Foreground: {frameFormat.foreground()}', indent + 2)
  debugOutput(f'Background: {frameFormat.background()}', indent + 2)

def dumpTextBlockFormat(blockFormat: QtGui.QTextBlockFormat, indent: int = 0):
  debugOutput(f'Text block format:', indent)
  debugOutput(f'Bottom margin: {blockFormat.bottomMargin()}', indent + 2)
  debugOutput(f'Top margin: {blockFormat.topMargin()}', indent + 2)
  debugOutput(f'Left margin: {blockFormat.leftMargin()}', indent + 2)
  debugOutput(f'Right margin: {blockFormat.rightMargin()}', indent + 2)
  debugOutput(f'Line height: {blockFormat.lineHeight()}', indent + 2)
  debugOutput(f'Line height type: {blockFormat.lineHeightType()}', indent + 2)
  debugOutput(f'Text indent: {blockFormat.textIndent()}', indent + 2)

def dumpBrush(brush: QtGui.QBrush):
  brushDump = f'Brush: Color: {brush.color()}, Style: {brush.style()}'
  return brushDump

def dumpTableCell(tableCell: QtGui.QTextTableCell, indent: int = 0):
  cellFormat = tableCell.format()

  debugOutput(f'Background: {dumpBrush(cellFormat.background())}', indent)
  debugOutput(f'Foreground: {dumpBrush(cellFormat.foreground())}', indent)

  iteratorBegin = tableCell.begin()
  iteratorEnd = tableCell.end()
  dumpIterator(iteratorBegin, iteratorEnd, indent + 2)

  # while iterator != tableCell.end():
  #   frame = iterator.currentFrame()

  #   # I think the iterator either points to a frame or a block, but not both
  #   if frame is not None:
  #     currentIteratorFormat = frame.format()
  #     debugOutput(f'{dumpTextFormat(currentIteratorFormat)}', indent)
  #   else:
  #     currentIteratorFormat = iterator.currentBlock().blockFormat()
  #     dumpTextBlockFormat(currentIteratorFormat, indent)

  #   iterator += 1

def dumpIterator(beginIterator: QtGui.QTextFrame.iterator, endIterator: QtGui.QTextFrame.iterator, indent = 0):
  iterator = beginIterator

  while iterator != endIterator:
    frame = iterator.currentFrame()
    if frame is not None:
      currentIteratorFormat = frame.format()
      debugOutput(f'{dumpTextFormat(currentIteratorFormat)}', indent)
      subIteratorBegin = frame.begin()
      subIteratorEnd = frame.end()
      dumpIterator(subIteratorBegin, subIteratorEnd, indent + 2)
    else:
      currentIteratorFormat = iterator.currentBlock().blockFormat()
      dumpTextBlockFormat(currentIteratorFormat, indent)

    iterator += 1
