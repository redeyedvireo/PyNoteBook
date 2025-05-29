import re
from PySide6 import QtCore, QtGui, QtWidgets

from text_table import TextTable
from text_image import TextImage
from style_manager import StyleManager
from styleDef import StyleDef
from database import Database

from choose_page_to_link_dlg import ChoosePageToLinkDlg
from add_web_link_dlg import AddWebLinkDlg

from notebook_types import kInvalidPageId, ENTITY_ID

# Defines for in-page links
WEBURLTAG =	"http://"
WEBURLTAGS =	"https://"
NOTEBOOKTAG	= "NB://"

class CustomTextEdit(QtWidgets.QTextEdit):
  CTE_TableFormat = QtCore.Signal()
  CTE_GotoPage = QtCore.Signal(ENTITY_ID)

  def __init__(self, parent):
    super(CustomTextEdit, self).__init__(parent)

    self.styleManager = None
    self.copiedRow = -1
    self.copiedColumn = -1
    self.m_bCursorOverLink = False
    self.hoveredLink = None     # Link over which the cursor is hovered.  Can be an ENTITY_ID (for a NoteBook page) or a string (for a web link)
    self.currentPageId = kInvalidPageId

  def initialize(self, styleManager: StyleManager, messageLabel: QtWidgets.QLabel, database: Database):
    self.styleManager = styleManager
    self.db = database
    self.messageLabel = messageLabel

  def keyPressEvent(self, event: QtGui.QKeyEvent):
    if event.key() == QtCore.Qt.Key.Key_Tab:
      if self.cursorInList():
        self.increaseSelectionIndent()
        return
      elif TextTable.isCursorInTable(self.textCursor()):
        self.goToNextCell()
        event.accept()
        return

    elif event.key() == QtCore.Qt.Key.Key_Backtab:
      if self.cursorInList():
        self.reduceSelectionIndent()
        return
      elif TextTable.isCursorInTable(self.textCursor()):
        self.goToPreviousCell()
        event.accept()
        return

    else:
      super(CustomTextEdit, self).keyPressEvent(event)

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
      menu.addAction('Dump Table', lambda: TextTable.dumpTable(self.textCursor()))
      menu.addAction('Dump Current Cell', lambda: TextTable.dumpCell(self.textCursor()))
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

  def mousePressEvent(self, event: QtGui.QMouseEvent):
    super(CustomTextEdit, self).mousePressEvent(event)

    if event.button() != QtCore.Qt.MouseButton.LeftButton:
      return

    # Determine if a link was clicked
    if self.pointOverLink(event.pos()):
      # Determine if this is a web link or a NoteBook link
      if type(self.hoveredLink) is str:
        # Web link
        QtGui.QDesktopServices.openUrl(self.hoveredLink)

      elif type(self.hoveredLink) is int:
        # NoteBook link
        self.CTE_GotoPage.emit(self.hoveredLink)

  def mouseMoveEvent(self, event: QtGui.QMouseEvent):
    super(CustomTextEdit, self).mouseMoveEvent(event)

    if self.pointOverLink(event.pos()):
      if not self.m_bCursorOverLink:
        # The cursor has just moved over a link
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.m_bCursorOverLink = True

        # If it's a NoteBook page link, get the title of the page
        if type(self.hoveredLink) is int:
          pageTitle = self.db.getPageTitle(self.hoveredLink)
          self.messageLabel.setText(f'Page: {pageTitle}')

        elif type(self.hoveredLink) is str:
          # For web links, just show the web URL
          self.messageLabel.setText(self.hoveredLink)

    else:
      if self.m_bCursorOverLink:
        # Cursor was formerly over a link, and now is not.  Remove the override cursor.
        QtWidgets.QApplication.restoreOverrideCursor()
        self.m_bCursorOverLink = False

        # Blank out the message
        self.messageLabel.setText('')

  def pointOverLink(self, pt: QtCore.QPoint) -> bool:
    """Determines if the pt is over a link in the document.  If so, sets self.hoveredLink to an ENTITY_ID
       if the cursor is over a NoteBook page link, or to a string if the cursor is over a web link, or to
       None if neither is true.

    Args:
        pt (QtCore.QPoint): Point in question (usually the position of the mouse cursor)

    Returns:
        bool: Returns True if the pt is over a link, False otherwise.
    """
    linkAtCursor = self.anchorAt(pt)

    if len(linkAtCursor) > 0 and '://' in linkAtCursor:
      if linkAtCursor.startswith(NOTEBOOKTAG):
        self.hoveredLink = self.getNotebookLinkPage(linkAtCursor)
        return True

      possibleUrl = QtCore.QUrl(linkAtCursor)

      if possibleUrl.isValid():
        self.hoveredLink = linkAtCursor
        return True

    return False

  def getNotebookLinkPage(self, linkStr: str) -> ENTITY_ID:
    pageIdRx = r'page=(\d+)'

    matchResult = re.search(pageIdRx, linkStr)

    if matchResult is not None:
      pageIdStr = matchResult.group(1)
      return int(pageIdStr)
    else:
      return kInvalidPageId


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
    TextTable.insertColumn(self.textCursor(), True)
    self.copiedColumn = -1  # Inserting a new column will throw off the row numbering

  @QtCore.Slot()
  def onInsertTableColumnRight(self):
    TextTable.insertColumn(self.textCursor(), False)
    self.copiedColumn = -1  # Inserting a new column will throw off the row numbering

  @QtCore.Slot()
  def onCopyTableColumn(self):
    self.copiedColumn = TextTable.currentTableColumn(self.textCursor())

  @QtCore.Slot()
  def onPasteTableColumn(self):
    TextTable.copyColumn(self.textCursor(), self.copiedColumn)

  @QtCore.Slot()
  def onDeleteTableColumn(self):
    TextTable.deleteColumnAtCursor(self.textCursor())
    self.copiedColumn = -1  # Deleting a column will throw off the column numbering

  @QtCore.Slot()
  def onConvertTableToText(self):
    TextTable.tableToText(self.textCursor())

  @QtCore.Slot()
  def onTableFormat(self):
    self.CTE_TableFormat.emit()

  @QtCore.Slot()
  def onInsertPageLinkDlg(self):
    dlg = ChoosePageToLinkDlg(self.db, self)
    result = dlg.exec()

    if result == QtWidgets.QDialog.DialogCode.Accepted:
      self.insertPageLink(dlg.getSelectedPage())

  def insertPageLink(self, pageId: ENTITY_ID):
    pageTitle = self.db.getPageTitle(pageId)

    if pageTitle is not None:
      # Note the terminating <br>.  This is being added as a way of providing separation
      # from the link tag.  Without this, if the user were to move the cursor past the link
      # and begin typing, the text he/she types would end up being part of the link.  By
      # adding the <br>, the user is able to type beyond the link.  More research is needed
      # to allow the OnCursorPositionChanged() function to be able to identify that the cursor
      # is within a link, and to move it out of the link.
      self.insertHtml(f'<a href=\"NB://page={pageId}\">[{pageTitle}]</a><br>')

  def insertWebLink(self, url: str, description: str, withBrackets: bool):
    webUrlStr = url

    # if not (url.startswith(WEBURLTAG) or url.startswith(WEBURLTAGS)):
    if not ('://' in url):
      # Add "http://" header
      webUrlStr = f'{WEBURLTAG}{url}'

    # Note the terminating <br>.  This is being added as a way of providing separation
    # from the link tag.  Without this, if the user were to move the cursor past the link
    # and begin typing, the text he/she types would end up being part of the link.  By
    # adding the <br>, the user is able to type beyond the link.  More research is needed
    # to allow the OnCursorPositionChanged() function to be able to identify that the cursor
    # is within a link, and to move it out of the link.

    webLinkStr = f'<a href=\"{webUrlStr}\">[{description}]</a><br>' if withBrackets else f'<a href=\"{webUrlStr}\">{description}</a><br>'

    self.insertHtml(webLinkStr)

  @QtCore.Slot()
  def onInsertWebLink(self):
    dlg = AddWebLinkDlg(self)
    result = dlg.exec()

    if result == QtWidgets.QDialog.DialogCode.Accepted:
      url, description = dlg.getLink()
      self.insertWebLink(url, description, True)

  def insertFromMimeData(self, source: QtCore.QMimeData):
    """Override the insertFromMimeData to handle custom text insertion."""
    if source.hasHtml():
      # The text has formatting.  Ask user if it should be pasted with formatting or as plain text
      reply = QtWidgets.QMessageBox.question(self, 'Paste with Formatting?', 'The text contains formatting.  Paste text with formatting intact?',
                                              QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

      if reply == QtWidgets.QMessageBox.StandardButton.No:
        # Convert it to a plain text object
        plainText = source.text()
        newMimeData = QtCore.QMimeData()
        newMimeData.setText(plainText)
        super(CustomTextEdit, self).insertFromMimeData(newMimeData)
      else:
        # Call the base class to insert the HTML
        super(CustomTextEdit, self).insertFromMimeData(source)

  @QtCore.Slot()
  def onConvertSelectionToTable(self):
    TextTable.selectionToTable(self.textCursor())

  @QtCore.Slot()
  def onUrlifySelection(self):
    selectionCursor = self.textCursor()
    selectedText = selectionCursor.selectedText()

    selectionCursor.removeSelectedText()
    self.insertWebLink(selectedText, selectedText, False)

  @QtCore.Slot()
  def onMergeListWithPrevious(self):
    curBlock = self.textCursor().block()
    prevBlock = self.getPreviousMatchingListBlock(curBlock)

    if prevBlock is not None:
      prevList = prevBlock.textList()

      if prevList is not None:
        prevList.add(curBlock)

  @QtCore.Slot()
  def onInsertImageFromFile(self):
    filePath, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Image File', '', 'Images (*.png *.jpg *.bmp)')

    if filePath is not None and len(filePath) > 0:
      TextImage.insertImageIntoDocument(self.document(), self.textCursor(), filePath, self.currentPageId, self.db)

  def increaseSelectionIndent(self):
    selectionCursor = self.textCursor()
    currentList = selectionCursor.currentList()

    if currentList is not None:
      listFormat = currentList.format()

      if selectionCursor.hasSelection():
        # Indent the lines that are selected
        listFormat.setIndent(listFormat.indent() + 1)
        listFormat.setStyle(self.nextBullet(listFormat.style()))
        selectionCursor.createList(listFormat)
      else:
        # No selection; just indent the current line
        if currentList.count() == 1:
          # There is only one item in the list, so can just indent it
          listFormat.setIndent(listFormat.indent() + 1)
          listFormat.setStyle(self.nextBullet(listFormat.style()))
          currentList.setFormat(listFormat)
        else:
          # Indent the line containing the cursor
          listFormat.setIndent(listFormat.indent() + 1)
          listFormat.setStyle(self.nextBullet(listFormat.style()))
          selectionCursor.createList(listFormat)

  def reduceSelectionIndent(self):
    selectionCursor = self.textCursor()
    currentList = selectionCursor.currentList()

    if currentList is not None:
      listFormat = currentList.format()
      curIndent = listFormat.indent()

      if curIndent > 0:
        if selectionCursor.hasSelection():
          # Dedent the items that are selected
          listFormat.setIndent(listFormat.indent() - 1)
          listFormat.setStyle(self.prevBullet(listFormat.style()))
          selectionCursor.createList(listFormat)
        else:
          # Reduce indent of the current line
          if currentList.count() == 1:
            # There is only one item in the list, so can just dedent it
            listFormat.setIndent(curIndent - 1)
            listFormat.setStyle(self.prevBullet(listFormat.style()))
            currentList.setFormat(listFormat)

            # In case this list is adjacent to a previous list, check if it can be
            # merged with the previous list.
            newBlock = currentList.item(0)
            prevMatchingBlock = self.getPreviousMatchingListBlock(newBlock)

            if prevMatchingBlock is not None:
              prevList = prevMatchingBlock.textList()
              if prevList is not None:
                prevList.add(newBlock)

            self.setTextCursor(selectionCursor)
          else:
            # Dedent the line containing the cursor
            listFormat.setIndent(listFormat.indent() - 1)
            listFormat.setStyle(self.prevBullet(listFormat.style()))

            # Must create a new list, or else the entire sublist will be dedented
            newList = selectionCursor.createList(listFormat)
            newBlock = newList.item(0)        # This will be the first item
            prevMatchingBlock = self.getPreviousMatchingListBlock(newBlock)

            if prevMatchingBlock is not None:
              prevList = prevMatchingBlock.textList()
              if prevList is not None:
                prevList.add(newBlock)

  def getPreviousMatchingListBlock(self, block: QtGui.QTextBlock) -> QtGui.QTextBlock | None:
    selectionCursor = self.textCursor()
    list = selectionCursor.currentList()
    returnBlock = QtGui.QTextBlock()

    if list is not None:
      listFormat = list.format()
      initialIndent = listFormat.indent()

      curBlock = block.previous()
      curList = curBlock.textList()

      while curList is not None:
        curListFormat = curList.format()

        if curListFormat.indent() == initialIndent:
          # Found one
          returnBlock = curBlock
          break

        # Go to previous block
        curBlock = curBlock.previous()
        curList = curBlock.textList()

      return returnBlock
    else:
      return None

  def nextBullet(self, currentBullet: QtGui.QTextListFormat.Style) -> QtGui.QTextListFormat.Style:
    """Returns the next bullet style in the bullet enumeration.
       In the C++ version, it was possible to just cast the style value to an integer, and
       then subtract 1 from it.  In Python, this is not possible, so we must use a switch
       statement to accomplish this.

    Args:
        currentBullet (QtGui.QTextListFormat.Style): Current bullet style

    Returns:
        QtGui.QTextListFormat.Style: The next bullet style in the bullet style enumeration
    """
    match currentBullet:
      case QtGui.QTextListFormat.Style.ListDisc:
        return QtGui.QTextListFormat.Style.ListCircle

      case QtGui.QTextListFormat.Style.ListCircle:
        return QtGui.QTextListFormat.Style.ListSquare

      case QtGui.QTextListFormat.Style.ListSquare:
        # Go to next non-numeric bullet
        return QtGui.QTextListFormat.Style.ListDisc

      case QtGui.QTextListFormat.Style.ListDecimal:
        return QtGui.QTextListFormat.Style.ListLowerAlpha

      case QtGui.QTextListFormat.Style.ListLowerAlpha:
        return QtGui.QTextListFormat.Style.ListUpperAlpha

      case QtGui.QTextListFormat.Style.ListUpperAlpha:
        return QtGui.QTextListFormat.Style.ListLowerRoman

      case QtGui.QTextListFormat.Style.ListLowerRoman:
        return QtGui.QTextListFormat.Style.ListUpperRoman

      case QtGui.QTextListFormat.Style.ListUpperRoman:
        # Go to next numeric bullet
        return QtGui.QTextListFormat.Style.ListDecimal

      case _:
        # Should never get here, but just in case...
        return QtGui.QTextListFormat.Style.ListDisc

  def prevBullet(self, currentBullet: QtGui.QTextListFormat.Style) -> QtGui.QTextListFormat.Style:
    """Returns the previous bullet style in the bullet enumeration.
       In the C++ version, it was possible to just cast the style value to an integer, and
       then add 1 from it.  In Python, this is not possible, so we must use a switch
       statement to accomplish this.

    Args:
        currentBullet (QtGui.QTextListFormat.Style): Current bullet style

    Returns:
        QtGui.QTextListFormat.Style: The next bullet style in the bullet style enumeration
    """
    match currentBullet:
      case QtGui.QTextListFormat.Style.ListDisc:
        return QtGui.QTextListFormat.Style.ListSquare

      case QtGui.QTextListFormat.Style.ListCircle:
        return QtGui.QTextListFormat.Style.ListDisc

      case QtGui.QTextListFormat.Style.ListSquare:
        # Go to previous non-numeric bullet
        return QtGui.QTextListFormat.Style.ListCircle

      case QtGui.QTextListFormat.Style.ListDecimal:
        return QtGui.QTextListFormat.Style.ListUpperRoman

      case QtGui.QTextListFormat.Style.ListLowerAlpha:
        return QtGui.QTextListFormat.Style.ListDecimal

      case QtGui.QTextListFormat.Style.ListUpperAlpha:
        return QtGui.QTextListFormat.Style.ListLowerAlpha

      case QtGui.QTextListFormat.Style.ListLowerRoman:
        return QtGui.QTextListFormat.Style.ListUpperAlpha

      case QtGui.QTextListFormat.Style.ListUpperRoman:
        # Go to previous numeric bullet
        return QtGui.QTextListFormat.Style.ListLowerRoman

      case _:
        # Should never get here, but just in case...
        return QtGui.QTextListFormat.Style.ListDisc

  def goToNextCell(self):
    cursor = self.textCursor()
    cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextCell)
    self.setTextCursor(cursor)

  def goToPreviousCell(self):
    cursor = self.textCursor()
    cursor.movePosition(QtGui.QTextCursor.MoveOperation.PreviousCell)
    self.setTextCursor(cursor)
