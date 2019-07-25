import os
import sublime
import sublime_plugin
import subprocess
import tempfile


# Directories with the following names are not considered valid schema names.
NOT_SCHEMA_NAMES = [
        "package",
        "public_synonym",
        "role",
        "sequence",
        "table",
        "trigger",
        "type",
        "user",
        "view",
        ]


class DiffDbCommand(sublime_plugin.TextCommand):
    """Extract the database version of the current file and diff the two.

    The following assumptions are made:
    1. The current file's immediate directory is the schema name, unless it is
       one of a select list of values like "package", "view", etc., in which
       case it is the directory above that.  However, the user will have the
       opportunity to change it.
    2. If the User Preferences does not contain a "last_password" setting, the
       schema password is the same as the database name.  However, the user
       will have the opportunity to change it.
    3. The User Preferences has a setting for "last_database" that contains the
       database to use.  If this setting does not exist, the string "<db>" is
       suggested, and the user will have the opportunity to change it.
    4. DescribeObject.exe (part of cx_OracleTools) is available, and the path
       to it has been specified in the User Preferences under the key
       "describeobject_dir".  For example:
           "describeobject_dir": "C:\\Program Files\\cx_OracleTools",
    5. A diff tool exe has been specified in the User Preferences under the key
       "diff_tool".  For example:
           "diff_tool": "C:\\Program Files\\Beyond Compare 4\\BComp.exe",
    """

    def diff_to_file(self, extractedFile):
        """Diff the given file to the current one."""
        diffTool = sublime.load_settings("Preferences.sublime-settings").get("diff_tool", "")
        if not diffTool:
            sublime.error_message("Cannot find 'diff_tool' setting in User Preferences.")
            return
        if not os.path.isfile(diffTool):
            sublime.error_message("File not found: %s" % diffTool)
            return
        args = [
                diffTool,
                self.view.file_name(),  #  current file
                extractedFile,
                ]
        subprocess.Popen(args)  # Do not wait for the return value

    def extract_db_object(self):
        """Extract the database version of the current file."""
        describePath = sublime.load_settings("Preferences.sublime-settings").get("describeobject_dir", "")
        if not describePath:
            sublime.error_message("Cannot find 'describeobject_dir' setting in User Preferences.")
            return
        describeExe = os.path.join(describePath, "DescribeObject.exe")
        if not os.path.isfile(describeExe):
            sublime.error_message("File not found: %s" % describeExe)
            return
        handle, tempFile = tempfile.mkstemp(
                prefix = "%s_%s_" % (self.fileName, self.db),
                suffix = ".sql")
        connectString = "%s/%s@%s" % (self.schema, self.pw, self.db)
        args = [
                describeExe,
                "--schema=%s" % connectString,
                self.fileName,
                tempFile,
                ]
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # Do not show command window
        try:
            retVal = subprocess.check_call(args, startupinfo = info)
        except subprocess.CalledProcessError as exc:
            tempFile = None
            sublime.error_message("Call to DescribeObject.exe returned error code %s" % exc.returncode)
        return tempFile

    def get_names(self):
        """Return a 2-tuple consisting of the schema and object names."""
        fullDir, fullName = os.path.split(self.view.file_name())
        shorterDir, schema = os.path.split(fullDir)
        if schema.lower() in NOT_SCHEMA_NAMES:
            schema = os.path.split(shorterDir)[1]
        return (schema, os.path.splitext(fullName)[0])

    def on_input_done(self, text):
        """Use the user-entered values to extract the db object and diff it."""
        if "/" not in text or "@" not in text:
            sublime.error_message("Connect string must be in the form "
                    '"<schema>/<password>@<database>".')
            return

        self.schema, remainder = text.split("/")
        self.pw, self.db = remainder.split("@")

        extractedFile = self.extract_db_object()
        if extractedFile:
            settings = sublime.load_settings("Preferences.sublime-settings")
            settings.set("last_database", self.db)
            if self.db == self.pw:
                if settings.has("last_password"):
                    settings.erase("last_password")
            else:
                settings.set("last_password", self.pw)
            sublime.save_settings("Preferences.sublime-settings")

            self.diff_to_file(extractedFile)

    def run(self, edit):
        self.schema, self.fileName = self.get_names()

        # Extract the most recently used database and password from the user settings.
        settings = sublime.load_settings("Preferences.sublime-settings")
        lastDb = settings.get("last_database", "")
        if lastDb:
            self.db = lastDb
        else:
            self.db = "<db>"
        lastPw = settings.get("last_password", "")
        if lastPw:
            self.pw = lastPw
        else:
            if lastDb:
                self.pw = lastDb
            else:
                self.pw = "<pw>"

        # Present the connect string to the user, so that it can be modified.
        connectString = "%s/%s@%s" % (self.schema, self.pw, self.db)
        w = self.view.window()
        w.show_input_panel("Connect String:", connectString,
                self.on_input_done, None, None)
