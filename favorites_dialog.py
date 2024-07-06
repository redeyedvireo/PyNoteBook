from PySide6 import QtCore, QtGui, QtWidgets
from notebook_types import ID_TITLE_LIST

from ui_favorites_dialog import Ui_favoritesDialog

class FavoritesDialog(QtWidgets.QDialog):
  def __init__(self, favoritesList: ID_TITLE_LIST, parent: QtWidgets.QWidget) -> None:
    super(FavoritesDialog, self).__init__(parent)

    self.ui = Ui_favoritesDialog()
    self.ui.setupUi(self)

    self.ui.removeButton.setEnabled(False)

    self.populateList(favoritesList)

  @property
  def favoritesList(self) -> ID_TITLE_LIST:
    numItems = self.ui.listWidget.count()
    theList: ID_TITLE_LIST = []

    for row in range(numItems):
      item = self.ui.listWidget.item(row)
      theList.append((item.data(QtCore.Qt.ItemDataRole.UserRole), item.text()))

    return theList

  def populateList(self, favoritesList: ID_TITLE_LIST):
    for item in favoritesList:
      newItem = QtWidgets.QListWidgetItem(item[1])
      newItem.setData(QtCore.Qt.ItemDataRole.UserRole, item[0])
      self.ui.listWidget.addItem(newItem)

  @QtCore.Slot()
  def on_buttonBox_accepted(self):
    print('on_buttonBox_accepted')

  @QtCore.Slot()
  def on_removeButton_clicked(self):
    currentItem = self.ui.listWidget.currentItem()
    pageId = currentItem.data(QtCore.Qt.ItemDataRole.UserRole)
    row = self.ui.listWidget.row(currentItem)
    self.ui.listWidget.takeItem(row)

  @QtCore.Slot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
  def on_listWidget_currentItemChanged(self, current: QtWidgets.QListWidgetItem, previous: QtWidgets.QListWidgetItem):
    self.ui.removeButton.setEnabled(current is not None)
