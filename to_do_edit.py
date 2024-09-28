from PySide6 import QtCore, QtGui, QtWidgets

from priority_delegate import PriorityDelegate
from taskdef import TaskDef, Task
from task_reader import TaskReader
from task_writer import writeTasks
from to_do_item import ToDoItem
from to_do_item_part import ToDoItemPart
from taskdef import TaskDef, Task

from ui_to_do_edit import Ui_ToDoEditWidget

kDoneColumnWidth = 60
kPriorityColumnWidth = 70

from task_constants import kDoneColumn, kPriorityColumn, kTaskColumn

class ToDoEditWidget(QtWidgets.QWidget):
  toDoListModifiedSignal = QtCore.Signal()
  toDoListSavePage = QtCore.Signal()

  def __init__(self, parent: QtWidgets.QWidget | None = None):
    super(ToDoEditWidget, self).__init__(parent)

    self.ui = Ui_ToDoEditWidget()
    self.ui.setupUi(self)

    self.model = QtGui.QStandardItemModel(0, 3, self.ui.treeView)

    self.singleRowHeight = 20
    self.modified = False
    self.autosave = True
    self.loading = False
    self.sorting = True

    # Toolbar buttons
    self.hideDoneTasks = False
    self.ui.hideDoneTasksButton.setChecked(self.hideDoneTasks)

    self.ui.treeView.setModel(self.model)

    self.configureTree()

  def configureTree(self):
    self.model.setHorizontalHeaderLabels(['Done', 'Priority', 'Task'])

    delegate = PriorityDelegate()
    self.ui.treeView.setItemDelegateForColumn(kPriorityColumn, delegate)

    # Compute row height based on the font used when createing new items
    tempItem = QtGui.QStandardItem()
    fm = QtGui.QFontMetrics(tempItem.font())
    self.singleRowHeight = fm.lineSpacing() + 2   # Adding a 2-pixel fudge factor, to ensure enough space

    self.ui.treeView.setWordWrap(True)

    self.ui.treeView.setColumnWidth(kDoneColumn, kDoneColumnWidth)
    self.ui.treeView.setColumnWidth(kPriorityColumn, kPriorityColumnWidth)

    # Center the text in the header
    header = self.ui.treeView.header()

    header.setSectionResizeMode(kDoneColumn, QtWidgets.QHeaderView.ResizeMode.Fixed)
    header.setSectionResizeMode(kPriorityColumn, QtWidgets.QHeaderView.ResizeMode.Fixed)

    self.model.setHeaderData(kDoneColumn, \
                             QtCore.Qt.Orientation.Horizontal, \
                             QtCore.Qt.AlignmentFlag.AlignHCenter, \
                             QtCore.Qt.ItemDataRole.TextAlignmentRole)

    self.model.setHeaderData(kPriorityColumn, \
                             QtCore.Qt.Orientation.Horizontal, \
                             QtCore.Qt.AlignmentFlag.AlignHCenter, \
                             QtCore.Qt.ItemDataRole.TextAlignmentRole)

    self.ui.treeView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

    self.ui.treeView.customContextMenuRequested.connect(self.onCustomContextMenu)
    self.ui.treeView.clicked.connect(self.handleItemClicked)
    self.model.itemChanged.connect(self.handleItemChanged)

  def setDocumentModified(self, modified: bool):
    self.modified = modified

  def isDocumentModified(self) -> bool:
    return self.modified

  def sortList(self):
    if self.sorting:
      self.model.sort(kPriorityColumn)

  def updateDoneRowVisibility(self):
    numRows = self.model.rowCount()
    rootItem = self.model.invisibleRootItem()
    rootIndex = rootItem.index()

    for row in range(numRows):
      toDoItem = self.getTopLevelToDoItem(row, kDoneColumn)
      if toDoItem is not None:
        if toDoItem.done:
          self.ui.treeView.setRowHidden(row, rootIndex, self.hideDoneTasks)

  def updateRowHeight(self, index: QtCore.QModelIndex):
    taskItem = self.model.itemFromIndex(index)

    if taskItem is None:
      return

    # Calculate width of task text, using current font
    fm = QtGui.QFontMetrics(taskItem.font())
    columnWidth = self.ui.treeView.columnWidth(kTaskColumn)

    # For some reason, QFontMetrics::width() doesn't return an accurate value of
    # the string width.  But using the average character width times the string
    # length seems to work pretty well.
    stringWidth = len(taskItem.text()) * fm.averageCharWidth()

    # The C++ version uses floating point division.  However, that is apparently
    # not a good solution on Python, due to obscure edge cases in floating point division.
    # This uses "upside-down floor division".  (The // operator is floor division.)  For
    # more details, see:
    # https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
    numTextRows = -(stringWidth // -columnWidth)

    hint = taskItem.sizeHint()
    hint.setHeight(self.singleRowHeight * numTextRows)

    taskItem.setSizeHint(hint)

  def getPageContents(self) -> str:
    # Collect all tasks

    tasks = self.getTopLevelTasks()

    # Use TaskWriter to make a string out of tasks (an XML string)
    return writeTasks(tasks)

  def getTopLevelTasks(self) -> list[Task]:
    tasks: list[Task] = []

    rootItem = self.model.invisibleRootItem()
    numRows = rootItem.rowCount()

    for row in range(numRows):
      child = rootItem.child(row, kDoneColumn)
      if type(child) is ToDoItemPart:
        toDoItem = child.container

        if type(toDoItem) is ToDoItem:
          task = toDoItem.toTask()
          tasks.append(task)

          taskDefs = self.getSubTasks(toDoItem)
          task.subTasks = taskDefs

    return tasks

  def getSubTasks(self, parent: ToDoItem) -> list[TaskDef]:
    subTasks: list[TaskDef] = []
    numRows = parent.getNumChildren()

    for row in range(numRows):
      childToDoItem = parent.getChildTaskToDoItemContainer(row)
      if childToDoItem is not None:
        subTask = childToDoItem.toTaskDef()
        subTasks.append(subTask)

    return subTasks

  def setPageContents(self, contents: str, imageNames: list[str]) -> None:
    taskReader = TaskReader()

    self.loading = True

    self.removeAllTasks()

    tasks = taskReader.readTasks(contents)

    # Populate the UI
    for task in tasks:
      toDoItem = self.addTask(task.taskDef, None)

      if toDoItem is not None:
        # Populate subtasks
        for subtask in task.subTasks:
          self.addTask(subtask, toDoItem)

    self.setDocumentModified(False)
    self.loading = False

  def removeAllTasks(self):
    self.model.removeRows(0, self.model.rowCount())

  def addTask(self, taskDef: TaskDef, parent: ToDoItem | None) -> ToDoItem | None:
    toDoItem = ToDoItem.createFromTaskDef(taskDef, parent)
    parentItem = self.model.invisibleRootItem() if parent is None else parent.getDonePart()

    if parentItem is not None:
      parentItem.appendRow([ toDoItem.donePart, toDoItem.priorityPart, toDoItem.taskPart ])

      self.sortList()

      # Note: when the application first starts, this function may not work right,
      # because the UI elements have not yet been sized

      self.updateRowHeight(toDoItem.taskPart.index())

      self.saveOrEmitModified()       # TODO: Not sure this is needed

      return toDoItem
    else:
      return None

  def createNewTask(self, parent: ToDoItem | None):
    toDoItem = self.addTask(TaskDef.createFromParts(False, 5, 'Task description'), parent)

    if toDoItem is not None:
      # Select the task item
      self.ui.treeView.setCurrentIndex(toDoItem.getItemIndex())

      # Start editing the task
      self.ui.treeView.edit(toDoItem.getItemIndex())

  def createNewSubtask(self):
    selectedRow, isTopLevel, parentQModelIndex = self.getSelectedRow()
    if selectedRow != -1:
      rootItem = self.model.invisibleRootItem()

      if isTopLevel:
        donePart = rootItem.child(selectedRow, kDoneColumn)

        if type(donePart) is ToDoItemPart:
          toDoItem = donePart.container
          self.createNewTask(toDoItem)
      else:
        # The selected row is not a top-level row.  Get its parent, and then create
        # the subtask off of that.
        if parentQModelIndex is not None:
          item = self.model.itemFromIndex(parentQModelIndex)

          if type(item) is ToDoItemPart:
            toDoItem = item.container
            self.createNewTask(toDoItem)

  def deleteSelectedTask(self):
    selectedRow, isTopLevel, parentQModelIndex = self.getSelectedRow()
    if selectedRow != -1:
      rootItem = self.model.invisibleRootItem()
      self.model.removeRow(selectedRow, rootItem.index())

      self.saveOrEmitModified()

  def getSelectedRow(self) -> tuple[int, bool, QtCore.QModelIndex | None]:
    """Returns the index of the selected row, whether this row is a top-level row, and if not,
       the row's parent QModelIndex.

    Returns:
        tuple[int, bool]: The first item is the row number.
                          The second item is a bool indicating whether the row is a top-level row.
                          The third item is the row's parent QModelIndex, if it exists, or None if it doesn't.
    """
    if self.ui.treeView.currentIndex().isValid():
      parent = self.ui.treeView.currentIndex().parent()

      return (self.ui.treeView.currentIndex().row(), not parent.isValid(), parent if parent.isValid() else None)
    else:
      return (-1, True, None)

  def getTopLevelToDoItem(self, row: int, column: int) -> ToDoItem | None:
    item = self.model.item(row, column)
    return item.container if type(item) is ToDoItemPart else None

  def saveOrEmitModified(self):
    # Don't save if currently in the middle of loading
    if not self.loading:
      if self.autosave:
        self.toDoListSavePage.emit()
      else:
        # Auto-save not enabled.  Tell the main window that it has been modified
        self.modified = True
        self.toDoListModifiedSignal.emit()

  @QtCore.Slot(QtCore.QPoint)
  def onCustomContextMenu(self, point: QtCore.QPoint):
    index = self.ui.treeView.indexAt(point)
    if index.isValid():
      menu = QtWidgets.QMenu()
      menu.addAction('Delete task', self.on_deleteTaskButton_clicked)
      menu.exec(self.ui.treeView.mapToGlobal(point))

  @QtCore.Slot(QtGui.QStandardItem)
  def handleItemChanged(self, item: QtGui.QStandardItem):
    if item.column() == kDoneColumn:
      # This will be handled by handleItemClicked().
      return

    elif item.column() == kPriorityColumn:
      # A priority has changed.  This data is stored in the QStandardItem; this
      # value needs to be copied to the ToDoItem container.
      if type(item) is ToDoItemPart:
        toDoItem = item.container
        toDoItem.priority = int(item.getValue())

        # Priorities have changed: initiate a sort
        self.sortList()

    elif item.column() == kTaskColumn:
      # Update the row height
      self.updateRowHeight(item.index())

    # Select the item
    self.ui.treeView.setCurrentIndex(item.index())

    self.saveOrEmitModified()

  @QtCore.Slot(QtCore.QModelIndex)
  def handleItemClicked(self, index: QtCore.QModelIndex):
    item = self.model.itemFromIndex(index)

    if type(item) is ToDoItemPart:
      toDoItem = item.container
      done = toDoItem.done

      toDoItem.crossOutTask(done)
      toDoItem.markSubtasksAsDone(done, True)
      toDoItem.updateParentDoneStatus()

      if done:
        # Set row visibility (this will hide subtasks as well)
        rootItem = self.model.invisibleRootItem()
        self.ui.treeView.setRowHidden(item.row(), rootItem.index(), self.hideDoneTasks)

      self.sortList()

      # Select the item
      self.ui.treeView.setCurrentIndex(item.index())

      self.saveOrEmitModified()

  @QtCore.Slot()
  def on_newTaskButton_clicked(self):
    self.createNewTask(None)

  @QtCore.Slot()
  def on_newSubtaskButton_clicked(self):
    self.createNewSubtask()

  @QtCore.Slot()
  def on_deleteTaskButton_clicked(self):
    self.deleteSelectedTask()

  @QtCore.Slot()
  def on_hideDoneTasksButton_clicked(self):
    self.hideDoneTasks = self.ui.hideDoneTasksButton.isChecked()
    self.updateDoneRowVisibility()