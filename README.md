# Launch for Sublime Text

Quickly launch/run applications or executables from the command palette (`Ctrl/Command+Shift+P`). You can use this to open a terminal window in the project directory or even open the selected file for editing in photoshop.


# Configuration

Edit the commands file via Preferences -> Package Settings -> Launch -> Commands

## Command Format

```json
{
    "caption": "Launch: Git - Checkout",
    "command": "launch",
    "args":{
        "command": "git",
        "parameters": ["checkout", "${branch:master:Branch?}"],
        "cwd": "${project_folder}"
    }
}
```

Argument     | Description
------------ | -----------
`command`    | Application or executable path
`parameters` | Array of parameters to call the executable with
`cwd`        | Current Working Directory path


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
`project_folder`    | Path to first project folder
`project_folder[n]` | Path to `n`th project folder
`selected_text`     | Currently selected text(s) in sublime
