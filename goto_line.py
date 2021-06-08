import sublime
import sublime_plugin


class OobugPromptGotoLineCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Goto Line:", "", self.on_done, None, None)

    def on_done(self, text):
        try:
            view = self.window.active_view()
            if view:
                view.run_command("oobug_goto_line", {"text": text})
        except ValueError:
            pass  # Ignore any exceptions


class OobugGotoLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        line = int(text) - 1  # In SublimeText lines are 0-based

        if text[0] in "+-":
            curLine, curCol = self.view.rowcol(self.view.sel()[0].begin())
            line = curLine + line + 1

        pt = self.view.text_point(line, 0)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))
        self.view.show(pt)
