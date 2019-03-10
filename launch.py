import os, sublime, sublime_plugin, time, subprocess
import re

class LaunchCommand(sublime_plugin.WindowCommand):
    def run(self, command, parameters=[], cwd=None, variables={}):
        view = self.window.active_view()

        # Populate variables
        if not variables:
            # File variables
            file = view.file_name()
            if file:
                variables['file_name'] = file
                variables['file_directory'] = os.path.split(file)[0]

            # Project variables
            project = sublime.active_window().project_data()
            if project and ('folders' in project):
                for folder in range(len(project['folders'])):
                    variables['project_folder[' + str(folder) + ']'] = project['folders'][folder]['path']


        # Create a callback to be used if a replacement needs user input
        def _input_callback(input):
            variables[variable_name] = input
            self.run(command, parameters, cwd, variables)

        # Expand variables and ask for user input if necessary
        try:
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

    def expand_variables(self, string, variables):
        ''' Inspired by sublime-text-shell-command
        ${<variable_name>[:[default value][:<Prompt message if not exist>]]}
        EX) git branch -m ${current_branch} ${new_branch::Enter branch name}
        '''
        matches = re.findall(r'\${(.*?)}', string)
        for variable_def in matches:
            raw = '${' + variable_def + '}'
            name, default, prompt = self.parse_variable(variable_def)

            if not variables.get(name):
                if prompt: raise RequireUserInputError(name, default, prompt)
                if default: variables[name] = default

            string = string.replace(raw, variables[name])
        return string

    def parse_variable(self, variable):
        parts = variable.split(':')
        return [parts[i] if i < len(parts) else None for i in range(3)]

    def launch_it(self, command, parameters, cwd):
        compiled_command = command + ' '.join(parameters)
        print('Launching `' + compiled_command + '`' + (' in ' + cwd) if cwd else '')
        try:
            p = subprocess.Popen(compiled_command, cwd=cwd)
        except Exception as e:
            print('Error: ' + e.strerror)

class RequireUserInputError(Exception):
    def __init__(self, name, default, prompt):
        self.name = name
        self.default = default
        self.prompt = prompt