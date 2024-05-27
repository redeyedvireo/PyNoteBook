from PySide6 import QtCore, QtWidgets, QtGui

from ui_title_label_widget import Ui_CTitleLabelWidget

# TODO: Make this an enum?
kLabelPage = 0
kTitleEditPage = 1

class CTitleLabelWidget(QtWidgets.QWidget):
  def __init__(self, parent):
    super(CTitleLabelWidget, self).__init__(parent)
    self.ui = Ui_CTitleLabelWidget()
    self.ui.setupUi(self)

    self.ui.stackedWidget.setCurrentIndex(kLabelPage)

  def setPageTitleLabel(self, title: str) -> None:
    self.ui.pageTitleLabel.setText(title)
    self.ui.stackedWidget.setCurrentIndex(kLabelPage)