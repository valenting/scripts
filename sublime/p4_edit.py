import sublime, sublime_plugin
import subprocess

class P4_editCommand(sublime_plugin.TextCommand):
  def run(self, edit):
      command = ["p4 edit "+self.view.file_name(), '']
      process = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
      print process.communicate()[0]
