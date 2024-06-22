import configparser
import logging
import os.path
from pathlib import Path
from PySide6 import QtCore

from constants import kStartupLoadPreviousLog, \
                      kStartupEmptyWorkspace, \
                      kGeneralStartupLoad, \
                      kEditorDefaultTextSize, \
                      kEditorDefaultFontFamily, \
                      kFilesLastFile, \
                      kRecentFiles, \
                      kWindowSize, \
                      kWindowPos
class Preferences():
  def __init__(self, prefsFilePath) -> None:
    self.prefsFilePath = prefsFilePath

    # Default prefs
    self.prefsMap = {
      kGeneralStartupLoad: kStartupLoadPreviousLog,
      kEditorDefaultTextSize: 10,
      kEditorDefaultFontFamily: 'Arial',
      kFilesLastFile: '',
      kRecentFiles: [],
      kWindowSize: '',
      kWindowPos: ''
    }

  def readPrefsFile(self):
    """ Reads the prefs from the prefs INI file. """
    configObj = configparser.ConfigParser()

    if not os.path.exists(self.prefsFilePath):
      # The prefs file does not exist.  Create it with app defaults
      self.writePrefsFile()
    else:
      try:
        configObj.read(self.prefsFilePath)

        self.prefsMap[kGeneralStartupLoad] = configObj.get('general', 'startupload', fallback=kStartupEmptyWorkspace)
        self.prefsMap[kEditorDefaultTextSize] = configObj.getint('editor', 'defaulttextsize', fallback=10)
        self.prefsMap[kEditorDefaultFontFamily] = configObj.get('browser', 'defaultfontfamily', fallback='Arial')
        self.prefsMap[kFilesLastFile] = configObj.get('files', 'lastfile', fallback='')
        self.prefsMap[kWindowPos] = configObj.get('window', 'pos', fallback='')
        self.prefsMap[kWindowSize] = configObj.get('window', 'size', fallback='')

        # Read recent files list
        if configObj.has_section(kRecentFiles):
          fileList = []
          for key in configObj[kRecentFiles]:
            fileList.append(configObj[kRecentFiles][key])

          self.prefsMap[kRecentFiles] = fileList
      except Exception as inst:
        errMsg = "Exception: {}".format(inst)
        print(errMsg)
        logging.error(f'[readPrefsFile] {errMsg}')

  def writePrefsFile(self):
    configObj = configparser.ConfigParser()

    # Set prefs in in-memory prefs object
    for prefKey in self.prefsMap:
      if prefKey == kRecentFiles:
        if not configObj.has_section(kRecentFiles):
          # The section must be created before data can be stored in it
          configObj[kRecentFiles] = {}

        for index, recentFile in enumerate(self.prefsMap[kRecentFiles]):
          configObj[kRecentFiles][f'file{index}'] = recentFile
      else:
        items = prefKey.split('-')
        section = items[0]
        pref = items[1]

        if not configObj.has_section(section):
          # The section must be created before data can be stored in it
          configObj[section] = {}

        configObj[section][pref] = str(self.prefsMap[prefKey])

    # Write prefs to disk
    try:
      # Make sure the directory exists
      directory = os.path.dirname(self.prefsFilePath)
      path = Path(directory)
      if not path.exists():
        try:
          path.mkdir(parents=True)
        except Exception as inst:
          errMsg = "Creating prefs directory: {}".format(inst)
          print(errMsg)
          logging.error(f'[writePrefsFile] {errMsg}')
          return

      with open(self.prefsFilePath, 'w') as configFile:
        configObj.write(configFile)
    except Exception as inst:
      errMsg = "Writing prefs file: {}".format(inst)
      print(errMsg)
      logging.error(f'[writePrefsFile] {errMsg}')

  def prefsItemExists(self, prefsItem) -> bool:
    if prefsItem in self.prefsMap:
      match self.prefsMap[prefsItem]:
        case str():
          return len(self.prefsMap[prefsItem]) > 0

        case int():
          return True

        case _:
          return True
    else:
      return False

  @property
  def onStartupLoad(self) -> str:
    return kStartupEmptyWorkspace if not self.prefsItemExists(kGeneralStartupLoad) else self.prefsMap[kGeneralStartupLoad]

  @onStartupLoad.setter
  def onStartupLoad(self, value: str):
    self.prefsMap[kGeneralStartupLoad] = value

  @property
  def lastFile(self) -> str:
    return '' if not self.prefsItemExists(kFilesLastFile) else self.prefsMap[kFilesLastFile]

  @lastFile.setter
  def lastFile(self, value: str):
    self.prefsMap[kFilesLastFile] = value

  @property
  def recentFiles(self) -> list[str]:
    return [] if not self.prefsItemExists(kRecentFiles) else self.prefsMap[kRecentFiles]

  @recentFiles.setter
  def recentFiles(self, files: list[str]):
    self.prefsMap[kRecentFiles] = files

  @property
  def editorDefaultFontSize(self) -> int:
    return 10 if not self.prefsItemExists(kEditorDefaultTextSize) else self.prefsMap[kEditorDefaultTextSize]

  @editorDefaultFontSize.setter
  def editorDefaultFontSize(self, value: int):
    self.prefsMap[kEditorDefaultTextSize] = value

  @property
  def editorDefaultFontFamily(self) -> str:
    return 'Arial' if not self.prefsItemExists(kEditorDefaultFontFamily) else self.prefsMap[kEditorDefaultFontFamily]

  @editorDefaultFontFamily.setter
  def editorDefaultFontFamily(self, value: str):
    self.prefsMap[kEditorDefaultFontFamily] = value

  @property
  def windowSize(self) -> QtCore.QSize | None:
    if self.prefsItemExists(kWindowSize):
      width, height = self.prefsMap[kWindowSize].split(',')
      return QtCore.QSize(int(width), int(height))

    return None

  @windowSize.setter
  def windowSize(self, size: QtCore.QSize):
    self.prefsMap[kWindowSize] = f'{size.width()},{size.height()}'

  @property
  def windowPos(self) -> QtCore.QPoint | None:
    if self.prefsItemExists(kWindowPos):
      x, y = self.prefsMap[kWindowPos].split(',')
      return QtCore.QPoint(int(x), int(y))

    return None

  @windowPos.setter
  def windowPos(self, pos: QtCore.QPoint):
    self.prefsMap[kWindowPos] = f'{pos.x()},{pos.y()}'