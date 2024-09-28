# This represents a complete task, either a top-level task, or a subtask.  It consists
# of 3 parts: the Done part, the Priorty part, and the Task part.
# Note that this object (which I refer to as a "container") is not a QObject; it does
# not get inserted into the QTreeView.

from PySide6 import QtCore, QtGui, QtWidgets
from typing import Self

from to_do_item_part import ToDoItemPart

from task_constants import kDoneColumn, kPriorityColumn, kTaskColumn
from taskdef import TaskDef, Task

class ToDoItem:
  def __init__(self, done: bool, priority: int, taskText: str, parentContainer: Self | None = None):
    """Creates a ToDoItem.

    Args:
        done (bool): Whether this task is done
        priority (int): Priority of this task
        taskText (str): Task text
        parentContainer (Self | None, optional): Parent ToDoItem container, if this is a subtask;
                                                  otherwise None. Defaults to None.
    """
    super(ToDoItem, self).__init__()

    self.done = done
    self.priority = priority
    self.taskText = taskText
    self.parentContainer = parentContainer

    # The data of each item contains its container (ie, this object)
    self.donePart = ToDoItemPart('')
    self.donePart.setData(self, QtCore.Qt.ItemDataRole.UserRole)

    self.priorityPart = ToDoItemPart('')
    self.priorityPart.setData(str(self.priority), QtCore.Qt.ItemDataRole.DisplayRole)
    self.priorityPart.setData(self, QtCore.Qt.ItemDataRole.UserRole)

    self.taskPart = ToDoItemPart(self.taskText)
    self.taskPart.setData(self, QtCore.Qt.ItemDataRole.UserRole)

  @staticmethod
  def createFromTaskDef(taskDef: TaskDef, parentContainer) -> 'ToDoItem':
    """Creates a ToDoItem from a TaskDef.

    Args:
        taskDef (TaskDef): _description_
        parentContainer (_type_): Parent ToDoItem, or None

    Returns:
        ToDoItem: The created ToDoItem.
    """
    toDoItem = ToDoItem(taskDef.done, taskDef.priority, taskDef.taskText, parentContainer)

    toDoItem.donePart.setCheckable(True)
    toDoItem.donePart.setCheckState(QtCore.Qt.CheckState.Checked if taskDef.done else QtCore.Qt.CheckState.Unchecked)
    toDoItem.donePart.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

    toDoItem.priorityPart.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

    toDoItem.setTaskDoneStatus(taskDef.done)
    return toDoItem

  def toTaskDef(self) -> TaskDef:
    return TaskDef.createFromParts(self.done, self.priority, self.taskText)

  def toTask(self) -> Task:
    """ Returns a Task item for this ToDoItem.  Does not pull in subtasks.
    """
    return Task.createFromTaskDef(self.toTaskDef())

  def getDonePart(self) -> ToDoItemPart:
    return self.donePart

  def getPriorityPart(self) -> ToDoItemPart:
    return self.priorityPart

  def getTaskPart(self) -> ToDoItemPart:
    return self.taskPart

  def isTaskDone(self) -> bool:
    return self.done

  def updateParentDoneStatus(self):
    parentContainer = self.parentContainer

    if parentContainer is not None:
      currentDoneStatus = parentContainer.isTaskDone()

      # If all subtasks are done, then the parent task is done.
      numRows = parentContainer.getNumChildren()
      allSubTasksDone = False

      if numRows > 0:
        childrenDoneFlags = []

        for row in range(numRows):
          childrenDoneFlags.append(parentContainer.isChildTaskDone(row))

        allSubTasksDone = all(childrenDoneFlags)
      else:
        allSubTasksDone = currentDoneStatus

      if currentDoneStatus != allSubTasksDone:
        # The status has changed.  Must update it.  If all subtasks are done,
        # then mark the parent as done.  If they are not all done, mark
        # the parent as not done.
        parentContainer.setTaskDoneStatus(allSubTasksDone)
        parentContainer.crossOutTask(allSubTasksDone)
        parentContainer.updateParentDoneStatus()

  def updateDoneStatusFromCheckState(self):
    """Updates the done status of the task from the check state of the done part.
    """
    self.done = self.donePart.isChecked()

  def setTaskDoneStatus(self, done: bool):
    """Sets the task done staus, AND sets the check state of the done part.

    Args:
        done (bool): True to set done, False otherwise.
    """
    self.done = done
    self.donePart.setCheckState(QtCore.Qt.CheckState.Checked if done else QtCore.Qt.CheckState.Unchecked)

  def crossOutTask(self, doCrossOut: bool):
    font = self.taskPart.font()
    font.setStrikeOut(doCrossOut)
    self.taskPart.setFont(font)

  def markSubtasksAsDone(self, done: bool, crossOutSubtasks: bool):
    numRows = self.getNumChildren()
    for row in range(numRows):
      childTask = self.getChildTaskToDoItemContainer(row)
      if childTask is not None:
        childTask.setTaskDoneStatus(done)

        if crossOutSubtasks:
          childTask.crossOutTask(done)

  def isChildTaskDone(self, row: int) -> bool:
    childTask = self.getChildTaskToDoItemContainer(row)
    return childTask.isTaskDone() if childTask is not None else False

  def getNumChildren(self) -> int:
    """Returns the number of subtasks for this task

    Returns:
        int: Number of subtasks
    """
    return self.donePart.rowCount()

  def getChildTask(self, row: int) -> ToDoItemPart | None:
    childItem = self.donePart.child(row, kDoneColumn)
    if type(childItem) is ToDoItemPart:
      return childItem
    else:
      return None

  def getChildTaskToDoItemContainer(self, row: int) -> 'ToDoItem | None':
    """Returns the ToDoItem container of the given subtask

    Args:
        row (int): Number of subtask to retrieve

    Returns:
        Self | None: Desired ToDoItem container, or None if row is out of bounds
    """
    childItem = self.getChildTask(row)
    if childItem is not None:
      return childItem.getToDoItemContainer()
    else:
      return None
