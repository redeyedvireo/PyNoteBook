# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'table_format_dlg.ui'
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
    QFormLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QSpacerItem, QSpinBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from ColorButton import CColorButton

class Ui_TableFormatDlg(object):
    def setupUi(self, TableFormatDlg):
        if not TableFormatDlg.objectName():
            TableFormatDlg.setObjectName(u"TableFormatDlg")
        TableFormatDlg.resize(295, 369)
        self.verticalLayout = QVBoxLayout(TableFormatDlg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.label = QLabel(TableFormatDlg)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.rowsSpin = QSpinBox(TableFormatDlg)
        self.rowsSpin.setObjectName(u"rowsSpin")
        self.rowsSpin.setMinimum(1)
        self.rowsSpin.setValue(1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.rowsSpin)

        self.label_2 = QLabel(TableFormatDlg)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.columnsSpin = QSpinBox(TableFormatDlg)
        self.columnsSpin.setObjectName(u"columnsSpin")
        self.columnsSpin.setMinimum(1)
        self.columnsSpin.setValue(1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.columnsSpin)


        self.verticalLayout.addLayout(self.formLayout)

        self.headerGroupBox = QGroupBox(TableFormatDlg)
        self.headerGroupBox.setObjectName(u"headerGroupBox")
        self.headerGroupBox.setEnabled(False)
        self.headerGroupBox.setCheckable(True)
        self.horizontalLayout = QHBoxLayout(self.headerGroupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.headerGroupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.headerBackgroundButton = CColorButton(self.headerGroupBox)
        self.headerBackgroundButton.setObjectName(u"headerBackgroundButton")

        self.horizontalLayout.addWidget(self.headerBackgroundButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.headerGroupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label_5 = QLabel(TableFormatDlg)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.backgroundColorButton = CColorButton(TableFormatDlg)
        self.backgroundColorButton.setObjectName(u"backgroundColorButton")

        self.horizontalLayout_2.addWidget(self.backgroundColorButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_3 = QLabel(TableFormatDlg)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(True)

        self.verticalLayout.addWidget(self.label_3)

        self.tableWidget = QTableWidget(TableFormatDlg)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEnabled(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.verticalSpacer = QSpacerItem(20, 14, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(TableFormatDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

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
        self.headerGroupBox.setTitle(QCoreApplication.translate("TableFormatDlg", u"Has Header", None))
        self.label_4.setText(QCoreApplication.translate("TableFormatDlg", u"Header Background", None))
        self.headerBackgroundButton.setText("")
        self.label_5.setText(QCoreApplication.translate("TableFormatDlg", u"Background Color", None))
        self.backgroundColorButton.setText("")
        self.label_3.setText(QCoreApplication.translate("TableFormatDlg", u"Column Widths", None))
    # retranslateUi

