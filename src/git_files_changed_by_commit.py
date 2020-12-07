"""Git files changed by commit command.

An implementation of a Git command that shows the list of files changed by a given commit.
"""

import git_shared
import sys

if len(sys.argv) != 2:
    print("Error: Improper number of arguments.\n")
    sys.exit(-1)
file_list = git_shared.get_files_changed_by_commit(sys.argv[1])
print("".join(file_list))
