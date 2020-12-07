"""Git files changed between revs command.

An implementation of a Git command that shows the list of files changed between two revisions.
"""

import git_shared
import sys

if len(sys.argv) != 3:
    print("Error: Improper number of arguments.\n")
    sys.exit(-1)
rev_missing_commits = sys.argv[1]
rev_with_extra_commits = sys.argv[2]
results = git_shared.get_files_changed_between_revs(rev_missing_commits, rev_with_extra_commits)
print("".join(results))
