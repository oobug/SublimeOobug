# SublimeOobug

A repository to contain my settings, snippets, and extensions for Sublime Text 3.

## Other Repositories

Standard repositories to install:

- Alignment
- Material Theme
- Material Theme - Appbar
- Oracle PL SQL
- Theme - Cobalt2
- Toggle Read-Only

## Repository Settings

### Anaconda.sublime-settings

    {
        "anaconda_linter_mark_style": "squiggly_underline",
        "pep8_ignore":
        [
            "E126",
            "E309",
            "W503"
        ],
        "swallow_startup_errors": true
    }

### Python.sublime-settings

    {
        "rulers": [
            72,
            79
        ],
        "trim_trailing_white_space_on_save": true
    }

### PL SQL (Oracle).sublime-settings

    {
        "extensions":
        [
            "sql"
        ],
        "rulers":
        [
            40,
            79
        ],
        "tab_size": 2,
        "trim_trailing_white_space_on_save": true
    }

### User.sublime-settings

This may need to be cleaned up.

    {
        "binary_file_patterns":
        [
            "*.jpg",
            "*.jpeg",
            "*.png",
            "*.gif",
            "*.ttf",
            "*.tga",
            "*.dds",
            "*.ico",
            "*.eot",
            "*.pdf",
            "*.swf",
            "*.jar",
            "*.zip",
            "*.doc",
            "*.docx",
            "*.xls",
            "*.xlsx",
            "*.pyc",
            "*.pyd"
        ],
        "color_scheme": "Packages/Theme - Cobalt2/cobalt2.tmTheme",
        "describeobject_dir": "C:\\Program Files (x86)\\cx_OracleTools",
        "diff_tool": "C:\\Program Files (x86)\\WinMerge\\WinMergeU.exe",
        "font_face": "Fira Code",
        "font_options":
        [
            "no_italic"
        ],
        "font_size": 10,
        "ignored_packages":
        [
            "Markdown",
            "SublimeLinter-eslint",
            "SublimeLinter-pylint",
            "Vintage"
        ],
        "material_theme_accent_lime": true,
        "material_theme_appbar_lime": true,
        "material_theme_tree_headings": true,
        "theme": "Material-Theme.sublime-theme",
        "translate_tabs_to_spaces": true,
        "trim_trailing_white_space_on_save": false
    }
