# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'favorites_widget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_CFavoritesWidget(object):
    def setupUi(self, CFavoritesWidget):
        if not CFavoritesWidget.objectName():
            CFavoritesWidget.setObjectName(u"CFavoritesWidget")
        CFavoritesWidget.resize(380, 404)
        self.verticalLayout = QVBoxLayout(CFavoritesWidget)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.removeSelectedButton = QPushButton(CFavoritesWidget)
        self.removeSelectedButton.setObjectName(u"removeSelectedButton")

        self.horizontalLayout.addWidget(self.removeSelectedButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.clearButton = QPushButton(CFavoritesWidget)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout.addWidget(self.clearButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.favoritesListWidget = QListWidget(CFavoritesWidget)
        self.favoritesListWidget.setObjectName(u"favoritesListWidget")
        self.favoritesListWidget.setSelectionMode(QAbstractItemView.NoSelection)

        self.verticalLayout.addWidget(self.favoritesListWidget)


        self.retranslateUi(CFavoritesWidget)

        QMetaObject.connectSlotsByName(CFavoritesWidget)
    # setupUi

    def retranslateUi(self, CFavoritesWidget):
        CFavoritesWidget.setWindowTitle(QCoreApplication.translate("CFavoritesWidget", u"CFavoritesWidget", None))
        self.removeSelectedButton.setText(QCoreApplication.translate("CFavoritesWidget", u"Remove Selected", None))
        self.clearButton.setText(QCoreApplication.translate("CFavoritesWidget", u"Remove All", None))
    # retranslateUi

