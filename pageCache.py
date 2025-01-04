
from page_data import PageDataDict
from notebook_types import ENTITY_ID


class PageCache:
  """Implements a simple page cache.  The cache is a dictionary that maps page IDs to page titles.
  """
  def __init__(self, capacity=100):
    self.pageDict: dict[ENTITY_ID, str] = {}

  def addPages(self, pages: PageDataDict) -> None:
    for pageId, pageData in pages.items():
      self.pageDict[pageId] = pageData.m_title

  def addPage(self, pageId: ENTITY_ID, title: str) -> None:
    self.pageDict[pageId] = title

  def removePage(self, pageId: ENTITY_ID) -> None:
    if pageId in self.pageDict:
      del self.pageDict[pageId]

  def pageTitle(self, pageId: ENTITY_ID) -> str:
    return self.pageDict.get(pageId, '')

  def updatePageTitleForPage(self, pageId: ENTITY_ID, title: str) -> None:
    self.pageDict[pageId] = title

  def clear(self):
    self.pageDict.clear()
