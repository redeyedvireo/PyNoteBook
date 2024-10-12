from PySide6 import QtCore, QtWidgets, QtGui

from database import Database
from notebook_types import ENTITY_ID

# Number of letters to use in a random image name.
kNumLettersInImageName = 10

class TextImage:
  def __init__(self) -> None:
    pass

  @staticmethod
  def generateRandomImageName():
    uuid = QtCore.QUuid.createUuid()
    return uuid.toString()

  @staticmethod
  def insertImageIntoDocument(document: QtGui.QTextDocument, cursor: QtGui.QTextCursor, imageFilePath: str, pageId: ENTITY_ID, database: Database):
    pixmap = QtGui.QPixmap(imageFilePath)
    randomImageName = TextImage.generateRandomImageName()

    document.addResource(QtGui.QTextDocument.ResourceType.ImageResource, QtCore.QUrl(randomImageName), pixmap)

    success = database.addImage(randomImageName, pixmap, pageId)

    if success:
      imageFormat = QtGui.QTextImageFormat()
      imageFormat.setName(randomImageName)
      cursor.insertImage(imageFormat)



