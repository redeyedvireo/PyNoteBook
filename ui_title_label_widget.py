# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'title_label_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)

from clickable_label import CClickableLabel
import pynotebook_rc

class Ui_CTitleLabelWidget(object):
    def setupUi(self, CTitleLabelWidget):
        if not CTitleLabelWidget.objectName():
            CTitleLabelWidget.setObjectName(u"CTitleLabelWidget")
        CTitleLabelWidget.resize(697, 28)
        self.verticalLayout = QVBoxLayout(CTitleLabelWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.favoritesLabel = CClickableLabel(CTitleLabelWidget)
        self.favoritesLabel.setObjectName(u"favoritesLabel")
        self.favoritesLabel.setMaximumSize(QSize(16, 16))
        self.favoritesLabel.setPixmap(QPixmap(u":/NoteBook/Resources/star-outline.png"))
        self.favoritesLabel.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.favoritesLabel)

        self.stackedWidget = QStackedWidget(CTitleLabelWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout = QHBoxLayout(self.page)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pageTitleLabel = QLabel(self.page)
        self.pageTitleLabel.setObjectName(u"pageTitleLabel")
        font = QFont()
        font.setFamilies([u"Open Sans"])
        font.setPointSize(14)
        font.setBold(True)
        self.pageTitleLabel.setFont(font)

        self.horizontalLayout.addWidget(self.pageTitleLabel)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_2 = QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pageTitleCombo = QComboBox(self.page_2)
        self.pageTitleCombo.setObjectName(u"pageTitleCombo")
        self.pageTitleCombo.setEditable(True)
        self.pageTitleCombo.setMaxVisibleItems(50)
        self.pageTitleCombo.setInsertPolicy(QComboBox.InsertAtBottom)
        self.pageTitleCombo.setDuplicatesEnabled(True)

        self.horizontalLayout_2.addWidget(self.pageTitleCombo)

        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(CTitleLabelWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CTitleLabelWidget)
    # setupUi

    def retranslateUi(self, CTitleLabelWidget):
        CTitleLabelWidget.setWindowTitle(QCoreApplication.translate("CTitleLabelWidget", u"TitleLabelWidget", None))
        self.favoritesLabel.setText("")
        self.pageTitleLabel.setText(QCoreApplication.translate("CTitleLabelWidget", u"-", None))
    # retranslateUi

