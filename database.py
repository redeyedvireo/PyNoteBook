from PySide6 import QtCore, QtSql
from pathlib import Path
import datetime
import logging

from encrypter import Encrypter
from utility import toQByteArray, qByteArrayToBytes, qByteArrayToString, stringToArray, unknownToString

from page_data import PageData, PageDataDict, PageIdDict
from notebook_types import PAGE_TYPE, ENTITY_ID, ENTITY_LIST, ENTITY_PAIR, ENTITY_PAIR_LIST, kInvalidPageId

# Global value data type constants
kDataTypeInteger = 0
kDataTypeString = 1
kDataTypeBlob = 2

# Global keys
# TODO: Make this an Enum
kPageHistoryKey = "pagehistory"
kDatabaseVersionId = "databaseversion"
kPageOrderKey = "pageorder"

class Database:
  def __init__(self):
    super(Database, self).__init__()
    self.db = None
    self.encrypter = Encrypter()

  def openDatabase(self, pathName) -> bool:
    self.encrypter.clear()
    return self.open(pathName)

  def open(self, pathName) -> bool:
    self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    p = Path(pathName)
    dbExists = p.is_file()

    self.db.setDatabaseName(pathName)

    if self.db.open():
      if dbExists:
        logging.info("Database open")
        self.updateDatabase()
      else:
        # Create the database, and all tables
        self.createNewDatabase()
        logging.info(f'Created new database at: {pathName}')
      return True
    else:
      logging.error("Could not open database")
      return False

  def isDatabaseOpen(self):
    if self.db is not None:
      return self.db.isOpen()
    else:
      return False

  def closeDatabase(self):
    self.close()
    self.encrypter.clear()

  def close(self):
    if self.db is not None:
      self.db.close()

  def reportError(self, errorMessage):
    logging.error(errorMessage)

  def updateDatabase(self):
    """ Updates the database to the current version. """
    # Nothing to do at this point.
    pass

  def createNewDatabase(self):
    # TODO: Create database tables
    pass

  def getQueryField(self, queryObj, fieldName) -> int | str | bytes | None:
    fieldIndex = queryObj.record().indexOf(fieldName)
    return queryObj.value(fieldIndex)

  def getGlobalValue(self, key: str) -> int | str | bytes | None:
    """ Returns the value of a 'global value' for the given key. """
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select datatype from globals where key = ?")
    queryObj.bindValue(0, key)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError("Error when attempting to retrieve a global value key: {}".format(sqlErr.text()))
      return None

    if queryObj.next():
      typeField = queryObj.record().indexOf("datatype")

      dataType = queryObj.value(typeField)
    else:
      # key not found
      return None

    if dataType == kDataTypeInteger:
      createStr = "select intval from globals where key=?"
    elif dataType == kDataTypeString:
      createStr = "select stringval from globals where key=?"
    elif dataType == kDataTypeBlob:
      createStr = "select blobval from globals where key=?"
    else:
      # Unknown data type
      self.reportError("getGlobalValue: unknown data type: {}".format(dataType))
      return None

    # Now that the data type is known, retrieve the data itself.
    queryObj.prepare(createStr)
    queryObj.bindValue(0, key)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()
    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError("Error when attempting to retrieve a page: {}".format(sqlErr.text()))
      return None

    if queryObj.next():
      if dataType == kDataTypeInteger:
        valueField = queryObj.record().indexOf("intval")
      elif dataType == kDataTypeString:
        valueField = queryObj.record().indexOf("stringval")
      elif dataType == kDataTypeBlob:
        valueField = queryObj.record().indexOf("blobval")
      else:
        return None

      value = queryObj.value(valueField)

      if isinstance(value, QtCore.QByteArray):
        value = qByteArrayToBytes(value)

      return value

  def setGlobalValue(self, key: str, value: int | str | bytes) -> bool:
    """ Sets the value of the given key to the given value. """

    # See if the key exists
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select datatype from globals where key = ?")
    queryObj.bindValue(0, key)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError("Error when attempting to determine if a global value exists: {}".format(sqlErr.text()))
      return False

    valueToStore = value

    if queryObj.next():
      # Key exists; update its value
      if isinstance(value, int):
        createStr = "update globals set intval=? where key=?"
      elif isinstance(value, str):
        createStr = "update globals set stringval=? where key=?"
      elif isinstance(value, bytes):
        createStr = "update globals set blobval=? where key=?"
        # Must convert to a QByteArray
        valueToStore = toQByteArray(value)
      else:
        self.reportError("setGlobalValue: invalid data type")
        return False

      queryObj.prepare(createStr)
      queryObj.addBindValue(valueToStore)
      queryObj.addBindValue(key)
    else:
      if isinstance(value, int):
        createStr = "insert into globals (key, datatype, intval) values (?, ?, ?)"
        dataType = kDataTypeInteger
      elif isinstance(value, str):
        createStr = "insert into globals (key, datatype, stringval) values (?, ?, ?)"
        dataType = kDataTypeString
      elif isinstance(value, bytes):
        createStr = "insert into globals (key, datatype, blobval) values (?, ?, ?)"
        dataType = kDataTypeBlob

        # Must convert to a QByteArray
        valueAsBytes = toQByteArray(value)
      else:
        self.reportError("setGlobalValue: invalid data type")
        return False

      queryObj.prepare(createStr)

      queryObj.addBindValue(key)
      queryObj.addBindValue(dataType)
      queryObj.addBindValue(valueAsBytes)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError("Error when attempting to set a global value: {}".format(sqlErr.text()))
      return False

    return True


  def globalValueExists(self, key):
    """ Checks if a global value exists. """
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select datatype from globals where key=?")
    queryObj.addBindValue(key)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      return False
    else:
      atLeastOne = queryObj.next()
      return atLeastOne

  def setPageOrder(self, pageOrderStr) -> bool:
    return self.setGlobalValue(kPageOrderKey, pageOrderStr)

  def getPageOrder(self) -> str | None:
    pageOrder = str(self.getGlobalValue(kPageOrderKey))

    if pageOrder is not None:
      return pageOrder
    else:
      return None

  def pageExists(self, pageId: ENTITY_ID) -> bool:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pageid from pages where pageid=?")
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[pageExists]: {sqlErr.type()}')
      return False

    # If queryObj.first() returns False, then the page doesn't exist
    if not queryObj.first():
      return False
    else:
      return True

  def getAllPageIdsAndParents(self) -> tuple[ENTITY_PAIR_LIST, bool]:
    """ Retrieves page IDs and the parent IDs. """
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pageid, parentid from pages")

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.getAllPageIdsAndParents] error: {sqlErr.type()}')
      return ([(kInvalidPageId, kInvalidPageId)], False)

    pageList = []

    while queryObj.next():
      pageId = self.getQueryField(queryObj, 'pageid')
      parentId = self.getQueryField(queryObj, 'parentid')

      if pageId != kInvalidPageId:
        pageList.append((pageId, parentId))

    return (pageList, True)

  def getPageList(self) -> tuple[PageDataDict, bool]:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pageid, parentid, pagetitle, lastmodified, pagetype from pages order by pagetitle asc")

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'getPageList error: {sqlErr.type()}')
      return ({}, False)

    pageDict = {}

    while queryObj.next():
      pageIdField = queryObj.record().indexOf('pageid')
      parentIdField = queryObj.record().indexOf('parentid')
      pageTitleField = queryObj.record().indexOf('pagetitle')
      lastModifiedField = queryObj.record().indexOf('lastmodified')
      pageTypeField = queryObj.record().indexOf('pagetype')

      # TODO: Check for encryption, and if so, decrypt (page & title) (may need to convert to bytes)


      newPage = PageData()

      newPage.m_pageId = queryObj.value(pageIdField)          # This should be an int
      newPage.m_parentId = queryObj.value(parentIdField)
      newPage.m_modifiedDateTime = datetime.datetime.fromtimestamp(queryObj.value(lastModifiedField))
      newPage.m_title = unknownToString(queryObj.value(pageTitleField))
      newPage.m_pageType = queryObj.value(pageTypeField)

      pageDict[newPage.m_pageId] = newPage

    return (pageDict, True)

  def getTagList(self) -> tuple[PageIdDict, bool]:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pageid, tags from pages")

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'getPageList error: {sqlErr.type()}')
      return ({}, False)

    pageIdDict = {}

    while queryObj.next():
      pageIdField = queryObj.record().indexOf('pageid')
      tagsField = queryObj.record().indexOf('tags')

      pageId = queryObj.value(pageIdField)
      tagsList = queryObj.value(tagsField)

      # TODO: Check for encryption, and if encrypted, decrypt

      if tagsList != '':
        tagsList = unknownToString(tagsList).strip()

      tagsArray = stringToArray(tagsList)

      for tag in tagsArray:
        if pageId in pageIdDict:
          tags = pageIdDict[pageId]
          tags.append(tag)      # This updates the copy in the dictionary
        else:
          pageIdDict[pageId] = [tag]

    return (pageIdDict, True)

  # TODO: Should return an error message
  def getPage(self, pageId) -> PageData | None:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pagetype, parentid, contents, pagetitle, tags, created, lastmodified, nummodifications, additionalitems, isfavorite from pages where pageid=?")
    queryObj.bindValue(0, pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'getPage error: {sqlErr.type()}')
      return None

    # If queryObj.first() returns False, then the page doesn't exist
    if not queryObj.first():
      return None

    pageData = PageData()

    pageTypeField = queryObj.record().indexOf('pagetype')
    parentIdField = queryObj.record().indexOf('parentid')
    contentsField = queryObj.record().indexOf('contents')
    pageTitleField = queryObj.record().indexOf('pagetitle')
    tagsField = queryObj.record().indexOf('tags')
    createdField = queryObj.record().indexOf('created')
    lastModifiedDateField = queryObj.record().indexOf('lastmodified')
    numModificationsField = queryObj.record().indexOf("nummodifications")
    additionalItemsField = queryObj.record().indexOf("additionalitems")
    isFavoriteField = queryObj.record().indexOf("isfavorite")

    pageType = queryObj.value(pageTypeField)
    parentId = queryObj.value(parentIdField)
    contentsData = queryObj.value(contentsField)
    titleData = queryObj.value(pageTitleField)
    tagData = queryObj.value(tagsField)
    lastModifiedTime_t = queryObj.value(lastModifiedDateField)
    numModifications = queryObj.value(numModificationsField)
    createdTime_t = queryObj.value(createdField)
    additionalItemsStr = queryObj.value(additionalItemsField)
    bIsFavorite = queryObj.value(isFavoriteField) != 0

    # TODO: Check for encryption, and if encrypted, decrypt

    pageData.m_contentString = unknownToString(contentsData) if contentsData != '' else ''
    pageData.m_title = unknownToString(titleData) if titleData != '' else ''
    pageData.m_tags = unknownToString(tagData) if tagData != '' else ''
    pageData.m_pageId = pageId

    try:
      pageData.m_pageType = PAGE_TYPE(pageType)
    except ValueError:
      self.reportError(f'getPage: page type is invalid: {pageType}, for page ID {pageId}')
      pageData.m_pageType = PAGE_TYPE.kPageTypeUserText

    pageData.m_parentId = parentId
    pageData.m_modifiedDateTime = datetime.datetime.fromtimestamp(lastModifiedTime_t)
    pageData.m_createdDateTime = datetime.datetime.fromtimestamp(createdTime_t)
    pageData.m_numModifications = numModifications
    pageData.m_bIsFavorite = bIsFavorite

    # Process additional items
    additionalItems = ''
    if additionalItemsStr != '':
      additionalItems = qByteArrayToString(additionalItemsStr).strip()

      if len(additionalItems) > 0:
        pageData.m_additionalDataItems = additionalItems.split(',')

    return pageData

  # TODO: Should return an error message
  def saveNewPage(self, pageData: PageData) -> bool:
    return True

  # TODO: Should return an error message
  def updatePage(self, pageData) -> bool:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare('update pages set contents=?, pagetitle=?, tags=?, lastmodified=?, nummodifications=?, additionalitems=?, isfavorite=? where pageid=?')
    # queryObj.bindValue(0, pageId)
    queryObj.addBindValue(toQByteArray(pageData.m_contentString))
    queryObj.addBindValue(toQByteArray(pageData.m_title))
    queryObj.addBindValue(toQByteArray(pageData.m_tags))
    queryObj.addBindValue(pageData.m_modifiedDateTime.timestamp())
    queryObj.addBindValue(pageData.m_numModifications)
    queryObj.addBindValue(pageData.additionalItems())
    queryObj.addBindValue(pageData.m_bIsFavorite)
    queryObj.addBindValue(pageData.m_pageId)

    # TODO: Check if this is an encrypted Notebook, and if so, encrypt

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'updatePage error: {sqlErr.type()}')
      return False

    return True

  def addNewBlankPage(self, pageData: PageData) -> bool:
    """ Creates a blank Notebook page in the database.  The pageData parameter must contain a valid page ID.
        Returns True if successful, False otherwise.
    """
    if pageData.m_pageId == kInvalidPageId:
      self.reportError(f'addNewBlankPage error: invalid page ID')
      return False

    # TODO: If this is an encrypted notebook, encrypt the content
    titleData = toQByteArray(pageData.m_title)

    queryObj = QtSql.QSqlQuery()

    numModifications = 0    # This does not count as a modification

    queryObj.prepare("insert into pages (pageid, parentid, created, lastModified, numModifications, pagetype, pagetitle) values (?, ?, ?, ?, ?, ?, ?)")
    queryObj.addBindValue(pageData.m_pageId)
    queryObj.addBindValue(pageData.m_parentId)
    queryObj.addBindValue(pageData.m_createdDateTime.timestamp())
    queryObj.addBindValue(pageData.m_modifiedDateTime.timestamp())		# Last modified date and time is same as created date/time for a new page
    queryObj.addBindValue(numModifications)
    queryObj.addBindValue(pageData.m_pageType.value)
    queryObj.addBindValue(titleData)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'addNewBlankPage error: {sqlErr.type()}')
      return False

    return True

  def changePageTitle(self, pageId: ENTITY_ID, newTitle: str, isModification: bool) -> bool:
    """ Changes the title of a page.
        isModification indicates whether this change should be recorded as a modification (for example, when
        a page is first created, its title is changed in this manner.  Such a change wouldn't count as a modification).
    """
    # TODO: If page is encrypted, encrypt the title

    if isModification:
      # Get current modification count
      if not self.incrementPageModificationCount(pageId):
        return False

    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("update pages set pagetitle=?, lastmodified=? where pageid=?")
    queryObj.addBindValue(newTitle)
    queryObj.addBindValue(datetime.datetime.now().timestamp())
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.changePageTitle]: {sqlErr.type()}')
      return False

    return True

  def incrementPageModificationCount(self, pageId: ENTITY_ID) -> bool:
    """ Increases the modification count of a page. """
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select nummodifications from pages where pageid=?")
    queryObj.bindValue(0, pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'incrementPageModificationCount error: {sqlErr.type()}')
      return False

    if not queryObj.first():
      return False

    numModifications = self.getQueryField(queryObj, 'nummodifications')

    if type(numModifications) is int:
      numModifications += 1   # Increment it!

      queryObj.prepare('update pages set nummodifications=? where pageid=?')

      queryObj.addBindValue(numModifications)
      queryObj.addBindValue(pageId)

      queryObj.exec_()

      # Check for errors
      sqlErr = queryObj.lastError()
      if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
        self.reportError(f'[incrementPageModificationCount] page {pageId}: {sqlErr.text()}')
        return False
      else:
        return True
    else:
      self.reportError('[incrementPageModificationCount] nummodifications was not an int')
      return False

  def nextPageId(self) -> ENTITY_ID:
    """ Returns the next available page ID. """
    queryObj = QtSql.QSqlQuery()

    queryObj.prepare("select max(pageid) as maxpageid from pages")

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'nextPageId error: {sqlErr.type()}')
      return kInvalidPageId

    fieldNum = queryObj.record().indexOf('maxpageid')

    if queryObj.first():
      nextId = queryObj.value(fieldNum)
      return nextId + 1
    else:
      self.reportError(f'nextPageId error: maxpageid was not returned by the query')
      return kInvalidPageId

  def deletePage(self, pageId: ENTITY_ID) -> bool:
    """ Deletes the requested page. """
    queryObj = QtSql.QSqlQuery()

    queryObj.prepare("delete from pages where pageid=?")
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[deletePage]: {sqlErr.type()}')
      return False

    return True

  def updatePageParent(self, pageId: ENTITY_ID, newParentId: ENTITY_ID) -> bool:
    if self.pageExists(pageId):
      queryObj = QtSql.QSqlQuery()

      queryObj.prepare("update pages set parentid=? where pageid=?")
      queryObj.addBindValue(newParentId)
      queryObj.addBindValue(pageId)

      queryObj.exec_()

      # Check for errors
      sqlErr = queryObj.lastError()

      if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
        self.reportError(f'[updatePageParent]: {sqlErr.type()}')
        return False
      else:
        return True
    else:
      # The page does not exist
      return False

