from PySide6 import QtCore, QtGui, QtWidgets

from ui_set_password_dlg import Ui_SetPasswordDlg

class SetPasswordDlg(QtWidgets.QDialog):
  def __init__(self, parent):
    super(SetPasswordDlg, self).__init__(parent)

    self.ui = Ui_SetPasswordDlg()
    self.ui.setupUi(self)

    # Disable the OK button until a password is entered
    self.ui.buttonBox.setEnabled(False)

    self.ui.noPasswordButton.clicked.connect(self.onNoPasswordClicked)
    self.ui.buttonBox.accepted.connect(self.onOkClicked)
    self.ui.passwordEdit.textEdited.connect(self.onPasswordEdited)

  def onPasswordEdited(self):
    self.ui.buttonBox.setEnabled(len(self.ui.passwordEdit.text()) > 0)

  def onNoPasswordClicked(self):
    self.ui.passwordEdit.clear()
    self.ui.reEnterPasswordEdit.clear()
    self.accept()

  def getPassword(self):
    return self.ui.passwordEdit.text()

  def onOkClicked(self):
    # Verify that the two passwords match
    if self.ui.passwordEdit.text() == self.ui.reEnterPasswordEdit.text():
      self.accept()
      return
    else:
      QtWidgets.QMessageBox.critical(self, "Password Mismatch", "The passwords don't match.")
