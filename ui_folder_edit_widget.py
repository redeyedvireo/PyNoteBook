# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'folder_edit_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_FolderEditWidget(object):
    def setupUi(self, FolderEditWidget):
        if not FolderEditWidget.objectName():
            FolderEditWidget.setObjectName(u"FolderEditWidget")
        FolderEditWidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(FolderEditWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(FolderEditWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)


        self.retranslateUi(FolderEditWidget)

        QMetaObject.connectSlotsByName(FolderEditWidget)
    # setupUi

    def retranslateUi(self, FolderEditWidget):
        FolderEditWidget.setWindowTitle(QCoreApplication.translate("FolderEditWidget", u"Form", None))
    # retranslateUi

