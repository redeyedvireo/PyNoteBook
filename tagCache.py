
from notebook_types import ENTITY_ID
from page_data import PageIdDict


class TagCache:
  def __init__(self):
    self.tagDict: dict[str, set[ENTITY_ID]] = {}       # Maps tag -> list of pageIds

  def addTag(self, pageId: ENTITY_ID, tag: str) -> None:
    if tag not in self.tagDict:
      self.tagDict[tag] = set()

    self.tagDict[tag].add(pageId)

  def addTags(self, tags: PageIdDict) -> None:
    for pageId, tagsForPage in tags.items():
      for tag in tagsForPage:
        self.addTag(pageId, tag)

  def removePageIdFromTag(self, pageId: ENTITY_ID, tag: str) -> None:
    if tag in self.tagDict:
      if pageId in self.tagDict[tag]:
        pageDict = self.tagDict[tag]
        pageDict.remove(pageId)
        if len(pageDict) == 0:
          del self.tagDict[tag]

  def removePageIdFromAllTags(self, pageId: ENTITY_ID) -> None:
    """Removes the given page ID from all tags.

    Args:
        pageId (ENTITY_ID): ID of page to remove.
    """
    tagsToDelete = []

    for tag, tagsForPage in self.tagDict.items():
      if pageId in tagsForPage:
        self.tagDict[tag].remove(pageId)

        # If the tag is now empty, add it to the list of tags to delete
        if len(self.tagDict[tag]) == 0:
          tagsToDelete.append(tag)

    # Delete any empty tags
    for tag in tagsToDelete:
      del self.tagDict[tag]

  def updateTagsForPage(self, pageId: ENTITY_ID, tags: list[str]) -> None:
    tagsToDelete = []

    # Remove all tags for the page
    for tag, pageSet in self.tagDict.items():
      if pageId in pageSet:
        self.tagDict[tag].remove(pageId)

        # If the tag is now empty, add it to the list of tags to delete
        if len(self.tagDict[tag]) == 0:
          tagsToDelete.append(tag)

    # Delete any empty tags
    for tag in tagsToDelete:
      del self.tagDict[tag]

    # Add the new tags
    for tag in tags:
      self.addTag(pageId, tag)

  def pagesUsingTag(self, tag: str) -> list[ENTITY_ID]:
    if tag in self.tagDict:
      return list(self.tagDict[tag])
    else:
      return []

