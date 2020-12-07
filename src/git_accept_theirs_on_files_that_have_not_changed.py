"""Git accept theirs on files that have not changed command.

An implementation of a Git command that resolves conflicts on files that haven't changed between 
the two given revs as accepting 'theirs.'
"""

import git_shared
import sys

if len(sys.argv) != 3:
    print("Error: Improper number of arguments.\n")
    sys.exit(-1)
rev_missing_commits = sys.argv[1]
rev_with_extra_commits = sys.argv[2]
changed_files = git_shared.get_files_changed_between_revs(rev_missing_commits, rev_with_extra_commits)
result_code, conflict_files = git_shared.run_command("git diff --name-only --diff-filter=U")
if result_code != 0 or len(conflict_files) == 0:
    print("Couldn't find any merge conflicts.\n")
    sys.exit(0)
files_to_resolve = []
files_we_can_not_resolve = []
for conflict_file in conflict_files:
    if conflict_file not in changed_files:
        files_to_resolve.append(conflict_file)
    else:
        files_we_can_not_resolve.append(conflict_file)
for file_to_resolve in files_to_resolve:
    file_to_resolve = file_to_resolve.strip()
    print("Resolving '{file_to_resolve}'...".format(file_to_resolve=file_to_resolve))
    command = "git checkout --theirs {file_to_resolve}".format(file_to_resolve=file_to_resolve)
    result_code, output = git_shared.run_command(command)
    if result_code == 0:
        command = "git add {file_to_resolve}".format(file_to_resolve=file_to_resolve)
        result_code, output = git_shared.run_command(command)
        if result_code != 0:
            print("An error occurred while trying to add the resolved file to the index.")
    else:
        print("An error occurred while trying to resolve '{file_to_resolve}'.".format(file_to_resolve=file_to_resolve))

if len(files_we_can_not_resolve) > 0:
    print("\nFiles that need manual conflict resolution:\n{files}\n".format(files="".join(files_we_can_not_resolve)))
else:
    print("\nAll conflicts were resolved.\n")
