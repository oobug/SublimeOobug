import sublime
import sublime_plugin
import functools
import os


class RenameFileCommand(sublime_plugin.TextCommand):
    def run(self, *args):
        fileName = self.view.file_name()
        branch, leaf = os.path.split(fileName)
        v = self.view.window().show_input_panel(
            "New Name:",
            leaf,
            functools.partial(self.on_done, fileName, branch),
            None,
            None
        )
        name, ext = os.path.splitext(leaf)

        v.sel().clear()
        v.sel().add(sublime.Region(0, len(name)))

    def on_done(self, old, branch, leaf):
        new = os.path.join(branch, leaf)

        try:
            os.rename(old, new)

            self.view.retarget(new)
        except Exception:
            sublime.status_message("Unable to rename")

    def is_visible(self):
        return self.view.file_name() is not None
