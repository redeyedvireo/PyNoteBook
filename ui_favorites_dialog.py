# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'favorites_dialog.ui'
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
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_favoritesDialog(object):
    def setupUi(self, favoritesDialog):
        if not favoritesDialog.objectName():
            favoritesDialog.setObjectName(u"favoritesDialog")
        favoritesDialog.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(favoritesDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(favoritesDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.listWidget = QListWidget(favoritesDialog)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setStyleSheet(u"background-color: white")

        self.verticalLayout_2.addWidget(self.listWidget)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buttonBox = QDialogButtonBox(favoritesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.removeButton = QPushButton(favoritesDialog)
        self.removeButton.setObjectName(u"removeButton")

        self.verticalLayout.addWidget(self.removeButton)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(favoritesDialog)
        self.buttonBox.accepted.connect(favoritesDialog.accept)
        self.buttonBox.rejected.connect(favoritesDialog.reject)

        QMetaObject.connectSlotsByName(favoritesDialog)
    # setupUi

    def retranslateUi(self, favoritesDialog):
        favoritesDialog.setWindowTitle(QCoreApplication.translate("favoritesDialog", u"Manage Favorites", None))
        self.label.setText(QCoreApplication.translate("favoritesDialog", u"Favorites", None))
        self.removeButton.setText(QCoreApplication.translate("favoritesDialog", u"Remove", None))
    # retranslateUi

