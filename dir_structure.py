import sublime
import sublime_plugin
import re

class FileNode:
  def __init__(self, level, isLastChild, nodeStr, parent):
    """
    FileNode constructor

    Args:
      level: level of the node
      isLastChild: is last node?
      nodeStr: full content string of the node
    """
    self.level = level
    self.isLastChild = isLastChild
    self.text = ''
    self.comment = ''
    self.nodeStr = nodeStr
    self.hasChild = False
    self.children = self.getChildren()
    self.parent = parent

    if len(self.children):
      self.hasChild = True
    
    self.setText(nodeStr)


  def splitChild(self, childrenStr):
    """
    Split nodes with ','

    Args:
      childrenStr: content string of children

    Returns:
      children array
    """
    result = []
    temp = []
    count = 0
  
    arr = childrenStr.split(',')

    for i,str in enumerate(arr):
      count+=str.count('(')
      count-=str.count(')')

      temp.append(str)

      if count == 0:
        result.append(','.join(temp))
        temp = []

    return result

  def setText(self, nodeStr):
    """
    Set text and comment for the node

    Args:
      nodeStr: full content string of the node
    """
    pattern = re.compile(r'^([\w\#\.]+)')
    matched = pattern.match(nodeStr)

    if matched and matched.group(1):
      arr = matched.group(1).split('#')
      self.text = arr[0]
      if len(arr) == 2:
        self.comment = arr[1]

  def getChildren(self):
    """
    Get children of the node

    Returns:
      children array
    """
    pattern = re.compile(r'^.+?\((.*)\)$')
    matched = pattern.match(self.nodeStr)
    result = []

    if matched:
      s = matched.group(1)

      children = self.splitChild(s)

      for i,child in enumerate(children):
        child = FileNode(self.level + 1, bool(i == len(children) - 1), child, self)
        result.append(child)

    return result

class DirStructureCommand(sublime_plugin.TextCommand):

  def buildNodeList(self, node):
    self.nodeList.append(node)

    if node.hasChild:
      for i,a in enumerate(node.children):
        self.buildNodeList(node.children[i])

  def prefix(self, node):
    """
    Prefix node

    Args:
      node: node

    Return:
      string prefix of a node
    """
    if node.parent == 'root':
      return '' 
    else:
      return self.prefix(node.parent) + ('    ' if node.parent.isLastChild else '│   ')

  def run(self, edit):
    self.nodeList = []

    for region in self.view.sel():
      if not region.empty():
        s = self.view.substr(region)

        arr = s.split('\n')

        for i,a in enumerate(arr):
          node = FileNode(0, bool(i == len(arr) - 1), arr[i], 'root')
          self.buildNodeList(node)

        result = ['.']
        max = 0
        for j,node in enumerate(self.nodeList):
          line = self.prefix(node) + ('└── ' if node.isLastChild else '├── ') + node.text
          max = len(line) if max < len(line) else max
          node.line = line

        for k,node in enumerate(self.nodeList):
          padding = (max + 4 - len(node.line)) * '·'
          if node.comment:
            node.line = ' '.join([node.line, padding, node.comment])

          result.append(node.line)

        self.view.replace(edit, region, ('\n').join(result))