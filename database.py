from PySide6 import QtCore, QtSql
from pathlib import Path
import datetime
import logging

from encrypter import Encrypter
from utility import bytesToQByteArray, qByteArrayToBytes

# Global value data type constants
kDataTypeInteger = 0
kDataTypeString = 1
kDataTypeBlob = 2

# Global keys
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
