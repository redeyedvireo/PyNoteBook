from PySide6 import QtCore, QtSql, QtGui
from pathlib import Path
import datetime
import logging

from encrypter import Encrypter
from utility import toQByteArray, qByteArrayToBytes, qByteArrayToString, stringToArray, unknownToString, unknownToBytes, toQByteArray, pixmapToQByteArray, qByteArrayToPixmap

from constants import kHashedPwFieldName, kSaltFieldName

from page_data import PageData, PageDataDict, PageIdDict
from notebook_types import PAGE_TYPE, ENTITY_ID, ENTITY_LIST, ENTITY_PAIR, ENTITY_PAIR_LIST, ID_TITLE_LIST, kInvalidPageId

# Global value data type constants
kDataTypeInteger = 0
kDataTypeString = 1
kDataTypeBlob = 2

# Global keys
# TODO: Make this an Enum
kPageHistoryKey = "pagehistory"
kDatabaseVersionId = "databaseversion"
kPageOrderKey = "pageorder"

# Table names
kAdditionalDataTable = "additionaldata"

# Additional data types (for the Additional Data table)
kImageData = 1

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
        return True
      else:
        # Create the database, and all tables
        success = self.createNewDatabase()
        if success:
          logging.info(f'Created new database at: {pathName}')
        else:
          logging.error(f'Encountered errors in creating a new database')
        return success
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
    # Create database tables
    globalsTableSuccess = self.createGlobalsTable()
    pagesTableSuccess = self.createPagesTable()
    additionalDataTableSuccess = self.createAdditionalDataTable()

    return globalsTableSuccess and pagesTableSuccess and additionalDataTableSuccess

  def createGlobalsTable(self):
    """ Creates the globals table. """
    createStr = "create table globals ("
    createStr += "key text UNIQUE, "
    createStr += "datatype int, "
    createStr += "intval int, "
    createStr += "stringval text, "
    createStr += "blobval blob"
    createStr += ")"

    return self.createTable(createStr)

  def createPagesTable(self):
    """ Creates the pages table. """
    createStr = "create table pages ("
    createStr += "pageid integer UNIQUE, "			# Unique Page ID (must not be 0)
    createStr += "parentid integer, "				# Page ID of this page's parent page
    createStr += "created integer, "				# Date and time the page was created, as a time_t
    createStr += "lastmodified integer, "			# Date and time page was last modified, as a time_t
    createStr += "nummodifications integer, "		# Number of modifications made to the page
    createStr += "pagetype integer, "				# Type of page (0=user text, 1=folder, 2=HTML, 3=Javascript)
    createStr += "pagetitle blob, "				# Title of page.  Must be blob to hold encrypted data
    createStr += "contents blob, "					# Must be blob to hold encrypted data
    createStr += "tags blob, "						# Must be blob to hold encrypted data
    createStr += "additionalitems text, "			# Additional items needed by this page.  A string of comma-separated values
    createStr += "isfavorite integer default 0 "	# 1 if the page is a "favorite", 0 if not
    createStr += ")"

    return self.createTable(createStr)

  def createAdditionalDataTable(self):
    """ Create the additional data table.  This table holds supplementary data
	      for pages, such as images, audio clips and video clips."""
    createStr = "create table additionaldata ("
    createStr += "itemid text UNIQUE, "		# Unique ID for this data item (will be a UUID)
    createStr += "type integer, "				  # Type of data (1=image, 2=audio clip, 3=video clip)
    createStr += "contents blob, "				# Data contents.  Can be anything.
    createStr += "parentid integer "			# ID of its containing content data entry (not sure if this is really needed)
    createStr += ")"

    return self.createTable(createStr)


  def createTable(self, creationStr: str):
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare(creationStr)
    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError( "Error when attempting to the globals table: {}".format(sqlErr.text()))
      return False

    return True

  def isPasswordProtected(self):
    return self.globalValueExists(kHashedPwFieldName)

  def setPasswordInMemory(self, plainTextPassword) -> None:
    # First, get the salt value from the database
    salt = self.getGlobalValue(kSaltFieldName)

    if salt is not None and isinstance(salt, bytes):
      self.encrypter.setPasswordAndSalt(plainTextPassword, salt)

  def storePasswordInDatabase(self, plainTextPassword) -> None:
    """ Sets the password for a new log file.  The salt is generated here. """
    if len(plainTextPassword) > 0:
      self.encrypter.setPasswordGenerateSalt(plainTextPassword)
      hashedPassword = self.encrypter.hashedPassword()

      if hashedPassword is not None:
        self.setGlobalValue(kHashedPwFieldName, hashedPassword)
        self.setGlobalValue(kSaltFieldName, self.encrypter.salt)

  def passwordMatch(self, password) -> bool:
    storedHashedPassword = self.getGlobalValue(kHashedPwFieldName)

    if storedHashedPassword is not None and isinstance(storedHashedPassword, str):
      hashedPw = self.encrypter.hashValue(password)

      return storedHashedPassword == hashedPw
    else:
      logging.error(f'[passwordMatch] Error retrieving hashed password.')
      return False

  def getQueryField(self, queryObj, fieldName):
    """Retrieves a field from a query object.  If the field is encrypted, it is decrypted before being returned.

    Args:
        queryObj (_type_): Query object in question
        fieldName (_type_): Field to retrieve

    Returns:
        _type_: string or unknown
    """
    fieldIndex = queryObj.record().indexOf(fieldName)

    # Take encryption into account.
    rawValue = queryObj.value(fieldIndex)

    if self.encrypter.hasPassword():
      # Encypted database
      # Only contents, pagetitle, and tags are encrypted
      if fieldName == 'contents' or fieldName == 'pagetitle' or fieldName == 'tags':
        # Decrypt the field
        rawValueBytes = unknownToBytes(rawValue)
        decryptedValue = self.encrypter.decrypt(rawValueBytes)
        return decryptedValue
      else:
        return rawValue
    else:
      if type(rawValue) is int:
        return rawValue
      return unknownToString(rawValue)

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
      # Key does not exist - create it
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
        valueToStore = valueAsBytes
      else:
        self.reportError("setGlobalValue: invalid data type")
        return False

      queryObj.prepare(createStr)

      queryObj.addBindValue(key)
      queryObj.addBindValue(dataType)
      queryObj.addBindValue(valueToStore)

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

  def getPageHistory(self) -> str | None:
    pageHistory = self.getGlobalValue(kPageHistoryKey)
    return None if (pageHistory is None or pageHistory == '') else str(pageHistory)

  def setPageHistory(self, pageHistoryStr) -> bool:
    return self.setGlobalValue(kPageHistoryKey, pageHistoryStr)

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
      self.reportError(f'[pageExists]: {sqlErr.text()}')
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
      self.reportError(f'[Database.getAllPageIdsAndParents] error: {sqlErr.text()}')
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
      self.reportError(f'getPageList error: {sqlErr.text()}')
      return ({}, False)

    pageDict = {}

    while queryObj.next():
      pageIdField = queryObj.record().indexOf('pageid')
      parentIdField = queryObj.record().indexOf('parentid')
      lastModifiedField = queryObj.record().indexOf('lastmodified')
      pageTypeField = queryObj.record().indexOf('pagetype')

      # Note: getQueryField takes care of decryption
      pageTitle = str(self.getQueryField(queryObj, 'pagetitle'))

      newPage = PageData()

      newPage.m_pageId = queryObj.value(pageIdField)          # This should be an int
      newPage.m_parentId = queryObj.value(parentIdField)
      newPage.m_modifiedDateTime = datetime.datetime.fromtimestamp(queryObj.value(lastModifiedField))
      newPage.m_title = pageTitle
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
      self.reportError(f'getPageList error: {sqlErr.text()}')
      return ({}, False)

    pageIdDict = {}

    while queryObj.next():
      pageId = int(self.getQueryField(queryObj, 'pageid'))

      # Note: getQueryField takes care of decryption
      tagsList = str(self.getQueryField(queryObj, 'tags')).strip()

      tagsArray = stringToArray(tagsList)

      for tag in tagsArray:
        if pageId in pageIdDict:
          tags = pageIdDict[pageId]
          tags.append(tag)      # This updates the copy in the dictionary
        else:
          pageIdDict[pageId] = [tag]

    return (pageIdDict, True)

  def getFavoritePages(self) -> ID_TITLE_LIST:
    """Returns a list of favorite page IDs and their titles.

    Returns:
        list[tuple[ENTITY_ID, str]]: List of tuples where each tuple is a page ID and the page title.
    """
    resultList = []

    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pageid, pagetitle from pages where isfavorite=1")

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.getFavoritePages] error: {sqlErr.text()}')
      return []

    while queryObj.next():
      pageId = self.getQueryField(queryObj, 'pageid')
      pageTitle = unknownToString(self.getQueryField(queryObj, 'pagetitle'))
      resultList.append((pageId, pageTitle))

    return resultList

  def setPageFavoriteStatus(self, pageId: ENTITY_ID, isFavorite: bool) -> bool:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("update pages set isfavorite=? where pageid=?")
    queryObj.addBindValue(isFavorite)
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.setPageFavoriteStatus] error: {sqlErr.text()}')
      return False

    return True

  def getPage(self, pageId) -> PageData | None:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pagetype, parentid, contents, pagetitle, tags, created, lastmodified, nummodifications, additionalitems, isfavorite from pages where pageid=?")
    queryObj.bindValue(0, pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.getPage] error: {sqlErr.text()}')
      return None

    # If queryObj.first() returns False, then the page doesn't exist
    if not queryObj.first():
      return None

    pageData = PageData()

    pageTypeField = queryObj.record().indexOf('pagetype')
    parentIdField = queryObj.record().indexOf('parentid')
    createdField = queryObj.record().indexOf('created')
    lastModifiedDateField = queryObj.record().indexOf('lastmodified')
    numModificationsField = queryObj.record().indexOf("nummodifications")
    additionalItemsField = queryObj.record().indexOf("additionalitems")
    isFavoriteField = queryObj.record().indexOf("isfavorite")

    pageType = queryObj.value(pageTypeField)
    parentId = queryObj.value(parentIdField)
    lastModifiedTime_t = queryObj.value(lastModifiedDateField)
    numModifications = queryObj.value(numModificationsField)
    createdTime_t = queryObj.value(createdField)
    additionalItemsStr = queryObj.value(additionalItemsField)
    bIsFavorite = queryObj.value(isFavoriteField) != 0

    # Note: getQueryField takes care of decryption
    pageData.m_contentString = str(self.getQueryField(queryObj, 'contents'))
    pageData.m_title = str(self.getQueryField(queryObj, 'pagetitle'))
    pageData.m_tags = str(self.getQueryField(queryObj, 'tags'))
    pageData.m_pageId = pageId

    try:
      pageData.m_pageType = PAGE_TYPE(pageType)
    except ValueError:
      self.reportError(f'[Database.getPage]: page type is invalid: {pageType}, for page ID {pageId}')
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

  def getPageTextItems(self, pageId: ENTITY_ID) -> tuple[str, str, str] | None:
    """Gets all text items from a page.  This includes the title, contents, and tags.

    Args:
        pageId (ENTITY_ID): Page ID of page to query

    Returns:
        tuple[str] | None: List of text from the page: [title, contents, tags] or None
        if an error occurred.
    """
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pagetitle, contents, tags from pages where pageid=?")
    queryObj.bindValue(0, pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.getPageTextItems] error: {sqlErr.text()}')
      return None

    # If queryObj.first() returns False, then the page doesn't exist
    if not queryObj.first():
      return None

    # Note: getQueryField takes care of decryption
    pageTitle = str(self.getQueryField(queryObj, 'pagetitle'))
    pageContents = str(self.getQueryField(queryObj, 'contents'))
    tags = str(self.getQueryField(queryObj, 'tags')).strip()

    return (pageTitle, pageContents, tags)

  def updatePage(self, pageData) -> bool:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare('update pages set contents=?, pagetitle=?, tags=?, lastmodified=?, nummodifications=?, additionalitems=?, isfavorite=? where pageid=?')

    # If this is an encrypted Notebook, encrypt data
    contentData = unknownToBytes('')
    titleData = unknownToBytes('')
    tagsData = unknownToBytes('')

    if self.encrypter.hasPassword():
      # Encrypt the content
      contentData = self.encrypter.encrypt(pageData.m_contentString)
      titleData = self.encrypter.encrypt(pageData.m_title)
      tagsData = self.encrypter.encrypt(pageData.m_tags)
    else:
      contentData = pageData.m_contentString
      titleData = pageData.m_title
      tagsData = pageData.m_tags

    # Bytes data must be converted to a QByteArray before storing
    queryObj.addBindValue(toQByteArray(contentData))
    queryObj.addBindValue(toQByteArray(titleData))
    queryObj.addBindValue(toQByteArray(tagsData))
    queryObj.addBindValue(pageData.m_modifiedDateTime.timestamp())
    queryObj.addBindValue(pageData.m_numModifications)
    queryObj.addBindValue(pageData.additionalItems())
    queryObj.addBindValue(pageData.m_bIsFavorite)
    queryObj.addBindValue(pageData.m_pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'updatePage error: {sqlErr.text()}')
      return False

    return True

  def addNewBlankPage(self, pageData: PageData) -> bool:
    """ Creates a blank Notebook page in the database.  The pageData parameter must contain a valid page ID.
        Returns True if successful, False otherwise.
    """
    if pageData.m_pageId == kInvalidPageId:
      self.reportError(f'addNewBlankPage error: invalid page ID')
      return False

    # Encrypt if necessary
    titleData = self.encrypter.encrypt(pageData.m_title) if self.encrypter.hasPassword() else pageData.m_title

    queryObj = QtSql.QSqlQuery()

    numModifications = 0    # This does not count as a modification

    queryObj.prepare("insert into pages (pageid, parentid, created, lastModified, numModifications, pagetype, pagetitle) values (?, ?, ?, ?, ?, ?, ?)")
    queryObj.addBindValue(pageData.m_pageId)
    queryObj.addBindValue(pageData.m_parentId)
    queryObj.addBindValue(pageData.m_createdDateTime.timestamp())
    queryObj.addBindValue(pageData.m_modifiedDateTime.timestamp())		# Last modified date and time is same as created date/time for a new page
    queryObj.addBindValue(numModifications)
    queryObj.addBindValue(pageData.m_pageType.value)
    queryObj.addBindValue(toQByteArray(titleData))        # Must be stored as a QByteArray

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'addNewBlankPage error: {sqlErr.text()}')
      return False

    return True

  def changePageTitle(self, pageId: ENTITY_ID, newTitle: str, isModification: bool) -> bool:
    """ Changes the title of a page.
        isModification indicates whether this change should be recorded as a modification (for example, when
        a page is first created, its title is changed in this manner.  Such a change wouldn't count as a modification).
    """
    # Encrypt if necessary
    titleData = toQByteArray(self.encrypter.encrypt(newTitle)) if self.encrypter.hasPassword() else newTitle

    if isModification:
      # Get current modification count
      if not self.incrementPageModificationCount(pageId):
        return False

    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("update pages set pagetitle=?, lastmodified=? where pageid=?")
    queryObj.addBindValue(titleData)
    queryObj.addBindValue(datetime.datetime.now().timestamp())
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.changePageTitle]: {sqlErr.text()}')
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
      self.reportError(f'incrementPageModificationCount error: {sqlErr.text()}')
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
      self.reportError(f'nextPageId error: {sqlErr.text()}')
      return kInvalidPageId

    fieldNum = queryObj.record().indexOf('maxpageid')

    if queryObj.first():
      nextIdVal = queryObj.value(fieldNum)
      nextId = kInvalidPageId

      try:
        nextId = int(nextIdVal)
      except ValueError:
        # The next ID was probably a space, which would happen in the case of a new database
        nextId = 0      # This will cause the next ID (or first ID) to be 1

      return nextId + 1
    else:
      self.reportError(f'nextPageId error: maxpageid was not returned by the query')
      return kInvalidPageId

  def getPageTitle(self, pageId: ENTITY_ID) -> str | None:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pagetitle from pages where pageid=?")
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.getPageTitle]: {sqlErr.text()}')
      return None

    if queryObj.first():
      # Note: getQueryField takes care of decryption
      pageTitle = str(self.getQueryField(queryObj, 'pagetitle'))
      return pageTitle
    else:
      return None

  def deletePage(self, pageId: ENTITY_ID) -> bool:
    """ Deletes the requested page. """
    queryObj = QtSql.QSqlQuery()

    queryObj.prepare("delete from pages where pageid=?")
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[deletePage]: {sqlErr.text()}')
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
        self.reportError(f'[updatePageParent]: {sqlErr.text()}')
        return False
      else:
        return True
    else:
      # The page does not exist
      return False

  def getFirstPageId(self) -> ENTITY_ID | None:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare("select pageid from pages order by rowid asc limit 1")

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.getFirstPageId] error: {sqlErr.text()}')
      return None

    # If queryObj.first() returns False, then the page doesn't exist
    if not queryObj.first():
      return None
    else:
      val = self.getQueryField(queryObj, 'pageid')

      return val if type(val) == int else None

  def addImage(self, imageName: str, pixmap: QtGui.QPixmap, parentPageId: ENTITY_ID) -> bool:
    # Convert the pixmap to a QByteArray for storage
    # See: https://stackoverflow.com/questions/57404778/how-to-convert-a-qpixmaps-image-into-a-bytes
    pixmapSaveSuccess, imageData = pixmapToQByteArray(pixmap)

    if not pixmapSaveSuccess:
      self.reportError('[Database.addImage] error: Converting pixmap to byte array failed')
      return False

    queryObj = QtSql.QSqlQuery()
    queryObj.prepare(f"insert into {kAdditionalDataTable} (itemid, type, contents, parentid) values (?, ?, ?, ?)")

    queryObj.addBindValue(imageName)
    queryObj.addBindValue(kImageData)
    queryObj.addBindValue(imageData)
    queryObj.addBindValue(parentPageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.addImage] Error when attempting to save an image: {sqlErr.text()}')
      return False

    return True

  def getImage(self, imageName: str) -> QtGui.QPixmap | None:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare(f"select contents from {kAdditionalDataTable} where itemid=?")
    queryObj.addBindValue(imageName)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.getFirstPageId] error: {sqlErr.text()}')
      return None

    if queryObj.first():
      contentsField = queryObj.record().indexOf('contents')
      byteArray = queryObj.value(contentsField)
      pixmapConvertSuccess, pixmap = qByteArrayToPixmap(byteArray)

      if not pixmapConvertSuccess:
        self.reportError('[Database.addImage] error: Converting byte array to pixmap failed')
        return None

      else:
        return pixmap
    else:
      return None

  def getImageNamesForPage(self, pageId: ENTITY_ID) -> list[str]:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare(f"select itemid from {kAdditionalDataTable} where parentid=?")
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.getImageNamesForPage] Error when attempting to retrieve image names: {sqlErr.text()}')
      return []

    nameList = []

    while queryObj.next():
      nameField = queryObj.record().indexOf('itemid')
      imageName = unknownToString(queryObj.value(nameField))
      nameList.append(imageName)

    return nameList

  def deleteAllImagesForPage(self, pageId: ENTITY_ID) -> bool:
    queryObj = QtSql.QSqlQuery()
    queryObj.prepare(f"delete from {kAdditionalDataTable} where parentid=?")
    queryObj.addBindValue(pageId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.ErrorType.NoError:
      self.reportError(f'[Database.deleteAllImagesForPage] error: {sqlErr.text()}')
      return False
    else:
      return True
