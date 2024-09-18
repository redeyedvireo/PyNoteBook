from PySide6 import QtCore, QtGui, QtWidgets

from typing import Self
from task_constants import kDoneColumn, kPriorityColumn, kTaskColumn

class ToDoItem(QtGui.QStandardItem):
  def __init__(self, text: str):
    super(ToDoItem, self).__init__(text)

  def __lt__(self, other: 'ToDoItem') -> bool:
    # The sort order places done items as the lowest priority, so that
    # the list will place all non-done items before all done items,
    # and within each group (done and non-done), items will be sorted
    # by priority.
    thisItemIsDone = self.isTaskDone()
    otherItemIsDone = other.isTaskDone()

    thisItemPriority = self.priority()
    otherItemPriority = other.priority()

    if thisItemIsDone != otherItemIsDone:
      # If the "doneness" is different, then whichever one is done
      # has the lesser value (ie, is higher priority).
      return not thisItemIsDone
    else:
      # If both items are either done or not done, then priority
      #is the determining factor.
      return thisItemPriority < otherItemPriority

  def getSibling(self, col: int) -> 'ToDoItem | None':
    if self.column() == col:
      return self
    else:
      siblingIndex = self.model().sibling(self.row(), col, self.index())
      sibling = self.model().itemFromIndex(siblingIndex)
      # The following line shows an error in the editor, but the code works OK
      return sibling if sibling is not None else None

  def getDoneItem(self) -> 'ToDoItem | None':
    return self.getSibling(kDoneColumn)

  def getPriorityItem(self) -> 'ToDoItem | None':
    return self.getSibling(kPriorityColumn)

  def getTaskItem(self) -> 'ToDoItem | None':
    return self.getSibling(kTaskColumn)

  def isTaskDone(self) -> bool:
    doneItem = self.getDoneItem()
    return doneItem.checkState() == QtCore.Qt.CheckState.Checked if doneItem is not None else False

  def isChildTaskDone(self, row: int) -> bool:
    child = self.getChildTask(row)
    return child.isTaskDone() if child is not None else False

  def priority(self) -> int:
    priorityItem = self.getPriorityItem()
    return priorityItem.data(QtCore.Qt.ItemDataRole.DisplayRole) if priorityItem is not None else 0

  def updateParentDoneStatus(self):
    parent = self.parent()

    if type(parent) is ToDoItem:
      currentDoneStatus = parent.isTaskDone()

      # If all subtasks are done, then the parent task is done.
      numRows = parent.rowCount()
      allSubTasksDone = False

      if numRows > 0:
        childrenDoneFlags = []

        for row in range(numRows):
          childrenDoneFlags.append(parent.isChildTaskDone(row))

        allSubTasksDone = all(childrenDoneFlags)
      else:
        allSubTasksDone = currentDoneStatus

      if currentDoneStatus != allSubTasksDone:
        # The status has changed.  Must update it.  If all subtasks are done,
        # then mark the parent as done.  If they are not all done, mark
        # the parent as not done.
        parent.markTaskDone(allSubTasksDone)
        parent.crossOutTask(allSubTasksDone)
        parent.updateParentDoneStatus()

  def markTaskDone(self, done: bool):
    doneItem = self.getDoneItem()
    if doneItem is not None:
      doneItem.setCheckState(QtCore.Qt.CheckState.Checked if done else QtCore.Qt.CheckState.Unchecked)

  def markSubtasksAsDone(self, done: bool, crossOutSubtasks: bool):
    doneItem = self.getDoneItem()
    if doneItem is not None:
      numRows = doneItem.rowCount()
      for row in range(numRows):
        childItem = doneItem.getChildTask(row)
        if childItem is not None:
          childItem.markTaskDone(done)

          if crossOutSubtasks:
            childItem.crossOutTask(done)

  def crossOutTask(self, doCrossOut: bool):
    taskItem = self.getTaskItem()
    if taskItem is not None:
      font = taskItem.font()
      font.setStrikeOut(doCrossOut)
      taskItem.setFont(font)

  def getChildTask(self, row: int) -> 'ToDoItem | None':
    childItem = self.child(row, kDoneColumn)
    # The following line shows an error in the editor, but the code works OK
    return childItem if childItem is not None else None
