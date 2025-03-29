from re import U
from PySide6 import QtCore, QtGui, QtWidgets

from ui_folder_edit_widget import Ui_FolderEditWidget

class FolderEditWidget(QtWidgets.QWidget):
  def __init__(self, parent=None):
    super(FolderEditWidget, self).__init__(parent)
    self.ui = Ui_FolderEditWidget()
    self.ui.setupUi(self)

    self.populate()

  def populate(self):
    self.ui.listWidget.clear()
    self.ui.listWidget.addItem("Folder 1")