from typing import Any
import logging
from PySide6 import QtCore, QtGui
import os.path
import time
from datetime import date, datetime, timezone

def julianDayToDate(julianDay: int) -> date:
  """ Returns a Python date corresponding to the given Julian day. """
  qtDate = QtCore.QDate.fromJulianDay(julianDay)
  date = qtDate.toPython()
  return date     # I think this is a datetime.date, but the documentation doesn't say

def dateToJulianDay(inDate: date) -> int:
  """ Returns a Julian day for the given Python date. """
  qtDate = QtCore.QDate(inDate.year, inDate.month, inDate.day)    # TODO: Python days and months start with 1.  Same true of QDate?
  return qtDate.toJulianDay()

def datesEqual(date1: datetime | date, date2: datetime | date) -> bool:
  date1ToCompare = date1.date() if isinstance(date1, datetime) else date1
  date2ToCompare = date2.date() if isinstance(date2, datetime) else date2

  return date1ToCompare == date2ToCompare

def formatDateTime(inDateTime: datetime) -> str:
  return inDateTime.strftime("%B %d, %Y %I:%M %p")

def formatDateTimeWithDay(inDateTime: datetime) -> str:
  return inDateTime.strftime("%A, %B %d, %Y %I:%M %p")

# Format date
def formatDate(inDate: date) -> str:
  return inDate.strftime("%a %b %d %Y")

# Take a date string, and convert it to a date
def dateFromFormattedString(dateStr: str) -> date:
  thisDateTime = datetime.strptime(dateStr, "%a %b %d %Y")
  return thisDateTime.date()

def toQByteArray(data: int | str | bytes) -> QtCore.QByteArray:
  if type(data) is int:
    return QtCore.QByteArray(data.to_bytes(2, 'little'))
  elif type(data) is str:
    return QtCore.QByteArray(bytes(data, 'utf-8'))
  elif type(data) is bytes:
    return QtCore.QByteArray(data)
  else:
    return QtCore.QByteArray()

def qByteArrayToBytes(data: QtCore.QByteArray) -> bytes:
  if (type(data) is str):
    return bytes(data)
  elif isinstance(data, QtCore.QByteArray):
    return data.data()
  else:
    # Unknown data type
    return data

def qByteArrayToString(data: QtCore.QByteArray) -> str:
  return qByteArrayToBytes(data).decode()

def unknownToString(data: Any) -> str:
  return unknownToBytes(data).decode('utf-8')

def unknownToBytes(data: Any) -> bytes:
  if data is not None:
    try:
      if isinstance(data, QtCore.QByteArray):
        if data.length() > 0:
          return qByteArrayToBytes(data)
        else:
          return b''
      elif isinstance(data, bytes):
        return data
      elif isinstance(data, str):
        return bytes(data, 'utf-8')
      else:
        return bytes(data)
    except:
      logging.error(f'Data conversion error on: "{data}"')
      return b''
  else:
    return b''

def stringToArray(inStr: str) -> list[str]:
  """ Separates a joined list.  The list can be joined by either commas or spaces. """
  resultArray = []
  if len(inStr) > 0:
    if ' ' in inStr:
      resultArray = inStr.split(' ')
    elif ',' in inStr:
      resultArray = inStr.split(',')
    else:
      resultArray = [inStr]      # Just one element

  return resultArray

def pixmapToQByteArray(pixmap: QtGui.QPixmap) -> tuple[bool, QtCore.QByteArray]:
  # From: https://stackoverflow.com/questions/57404778/how-to-convert-a-qpixmaps-image-into-a-bytes
  imageData = QtCore.QByteArray()
  buffer = QtCore.QBuffer(imageData)
  buffer.open(QtCore.QIODevice.OpenModeFlag.WriteOnly)
  success = pixmap.save(buffer, 'PNG')
  buffer.close()

  return (success, imageData)

def qByteArrayToPixmap(data: QtCore.QByteArray) -> tuple[bool, QtGui.QPixmap]:
  # From: https://stackoverflow.com/questions/57404778/how-to-convert-a-qpixmaps-image-into-a-bytes
  byteArray = QtCore.QByteArray(data)
  pixmap = QtGui.QPixmap()
  success = pixmap.loadFromData(byteArray, 'PNG')

  return (success, pixmap)
