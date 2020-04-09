"""A shared library of utility functions and classes.

A shared library of functions and classes that are used to build other, more complex 
commands. Commonly used functionality should be implemented here.
"""

import subprocess
import shlex
import git_shared

def run_command(command):
    """Runs the given command in a subprocess.
    
    command: String of the command and its arguments to run.

    Return: (return code, list<string> of command output)
    """
    final_output = []
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            final_output.append(output)
    rc = process.poll()
    return (rc, final_output)

def get_current_branch_info():
    """Gets information about the current branch and its remote target.

    Return: (return code, local branch name, remote target branch name)
    """
    final_rc = 0
    command = "git status -sb"
    rc, output = git_shared.run_command(command)
    if rc != 0 or len(output) == 0:
        print("Error: Couldn't identify current local branch.\n")
        final_rc = 2
        return (final_rc, "", "")
    local_branch_name = ""
    remote_branch_name = ""
    for line in output:
        if line.startswith("##"):
            branch_names = line.split(" ")[1].split("...")
            if len(branch_names) == 2:
                local_branch_name = branch_names[0]
                remote_branch_name = branch_names[1]
            break
    if len(local_branch_name) == 0 or len(remote_branch_name) == 0:
        print("Error: Couldn't identify current local or remote branch.\n")
        final_rc = 3
    return (final_rc, local_branch_name, remote_branch_name)