import xml.etree.ElementTree as ET
import logging

from taskdef import TaskDef, Task

# Tag names
kXmlDocTag = "tasks"
kTaskTag = "task"
kTaskTextTag = "tasktext"

# Attributes
kDoneAttr = "done"
kPriorityAttr = "priority"
kRichTextAttr = "richtext"

class TaskReader:
  def readTasks(self, taskStr: str) -> list[Task]:
    tasks = []

    try:
      root = ET.fromstring(taskStr)

      if root.tag != kXmlDocTag:
        logging.error(f'[TaskReader.readTasks] XML is not a task')
        return []

      for child in root:
        taskDef = self.readTaskDef(child)

        subTaskDefs = self.readSubTasks(child)

        task = Task()
        task.taskDef = taskDef
        task.subTasks = subTaskDefs

        tasks.append(task)

      return tasks

    except ET.ParseError as e:
      logging.error(f'[TaskReader.readTasks] XML Parser error: {str(e)}')
      return []

  def readTaskDef(self, taskNode) -> TaskDef:
    """Parses a task def node.

    Args:
        taskNode (_type_): _description_

    Returns:
        TaskDef: Returns a task def
    """
    taskDef = TaskDef()

    doneStr = taskNode.get(kDoneAttr)
    taskDef.done =  True if doneStr == '1' else False

    priorityStr = taskNode.get(kPriorityAttr)
    taskDef.priority = int(priorityStr)

    taskTextNode = taskNode.find('tasktext')
    if taskTextNode is None:
      logging.error(f'[TaskReader.parseTask] No task text found')
      taskDef.taskText = ''
    else:
      taskDef.taskText = taskTextNode.text

    return taskDef

  def readSubTasks(self, taskNode) -> list[TaskDef]:
    """Reads sub tasks for the given node

    Args:
        taskNode (_type_): _description_

    Returns:
        list[TaskDef]: List of task defs.
    """
    subTasks = []
    taskNodes = taskNode.findall('task')

    for subTaskNode in taskNodes:
      subTask = self.readTaskDef(subTaskNode)
      subTasks.append(subTask)

    return subTasks