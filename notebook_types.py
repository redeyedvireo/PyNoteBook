from enum import Enum

kInvalidPageId = 0

# Type aliases
ENTITY_ID = int
ENTITY_LIST = list[ENTITY_ID]
TAG_LIST = list[str]


# Page type
class PAGE_TYPE(Enum):
  kPageTypeUserText = 0				# User-entered text
  kPageFolder = 1						  # Folder page (simply a placeholder that has children)
  kPageTypeToDoList = 2       # To Do list
  kPageTypeHtml = 3						# Specific HTML code
  kPageTypeJavascript = 4     # Javascript