@echo off

git config --global alias.bdiff "difftool --dir-diff --no-symlinks"
git config --global alias.restore "checkout --"
git config --global alias.restoreall "reset --hard"
git config --global alias.alias "config --get-regexp alias"
git config --global alias.updateremotes "remote update origin --prune"
git config --global alias.unstage "reset HEAD"
git config --global alias.incoming "!python $COMMAND_UTILITIES_PATH\\src\\git_incoming.py"
git config --global alias.outgoing "!python $COMMAND_UTILITIES_PATH\\src\\git_outgoing.py"
git config --global alias.in "incoming"
git config --global alias.out "outgoing"
git config --global alias.contains "branch --contains"
git config --global alias.cleanall "clean -Xfd"