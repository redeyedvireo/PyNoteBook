from re import U
from PySide6 import QtCore, QtGui, QtWidgets

from notebook_types import ENTITY_ID, PAGE_TYPE
from page_tree import CPageTree
from switchboard import Switchboard
from ui_folder_edit_widget import Ui_FolderEditWidget

class FolderEditWidget(QtWidgets.QWidget):
  def __init__(self, parent=None):
    super(FolderEditWidget, self).__init__(parent)
    self.ui = Ui_FolderEditWidget()
    self.ui.setupUi(self)

    self.ui.listWidget.setIconSize(QtCore.QSize(20, 20))

  def initialize(self, pageTree: CPageTree, switchboard: Switchboard):
    self.pageTree = pageTree
    self.switchboard = switchboard

  def displayFolder(self, pageId: ENTITY_ID):
    self.pageId = pageId
    self.populate()

  def populate(self):
    self.ui.folderLabel.setText(self.pageTree.getPageTitle(self.pageId))
    folderChildren = self.pageTree.getFolderChildren(self.pageId)

    self.ui.listWidget.clear()

    for child in folderChildren:
      itemText = f"{child['title']}"
      item = QtWidgets.QListWidgetItem(itemText)
      item.setData(QtCore.Qt.ItemDataRole.UserRole, child['pageId'])

      font = item.font()
      font.setPointSize(12)

      # Make the names look like HTML links
      font.setUnderline(True)
      item.setForeground(QtGui.QColor(0, 0, 255))

      match child['itemType']:
        case PAGE_TYPE.kPageFolder:
          item.setIcon(QtGui.QIcon(':/NoteBook/Resources/Folder Closed.png'))

          # Display folders in italics
          font.setItalic(True)

        case PAGE_TYPE.kPageTypeUserText:
          item.setIcon(QtGui.QIcon(':/NoteBook/Resources/Page.png'))

        case PAGE_TYPE.kPageTypeToDoList:
          item.setIcon(QtGui.QIcon(':/NoteBook/Resources/ToDoList.png'))

      item.setFont(font)
      item.setSizeHint(QtCore.QSize(0, 26))

      self.ui.listWidget.addItem(item)

  @QtCore.Slot(QtWidgets.QListWidgetItem)
  def on_listWidget_itemClicked(self, item: QtWidgets.QListWidgetItem):
    pageId = item.data(QtCore.Qt.ItemDataRole.UserRole)
    self.switchboard.emitPageSelected(pageId)
