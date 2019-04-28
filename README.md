# Launch for Sublime Text

Quickly launch/run applications or executables from the command palette (`Ctrl/⌘+Shift+P`). You can use this to open a terminal window in the project directory or even open the selected file for editing in photoshop.


# Configuration

Edit the commands file via Preferences -> Package Settings -> Launch -> Commands

## Command Format

```json
{
    "caption": "Launch: Git - Checkout",
    "command": "launch",
    "args":{
        "command": ["git", "checkout", "${branch:master:Branch?}"],
        "cwd": "${project_folder}"
    }
}
```

Argument     | Description
------------ | -----------
`command`    | Command to launch (string or array)
`cwd`        | Current Working Directory path

_Quotes will be added to command elements with spaces on Windows_

## Variables

Variables are replacement tokens that can be used in any argument.

Format: `${name:default:prompt}`

Variable Part | Description
------------- | ----------
`name`        | Variable name
`default`     | _(Optional)_ Default variable value
`prompt`      | _(Optional)_ String to present the user if variable is undefined

### Predefined variables

Variable            | Description
------------------- | -----------
`file`              | Path to current file
`file_path`         | Path to directory of current file
`file_name`         | Current file name
`file_project_path` | Path to current file relative to first project folder
`project`           | Project name
`project_folder`    | Path to first project folder
`project_folder[n]` | Path to `n`th project folder
`selected_text`     | Currently selected text(s) in sublime

### Project setting variables

You can set project specific variables in your project settings file by creating a key named `launch_variables`. These will get merged with the predefined variables at run time.

```json
{
    "folders": [],
    "launch_variables":
    {
        "one_variable": "is fun",
        "two_variables": "is a party"
    }
}
```

# Examples

```json5
[
    // Edit selected file in Paint
    {
        "caption": "Launch: Edit selected in Paint",
        "command": "launch",
        "args":{
            "command": [
                "C:\\Windows\\system32\\mspaint.exe",
                "${project_folder}\\${selected_text::Image to open?}"
            ],
        }
    },

    // Launch WSL Terminal in project_folder
    {
        "caption": "Launch: WSL Terminal",
        "command": "launch",
        "args":{
            "command": ["C:\\Windows\\System32\\wsl.exe"],
            "cwd": "${project_folder}"
        }
    },

    // Run Mac Terminal in project_folder
    {
        "caption": "Launch: Mac Terminal",
        "command": "launch",
        "args":{
            "command": ["open", "-a", "Terminal", "${project_folder}"]
        }
    },


    // Create Unix Terminal in project_folder
    {
        "caption": "Launch: Unix Terminal",
        "command": "launch",
        "args":{
            "command": ["gnome-terminal"],
            "cwd": "${project_folder}"
        }
    },

    // Open and Select current file in Explorer
    {
        "caption": "Launch: Open file in Explorer",
        "command": "launch",
        "args":{
            "command": ["explorer", "/select,${file}"]
        }
    },

    // Open Git Gui for current project
    {
        "caption": "Launch: Git Gui",
        "command": "launch",
        "args":{
            "command": ["C:\\Program Files\\Git\\cmd\\git-gui.exe"],
            "cwd": "${project_folder}"
        }
    },

    // Stage current file in Git
    {
        "caption": "Launch: Git - Stage file",
        "command": "launch",
        "args":{
            "command": ["git", "add", "${file_project_path}"],
            "cwd": "${project_folder}"
        }
    }
]
```