from PySide6 import QtCore, QtGui, QtWidgets

from text_table import TextTable
from style_manager import StyleManager
from styleDef import StyleDef

class CustomTextEdit(QtWidgets.QTextEdit):
  def __init__(self, parent):
    super(CustomTextEdit, self).__init__(parent)

    self.styleManager = None
    self.copiedRow = -1
    self.copiedColumn = -1

  def setStyleManager(self, styleManager: StyleManager):
    self.styleManager = styleManager

  def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
    menu = self.createStandardContextMenu()

    menu.addSeparator()

    if self.cursorInSelection() and self.styleManager is not None and self.styleManager.numStyles() > 0:
      # Add "Apply Style" menu
      styleMenu = QtWidgets.QMenu('Apply Style')
      self.populateStyleMenu(styleMenu)
      menu.addMenu(styleMenu)
      menu.addSeparator()

    if TextTable.isCursorInTable(self.textCursor()):
      rowMenu = QtWidgets.QMenu('Row')
      rowMenu.addAction('Insert Row Above', self.onInsertTableRowAbove)
      rowMenu.addAction('Insert Row Below', self.onInsertTableRowBelow)
      rowMenu.addAction('Copy Row', self.onCopyTableRow)

      if self.copiedRow != -1:
        rowMenu.addAction('Paste Row', self.onPasteTableRow)

      rowMenu.addAction('Delete Row', self.onDeleteTableRow)
      menu.addMenu(rowMenu)

      columnMenu = QtWidgets.QMenu('Column')

      columnMenu.addAction('Insert Column to the Left', self.onInsertTableColumnLeft)
      columnMenu.addAction('Insert Column to the Right', self.onInsertTableColumnRight)
      columnMenu.addAction('Copy Column', self.onCopyTableColumn)

      if self.copiedColumn != -1:
        columnMenu.addAction('Paste Column', self.onPasteTableColumn)

      columnMenu.addAction('Delete Column', self.onDeleteTableColumn)
      menu.addMenu(columnMenu)

      menu.addAction('Convert Table to Text', self.onConvertTableToText)
      menu.addAction('Format Table...', self.onTableFormat)
      menu.addSeparator()

    menu.addAction('Insert Link to Page...', self.onInsertPageLinkDlg)
    menu.addAction('Insert Web Link...', self.onInsertWebLink)

    if self.cursorInSelection():
      menu.addSeparator()
      menu.addAction('Convert Selection to Table', self.onConvertSelectionToTable)
      menu.addAction('URL-ify Selection', self.onUrlifySelection)

    if self.cursorInList():
      curBlock = self.textCursor().block()
      prevBlock = curBlock.previous()
      prevList = prevBlock.textList()

      if prevList is not None:
        # The previous block is a list; add menu item to merge this list into the previous one
        menu.addAction('Merge this List with Previous List', self.onMergeListWithPrevious)

    menu.addSeparator()
    menu.addAction('Insert Image from File...', self.onInsertImageFromFile)

    menu.exec(event.globalPos())

  def cursorInSelection(self) -> bool:
    return self.textCursor().hasSelection()

  def cursorInList(self) -> bool:
    return self.textCursor().currentList() is not None

  def populateStyleMenu(self, styleMenu: QtWidgets.QMenu):
    if self.styleManager is not None:
      styleIds = self.styleManager.getStyleIds()

      for styleId in styleIds:
        styleDef = self.styleManager.getStyle(styleId)
        if styleDef is not None:
          action = styleMenu.addAction(styleDef.strName)    # TODO: This needs a slot.  Then, won't need the styleItemMapper
          # TODO: styleItemMapper.setMapping(action, styleId)
          #       connect(action, SIGNAL(triggered()), &m_styleItemMapper, SLOT(map()))


  # *********** Slots ***********

  @QtCore.Slot()
  def onInsertTableRowAbove(self):
    TextTable.insertRow(self.textCursor(), True)
    self.copiedRow = -1   # Inserting a new row will throw off the row numbering

  @QtCore.Slot()
  def onInsertTableRowBelow(self):
    TextTable.insertRow(self.textCursor(), False)
    self.copiedRow = -1   # Inserting a new row will throw off the row numbering

  @QtCore.Slot()
  def onCopyTableRow(self):
    self.copiedRow = TextTable.currentTableRow(self.textCursor())

  @QtCore.Slot()
  def onPasteTableRow(self):
    TextTable.copyRow(self.textCursor(), self.copiedRow)

  @QtCore.Slot()
  def onDeleteTableRow(self):
    TextTable.deleteRowAtCursor(self.textCursor())

  @QtCore.Slot()
  def onInsertTableColumnLeft(self):
    # TODO: Implement
    print('Implement onInsertTableColumnLeft')

  @QtCore.Slot()
  def onInsertTableColumnRight(self):
    # TODO: Implement
    print('Implement onInsertTableColumnRight')

  @QtCore.Slot()
  def onCopyTableColumn(self):
    # TODO: Implement
    print('Implement onCopyTableColumn')

  @QtCore.Slot()
  def onPasteTableColumn(self):
    # TODO: Implement
    print('Implement onPasteTableColumn')

  @QtCore.Slot()
  def onDeleteTableColumn(self):
    # TODO: Implement
    print('Implement onDeleteTableColumn')

  @QtCore.Slot()
  def onConvertTableToText(self):
    # TODO: Implement
    print('Implement onConvertTableToText')

  @QtCore.Slot()
  def onTableFormat(self):
    # TODO: Implement
    print('Implement onTableFormat')

  @QtCore.Slot()
  def onInsertPageLinkDlg(self):
    # TODO: Implement
    print('Implement onInsertPageLinkDlg')

  @QtCore.Slot()
  def onInsertWebLink(self):
    # TODO: Implement
    print('Implement onInsertWebLink')

  @QtCore.Slot()
  def onConvertSelectionToTable(self):
    # TODO: Implement
    print('Implement onConvertSelectionToTable')

  @QtCore.Slot()
  def onUrlifySelection(self):
    # TODO: Implement
    print('Implement onUrlifySelection')

  @QtCore.Slot()
  def onMergeListWithPrevious(self):
    # TODO: Implement
    print('Implement onMergeListWithPrevious')

  @QtCore.Slot()
  def onInsertImageFromFile(self):
    # TODO: Implement
    print('Implement onInsertImageFromFile')



