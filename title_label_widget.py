from PySide6 import QtCore, QtWidgets, QtGui

from ui_title_label_widget import Ui_CTitleLabelWidget

# TODO: Make this an enum?
kLabelPage = 0
kTitleEditPage = 1

kPageIcon = ":/NoteBook/Resources/Page.png"
kFolderIcon = ":/NoteBook/Resources/Folder Closed.png"
kToDoIcon = ":/NoteBook/Resources/ToDoList.png"

class CTitleLabelWidget(QtWidgets.QWidget):
  TLW_SetPageAsFavorite = QtCore.Signal()
  TLW_SetPageAsNonFavorite = QtCore.Signal()

  def __init__(self, parent):
    super(CTitleLabelWidget, self).__init__(parent)
    self.ui = Ui_CTitleLabelWidget()
    self.ui.setupUi(self)

    self.ui.stackedWidget.setCurrentIndex(kLabelPage)

  def initialize(self):
    self.ui.stackedWidget.setCurrentIndex(kLabelPage)

    self.ui.favoritesLabel.loadIconForIndex(0, ':/NoteBook/Resources/star-outline.png')
    self.ui.favoritesLabel.loadIconForIndex(1, ':/NoteBook/Resources/star.png')

    self.setConnections()

  def setConnections(self):
    self.ui.favoritesLabel.LabelClicked.connect(self.setPageAsFavorite)
    self.ui.favoritesLabel.LabelRightClicked.connect(self.setPageAsNonFavorite)

  def clear(self):
    self.ui.pageTitleLabel.setText('')
    self.ui.stackedWidget.setCurrentIndex(kLabelPage)

  def setFavoritesIcon(self, isFavorite: bool):
    iconIndex = 1 if isFavorite else 0
    self.ui.favoritesLabel.setIcon(iconIndex)

  def setPageTitleLabel(self, title: str) -> None:
    self.ui.pageTitleLabel.setText(title)
    self.ui.stackedWidget.setCurrentIndex(kLabelPage)

  def getPageTitleLabel(self) -> str:
    return self.ui.pageTitleLabel.text()

  def setPageAsFavorite(self):
    self.TLW_SetPageAsFavorite.emit()

  def setPageAsNonFavorite(self):
    self.TLW_SetPageAsNonFavorite.emit()
