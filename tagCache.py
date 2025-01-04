
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

  def removeTag(self, pageId: ENTITY_ID, tag: str) -> None:
    if tag in self.tagDict:
      self.tagDict[tag].remove(pageId)

      if len(self.tagDict[tag]) == 0:
        del self.tagDict[tag]

  def pagesUsingTag(self, tag: str) -> list[ENTITY_ID]:
    if tag in self.tagDict:
      return list(self.tagDict[tag])
    else:
      return []

