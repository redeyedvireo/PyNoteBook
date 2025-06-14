# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'prefs_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFontComboBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QRadioButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        if not PrefsDialog.objectName():
            PrefsDialog.setObjectName(u"PrefsDialog")
        PrefsDialog.resize(526, 385)
        self.verticalLayout = QVBoxLayout(PrefsDialog)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = QListWidget(PrefsDialog)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMaximumSize(QSize(120, 16777215))
        self.listWidget.setAutoFillBackground(True)
        self.listWidget.setStyleSheet(u"background-color: white;")

        self.horizontalLayout.addWidget(self.listWidget)

        self.stackedWidget = QStackedWidget(PrefsDialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.stackedWidget.setSizeIncrement(QSize(0, 0))
        self.application_page = QWidget()
        self.application_page.setObjectName(u"application_page")
        self.verticalLayout_4 = QVBoxLayout(self.application_page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.application_page)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.emptyWorkspaceRadio = QRadioButton(self.groupBox)
        self.emptyWorkspaceRadio.setObjectName(u"emptyWorkspaceRadio")

        self.verticalLayout_3.addWidget(self.emptyWorkspaceRadio)

        self.loadPreviousNotebookRadio = QRadioButton(self.groupBox)
        self.loadPreviousNotebookRadio.setObjectName(u"loadPreviousNotebookRadio")
        self.loadPreviousNotebookRadio.setChecked(True)

        self.verticalLayout_3.addWidget(self.loadPreviousNotebookRadio)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 204, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.application_page)
        self.text_editor_page = QWidget()
        self.text_editor_page.setObjectName(u"text_editor_page")
        self.verticalLayout_2 = QVBoxLayout(self.text_editor_page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.text_editor_page)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.fontSizeCombo = QComboBox(self.text_editor_page)
        self.fontSizeCombo.setObjectName(u"fontSizeCombo")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.fontSizeCombo)

        self.label_2 = QLabel(self.text_editor_page)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.fontCombo = QFontComboBox(self.text_editor_page)
        self.fontCombo.setObjectName(u"fontCombo")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.fontCombo)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalSpacer_2 = QSpacerItem(48, 266, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.text_editor_page)
        self.to_do_list_page = QWidget()
        self.to_do_list_page.setObjectName(u"to_do_list_page")
        self.verticalLayout_5 = QVBoxLayout(self.to_do_list_page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.autoSaveCheckBox = QCheckBox(self.to_do_list_page)
        self.autoSaveCheckBox.setObjectName(u"autoSaveCheckBox")

        self.horizontalLayout_2.addWidget(self.autoSaveCheckBox)

        self.horizontalSpacer = QSpacerItem(298, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(369, 295, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.to_do_list_page)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(PrefsDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.buttonBox = QDialogButtonBox(PrefsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PrefsDialog)
        self.buttonBox.accepted.connect(PrefsDialog.accept)
        self.buttonBox.rejected.connect(PrefsDialog.reject)
        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PrefsDialog)
    # setupUi

    def retranslateUi(self, PrefsDialog):
        PrefsDialog.setWindowTitle(QCoreApplication.translate("PrefsDialog", u"Preferences", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("PrefsDialog", u"Application", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("PrefsDialog", u"Text Editor", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("PrefsDialog", u"To Do List", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.groupBox.setTitle(QCoreApplication.translate("PrefsDialog", u"On Startup", None))
        self.emptyWorkspaceRadio.setText(QCoreApplication.translate("PrefsDialog", u"Empty Workspace", None))
        self.loadPreviousNotebookRadio.setText(QCoreApplication.translate("PrefsDialog", u"Load Previous Notebook", None))
        self.label.setText(QCoreApplication.translate("PrefsDialog", u"Default text size", None))
        self.label_2.setText(QCoreApplication.translate("PrefsDialog", u"Default Font", None))
        self.autoSaveCheckBox.setText(QCoreApplication.translate("PrefsDialog", u"Auto-save", None))
    # retranslateUi

