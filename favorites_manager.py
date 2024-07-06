from PySide6 import QtCore, QtWidgets, QtGui
from typing import Callable
from copy import deepcopy
from notebook_types import ENTITY_ID, ID_TITLE, ID_TITLE_LIST

class FavoritesManager:
  def __init__(self):
    self.favoritesList: ID_TITLE_LIST = []

  def clear(self):
    self.favoritesList = []

  def setFavoriteItems(self, favoritePages: ID_TITLE_LIST):
    self.favoritesList = favoritePages

  def addFavoriteItem(self, pageId: ENTITY_ID, pageTitle: str):
    if self.pageExistsInList(pageId):
      self.favoritesList.append((pageId, pageTitle))

  def removeFavoriteItem(self, pageId: ENTITY_ID):
    # Remove from list
    for index, item in enumerate(self.favoritesList):
      if item[0] == pageId:
        self.favoritesList.pop(index)
        return

  def pageExistsInList(self, pageId: ENTITY_ID) -> bool:
    for favoriteItem in self.favoritesList:
      if favoriteItem[0] == pageId:
        return True

    return False   # Not found
