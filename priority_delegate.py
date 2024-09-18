from PySide6 import QtCore, QtGui, QtWidgets
import logging

class PriorityDelegate(QtWidgets.QStyledItemDelegate):
  def __init__(self, parent: QtWidgets.QWidget | None = None):
    super(PriorityDelegate, self).__init__(parent)

  def createEditor(self, parent: QtWidgets.QWidget, \
                   option: QtWidgets.QStyleOptionViewItem, \
                    index: QtCore.QModelIndex):
    comboBox = QtWidgets.QComboBox(parent)

    # Add priority levels to the combo box
    for i in range(1, 11):
      comboBox.addItem(f'{i}', i)

    return comboBox

  def setEditorData(self, editor: QtWidgets.QWidget, index: QtCore.QModelIndex):
    if type(editor) is QtWidgets.QComboBox:
      comboBox = editor
      # Get priority value from the index.
      # Then, use QComboBox::find to find the combo box item that corresponds to
      # the priority, then set that item as the current one.

      priority = int(index.model().data(index))
      data = comboBox.findData(priority)
      comboBox.setCurrentIndex(data)
    else:
      logging.warning('[PriorityDelegate.setEditorData] editor was not a combo box')

  def setModelData(self, \
                   editor: QtWidgets.QWidget, \
                   model: QtCore.QAbstractItemModel, \
                   index: QtCore.QModelIndex):
    if type(editor) is QtWidgets.QComboBox:
      comboBox = editor

      curComboIndex = comboBox.currentIndex()
      comboData = comboBox.itemData(curComboIndex)
      priorityValue = int(comboData)
      model.setData(index, priorityValue, QtCore.Qt.ItemDataRole.EditRole)
    else:
      logging.warning('[PriorityDelegate.setModelData] editor was not a combo box')
