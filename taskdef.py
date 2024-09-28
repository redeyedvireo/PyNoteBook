
class TaskDef:
  done: bool
  priority: int
  taskText: str

  @staticmethod
  def createFromParts(done: bool, priority: int, taskText: str) -> 'TaskDef':
    taskDef = TaskDef()
    taskDef.done = done
    taskDef.priority = priority
    taskDef.taskText = taskText

    return taskDef

class Task:
  taskDef: TaskDef
  subTasks: list[TaskDef]

  @staticmethod
  def createFromTaskDef(taskDef: TaskDef) -> 'Task':
    task = Task()
    task.taskDef = taskDef
    return task
