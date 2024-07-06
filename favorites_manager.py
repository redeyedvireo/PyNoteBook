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
    if not self.pageExistsInList(pageId):
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

  def getRemovedItems(self, newFavoritesList: ID_TITLE_LIST) -> list[ENTITY_ID]:
    """Returns the list of all page IDs that have been removed.  That is, returns a list
       of all page IDs that exist in self.favoritesList that do not exist in newFavoritesList.

    Args:
        newFavoritesList (ID_TITLE_LIST): New, updated favorites list

    Returns:
        list[ENTITY_ID]: List of page IDs contained in self.favoritesList that
                          don't exist in newFavoritesList.
    """
    removedIds = []

    newPageIds = [ item[0] for item in newFavoritesList ]
    existingPageIds = [ item[0] for item in self.favoritesList ]

    for pageId in existingPageIds:
      if pageId not in newPageIds:
        removedIds.append(pageId)

    return removedIds
