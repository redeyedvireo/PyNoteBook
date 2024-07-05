from PySide6 import QtCore, QtGui, QtWidgets

from ui_about_dialog import Ui_CAboutDialog

class AboutDialog(QtWidgets.QDialog):
  def __init__(self, parent: QtWidgets.QWidget):
    super(AboutDialog, self).__init__(parent)

    self.ui = Ui_CAboutDialog()
    self.ui.setupUi(self)
