# Class for a page item.
import datetime
from notebook_types import ENTITY_ID, ENTITY_LIST, PAGE_TYPE, kInvalidPageId


class PageData:
  def __init__(self):
    # Public data
    self.m_pageId = kInvalidPageId          # ENTITY_ID
    self.m_parentId = kInvalidPageId        # ENTITY_ID
    self.m_title = ''
    self.m_pageType = PAGE_TYPE.kPageTypeUserText
    self.m_contentString = ''
    self.m_tags = ''
    self.m_previousTags = ''			# Used when updating a page
    self.m_modifiedDateTime = datetime.datetime.now()		# When last modified
    self.m_createdDateTime = datetime.datetime.now()
    self.m_numModifications = 0
    self.m_additionalDataItems: list[str] = []
    self.m_bIsFavorite = False			# True if the page is a "favorite" page

  def additionalItems(self) -> str:
    return ','.join(self.m_additionalDataItems) if len(self.m_additionalDataItems) > 0 else ''


PageDataDict = dict[ENTITY_ID, PageData]      # Used when loading a new Notebook
PageIdDict = dict[ENTITY_ID, list[str]]       # Used when loading a new Notebook