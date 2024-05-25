from PySide6 import QtCore, QtWidgets, QtGui
from notebook_types import ENTITY_ID

class CTagList(QtWidgets.QListWidget):
  def __init__(self, parent):
    super(CTagList, self).__init__(parent)

  def addItems(self, pageIdDict) -> None:
    tagsAdded = []      # Used to prevent duplicates from being added

    for pageId, tagsArray in pageIdDict.items():
      for tag in tagsArray:
        if tag not in tagsAdded:
          self.addTag(pageId, tag)
          tagsAdded.append(tag)

  def addTag(self, pageId: ENTITY_ID, tag: str) -> None:
	  # Add to the list
    newItem = QtWidgets.QListWidgetItem(tag)

    newItem.setData(QtCore.Qt.ItemDataRole.UserRole, pageId)
    self.addItem(newItem)
