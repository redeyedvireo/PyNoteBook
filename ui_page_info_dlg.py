# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_info_dlg.ui'
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
    QFormLayout, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_CPageInfoDlg(object):
    def setupUi(self, CPageInfoDlg):
        if not CPageInfoDlg.objectName():
            CPageInfoDlg.setObjectName(u"CPageInfoDlg")
        CPageInfoDlg.resize(457, 160)
        self.verticalLayout = QVBoxLayout(CPageInfoDlg)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(CPageInfoDlg)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.pageTitleLabel = QLabel(CPageInfoDlg)
        self.pageTitleLabel.setObjectName(u"pageTitleLabel")
        font = QFont()
        font.setPointSize(8)
        self.pageTitleLabel.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.pageTitleLabel)

        self.label_2 = QLabel(CPageInfoDlg)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.createdLabel = QLabel(CPageInfoDlg)
        self.createdLabel.setObjectName(u"createdLabel")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.createdLabel)

        self.label_3 = QLabel(CPageInfoDlg)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.modifiedLabel = QLabel(CPageInfoDlg)
        self.modifiedLabel.setObjectName(u"modifiedLabel")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.modifiedLabel)

        self.label_4 = QLabel(CPageInfoDlg)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.numChangesLabel = QLabel(CPageInfoDlg)
        self.numChangesLabel.setObjectName(u"numChangesLabel")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.numChangesLabel)

        self.label_5 = QLabel(CPageInfoDlg)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.sizeLabel = QLabel(CPageInfoDlg)
        self.sizeLabel.setObjectName(u"sizeLabel")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.sizeLabel)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(CPageInfoDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CPageInfoDlg)
        self.buttonBox.rejected.connect(CPageInfoDlg.accept)

        QMetaObject.connectSlotsByName(CPageInfoDlg)
    # setupUi

    def retranslateUi(self, CPageInfoDlg):
        CPageInfoDlg.setWindowTitle(QCoreApplication.translate("CPageInfoDlg", u"Page Information", None))
        self.label.setText(QCoreApplication.translate("CPageInfoDlg", u"Page Title", None))
        self.pageTitleLabel.setText(QCoreApplication.translate("CPageInfoDlg", u"-", None))
        self.label_2.setText(QCoreApplication.translate("CPageInfoDlg", u"Created", None))
        self.createdLabel.setText(QCoreApplication.translate("CPageInfoDlg", u"-", None))
        self.label_3.setText(QCoreApplication.translate("CPageInfoDlg", u"Last Modified", None))
        self.modifiedLabel.setText(QCoreApplication.translate("CPageInfoDlg", u"-", None))
        self.label_4.setText(QCoreApplication.translate("CPageInfoDlg", u"Changes", None))
        self.numChangesLabel.setText(QCoreApplication.translate("CPageInfoDlg", u"-", None))
        self.label_5.setText(QCoreApplication.translate("CPageInfoDlg", u"Size", None))
        self.sizeLabel.setText(QCoreApplication.translate("CPageInfoDlg", u"-", None))
    # retranslateUi

