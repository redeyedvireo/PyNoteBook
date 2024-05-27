from PySide6 import QtCore, QtSql
from pathlib import Path
import datetime
import logging

from encrypter import Encrypter
from utility import bytesToQByteArray, qByteArrayToBytes, qByteArrayToString, stringToArray

from page_data import PageData, PageDataDict, PageIdDict
from notebook_types import PAGE_TYPE

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

  def setGlobalValue(self, key: str, value: int | str | bytes):
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
      return

    if queryObj.next():
      # Key exists; update its value
      if isinstance(value, int):
        createStr = "update globals set intval=? where key=?"
      elif isinstance(value, str):
        createStr = "update globals set stringval=? where key=?"
      elif isinstance(value, bytes):
        createStr = "update globals set blobval=? where key=?"

        # Must convert to a QByteArray
        valueAsBytes = bytesToQByteArray(value)
      else:
        self.reportError("setGlobalValue: invalid data type")
        return

      queryObj.prepare(createStr)

      queryObj.addBindValue(valueAsBytes)
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
        valueAsBytes = bytesToQByteArray(value)
      else:
        self.reportError("setGlobalValue: invalid data type")
        return

      queryObj.prepare(createStr)

      queryObj.addBindValue(key)
      queryObj.addBindValue(dataType)
      queryObj.addBindValue(valueAsBytes)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError("Error when attempting to set a global value: {}".format(sqlErr.text()))


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


  def getPageOrder(self) -> str | None:
    pageOrder = str(self.getGlobalValue(kPageOrderKey))

    if pageOrder is not None:
      return pageOrder
    else:
      return None

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
      newPage.m_title = qByteArrayToString(queryObj.value(pageTitleField))
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
        tagsList = qByteArrayToString(tagsList).strip()

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

    pageData = PageData()

    while queryObj.next():
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

      pageData.m_contentString = qByteArrayToString(contentsData) if contentsData != '' else ''
      pageData.m_title = qByteArrayToString(titleData) if titleData != '' else ''
      pageData.m_tags = qByteArrayToString(tagData) if tagData != '' else ''
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