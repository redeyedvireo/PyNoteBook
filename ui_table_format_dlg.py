# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'table_format_dlg.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QHeaderView, QLabel, QSizePolicy,
    QSpacerItem, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from ColorButton import CColorButton

class Ui_TableFormatDlg(object):
    def setupUi(self, TableFormatDlg):
        if not TableFormatDlg.objectName():
            TableFormatDlg.setObjectName(u"TableFormatDlg")
        TableFormatDlg.resize(316, 429)
        self.verticalLayout = QVBoxLayout(TableFormatDlg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(TableFormatDlg)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.rowsSpin = QSpinBox(TableFormatDlg)
        self.rowsSpin.setObjectName(u"rowsSpin")
        self.rowsSpin.setMinimum(1)
        self.rowsSpin.setValue(2)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.rowsSpin)

        self.label_2 = QLabel(TableFormatDlg)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.columnsSpin = QSpinBox(TableFormatDlg)
        self.columnsSpin.setObjectName(u"columnsSpin")
        self.columnsSpin.setMinimum(1)
        self.columnsSpin.setValue(2)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.columnsSpin)

        self.label_5 = QLabel(TableFormatDlg)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.backgroundColorButton = CColorButton(TableFormatDlg)
        self.backgroundColorButton.setObjectName(u"backgroundColorButton")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.backgroundColorButton)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_3 = QLabel(TableFormatDlg)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(True)

        self.verticalLayout.addWidget(self.label_3)

        self.tableWidget = QTableWidget(TableFormatDlg)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEnabled(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.verticalSpacer = QSpacerItem(20, 46, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(TableFormatDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TableFormatDlg)
        self.buttonBox.accepted.connect(TableFormatDlg.accept)
        self.buttonBox.rejected.connect(TableFormatDlg.reject)

        QMetaObject.connectSlotsByName(TableFormatDlg)
    # setupUi

    def retranslateUi(self, TableFormatDlg):
        TableFormatDlg.setWindowTitle(QCoreApplication.translate("TableFormatDlg", u"Create Table", None))
        self.label.setText(QCoreApplication.translate("TableFormatDlg", u"Rows", None))
        self.label_2.setText(QCoreApplication.translate("TableFormatDlg", u"Columns", None))
        self.label_5.setText(QCoreApplication.translate("TableFormatDlg", u"Table Background Color", None))
        self.backgroundColorButton.setText("")
        self.label_3.setText(QCoreApplication.translate("TableFormatDlg", u"Column Widths", None))
    # retranslateUi

