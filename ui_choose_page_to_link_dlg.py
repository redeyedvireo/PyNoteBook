# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'choose_page_to_link_dlg.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import pynotebook_rc

class Ui_ChoosePageToLinkDlg(object):
    def setupUi(self, ChoosePageToLinkDlg):
        if not ChoosePageToLinkDlg.objectName():
            ChoosePageToLinkDlg.setObjectName(u"ChoosePageToLinkDlg")
        ChoosePageToLinkDlg.resize(375, 443)
        self.verticalLayout = QVBoxLayout(ChoosePageToLinkDlg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(ChoosePageToLinkDlg)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.filterEdit = QLineEdit(ChoosePageToLinkDlg)
        self.filterEdit.setObjectName(u"filterEdit")

        self.horizontalLayout.addWidget(self.filterEdit)

        self.clearFilterButton = QPushButton(ChoosePageToLinkDlg)
        self.clearFilterButton.setObjectName(u"clearFilterButton")
        icon = QIcon()
        icon.addFile(u":/NoteBook/Resources/RedX.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clearFilterButton.setIcon(icon)
        self.clearFilterButton.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.clearFilterButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(ChoosePageToLinkDlg)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setSizeIncrement(QSize(0, 1))
        self.listWidget.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)

        self.verticalLayout.addWidget(self.listWidget)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.okButton = QPushButton(ChoosePageToLinkDlg)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.okButton)

        self.cancelButton = QPushButton(ChoosePageToLinkDlg)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ChoosePageToLinkDlg)
        self.cancelButton.clicked.connect(ChoosePageToLinkDlg.reject)
        self.okButton.clicked.connect(ChoosePageToLinkDlg.accept)

        QMetaObject.connectSlotsByName(ChoosePageToLinkDlg)
    # setupUi

    def retranslateUi(self, ChoosePageToLinkDlg):
        ChoosePageToLinkDlg.setWindowTitle(QCoreApplication.translate("ChoosePageToLinkDlg", u"Choose Page", None))
        self.label.setText(QCoreApplication.translate("ChoosePageToLinkDlg", u"Filter:", None))
        self.clearFilterButton.setText("")
        self.okButton.setText(QCoreApplication.translate("ChoosePageToLinkDlg", u"OK", None))
        self.cancelButton.setText(QCoreApplication.translate("ChoosePageToLinkDlg", u"Cancel", None))
    # retranslateUi

