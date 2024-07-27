from PySide6 import QtCore, QtGui, QtWidgets
from typing import TypedDict
import xml.etree.ElementTree as ET

from styleDef import FormatFlag, StyleDef

# Index of first user-defined style item
kUserStyleStartIndex = 0

class StyleManager:
  def __init__(self) -> None:
    self.styles: dict[int, StyleDef] = { }     # This is a Python dictionary

  def isValidStyleId(self, styleId: int) -> int:
    return styleId in self.styles

  def applyStyle(self, textEdit: QtWidgets.QTextEdit, styleId: int):
    if not self.isValidStyleId(styleId):
      return

    selectionCursor = textEdit.textCursor()

    if not selectionCursor.hasSelection():
      return

    styleDef: StyleDef = self.styles[styleId]

    if not styleDef.formatFlags.hasFlag(FormatFlag.NoFormat):
      # Apply font
      selectionFormat = selectionCursor.charFormat()

      if styleDef.formatFlags.hasFlag(FormatFlag.FontFamily):
        selectionFormat.setFontFamily(styleDef.strFontFamily)

      if styleDef.formatFlags.hasFlag(FormatFlag.FontSize):
        selectionFormat.setFontPointSize(styleDef.fontPointSize)

      if styleDef.formatFlags.hasFlag(FormatFlag.FGColorNone):
        selectionFormat.clearForeground()

      if styleDef.formatFlags.hasFlag(FormatFlag.FGColor):
        selectionFormat.setForeground(QtGui.QBrush(styleDef.textColor))

      if styleDef.formatFlags.hasFlag(FormatFlag.BGColorNone):
        selectionFormat.clearBackground()

      if styleDef.formatFlags.hasFlag(FormatFlag.BGColor):
        selectionFormat.setBackground(QtGui.QBrush(styleDef.backgroundColor))

      if styleDef.formatFlags.hasFlag(FormatFlag.Bold):
        selectionFormat.setFontWeight(QtGui.QFont.Weight.Bold if styleDef.bIsBold else QtGui.QFont.Weight.Normal)

      if styleDef.formatFlags.hasFlag(FormatFlag.Italic):
        selectionFormat.setFontItalic(styleDef.bIsItalic)

      if styleDef.formatFlags.hasFlag(FormatFlag.Underline):
        selectionFormat.setFontUnderline(styleDef.bIsUnderline)

      if styleDef.formatFlags.hasFlag(FormatFlag.Strikeout):
        selectionFormat.setFontStrikeOut(styleDef.bIsStrikeout)

      # Apply the cursor to the document
      selectionCursor.setCharFormat(selectionFormat)
      textEdit.setTextCursor(selectionCursor)

  def getStyleIds(self) -> list[int]:
    return list(self.styles)

  def getStyle(self, styleId) -> StyleDef | None:
    return self.styles[styleId] if self.isValidStyleId(styleId) else None

  def addStyle(self, styleDef: StyleDef) -> int:
    if len(self.styles) > 0:
      allIds = list(self.styles)
      allIds.sort()
      highestId = allIds[-1]      # Last element in the list
    else:
      highestId = 0

    newId = highestId + 1
    self.styles[newId] = styleDef
    return newId

  def setStyle(self, styleId: int, styleDef: StyleDef):
    self.styles[styleId] = styleDef

  def deleteStyle(self, styleId: int):
    if self.isValidStyleId(styleId):
      del self.styles[styleId]

  def loadStyleDefs(self, styleDefFilePath: str) -> bool:
    """Loads the styles from a file.  This is an XML file.

    Returns:
        boolean: Truu if successful, False otherwise
    """
    tree = ET.parse(styleDefFilePath)
    root = tree.getroot()

    for child in root:
      styleId, styleDef = self.parseStyle(child)
      self.setStyle(styleId, styleDef)

    return True

  def parseStyle(self, styleNode):
    # print(styleNode.tag, styleNode.attrib)
    # for child in styleNode.iter():
    #   print(f'{child.tag}: {child.get('value')}')

    styleId = styleNode.get('id')
    styleDef = StyleDef()

    styleDef.fontFamily = styleNode.find('fontfamily')
    styleDef.fontPointSize = styleNode.find('pointsize')
    styleDef.noForegroundColor = styleNode.find('fgcolornone')
    styleDef.fgColor = styleNode.find('fgcolor')
    styleDef.noBackgroundColor = styleNode.find('bgcolornone')
    styleDef.isBold = styleNode.find('bold')
    styleDef.isItalic = styleNode.find('italic')
    styleDef.isUnderline = styleNode.find('underline')
    styleDef.isStrikeout = styleNode.find('strikeout')

    return (styleId, styleDef)

  def getChildNodeValue(self, parentNode, childName):
    node = parentNode.find(childName)
    if node is not None:
      return node.get('value')
    else:
      return None
