""" Run an external command on the current file.

Usage: run command `external_command` and giving it the executable name as the
`executable` argument. The external command with be invoked with the current
file path and name, as its first and single argument.

"""

import sublime
import sublime_plugin


class ExecWrapperCommand(sublime_plugin.WindowCommand):
    """A wrapper around exec to support variables in sublime-commands"""

    def run(self, **kwargs):
        variables = self.window.extract_variables()

        for key, value in kwargs.items():
            new_value = sublime.expand_variables(value, variables)
            if new_value != value:
                kwargs[key] = new_value

        self.window.run_command("exec", kwargs)

    def description(self):
        return (
            "Runs an external process asynchronously. On Windows, GUIs are supressed."
        )
