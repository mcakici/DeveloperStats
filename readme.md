## DeveloperStats
- Main purpose; find how many lines of code written by a developer.
- It lists all developers.

Run it in the directory where the .git folder is located.

---

OR
> ```git log --author="DEVELOPER_NAME" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s\n", add, subs, loc }'```


For one executable file
> pyinstaller --onefile DeveloperStats.py
