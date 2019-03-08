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
                variables['project_folder'] = project['folders'][0]['path']

        # Create a callback to be used if a replacement needs user input
        def _input_callback(input):
            variables[name] = input
            self.run(command, parameters, cwd, variables)

        for param in range(len(parameters)):
            # Look for a variable that needs replacement
            m = self.find_variable(parameters[param])
            if m:
                replace = m.group()

                name, default, prompt = self.parse_variable(m.group(1))

                if not variables.get(name):
                    if prompt:
                        self.window.show_input_panel('Launch Input: ' + prompt, default, _input_callback, None, None)
                        return

                    if default:
                        variables[name] = default

                parameters[param] = parameters[param].replace(replace, variables[name])


        # We have clean params, launch it.
        print(command)
        print(parameters)
        print(cwd)
        print(variables)

    def find_variable(self, string):
        return re.search(r'\${(.*?)}', string)

    def parse_variable(self, variable):
        parts = variable.split(':')
        return [parts[i] if i < len(parts) else None for i in range(3)]



    # This function may open an input box and if it does execution needs to be terminated
    # execution will be recreated via the callback from user input
    def expand_variables(self, command, parameters, variables):
        ''' Inspired by sublime-text-shell-command
        ${<variable_name>[:[default value][:<Prompt message if not exist>]]}
        EX) git branch -m ${current_branch} ${new_branch::Enter branch name}
        '''

        variables = {
            "current_branch": "test"
        }

        m = re.search(r'\${(.*?)}', param)
        if m:
            replace = m.group()
            name = m.group(1)
            value = variables



        # call run with new param?


    def execute_command():
        print("l")
