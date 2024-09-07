from PySide6 import QtCore, QtGui, QtWidgets

from ui_add_web_link_dlg import Ui_AddWebLinkDlg

class AddWebLinkDlg(QtWidgets.QDialog):
  def __init__(self, parent: QtWidgets.QWidget) -> None:
    super(AddWebLinkDlg, self).__init__(parent)

    self.ui = Ui_AddWebLinkDlg()
    self.ui.setupUi(self)

  def getLink(self) -> tuple[str, str]:
    return (self.ui.urlEdit.text(), self.ui.descriptionEdit.text())