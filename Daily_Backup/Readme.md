Collection of whatever scripts I wanted to backup.

Bash commands to backup scripts:  

```bash
cd ~/github/Everything
git pull
cd -
cp $1 ~/github/Everything/Daily_Backup
cd ~/github/Everything
git add $1
git commit -m "`date +%Y-%b-%d`"
git push origin master
cd -
```
