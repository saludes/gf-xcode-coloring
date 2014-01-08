import sublime, sublime_plugin

def get_abstract(view):
	import re
	concrete_regex = (r'(incomplete\s+)?concrete (\w+) of (\w+)', 3)
	abstract_regex = (r'abstract\s+(\w+)', 1)
	for regex,k in (abstract_regex, concrete_regex):
		rg = view.find(regex, 0)
		if rg:
			m = re.match(regex, view.substr(rg))
			return m and m.group(k)

def get_related(module, near):
	from os.path import splitext, basename, dirname, join, walk

	def f(arg,dirname,fnames):
		mname, result = arg
		for fn in fnames:
			base,ext = splitext(basename(fn))
			if ext == '.gf' and base.startswith(mname):
				result.append(join(dirname,fn))

	result = []
	d = dirname(near)
	walk(d, f, (module,result))
	return result


class OpenRelatedCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		module = get_abstract(self.view)
		if not module: return
		where = self.view.file_name()
		win = self.view.window()
		for path in get_related(module, where):
			win.open_file(path)