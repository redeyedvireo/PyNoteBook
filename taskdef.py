
class TaskDef:
  done: bool
  priority: int
  taskText: str

class Task:
  taskDef: TaskDef
  subTasks: list[TaskDef]
