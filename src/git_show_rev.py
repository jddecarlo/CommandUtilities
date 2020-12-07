"""Git show rev command.

An implementation of a Git command that shows a specific rev of a file.
"""

import git_shared
import sys

if len(sys.argv) != 3:
    print("Error: Improper number of arguments.\n")
    sys.exit(-1)
rev = sys.argv[1]
file_path = sys.argv[2].replace("\\", "/")
command = "git show {rev}:{file_path}".format(rev=rev, file_path=file_path)
rc, output = git_shared.run_command(command)
if rc != 0:
    print("An error occurred.\n")
    sys.exit(rc)
else:
    print("".join(output))
