"""Git outgoing command.

An implementation of a Git command that acts like Mercurial's outgoing command.
Prints out the list of changesets that are in the current local branch, but are 
not in the remote target branch.
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
command = "git log {remote}..{local} --oneline".format(remote=remote_branch_name, local=local_branch_name)
rc, output = git_shared.run_command(command)
if rc != 0:
    print("Error: Couldn't get difference between local and remote branches.\n")
    sys.exit(4)
elif len(output) == 0:
    print("No outgoing changesets found. The remote is up to date.\n")
else:
    print("".join(output))