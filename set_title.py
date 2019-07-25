import sublime
import sublime_plugin
import functools


class SetTitleCommand(sublime_plugin.TextCommand):
    def run(self, *args):
        title = (self.view.name() or 'untitled')
        v = self.view.window().show_input_panel(
            'Set Title:',
            title,
            functools.partial(self.on_done, title),
            None,
            None
        )

        v.sel().clear()
        v.sel().add(sublime.Region(0, len(title)))

    def on_done(self, oldTitle, newTitle):
        if oldTitle == newTitle:
            pass
        else:
            if newTitle == 'untitled':
                newTitle = ''
            self.view.set_name(newTitle)

    def is_enabled(self):
        return self.view.file_name() is None
