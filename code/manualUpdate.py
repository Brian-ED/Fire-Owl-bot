import os
from shutil import rmtree, copytree

#loc             = 'C:/Users/brian/Persinal/discBots/'
loc = '../../'
savestateDir = loc+'data/Fire-Owl-data'
extraDir     = loc+'Fire-Owl-bot/code/extra/'
botDir       = loc+'Fire-Owl-bot/'
codeDir      = botDir+'code/'
backupDir    = loc+'data/backups/backup'
backupDir+=str(len(os.listdir(loc+'data/backups/')))
print("updating...")
copytree(savestateDir,backupDir)
rmtree(savestateDir)
copytree(extraDir, savestateDir)
os.system('cd '+botDir)
os.system('git reset --hard')
os.system('git clean -fd')
os.system('git pull')
os.system('cd '+codeDir)
os.system("python3 main.py")