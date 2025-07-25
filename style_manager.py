from PySide6 import QtCore, QtGui, QtWidgets
from typing import TypedDict
import xml.etree.ElementTree as ET
import logging
import os.path

from styleDef import FormatFlag, StyleDef

# Index of first user-defined style item
kUserStyleStartIndex = 0

# Number of style shortcuts
kNumStyleShortcuts = 8
kStyleShortcutNoStyle = -1  # No style assigned to this shortcut

kStyleDefRoot = 'StyleDoc'
kStyleElement = 'Style'

kStyleDefId = 'id'
kStyleDefName = 'name'
kStyleDefDescription = 'description'

kValueAttr = 'value'

kFontFamilyRoot = 'fontfamily'
kPointSizeRoot = 'pointsize'
kFgColorNoneRoot = 'fgcolornone'
kFgColorRoot = 'fgcolor'
kBgColorNoneRoot = 'bgcolornone'
kBgColorRoot = 'bgcolor'
kBoldRoot = 'bold'
kItalicRoot = 'italic'
kUnderlineRoot = 'underline'
kStrikeoutRoot = 'strikeout'

kStyleShortcutElement = 'Shortcut'


class StyleManager:
  def __init__(self) -> None:
    self.styles: dict[int, StyleDef] = { }     # This is a Python dictionary
    self.styleShortcuts = [kStyleShortcutNoStyle for _ in range(kNumStyleShortcuts)]  # Initialize with -1 (no style)

  def numShortcuts(self) -> int:
    return kNumStyleShortcuts

  def getShortcutStyleId(self, shortcutIndex: int) -> int:
    """Returns the style ID for the given shortcut index.
    If the index is invalid, returns kStyleShortcutNoStyle.

    Args:
        shortcutIndex (int): Index of the shortcut (0 to numShortcuts - 1)

    Returns:
        int: Style ID for the shortcut, or kStyleShortcutNoStyle if invalid.
    """
    if shortcutIndex < 0 or shortcutIndex >= self.numShortcuts():
      return kStyleShortcutNoStyle

    return self.styleShortcuts[shortcutIndex]

  def styleShortcutIsValid(self, shortcutIndex: int) -> bool:
    """Checks if the given shortcut index is valid and has a style assigned.

    Args:
        shortcutIndex (int): Index of the shortcut (0 to numShortcuts - 1)

    Returns:
        bool: True if the shortcut index is valid and has a style assigned, False otherwise.
    """
    if shortcutIndex < 0 or shortcutIndex >= self.numShortcuts():
      return False

    return self.styleShortcuts[shortcutIndex] != kStyleShortcutNoStyle

  def setShortcutStyleId(self, shortcutIndex: int, styleId: int):
    """Sets the style ID for the given shortcut index.
    Args:
        shortcutIndex (int): Index of the shortcut (0 to numShortcuts - 1)
        styleId (int): Style ID to set for the shortcut
    """
    if shortcutIndex < 0 or shortcutIndex >= self.numShortcuts():
      return

    if not self.isValidStyleId(styleId):
      return

    self.styleShortcuts[shortcutIndex] = styleId

  def clearStyleShortcut(self, shortcutIndex: int):
    """Clears the style assigned to the given shortcut index.
    Args:
        shortcutIndex (int): Index of the shortcut (0 to numShortcuts - 1)
    """
    if shortcutIndex < 0 or shortcutIndex >= self.numShortcuts():
      return

    self.styleShortcuts[shortcutIndex] = kStyleShortcutNoStyle

  def numStyles(self) -> int:
    return len(self.styles)

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
        boolean: True if successful, False otherwise
    """
    if not os.path.exists(styleDefFilePath):
      return False

    tree = ET.parse(styleDefFilePath)
    root = tree.getroot()

    for child in root:
      if child.tag == kStyleElement:
        styleId, styleDef = self.parseStyle(child)
        self.setStyle(styleId, styleDef)
      elif child.tag == kStyleShortcutElement:
        self.parseStyleShortcut(child)

    return True

  def parseStyle(self, styleNode):
    styleId = styleNode.get(kStyleDefId)
    styleDef = StyleDef()
    styleDef.strName = styleNode.get(kStyleDefName)
    styleDef.strDescription = styleNode.get(kStyleDefDescription)

    styleDef.fontFamily = self.getChildNodeValue(styleNode, 'fontfamily')
    styleDef.pointSize = self.getChildNodeValue(styleNode, 'pointsize')
    styleDef.noForegroundColor = self.getChildNodeValue(styleNode, 'fgcolornone')
    styleDef.fgColor = self.getChildNodeValue(styleNode, 'fgcolor')
    styleDef.noBackgroundColor = self.getChildNodeValue(styleNode, 'bgcolornone')
    styleDef.bgColor = self.getChildNodeValue(styleNode, 'bgcolor')
    styleDef.isBold = self.getChildNodeValue(styleNode, 'bold')
    styleDef.isItalic = self.getChildNodeValue(styleNode, 'italic')
    styleDef.isUnderline = self.getChildNodeValue(styleNode, 'underline')
    styleDef.isStrikeout = self.getChildNodeValue(styleNode, 'strikeout')

    return (int(styleId), styleDef)

  def parseStyleShortcut(self, shortcutNode):
    index = int(shortcutNode.get('index'))
    styleId = int(shortcutNode.get('styleId', kStyleShortcutNoStyle))

    if 0 <= index < self.numShortcuts():
      self.setShortcutStyleId(index, styleId)
    else:
      logging.error(f'[parseStyleShortcut] Invalid shortcut index: {index}')

  def getChildNodeValue(self, parentNode, childName) -> str | None:
    node = parentNode.find(childName)
    if node is not None:
      return node.get('value')
    else:
      return None

  def saveStyleDefs(self, styleDefFilePath: str) -> bool:
    """Saves the style defs.

    Args:
        styleDefFilePath (str): Path to style definition file.

    Returns:
        bool: Returns True if successful, False otherwise.
    """
    root = ET.Element(kStyleDefRoot)

    styleIds = self.getStyleIds()

    for styleId in styleIds:
      styleDef = self.getStyle(styleId)
      if styleDef is not None:
        self.addStyleToDom(root, styleDef, styleId)

    # Store style shortcuts
    for i in range(self.numShortcuts()):
      styleId = self.getShortcutStyleId(i)
      self.addShortcutToDom(root,  i, styleId)

    elementTree = ET.ElementTree(root)

    try:
      ET.indent(elementTree)
      elementTree.write(styleDefFilePath, encoding='utf-8')
    except Exception as inst:
      logging.error(f'[saveStyleDefs] Exception: type: {type(inst)}')
      logging.error(f'[saveStyleDefs] Exception args: {inst.args}')
      logging.error(f'[saveStyleDefs] Exception object: {inst}')
      return False

    return True

  def addStyleToDom(self, domRoot: ET.Element, styleDef: StyleDef, styleId: int):
    styleDefRoot = ET.SubElement(domRoot, kStyleElement)

    # Main node
    styleDefRoot.set(kStyleDefId, str(styleId))
    styleDefRoot.set(kStyleDefName, styleDef.strName)
    styleDefRoot.set(kStyleDefDescription, styleDef.strDescription)

    # Sub-nodes
    self.addStyleNode(styleDefRoot, kFontFamilyRoot, styleDef.fontFamily)
    self.addStyleNode(styleDefRoot, kPointSizeRoot, styleDef.pointSize)
    self.addStyleNode(styleDefRoot, kFgColorNoneRoot, styleDef.noForegroundColor)
    self.addStyleNode(styleDefRoot, kFgColorRoot, styleDef.fgColor)
    self.addStyleNode(styleDefRoot, kBgColorNoneRoot, styleDef.noBackgroundColor)
    self.addStyleNode(styleDefRoot, kBgColorRoot, styleDef.bgColor)
    self.addStyleNode(styleDefRoot, kBoldRoot, styleDef.isBold)
    self.addStyleNode(styleDefRoot, kItalicRoot, styleDef.isItalic)
    self.addStyleNode(styleDefRoot, kUnderlineRoot, styleDef.isUnderline)
    self.addStyleNode(styleDefRoot, kStrikeoutRoot, styleDef.isStrikeout)


  def addStyleNode(self, parentNode: ET.Element, nodeName: str, value: str | int | bool | QtGui.QColor | None):
    if value is not None:
      root = ET.SubElement(parentNode, nodeName)

      if type(value) is str:
        root.set(kValueAttr, value)
      elif type(value) is int:
        root.set(kValueAttr, str(value))
      elif type(value) is bool:
        root.set(kValueAttr, 'yes' if value else 'no')
      elif type(value) is QtGui.QColor:
        root.set(kValueAttr, value.name())
      else:
        print(f'[addStyleNode] Unknown type for {nodeName}: {value}')

  def addShortcutToDom(self, domRoot: ET.Element, shortcutIndex: int, styleId: int):
    shortcutNode = ET.SubElement(domRoot, kStyleShortcutElement)

    shortcutNode.set('index', str(shortcutIndex))
    shortcutNode.set('styleId', str(styleId))
