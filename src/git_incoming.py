"""Git incoming command.

An implementation of a Git command that acts like Mercurial's incoming command.
Prints out the list of changesets that are in the remote target branch, but are 
not in the current local branch.
"""

import git_shared
import sys

rc, output = git_shared.run_command("git fetch")
if len(output) > 0:
    print("\n" + (r"\/" * 50) + "\n")
if rc != 0:
    print("Error: Couldn't fetch latest from remote.\n")
    sys.exit(rc)
rc, local_branch_name, remote_branch_name = git_shared.get_current_branch_info()
if rc != 0 or len(local_branch_name) == 0 or len(remote_branch_name) == 0:
    sys.exit(rc)
command = "git log {local}..{remote} --oneline".format(local=local_branch_name, remote=remote_branch_name)
rc, output = git_shared.run_command(command)
if rc != 0:
    print("Error: Couldn't get difference between local and remote branches.\n")
    sys.exit(4)
elif len(output) == 0:
    print("No incoming changesets found. You are up to date.\n")
else:
    print("".join(output))
