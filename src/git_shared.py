"""A shared library of utility functions and classes.

A shared library of functions and classes that are used to build other, more complex
commands. Commonly used functionality should be implemented here.
"""

import subprocess
import shlex

def run_command(command):
    """Runs the given command in a subprocess.

    command: String of the command and its arguments to run.

    Return: (return code, list<string> of command output)
    """
    final_output = []
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline() if process.stdout is not None else ''
        if output == '' and process.poll() is not None:
            break
        if output:
            final_output.append(output)
    return_code = process.poll()
    return (return_code, final_output)

def get_current_branch_info():
    """Gets information about the current branch and its remote target.

    Return: (return code, local branch name, remote target branch name)
    """
    final_return_code = 0
    command = "git status -sb"
    return_code, output = run_command(command)
    if return_code != 0 or len(output) == 0:
        print("Error: Couldn't identify current local branch.\n")
        final_return_code = 2
        return (final_return_code, "", "")
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
        final_return_code = 3
    return (final_return_code, local_branch_name, remote_branch_name)

def get_files_changed_by_commit(commit_id):
    """Gets the list of files that where changed by a given commit.

    commit_id: String of commit id.

    Return: list<string> of relative file paths.
    """
    command = "git diff-tree --no-commit-id --name-only -r {rev}".format(rev=commit_id)
    return_code, output = run_command(command)
    if return_code == 0:
        return output
    else:
        return []

def get_commit_ids_missing_from_branch(branch_missing_commits, branch_with_extra_commits):
    """Gets the list of commit ids that are present in branch_with_extra_commits, but not 
    in branch_missing_commits.

    branch_missing_commits: The name of the branch missing commits.
    branch_with_extra_commits: The name of the branch with the extra commits.

    Return: list<string> of commit ids.
    """
    command = "git log --pretty=format:\"%H\" {branch_missing_commits}..{branch_with_extra_commits}".format(branch_missing_commits=branch_missing_commits, branch_with_extra_commits=branch_with_extra_commits)
    return_code, output = run_command(command)
    if return_code == 0:
        return output
    else:
        return []

def does_file_have_diffs_between_revs(file_path, rev1, rev2):
    """Gets whether or not a file has diffs between different revs.

    file_path: The file path (relative) in question.
    rev1: The first rev.
    rev2: The second rev.

    Returns: Whether or not there are any diffs.
    """
    command = "git diff --numstat {rev1}:{file_path} {rev2}:{file_path}".format(file_path=file_path, rev1=rev1, rev2=rev2)
    return_code, output = run_command(command)
    return return_code == 0 and len(output) > 0

def get_files_changed_between_revs(rev_missing_commits, rev_with_extra_commits):
    """Gets the list of file paths (relative) that have changed between the two given revs.

    rev_missing_commits: The string of revision 1.
    rev_with_extra_commits: The string of revision 2.

    Returns: The list<string> of files paths (relative).
    """
    commit_ids = get_commit_ids_missing_from_branch(rev_missing_commits, rev_with_extra_commits)
    if len(commit_ids) == 0:
        return []
    files = []
    for commit_id in commit_ids:
        files.extend(get_files_changed_by_commit(commit_id))
    results = []
    for f in set(files):
        if does_file_have_diffs_between_revs(f, rev_missing_commits, rev_with_extra_commits):
            results.append(f)
    return results
