import sublime
import sublime_plugin


class SetTabSizeCommand(sublime_plugin.TextCommand):
    def run(self, edit, tab_size=None, **kw):
        if tab_size is not None:
            view = self.view

            try:
                tabSize = int(tab_size)
                view.settings().set('tab_size', tabSize)
            except ValueError:
                pass
