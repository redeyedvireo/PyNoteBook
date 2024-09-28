# This is for a part of a To Do item, such as the Done, Priority, or Task parts.

from PySide6 import QtCore, QtGui, QtWidgets

from typing import Self
from task_constants import kDoneColumn, kPriorityColumn, kTaskColumn

# Would like to import ToDoItem, but can't because it causes a circular dependency.
# from to_do_item import ToDoItem

class ToDoItemPart(QtGui.QStandardItem):
  def __init__(self, text: str):
    super(ToDoItemPart, self).__init__(text)

  def __lt__(self, other: 'ToDoItemPart') -> bool:
    # The sort order places done items as the lowest priority, so that
    # the list will place all non-done items before all done items,
    # and within each group (done and non-done), items will be sorted
    # by priority.
    from to_do_item import ToDoItem
    toDoItemContainer = self.getToDoItemContainer()
    otherToDoItemContainer = other.getToDoItemContainer()

    if type(toDoItemContainer) is ToDoItem and type(otherToDoItemContainer) is ToDoItem:
      thisItemIsDone = toDoItemContainer.isTaskDone()
      otherItemIsDone = otherToDoItemContainer.isTaskDone()

      thisItemPriority = toDoItemContainer.priority
      otherItemPriority = otherToDoItemContainer.priority

      if thisItemIsDone != otherItemIsDone:
        # If the "doneness" is different, then whichever one is done
        # has the lesser value (ie, is higher priority).
        return not thisItemIsDone
      else:
        # If both items are either done or not done, then priority
        #is the determining factor.
        return thisItemPriority < otherItemPriority
    else:
      return False      # Should never get here

  def getToDoItemContainer(self):
    """Returns the ToDoItem 'container' of this ToDoItemPart

    Returns:
        ToDoItem: Container item
                  Note: can't declare the return type due to a circular import
    """
    return self.data(QtCore.Qt.ItemDataRole.UserRole)

  def getValue(self) -> str:
    return self.data(QtCore.Qt.ItemDataRole.DisplayRole)

  def isChecked(self) -> bool:
    """ Gets the checked state of the item, if it is checkable.  If not, False is returned. """
    return self.checkState() == QtCore.Qt.CheckState.Checked if self.isCheckable() else False
