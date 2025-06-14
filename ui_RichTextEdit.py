# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RichTextEdit.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFontComboBox,
    QHBoxLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

from ColorButton import CColorButton
from custom_text_edit import CustomTextEdit
import pynotebook_rc

class Ui_RichTextEditWidget(object):
    def setupUi(self, RichTextEditWidget):
        if not RichTextEditWidget.objectName():
            RichTextEditWidget.setObjectName(u"RichTextEditWidget")
        RichTextEditWidget.resize(688, 628)
        self.verticalLayout = QVBoxLayout(RichTextEditWidget)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fontCombo = QFontComboBox(RichTextEditWidget)
        self.fontCombo.setObjectName(u"fontCombo")
        self.fontCombo.setEditable(False)

        self.horizontalLayout_2.addWidget(self.fontCombo)

        self.sizeCombo = QComboBox(RichTextEditWidget)
        self.sizeCombo.setObjectName(u"sizeCombo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizeCombo.sizePolicy().hasHeightForWidth())
        self.sizeCombo.setSizePolicy(sizePolicy)
        self.sizeCombo.setMinimumSize(QSize(45, 0))
        self.sizeCombo.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_2.addWidget(self.sizeCombo)

        self.textColorButton = CColorButton(RichTextEditWidget)
        self.textColorButton.setObjectName(u"textColorButton")
        icon = QIcon()
        icon.addFile(u":/NoteBook/Resources/Text Foreground.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.textColorButton.setIcon(icon)
        self.textColorButton.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.textColorButton)

        self.textBackgroundButton = CColorButton(RichTextEditWidget)
        self.textBackgroundButton.setObjectName(u"textBackgroundButton")
        icon1 = QIcon()
        icon1.addFile(u":/NoteBook/Resources/Text Background.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.textBackgroundButton.setIcon(icon1)
        self.textBackgroundButton.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.textBackgroundButton)

        self.leftAlignButton = QToolButton(RichTextEditWidget)
        self.leftAlignButton.setObjectName(u"leftAlignButton")
        icon2 = QIcon()
        icon2.addFile(u":/NoteBook/Resources/Left.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.leftAlignButton.setIcon(icon2)
        self.leftAlignButton.setIconSize(QSize(16, 16))
        self.leftAlignButton.setCheckable(True)
        self.leftAlignButton.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.leftAlignButton)

        self.centerAlignButton = QToolButton(RichTextEditWidget)
        self.centerAlignButton.setObjectName(u"centerAlignButton")
        icon3 = QIcon()
        icon3.addFile(u":/NoteBook/Resources/Center.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.centerAlignButton.setIcon(icon3)
        self.centerAlignButton.setIconSize(QSize(16, 16))
        self.centerAlignButton.setCheckable(True)
        self.centerAlignButton.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.centerAlignButton)

        self.rightAlignButton = QToolButton(RichTextEditWidget)
        self.rightAlignButton.setObjectName(u"rightAlignButton")
        icon4 = QIcon()
        icon4.addFile(u":/NoteBook/Resources/Right.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rightAlignButton.setIcon(icon4)
        self.rightAlignButton.setIconSize(QSize(16, 16))
        self.rightAlignButton.setCheckable(True)
        self.rightAlignButton.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.rightAlignButton)

        self.boldButton = QToolButton(RichTextEditWidget)
        self.boldButton.setObjectName(u"boldButton")
        font = QFont()
        font.setBold(True)
        self.boldButton.setFont(font)
        icon5 = QIcon()
        icon5.addFile(u":/NoteBook/Resources/Bold.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.boldButton.setIcon(icon5)
        self.boldButton.setIconSize(QSize(16, 16))
        self.boldButton.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.boldButton)

        self.italicButton = QToolButton(RichTextEditWidget)
        self.italicButton.setObjectName(u"italicButton")
        font1 = QFont()
        font1.setItalic(True)
        self.italicButton.setFont(font1)
        icon6 = QIcon()
        icon6.addFile(u":/NoteBook/Resources/Italic.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.italicButton.setIcon(icon6)
        self.italicButton.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.italicButton)

        self.underlineButton = QToolButton(RichTextEditWidget)
        self.underlineButton.setObjectName(u"underlineButton")
        font2 = QFont()
        font2.setUnderline(True)
        self.underlineButton.setFont(font2)
        icon7 = QIcon()
        icon7.addFile(u":/NoteBook/Resources/Underline.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.underlineButton.setIcon(icon7)
        self.underlineButton.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.underlineButton)

        self.strikethroughButton = QToolButton(RichTextEditWidget)
        self.strikethroughButton.setObjectName(u"strikethroughButton")
        icon8 = QIcon()
        icon8.addFile(u":/NoteBook/Resources/Strikethrough.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.strikethroughButton.setIcon(icon8)
        self.strikethroughButton.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.strikethroughButton)

        self.bulletTableInsertButton = QToolButton(RichTextEditWidget)
        self.bulletTableInsertButton.setObjectName(u"bulletTableInsertButton")
        icon9 = QIcon()
        icon9.addFile(u":/NoteBook/Resources/Bullet Table.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bulletTableInsertButton.setIcon(icon9)
        self.bulletTableInsertButton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout_2.addWidget(self.bulletTableInsertButton)

        self.numberTableInsertButton = QToolButton(RichTextEditWidget)
        self.numberTableInsertButton.setObjectName(u"numberTableInsertButton")
        icon10 = QIcon()
        icon10.addFile(u":/NoteBook/Resources/Number Table.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.numberTableInsertButton.setIcon(icon10)
        self.numberTableInsertButton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout_2.addWidget(self.numberTableInsertButton)

        self.tableButton = QToolButton(RichTextEditWidget)
        self.tableButton.setObjectName(u"tableButton")
        icon11 = QIcon()
        icon11.addFile(u":/NoteBook/Resources/Table.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tableButton.setIcon(icon11)

        self.horizontalLayout_2.addWidget(self.tableButton)

        self.insertHLineButton = QToolButton(RichTextEditWidget)
        self.insertHLineButton.setObjectName(u"insertHLineButton")
        icon12 = QIcon()
        icon12.addFile(u":/NoteBook/Resources/Horizontal Line.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.insertHLineButton.setIcon(icon12)

        self.horizontalLayout_2.addWidget(self.insertHLineButton)

        self.indentRightButton = QToolButton(RichTextEditWidget)
        self.indentRightButton.setObjectName(u"indentRightButton")
        icon13 = QIcon()
        icon13.addFile(u":/NoteBook/Resources/IndentRight.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.indentRightButton.setIcon(icon13)

        self.horizontalLayout_2.addWidget(self.indentRightButton)

        self.indentLeftButton = QToolButton(RichTextEditWidget)
        self.indentLeftButton.setObjectName(u"indentLeftButton")
        icon14 = QIcon()
        icon14.addFile(u":/NoteBook/Resources/IndentLeft.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.indentLeftButton.setIcon(icon14)

        self.horizontalLayout_2.addWidget(self.indentLeftButton)

        self.clearFormattingButton = QToolButton(RichTextEditWidget)
        self.clearFormattingButton.setObjectName(u"clearFormattingButton")
        icon15 = QIcon()
        icon15.addFile(u":/NoteBook/Resources/clear-formatting.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clearFormattingButton.setIcon(icon15)

        self.horizontalLayout_2.addWidget(self.clearFormattingButton)

        self.searchButton = QToolButton(RichTextEditWidget)
        self.searchButton.setObjectName(u"searchButton")
        icon16 = QIcon()
        icon16.addFile(u":/NoteBook/Resources/Search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.searchButton.setIcon(icon16)

        self.horizontalLayout_2.addWidget(self.searchButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.styleButton = QToolButton(RichTextEditWidget)
        self.styleButton.setObjectName(u"styleButton")
        self.styleButton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout.addWidget(self.styleButton)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.styleShortcut1 = QToolButton(RichTextEditWidget)
        self.styleShortcut1.setObjectName(u"styleShortcut1")
        self.styleShortcut1.setMinimumSize(QSize(64, 0))
        self.styleShortcut1.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout.addWidget(self.styleShortcut1)

        self.styleShortcut2 = QToolButton(RichTextEditWidget)
        self.styleShortcut2.setObjectName(u"styleShortcut2")
        self.styleShortcut2.setMinimumSize(QSize(64, 0))
        self.styleShortcut2.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout.addWidget(self.styleShortcut2)

        self.styleShortcut3 = QToolButton(RichTextEditWidget)
        self.styleShortcut3.setObjectName(u"styleShortcut3")
        self.styleShortcut3.setMinimumSize(QSize(64, 0))
        self.styleShortcut3.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout.addWidget(self.styleShortcut3)

        self.styleShortcut4 = QToolButton(RichTextEditWidget)
        self.styleShortcut4.setObjectName(u"styleShortcut4")
        self.styleShortcut4.setMinimumSize(QSize(64, 0))
        self.styleShortcut4.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout.addWidget(self.styleShortcut4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.textEdit = CustomTextEdit(RichTextEditWidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.setStyleSheet(u"background-color: white;")

        self.verticalLayout.addWidget(self.textEdit)

        self.richTextEditSearchWidget = QWidget(RichTextEditWidget)
        self.richTextEditSearchWidget.setObjectName(u"richTextEditSearchWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.richTextEditSearchWidget)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.searchHideButton = QPushButton(self.richTextEditSearchWidget)
        self.searchHideButton.setObjectName(u"searchHideButton")
        icon17 = QIcon()
        icon17.addFile(u":/NoteBook/Resources/Close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.searchHideButton.setIcon(icon17)
        self.searchHideButton.setFlat(True)

        self.horizontalLayout_3.addWidget(self.searchHideButton)

        self.searchEdit = QLineEdit(self.richTextEditSearchWidget)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setStyleSheet(u"background-color: white;")

        self.horizontalLayout_3.addWidget(self.searchEdit)

        self.horizontalSpacer_4 = QSpacerItem(5, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.matchCaseCheckBox = QCheckBox(self.richTextEditSearchWidget)
        self.matchCaseCheckBox.setObjectName(u"matchCaseCheckBox")

        self.horizontalLayout_3.addWidget(self.matchCaseCheckBox)

        self.wholeWordCheckBox = QCheckBox(self.richTextEditSearchWidget)
        self.wholeWordCheckBox.setObjectName(u"wholeWordCheckBox")

        self.horizontalLayout_3.addWidget(self.wholeWordCheckBox)

        self.prevButton = QPushButton(self.richTextEditSearchWidget)
        self.prevButton.setObjectName(u"prevButton")

        self.horizontalLayout_3.addWidget(self.prevButton)

        self.nextButton = QPushButton(self.richTextEditSearchWidget)
        self.nextButton.setObjectName(u"nextButton")

        self.horizontalLayout_3.addWidget(self.nextButton)


        self.verticalLayout.addWidget(self.richTextEditSearchWidget)


        self.retranslateUi(RichTextEditWidget)

        QMetaObject.connectSlotsByName(RichTextEditWidget)
    # setupUi

    def retranslateUi(self, RichTextEditWidget):
        RichTextEditWidget.setWindowTitle(QCoreApplication.translate("RichTextEditWidget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.fontCombo.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Font", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sizeCombo.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Font Size", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.textColorButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Text (Foreground) Color", None))
#endif // QT_CONFIG(tooltip)
        self.textColorButton.setText("")
#if QT_CONFIG(tooltip)
        self.textBackgroundButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Background Color", None))
#endif // QT_CONFIG(tooltip)
        self.textBackgroundButton.setText("")
#if QT_CONFIG(tooltip)
        self.leftAlignButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Left Alignment", None))
#endif // QT_CONFIG(tooltip)
        self.leftAlignButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Left", None))
#if QT_CONFIG(tooltip)
        self.centerAlignButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Center Alignment", None))
#endif // QT_CONFIG(tooltip)
        self.centerAlignButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Center", None))
#if QT_CONFIG(tooltip)
        self.rightAlignButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Right Alignment", None))
#endif // QT_CONFIG(tooltip)
        self.rightAlignButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Right", None))
#if QT_CONFIG(tooltip)
        self.boldButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Bold (Ctrl+B)", None))
#endif // QT_CONFIG(tooltip)
        self.boldButton.setText(QCoreApplication.translate("RichTextEditWidget", u"B", None))
#if QT_CONFIG(shortcut)
        self.boldButton.setShortcut(QCoreApplication.translate("RichTextEditWidget", u"Ctrl+B", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.italicButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Italic (Ctrl+I)", None))
#endif // QT_CONFIG(tooltip)
        self.italicButton.setText(QCoreApplication.translate("RichTextEditWidget", u"I", None))
#if QT_CONFIG(shortcut)
        self.italicButton.setShortcut(QCoreApplication.translate("RichTextEditWidget", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.underlineButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Underline (Ctrl+U)", None))
#endif // QT_CONFIG(tooltip)
        self.underlineButton.setText(QCoreApplication.translate("RichTextEditWidget", u"u", None))
#if QT_CONFIG(shortcut)
        self.underlineButton.setShortcut(QCoreApplication.translate("RichTextEditWidget", u"Ctrl+U", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.strikethroughButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Strikethrough", None))
#endif // QT_CONFIG(tooltip)
        self.strikethroughButton.setText(QCoreApplication.translate("RichTextEditWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.bulletTableInsertButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Bulleted List", None))
#endif // QT_CONFIG(tooltip)
        self.bulletTableInsertButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Table", None))
#if QT_CONFIG(tooltip)
        self.numberTableInsertButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Numbered List", None))
#endif // QT_CONFIG(tooltip)
        self.numberTableInsertButton.setText(QCoreApplication.translate("RichTextEditWidget", u".", None))
#if QT_CONFIG(tooltip)
        self.tableButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Table", None))
#endif // QT_CONFIG(tooltip)
        self.tableButton.setText(QCoreApplication.translate("RichTextEditWidget", u".", None))
#if QT_CONFIG(tooltip)
        self.insertHLineButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Horizontal Line", None))
#endif // QT_CONFIG(tooltip)
        self.insertHLineButton.setText(QCoreApplication.translate("RichTextEditWidget", u".", None))
#if QT_CONFIG(tooltip)
        self.indentRightButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Increase Indent", None))
#endif // QT_CONFIG(tooltip)
        self.indentRightButton.setText(QCoreApplication.translate("RichTextEditWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.indentLeftButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Reduce Indent", None))
#endif // QT_CONFIG(tooltip)
        self.indentLeftButton.setText(QCoreApplication.translate("RichTextEditWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.clearFormattingButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Clear all formatting", None))
#endif // QT_CONFIG(tooltip)
        self.clearFormattingButton.setText("")
#if QT_CONFIG(tooltip)
        self.searchButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Search (Alt+S)", None))
#endif // QT_CONFIG(tooltip)
        self.searchButton.setText("")
#if QT_CONFIG(shortcut)
        self.searchButton.setShortcut(QCoreApplication.translate("RichTextEditWidget", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.styleButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Style", None))
#endif // QT_CONFIG(tooltip)
        self.styleButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Apply Style...", None))
        self.styleShortcut1.setText(QCoreApplication.translate("RichTextEditWidget", u"Style 1", None))
        self.styleShortcut2.setText(QCoreApplication.translate("RichTextEditWidget", u"Style 2", None))
        self.styleShortcut3.setText(QCoreApplication.translate("RichTextEditWidget", u"Style 3", None))
        self.styleShortcut4.setText(QCoreApplication.translate("RichTextEditWidget", u"Style 4", None))
        self.searchHideButton.setText("")
        self.matchCaseCheckBox.setText(QCoreApplication.translate("RichTextEditWidget", u"Match Case", None))
        self.wholeWordCheckBox.setText(QCoreApplication.translate("RichTextEditWidget", u"Whole Words", None))
#if QT_CONFIG(tooltip)
        self.prevButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Previous Occurrence (Ctrl+P)", None))
#endif // QT_CONFIG(tooltip)
        self.prevButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Previous", None))
#if QT_CONFIG(shortcut)
        self.prevButton.setShortcut(QCoreApplication.translate("RichTextEditWidget", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.nextButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Next Occurrence (Ctrl+N)", None))
#endif // QT_CONFIG(tooltip)
        self.nextButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Next", None))
#if QT_CONFIG(shortcut)
        self.nextButton.setShortcut(QCoreApplication.translate("RichTextEditWidget", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

