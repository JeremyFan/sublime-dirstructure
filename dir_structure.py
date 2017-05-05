import sublime
import sublime_plugin
import re

class DirStructureCommand(sublime_plugin.TextCommand):

  def gen(self, str):
		pattern = re.compile(r'.+\((.+)\)$')
		match = pattern.match(str)

		if(match):
      s = match.group(1)
      arr = s.split(',')

      for i,a in enumerate(arr):
        

			self.gen(match.group(1))
		else
			return str


  def run(self, edit):

  	# def insert(x):
  		# return x.insert(0, '├── ')
    for region in self.view.sel():
      if not region.empty():
        s = self.view.substr(region)

        arr = s.split('\n')

        for i,a in enumerate(arr):
        	# pattern = re.compile(r'.+\((.+)\)$')
        	# match = pattern.match(arr[i])
        	# if(match):
        		# self.gen(match.group(1))

        	if i == len(arr) - 1:
        		arr[i] = '└── ' + a[0:]
        	else:
	          arr[i] = '├── ' + a[0:]

	        self.gen(arr[i])


        self.view.replace(edit, region, ('\n').join(arr))
