from PySide6 import QtWidgets, QtGui

class ColumnTypeComboBox(QtWidgets.QComboBox):
  def __init__(self, parent=None):
    super(ColumnTypeComboBox, self).__init__(parent)
    self.addItem('Fixed', QtGui.QTextLength.Type.FixedLength)
    self.addItem('Percentage', QtGui.QTextLength.Type.PercentageLength)
    self.addItem('Variable', QtGui.QTextLength.Type.VariableLength)
    self.setCurrentIndex(0)  # Default to 'Fixed'

  @property
  def type(self) -> QtGui.QTextLength.Type:
    """ Returns the current column type. """
    return self.currentData()

  @type.setter
  def type(self, columnType: QtGui.QTextLength.Type):
    """ Sets the current column type. """
    if columnType in [QtGui.QTextLength.Type.FixedLength, QtGui.QTextLength.Type.PercentageLength, QtGui.QTextLength.Type.VariableLength]:
      index = self.findData(columnType)
      if index != -1:
        self.setCurrentIndex(index)

