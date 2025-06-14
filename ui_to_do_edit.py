# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'to_do_edit.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QSizePolicy, QSpacerItem, QToolButton, QTreeView,
    QVBoxLayout, QWidget)

class Ui_ToDoEditWidget(object):
    def setupUi(self, ToDoEditWidget):
        if not ToDoEditWidget.objectName():
            ToDoEditWidget.setObjectName(u"ToDoEditWidget")
        ToDoEditWidget.resize(502, 631)
        self.verticalLayout = QVBoxLayout(ToDoEditWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.newTaskButton = QToolButton(ToDoEditWidget)
        self.newTaskButton.setObjectName(u"newTaskButton")

        self.horizontalLayout.addWidget(self.newTaskButton)

        self.newSubtaskButton = QToolButton(ToDoEditWidget)
        self.newSubtaskButton.setObjectName(u"newSubtaskButton")

        self.horizontalLayout.addWidget(self.newSubtaskButton)

        self.deleteTaskButton = QToolButton(ToDoEditWidget)
        self.deleteTaskButton.setObjectName(u"deleteTaskButton")

        self.horizontalLayout.addWidget(self.deleteTaskButton)

        self.hideDoneTasksButton = QToolButton(ToDoEditWidget)
        self.hideDoneTasksButton.setObjectName(u"hideDoneTasksButton")
        self.hideDoneTasksButton.setCheckable(True)

        self.horizontalLayout.addWidget(self.hideDoneTasksButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeView = QTreeView(ToDoEditWidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setStyleSheet(u"background-color: white;")
        self.treeView.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.treeView.setDragEnabled(True)
        self.treeView.setDragDropMode(QAbstractItemView.InternalMove)
        self.treeView.setDefaultDropAction(Qt.MoveAction)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setAnimated(True)
        self.treeView.setWordWrap(True)

        self.verticalLayout.addWidget(self.treeView)


        self.retranslateUi(ToDoEditWidget)

        QMetaObject.connectSlotsByName(ToDoEditWidget)
    # setupUi

    def retranslateUi(self, ToDoEditWidget):
        ToDoEditWidget.setWindowTitle(QCoreApplication.translate("ToDoEditWidget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.newTaskButton.setToolTip(QCoreApplication.translate("ToDoEditWidget", u"Adds a new top-level task", None))
#endif // QT_CONFIG(tooltip)
        self.newTaskButton.setText(QCoreApplication.translate("ToDoEditWidget", u"New Task", None))
#if QT_CONFIG(tooltip)
        self.newSubtaskButton.setToolTip(QCoreApplication.translate("ToDoEditWidget", u"Adds a new subtask task to the selected task", None))
#endif // QT_CONFIG(tooltip)
        self.newSubtaskButton.setText(QCoreApplication.translate("ToDoEditWidget", u"New Subtask", None))
        self.deleteTaskButton.setText(QCoreApplication.translate("ToDoEditWidget", u"Delete Task", None))
#if QT_CONFIG(tooltip)
        self.hideDoneTasksButton.setToolTip(QCoreApplication.translate("ToDoEditWidget", u"When on, tasks marked as Done are hidden", None))
#endif // QT_CONFIG(tooltip)
        self.hideDoneTasksButton.setText(QCoreApplication.translate("ToDoEditWidget", u"Hide Done Tasks", None))
    # retranslateUi

