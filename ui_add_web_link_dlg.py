# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_web_link_dlg.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_AddWebLinkDlg(object):
    def setupUi(self, AddWebLinkDlg):
        if not AddWebLinkDlg.objectName():
            AddWebLinkDlg.setObjectName(u"AddWebLinkDlg")
        AddWebLinkDlg.resize(406, 168)
        self.verticalLayout = QVBoxLayout(AddWebLinkDlg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(AddWebLinkDlg)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.urlEdit = QLineEdit(AddWebLinkDlg)
        self.urlEdit.setObjectName(u"urlEdit")

        self.verticalLayout.addWidget(self.urlEdit)

        self.verticalSpacer = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_2 = QLabel(AddWebLinkDlg)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.descriptionEdit = QLineEdit(AddWebLinkDlg)
        self.descriptionEdit.setObjectName(u"descriptionEdit")

        self.verticalLayout.addWidget(self.descriptionEdit)

        self.verticalSpacer_2 = QSpacerItem(20, 136, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.buttonBox = QDialogButtonBox(AddWebLinkDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddWebLinkDlg)
        self.buttonBox.accepted.connect(AddWebLinkDlg.accept)
        self.buttonBox.rejected.connect(AddWebLinkDlg.reject)

        QMetaObject.connectSlotsByName(AddWebLinkDlg)
    # setupUi

    def retranslateUi(self, AddWebLinkDlg):
        AddWebLinkDlg.setWindowTitle(QCoreApplication.translate("AddWebLinkDlg", u"Add Web Link", None))
        self.label.setText(QCoreApplication.translate("AddWebLinkDlg", u"Web URL", None))
        self.label_2.setText(QCoreApplication.translate("AddWebLinkDlg", u"Description", None))
    # retranslateUi

