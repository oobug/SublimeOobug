import sublime
import sublime_plugin


def command_is_valid(view: sublime.View) -> bool:
    """Return whether the command is valid for the given view"""
    scopename = view.scope_name(0)
    if scopename.startswith("text.html.markdown"):
        return True
    filename = view.file_name()
    if filename.endswith(".md"):
        return True
    return False


class IncreaseMarkdownFontSizeCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
        return command_is_valid(self.view)

    def run(self, edit: sublime.Edit) -> None:
        s = sublime.load_settings("Markdown.sublime-settings")
        current = s.get("font_size", 10)

        if current >= 36:
            current += 4
        elif current >= 24:
            current += 2
        else:
            current += 1

        if current > 128:
            current = 128
        s.set("font_size", current)

        sublime.save_settings("Markdown.sublime-settings")


class DecreaseMarkdownFontSizeCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
        return command_is_valid(self.view)

    def run(self, edit: sublime.Edit) -> None:
        s = sublime.load_settings("Markdown.sublime-settings")
        current = s.get("font_size", 10)
        # current -= 1

        if current >= 40:
            current -= 4
        elif current >= 26:
            current -= 2
        else:
            current -= 1

        if current < 10:
            current = 10
        s.set("font_size", current)

        sublime.save_settings("Markdown.sublime-settings")
