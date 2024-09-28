# This is for a part of a To Do item, such as the Done, Priority, or Task parts.

from PySide6 import QtCore, QtGui, QtWidgets

from typing import Self
from task_constants import kDoneColumn, kPriorityColumn, kTaskColumn

# Would like to import ToDoItem, but can't because it causes a circular dependency.
# from to_do_item import ToDoItem

class ToDoItemPart(QtGui.QStandardItem):
  def __init__(self, text: str):
    super(ToDoItemPart, self).__init__(text)

  @property
  def checked(self) -> bool:
    return self.checkState() == QtCore.Qt.CheckState.Checked if self.isCheckable() else False

  @checked.setter
  def checked(self, checked: bool):
    self.setCheckState(QtCore.Qt.CheckState.Checked if checked else QtCore.Qt.CheckState.Unchecked)

  # The 'container' is the ToDoItem object, which contains each of the 3 parts (donePart, priorityPart, taskTextPart)
  # Note: can't declare the return type due to a circular import
  @property
  def container(self):
    return self.data(QtCore.Qt.ItemDataRole.UserRole)

  @container.setter
  def container(self, container):
    self.setData(container, QtCore.Qt.ItemDataRole.UserRole)

  def __lt__(self, other: 'ToDoItemPart') -> bool:
    # The sort order places done items as the lowest priority, so that
    # the list will place all non-done items before all done items,
    # and within each group (done and non-done), items will be sorted
    # by priority.
    from to_do_item import ToDoItem
    toDoItemContainer = self.container
    otherToDoItemContainer = other.container

    if type(toDoItemContainer) is ToDoItem and type(otherToDoItemContainer) is ToDoItem:
      thisItemIsDone = toDoItemContainer.done
      otherItemIsDone = otherToDoItemContainer.done

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

  def getValue(self) -> str:
    return self.data(QtCore.Qt.ItemDataRole.DisplayRole)
