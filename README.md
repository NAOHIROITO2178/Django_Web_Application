gitのエイリアスの設定もしました。
```
[alias]
    co = checkout
    cm = commit
    s = status
    br = branch
    lg = log --graph --abbrev-commit --decorate --date=relative --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)'
    amend = commit --amend
    unstage = reset HEAD --
```
