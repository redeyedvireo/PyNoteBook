from typing import Any
import logging
from PySide6 import QtCore
import os.path
import time
import datetime
from datetime import timezone

def julianDayToDate(julianDay: int) -> datetime.date:
  """ Returns a Python date corresponding to the given Julian day. """
  qtDate = QtCore.QDate.fromJulianDay(julianDay)
  date = qtDate.toPyDate()
  return date

def dateToJulianDay(inDate: datetime.date) -> int:
  """ Returns a Julian day for the given Python date. """
  qtDate = QtCore.QDate(inDate.year, inDate.month, inDate.day)    # TODO: Python days and months start with 1.  Same true of QDate?
  return qtDate.toJulianDay()

def formatDateTime(inDateTime: datetime.datetime) -> str:
  return inDateTime.strftime("%B %d, %Y %I:%M %p")

# Format date
def formatDate(inDate: datetime.date) -> str:
  return inDate.strftime("%a %b %d %Y")

# Take a date string, and convert it to a date
def dateFromFormattedString(dateStr: str) -> datetime.date:
  thisDateTime = datetime.datetime.strptime(dateStr, "%a %b %d %Y")
  return thisDateTime.date()

def bytesToQByteArray(data: int | str | bytes) -> QtCore.QByteArray:
  if type(data) is int:
    return QtCore.QByteArray(data.to_bytes(2, 'little'))
  elif type(data) is str:
    return QtCore.QByteArray(bytes(data, 'utf-8'))
  elif type(data) is bytes:
    return QtCore.QByteArray(data)
  else:
    return QtCore.QByteArray()

def qByteArrayToBytes(data: QtCore.QByteArray) -> bytes:
  return data.data()

def qByteArrayToString(data: QtCore.QByteArray) -> str:
  return qByteArrayToBytes(data).decode()

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