# Code to recover lost pages.
import logging

from database import Database
from page_data import PageData, PageDataDict, PageIdDict
from notebook_types import ENTITY_ID, ENTITY_LIST, ENTITY_PAIR, ENTITY_PAIR_LIST, kInvalidPageId

kPageId = 0         # First element of an ENTITY_PAIR_LIST
kParentId = 1       # Second element of an ENTITY_PAIR_LIST

class PageRecovery:
  def __init__(self, pagesAndParentsFromDb: ENTITY_PAIR_LIST, pageTreePageIds: ENTITY_LIST) -> None:
    """ pagesAndParentsFromDb: tuples of page IDs and parent IDs, as retrieved from the database
        pageTreePageIds: List of page IDs from the page tree
    """
    self.pagesAndParentsFromDb = pagesAndParentsFromDb
    self.pageTreeIds = pageTreePageIds

    self.pageIdsInDb = [x[0] for x in self.pagesAndParentsFromDb]

    self.pagesOnDiskSet = set(self.pageIdsInDb)
    self.pagesInTreeSet = set(self.pageTreeIds)

  def thereAreLostPages(self):
    """ Returns True if there are pages in the database that are not included in the page tree.  This
        generally means that the page order string as stored in the database is incomplete, ie, there are
        pages in the database that are not included in the page order string.
    """
    pageDifferenceSet = self.pagesOnDiskSet - self.pagesInTreeSet

    # If there is a non-zero difference, it means that there are lost pages.  These need to be restored.
    return len(pageDifferenceSet) > 0

  def computeLostPagesAndParents(self) -> ENTITY_PAIR_LIST:
    """ Creates an ENTITY_PAIR_LIST (page IDs and their parent IDs) of all pages that are
        missing from the page tree.  These will need to be read from the database and inserted
        into the page tree.
    """
    pageDifferenceSet = self.pagesOnDiskSet - self.pagesInTreeSet
    pageDifferenceList = list(pageDifferenceSet)

    # Construct an ENTITY_PAIR_LIST from the pageDifferenceList (ie, get the parents for the page IDs in pageDifferencesList)
    pagesAndParents = []

    for pageId in pageDifferenceList:
      parentId = self.getParentId(pageId)
      if parentId is not None:
        pagesAndParents.append((pageId, parentId))

    return pagesAndParents

  def getParentId(self, pageId: ENTITY_ID) -> ENTITY_ID | None:
    """ Returns the parent ID of the given page ID, by looking it up in the self.pagesAndParentsFromDb list. """
    for pageAndParent in self.pagesAndParentsFromDb:
      if pageAndParent[kPageId] == pageId:
        return pageAndParent[kParentId]

    return None       # Not found

  def createListOfPagesToInsert(self) -> ENTITY_LIST:
    """ Creates an ordered list of page IDs to insert.  The pages must be inserted in this order, to ensure
        the parents will exist.
    """
    pagesAndParents = self.computeLostPagesAndParents()

    pageIdList = []
    allKnownPageIds = self.pagesInTreeSet.union(self.pagesOnDiskSet)

    while len(pagesAndParents) > 0:
      topItem = pagesAndParents.pop(0)      # Get first item
      topItemPageId = topItem[kPageId]
      topItemParentId = topItem[kParentId]

      # If the page is a top-level item (ie, its parent ID is kInvalidPageId), or its parent exists either in the
      # pageIdList or its parent exists in self.pageTreeIds, then move the page to the pageIdList

      if topItemParentId == kInvalidPageId or topItemParentId in pageIdList or topItemParentId in self.pageTreeIds:
        pageIdList.append(topItemPageId)
      else:
        if topItemParentId in allKnownPageIds:
          # We know the parent does, indeed, exist, but hasn't been re-inserted yet.  So,
          # just add the item to the end of the list.
          pagesAndParents.append(topItem)
        else:
          logging.error(f'Page ID {topItemPageId} has a parent of {topItemParentId} which does not exist')

    return pageIdList

  def recoverPages(self) -> ENTITY_LIST:
    """ Returns a list of page IDs that need to be reloaded from the database, so they can be inserted
    into the page tree.

    Returns:
        ENTITY_LIST: List of page IDs to reload from the database.
    """
    listOfPagesToInsert = self.createListOfPagesToInsert()
    logging.info(f'[PageRecovery.recoverPages] List of pages to insert: {listOfPagesToInsert}')
    return listOfPagesToInsert

