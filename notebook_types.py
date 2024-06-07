from enum import Enum

kInvalidPageId = 0

# Type aliases
ENTITY_ID = int
ENTITY_LIST = list[ENTITY_ID]
ENTITY_PAIR = tuple[ENTITY_ID, ENTITY_ID]       # Used to indicate a page ID and a parent ID
ENTITY_PAIR_LIST = list[ENTITY_PAIR]
TAG_LIST = list[str]


# Page type
class PAGE_TYPE(Enum):
  kPageTypeUserText = 0				# User-entered text
  kPageFolder = 1						  # Folder page (simply a placeholder that has children)
  kPageTypeToDoList = 2       # To Do list
  kPageTypeHtml = 3						# Specific HTML code
  kPageTypeJavascript = 4     # Javascript

class PAGE_ADD(Enum):
  kNewPage = 0
  kNewFolder = 1
  kNewToDoListPage =2

class PAGE_ADD_WHERE(Enum):
  kPageAddDefault = 0
  kPageAddAfterCurrentItem = 1
  kPageAddBeforeCurrentItem = 2
  kPageAddTopLevel = 3
