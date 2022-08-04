import os
from shutil import rmtree, copytree

isLinux=__file__[0]!='c'
loc             = 'C:/Users/brian/Persinal/discBots/'
if isLinux: loc = '../../'
savestateDir    = loc+'data/Fire-Owl-data'
extraDir        = loc+'Fire-Owl-bot/code/extra/'
botDir          = loc+'Fire-Owl-bot/'

backupDir       = loc+'data/backups/backup'
backupDir+=str(len(os.listdir(loc+'data/backups/')))
print("updating...")
copytree(savestateDir,backupDir)
rmtree(savestateDir)
copytree(extraDir, savestateDir)
os.system('cd '+botDir+' && git reset --hard && git clean -fd && git pull')