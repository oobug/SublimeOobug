import sublime
import sublime_plugin


class SetLineEndingsCommand(sublime_plugin.TextCommand):
    def run(self, edit, ending_type=None, **kw):
        """Set the line endings of the current document

        ending_type options are: "Windows", "Unix", "CR" (don't use CR)
        """
        if ending_type is not None:
            view = self.view
            if view.line_endings() != ending_type:
                view.set_line_endings(ending_type)


class SetLineEndingsToUnixCommand(SetLineEndingsCommand):
    def run(self, edit, **kw):
        super(SetLineEndingsToUnixCommand, self).run(
            edit, ending_type='Unix', **kw
        )

    def is_visible(self):
        return self.view.line_endings() != 'Unix'


class SetLineEndingsToWindowsCommand(SetLineEndingsCommand):
    def run(self, edit, **kw):
        super(SetLineEndingsToWindowsCommand, self).run(
            edit, ending_type='Windows', **kw
        )

    def is_visible(self):
        return self.view.line_endings() != 'Windows'
