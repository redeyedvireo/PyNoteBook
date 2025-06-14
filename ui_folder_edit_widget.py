# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'folder_edit_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import pynotebook_rc

class Ui_FolderEditWidget(object):
    def setupUi(self, FolderEditWidget):
        if not FolderEditWidget.objectName():
            FolderEditWidget.setObjectName(u"FolderEditWidget")
        FolderEditWidget.resize(577, 407)
        FolderEditWidget.setAutoFillBackground(False)
        FolderEditWidget.setStyleSheet(u"background-color: rgb(240, 240, 240);")
        self.verticalLayout = QVBoxLayout(FolderEditWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(30, 10, 20, 10)
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.iconLlabel = QLabel(FolderEditWidget)
        self.iconLlabel.setObjectName(u"iconLlabel")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(20)
        font.setBold(False)
        self.iconLlabel.setFont(font)
        self.iconLlabel.setAutoFillBackground(True)
        self.iconLlabel.setPixmap(QPixmap(u":/NoteBook/Resources/Folder Closed.png"))
        self.iconLlabel.setScaledContents(False)
        self.iconLlabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.iconLlabel)

        self.folderLabel = QLabel(FolderEditWidget)
        self.folderLabel.setObjectName(u"folderLabel")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.folderLabel.setFont(font1)
        self.folderLabel.setAutoFillBackground(False)
        self.folderLabel.setStyleSheet(u"background-color: rgb(243, 243, 243);")

        self.horizontalLayout.addWidget(self.folderLabel)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(2, 3)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.listWidget = QListWidget(FolderEditWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.PointingHandCursor))
        self.listWidget.setMouseTracking(True)
        self.listWidget.setAutoFillBackground(False)
        self.listWidget.setStyleSheet(u"background-color: rgb(243, 243, 243);\n"
"\n"
"item {\n"
"   padding-left: 40px;\n"
" }")
        self.listWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.listWidget.setFrameShadow(QFrame.Shadow.Plain)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.listWidget.setProperty(u"showDropIndicator", False)

        self.verticalLayout.addWidget(self.listWidget)


        self.retranslateUi(FolderEditWidget)

        QMetaObject.connectSlotsByName(FolderEditWidget)
    # setupUi

    def retranslateUi(self, FolderEditWidget):
        FolderEditWidget.setWindowTitle(QCoreApplication.translate("FolderEditWidget", u"Form", None))
        self.iconLlabel.setText("")
        self.folderLabel.setText(QCoreApplication.translate("FolderEditWidget", u"TextLabel", None))
    # retranslateUi

