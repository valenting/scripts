import sublime, sublime_plugin
import threading, os.path
from subprocess import PIPE, Popen

class i_grepCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        self.last_search_string = ''

    def run(self):
        self.window.run_command("hide_overlay")
        self.goon = False
        selection_text = self.window.active_view().substr(self.window.active_view().sel()[0])
        self.lists = []
        self.window.show_input_panel(
            "Search in project:",
            selection_text or '',
            self.perform_search, None, None)


    def goto_result(self, file_no):
        self.goon = False
        pass

    def perform_search(self, text):
        folders = self.search_folders()
        self.first = True
        self.goon = True
        self.overlay()
        for folder in folders:
            mylist = []
            self.lists.append(mylist)
            thread = iGrepThread(folder, text, mylist)
            thread.daemon = True
            thread.start()
    
    def overlay(self):
        if not self.goon:
            return
        results = []
        for tlist in self.lists:
            results += tlist
        if (len(results)==0):
            results = ["No results"]
        self.window.run_command("hide_overlay")
        self.window.show_quick_panel(results, self.goto_result)
        if self.goon:
            sublime.set_timeout(self.overlay, 200)

    def search_folders(self):
        return self.window.folders() or [os.path.dirname(self.window.active_view().file_name())]

class iGrepThread(threading.Thread):
    def __init__(self, folder, text, mylist):
        threading.Thread.__init__(self)
        self.folder = folder
        self.text = text
        self.mylist = mylist
        self.command = ['grep', '--color=auto', '-nriH', '--binary-files=without-match', text, str(folder)]
        
    def run(self):
        p = Popen(self.command, stdout=PIPE)
        while (True):
            line = p.stdout.readline()
            if not line:
                break
            if line == '':  
                break
            line = line.strip('\n')
            self.mylist.append(line)
               

