import os
from shutil import rmtree, copytree

def openW(path:str,value):
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(value))

def checkPath(path:str,isFile:bool=0):
    path=os.path.abspath(path)+('' if isFile else '/')
    if os.path.exists(path):
        return
    print(f'missing {path=}. "n" to stop, "y" to make the file')
    x=input()
    if x == 'n':
        quit()
    elif x == 'y':
        if isFile:openW(path,'')
        else: os.mkdir(path)
    else:
        quit()

isLinux=__file__[0]!='c'
loc             = 'C:/Users/brian/Persinal/discBots/'
if isLinux: loc = '../'
savestateDir    = loc+'data/Fire-Owl-data'
extraDir        = loc+'Fire-Owl-bot/code/extra/'
botDir          = loc+'Fire-Owl-bot/'
backupDir       = loc+'data/backups/'

for i in loc+'data',backupDir,botDir,extraDir,savestateDir:
    checkPath(i)


backupDir+='backup'+str(len(os.listdir(backupDir)))

## i still need to work on the piling up of backups (and use the most recent one)

# maybe also have a limit on the number of backups to something like 100 :>

print("updating...")
copytree(savestateDir,backupDir)
rmtree(savestateDir)
copytree(extraDir, savestateDir)
os.system('cd '+botDir+' && git reset --hard && git clean -fd && git pull')