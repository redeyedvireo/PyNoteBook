from PySide6 import QtCore, QtWidgets, QtGui
from page_data import PageData
from utility import formatDateTimeWithDay

from ui_page_info_dlg import Ui_CPageInfoDlg

class CPageInfoDlg(QtWidgets.QDialog):
  def __init__(self, parent: QtWidgets.QWidget, page: PageData) -> None:
    super(CPageInfoDlg, self).__init__(parent)

    self.ui = Ui_CPageInfoDlg()
    self.ui.setupUi(self)

    self.page = page
    self.populateControls()

  def populateControls(self):
    self.ui.pageTitleLabel.setText(self.page.m_title)
    self.ui.createdLabel.setText(f'{formatDateTimeWithDay(self.page.m_createdDateTime)}')
    self.ui.modifiedLabel.setText(f'{formatDateTimeWithDay(self.page.m_modifiedDateTime)}')
    self.ui.numChangesLabel.setText(f'{self.page.m_numModifications}')

    # To compute the size, we must create a temporary QTextDocument
    tempDoc = QtGui.QTextDocument()
    tempDoc.setHtml(self.page.m_contentString)
    self.ui.sizeLabel.setText(f'{tempDoc.characterCount()} characters')
