import sublime
import sublime_plugin

import sys
import threading
from subprocess import Popen, PIPE, STDOUT


class OraclePackageBuild(sublime_plugin.WindowCommand):

    panel_lock = threading.Lock()

    def run(self):
        self.window.show_input_panel(
            'Connect String:', '', self.compile_package, None, None)

    def compile_package(self, connectString):
        vars = self.window.extract_variables()
        working_dir = vars['file_path']
        file_name = vars['file_name']
        encoding = sys.getdefaultencoding()

        args = ['sqlplus', connectString]

        input_lines = [
            'set define off',
            '@{}'.format(file_name),
            'exit'
        ]
        input_text = b'\n'.join(bytes(t, encoding=encoding) for t in input_lines)

        p = Popen(args, cwd=working_dir, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        output, errs = p.communicate(input_text)

        self.queue_write(output.decode())

    def queue_write(self, text):
        sublime.set_timeout(lambda: self.do_write(text), 1)

    def do_write(self, text):
        with self.panel_lock:
            self.panel = self.window.create_output_panel('exec')
            self.window.run_command('show_panel', {'panel': 'output.exec'})
            self.panel.run_command('append', {'characters': text})
