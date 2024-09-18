from PySide6 import QtCore, QtGui, QtWidgets

from priority_delegate import PriorityDelegate
from taskdef import TaskDef, Task
from task_reader import TaskReader
from to_do_item import ToDoItem

from ui_to_do_edit import Ui_ToDoEditWidget

kDoneColumnWidth = 60
kPriorityColumnWidth = 70

from task_constants import kDoneColumn, kPriorityColumn, kTaskColumn

class ToDoEditWidget(QtWidgets.QWidget):
  toDoListModifiedSignal = QtCore.Signal()

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

  def setPageContents(self, contents: str, imageNames: list[str]) -> None:
    taskReader = TaskReader()

    self.loading = True

    self.removeAllTasks()

    tasks = taskReader.readTasks(contents)

    # Populate the UI
    for task in tasks:
      toDoItem = self.addTask(task.taskDef.done, task.taskDef, None)

      if toDoItem is not None:
        # Populate subtasks
        for subtask in task.subTasks:
          self.addTask(subtask.done, subtask, toDoItem)

    self.setDocumentModified(False)
    self.loading = False

  def removeAllTasks(self):
    self.model.removeRows(0, self.model.rowCount())

  def addTask(self, done: bool, taskDef: TaskDef, parent: ToDoItem | None) -> ToDoItem | None:
    parentItem = self.model.invisibleRootItem() if parent is None else parent.getDoneItem()

    if parentItem is not None:
      doneItem = ToDoItem('')
      priorityItem = ToDoItem(str(taskDef.priority))
      taskItem = ToDoItem(taskDef.taskText)

      doneItem.setCheckable(True)
      doneItem.setCheckState(QtCore.Qt.CheckState.Checked if done else QtCore.Qt.CheckState.Unchecked)
      doneItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

      priorityItem.setData(taskDef.priority, QtCore.Qt.ItemDataRole.DisplayRole)
      priorityItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

      parentItem.appendRow([ doneItem, priorityItem, taskItem ])

      doneItem.markTaskDone(done)

      self.sortList()

      # Note: when the application first starts, this function may not work right,
      # because the UI elements have not yet been sized

      self.updateRowHeight(taskItem.index())

      self.saveOrEmitModified()       # TODO: Not sure this is needed

      return taskItem
    else:
      return None

  def saveOrEmitModified(self):
    # Don't save if currently in the middle of loading
    if not self.loading:
      if self.autosave:
        pass
        # TODO: emit SavePage()
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

    if type(item) is ToDoItem:
      done = item.isTaskDone()

      item.crossOutTask(done)
      item.markSubtasksAsDone(done, True)
      item.updateParentDoneStatus()

      if done:
        # Set row visibility (this will hide subtasks as well)
        rootItem = self.model.invisibleRootItem()
        self.ui.treeView.setRowHidden(item.row(), rootItem.index(), self.hideDoneTasks)

      self.sortList()

      # Select the item
      self.ui.treeView.setCurrentIndex(item.index())

      self.saveOrEmitModified()

  @QtCore.Slot()
  def on_deleteTaskButton_clicked(self):
    # TODO: Implement
    pass