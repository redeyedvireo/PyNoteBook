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


def writeTasks(tasks: list[Task]):
  root = ET.Element(kXmlDocTag)

  for task in tasks:
    addTaskToDom(root, task)

  elementTree = ET.ElementTree(root)

  return ET.tostring(root, encoding='utf8').decode('utf-8')

def addTaskToDom(parent: ET.Element, task: Task):
  taskElement = addTaskDefToDom(parent, task.taskDef)

  # Add subtasks
  for subtask in task.subTasks:
    addTaskDefToDom(taskElement, subtask)

def addTaskDefToDom(parent: ET.Element, taskDef: TaskDef) -> ET.Element:
  taskElement = ET.SubElement(parent, kTaskTag)

  # Attributes
  taskElement.set(kDoneAttr, '1' if taskDef.done else '0')
  taskElement.set(kPriorityAttr, str(taskDef.priority))

  # Task text
  taskTextElement = ET.SubElement(taskElement, kTaskTextTag)
  taskTextElement.text = taskDef.taskText

  return taskElement