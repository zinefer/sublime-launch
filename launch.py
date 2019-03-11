import os, sublime, sublime_plugin, time, subprocess, functools
import re

class LaunchCommand(sublime_plugin.WindowCommand):
    def run(self, command, parameters=[], cwd=None, variables={}):
        # Populate variables if we don't have any
        if not variables:
            variables = self.populate_variables()


        # Create a callback to be used if a replacement needs user input
        def _input_callback(input):
            variables[variable_name] = input
            self.run(command, parameters, cwd, variables)

        # Expand variables and ask for user input if necessary
        try:
            command = self.expand_variables(command, variables)

            for param in range(len(parameters)):
                parameters[param] = self.expand_variables(parameters[param], variables)

            if cwd: cwd = self.expand_variables(cwd, variables)
        except RequireUserInputError as e:
            variable_name = e.name
            self.window.show_input_panel('Launch Input: ' + e.prompt, e.default, _input_callback, None, None)
            return


        # We have clean params, launch it.
        self.launch_it(command, parameters, cwd)
        variables.clear()

    # Inspired by sublime-text-shell-command
    # Replaces variable tokens with their values or raises an exception for user input
    def expand_variables(self, string, variables):
        matches = re.findall(r'\${(.*?)}', string)
        for variable_def in matches:
            raw = '${' + variable_def + '}'
            name, default, prompt = self.parse_variable(variable_def)

            if not name in variables:
                if prompt: raise RequireUserInputError(name, default, prompt)
                if default: variables[name] = default

            string = string.replace(raw, variables[name])
        return string

    def populate_variables(self):
        view = self.window.active_view()
        variables = {}

        # Project variables
        project = sublime.active_window().project_data()
        if project:
            if 'folders' in project:
                # Add project folders
                variables['project_folder'] = project['folders'][0]['path']
                for folder in range(len(project['folders'])):
                    variables["project_folder[{0:d}]".format(folder)] = project['folders'][folder]['path']
            if 'launch_variables' in project:
                # Merge project variables
                variables.update(project['launch_variables'])

        project_file = sublime.active_window().project_file_name()
        if project_file:
            variables['project'] = os.path.basename(os.path.splitext(project_file)[0])

        # File variables
        file = view.file_name()
        if file:
            variables['file'] = file
            variables['file_path'] = os.path.split(file)[0]
            variables['file_name'] = os.path.basename(file)
            if project and ('folders' in project):
                variables['file_poject_path'] = os.path.relpath(file, project['folders'][0]['path'])

        # Selected text variable
        if (view.sel())[0].size() > 0:
            # Combine all selections if there are more than one
            variables['selected_text'] = functools.reduce((lambda a, b: a + view.substr(b)), view.sel(), '')

        return variables

    # Format: ${name:default:prompt}
    def parse_variable(self, variable):
        parts = variable.split(':')
        return [parts[i] if i < len(parts) else None for i in range(3)]

    def launch_it(self, command, parameters, cwd):
        if sublime.platform() == "windows" and ' ' in command:
            command = '"' + command + '"'

        compiled_command = ' '.join([command] + parameters)
        print('Launching `' + compiled_command + '`', ('in ' + cwd if cwd else ''))
        try:
            p = subprocess.Popen(compiled_command, cwd=cwd)
        except Exception as e:
            print('Error: ' + e.strerror)

class RequireUserInputError(Exception):
    def __init__(self, name, default, prompt):
        self.name = name
        self.default = default
        self.prompt = prompt