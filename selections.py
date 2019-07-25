import sublime
import sublime_plugin


def split_selection_to_begin_end(view):
    new_sel = []
    for s in view.sel():
        if not s.empty():
            new_sel.append(sublime.Region(s.a))
            new_sel.append(sublime.Region(s.b))
        else:
            new_sel.append(s)

    view.sel().clear()
    for s in new_sel:
        view.sel().add(s)


class SplitSelectionToBeginEndCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        split_selection_to_begin_end(self.view)


class LastSingleSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        s = self.view.sel()[-1]
        self.view.sel().clear()
        self.view.sel().add(s)
        if not self.view.visible_region().contains(s):
            self.view.show_at_center(s)

    def is_enabled(self):
        return len(self.view.sel()) > 1


class DeleteAroundSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, inside=False):
        # edit = self.view.begin_edit()
        for s in self.view.sel():
            b = s.begin()
            e = s.end()
            if inside:
                if s.size() <= 2:
                    self.view.erase(edit, s)
                else:
                    self.view.erase(edit, sublime.Region(e - 1, e))
                    self.view.erase(edit, sublime.Region(b, b + 1))
            else:
                self.view.erase(edit, sublime.Region(e, e + 1))
                self.view.erase(edit, sublime.Region(b - 1, b))
        # self.view.end_edit(edit)


'''
class ToggleBracketsCommand(sublime_plugin.TextCommand):
    bracketPairs = {
        '(':')',
        '[':']',
        '{':'}'
    }

    def run(self, edit):
        currentRegions = self.view.sel()
        for region in self.view.sel():
            points = (region.begin(), region.end())
            if self.view.substr(region.begin() - 1) in self.openBrackets

                pass
            if not region.empty():
                beRegions.append(sublime.Region(region.a))
                beRegions.append(sublime.Region(region.b))
            else:
                beRegions.append(region)
        self.view.sel().clear()
        # for region in beRegions
        #     self.view.sel().add(region)
'''
