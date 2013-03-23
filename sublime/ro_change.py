import sublime, sublime_plugin
import subprocess, os, stat

class ro_changeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		def writable(mode):
			return mode&stat.S_IWUSR==stat.S_IWRITE

		mode = os.stat(self.view.file_name()).st_mode
		if (writable(mode)):
			os.chmod(self.view.file_name(),  mode&(~stat.S_IWRITE))
			print "LOCK "+ self.view.file_name()
		else:
			os.chmod(self.view.file_name(),  mode|stat.S_IWRITE)
			print "UNLOCK "+ self.view.file_name()