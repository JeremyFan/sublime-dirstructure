import sublime
import sublime_plugin
import re

class FileNode:
  def __init__(self, level, type, nodeStr):
    self.level = level
    self.type = type
    self.text = ''
    self.nodeStr = nodeStr
    self.hasChild = False
    self.children = self.getChildren()

    if len(self.children):
      self.hasChild = True
    
    self.setText(nodeStr)

  def setText(self, nodeStr):
    pattern = re.compile(r'^([\w\#\.]+)')
    matched = pattern.match(nodeStr)

    if matched and matched.group(1):
      arr = matched.group(1).split('#')
      self.text = arr[0]
      if len(arr) == 2:
        self.comment = arr[1]

  def getChildren(self):
    pattern = re.compile(r'.*?\((.+)\)$')
    matched = pattern.match(self.nodeStr)
    result = []

    if matched:
      s = matched.group(1)

      matched = re.compile(r'((\w+\,)|(\w+\(.+\)\,))*').match(s)

      print(matched.group(1))
      arr = s.split(',')
      for i,a in enumerate(arr):
        child = FileNode(2, 0, arr[i])
        result.append(child)

    return result

class DirStructureCommand(sublime_plugin.TextCommand):

  def showNode(self, node):
    self.nodeList.append(node)

    if node.hasChild:
      for i,a in enumerate(node.children):
        self.showNode(node.children[i])

  def run(self, edit):
    self.nodeList = []

    # node = FileNode(1, 0, 'dist#什么(css(1,2))')
    for region in self.view.sel():
      if not region.empty():
        s = self.view.substr(region)

        arr = s.split('\n')

        for i,a in enumerate(arr):
          type = 0 if i == len(arr) - 1 else 1
          node = FileNode(1, type, arr[i])
          self.showNode(node)

        result = []
        for j,node in enumerate(self.nodeList):
          r = node.level * '  ' + node.text
          result.append(r)


          # pattern = re.compile(r'.+\((.+)\)$')
          # match = pattern.match(arr[i])
          # if(match):
            # self.gen(match.group(1))
          
          # type = (len(arr) - 1) ? 0 : 1

          # node = i== FileNode(1, type, )

          # if i == len(arr) - 1:
          #   arr[i] = '└── ' + a[0:]
          # else:
          #   arr[i] = '├── ' + a[0:]

          # self.gen(arr[i])


        self.view.replace(edit, region, ('\n').join(result))
