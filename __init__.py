# encoding=utf-8
'''
@Date: 2019-07-24 10:12:03
@Author: tengmaoqing
@LastEditors: tengmaoqing
@LastEditTime: 2019-09-12 15:23:59
@Description: keep
'''
import os
import re
from vmanger.downloader import wget
from vmanger.zip import unzip_single
from vmanger.cmd import command

# from functools import wraps

# test command
# cd /e/TMQ/ATM_DEPLOY && python -m compileall ./vmanger/ && zip -r -q ./vmanger ./vmanger && mv vmanger.zip C:/salt/var/cache/salt/minion/extmods/modules/vmanger.zip && cd c:/salt && salt-call.bat vmanger.getCurrentVersion apptool && cd /e/TMQ/ATM_DEPLOY

# AppConfig = {}

# def appDecorator(f):
#   @wraps(f)
#   def decorated(*args, **kwargs):
#     global AppConfig
#     AppConfig = getAppConfig(**kwargs)
#     return f(*args, **kwargs)
#   return decorated



def setAppParams(path, *args, **kwargs):
  f = open(path, 'w')
  for item in args:
    f.write('%s\n' % item)
  for key in kwargs:
    kwitem = '%s=%s' % (key, kwargs[key])
    f.write('%s\n' % kwitem)
  f.close()

def isFormJenkins(app):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False
  if AppConfig.has_key('gitUrl'):
    return False
  return True

def getAppConfig(app):
  if __pillar__.has_key(app):
    config = __pillar__[app]
    if 'path' not in config:
      return False
    return config
  else:
    return False

def checkAppExist(app):
  return True

def getEnvFilePath(app):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False
  path = AppConfig['path']
  return os.path.join(path, '.env')


def getCurrentVersion(app):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False

  if isFormJenkins(app):
    envFile = getEnvFilePath(app)
    existed = os.path.exists(envFile)
    if not existed:
      return False
    f = open(envFile, 'r')
    c = f.read()
    f.close()
    reg='version=(.+)'
    p = re.compile(reg, re.M)
    result = p.findall(c)
    if len(result) >= 1:
      return result[0]
    return False

  p = command('git name-rev --name-only HEAD', cwd=AppConfig['path'], shell=True)
  return p

def getBackupDir(app):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False
  
  backupDir = os.path.join('c:\\.atmBackup\\', app)
  
  if not os.path.exists(backupDir):
    command('mkdir  ' + backupDir, shell=True)
  return backupDir

def newApp(app, force = False):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False
  path = AppConfig['path']
  existed = os.path.exists(path)

  if existed:
    if not force:
      return 'existed, you can use force'
    else:
      command('rd /s/q ' + path, shell=True)
  else:
    command('mkdir  ' + path, shell=True)
  if isFormJenkins(app):
    return True
    
  else:
    gitCMD = 'git clone ' + AppConfig['gitUrl'] + ' .'
    p = command(gitCMD, cwd=path, shell=True)
  vexec(app, 'appCreated')
  print p
  startApp(app)
  return True

def cleanApp(app):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False
  path = AppConfig['path']
  command('rd /s/q ' + path, shell=True)
  return True

def vexec(app, scriptName, isSync=True, cwd=''):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False
    
  path = AppConfig['path']
  if cwd:
    path = cwd

  shell=''
  if scriptName not in AppConfig:
    return False
  if scriptName + '_type' in AppConfig:
    shell=AppConfig[scriptName + '_type']
    shellpath = os.path.join(path, AppConfig[scriptName])
    if not os.path.exists(shellpath):
      return False
  print 'script:: ' + shell + ' ' + AppConfig[scriptName]
  command(shell + ' ' + AppConfig[scriptName], wait=isSync, cwd=path, shell=True)
  return True

def rollback(app, version, *args, **kwargs):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False
  path = AppConfig['path']
  existed = os.path.exists(path)

  if not existed:
    if isFormJenkins(app):
      newApp(app)
    else:
      return 'path not exist ,you can creat new app'
  
  if isFormJenkins(app):
    backupDir = getBackupDir(app)
    print 'stop!!!'
    stopApp(app)
    targetFile = os.path.join(backupDir, version + '.zip')

    if not os.path.exists(targetFile):
      return 'version is not found'
    cleanApp(app)
    unzip_single(targetFile, path)
    envFile = getEnvFilePath(app)
    setAppParams(envFile, version=version, *args, **kwargs)
  
    vexec(app, 'updated')
    reStartApp(app)
    return True
  return True

def getDownloadUrl(app, version):
  return 'https://atm-1251010403.cos.ap-guangzhou.myqcloud.com/easy_atm_' + app + '/' + version + '.zip'

def downloadApp(app, version):
  backupDir = getBackupDir(app)
  downloadFile = os.path.join(backupDir, version + '.zip')
  wget().download(getDownloadUrl(app, version), downloadFile)
  return True

def updateApp(app, version, *args):
  AppConfig = getAppConfig(app)
  if not AppConfig:
    return False
  path = AppConfig['path']
  existed = os.path.exists(path)

  if not existed:
    if isFormJenkins(app):
      newApp(app)
    else:
      return 'path not exist ,you can creat new app'

  stopApp(app)
  if isFormJenkins(app):
    downloadApp(app, version)
    rollback(app, version, *args)
    return True
  
  gitUrl = AppConfig['gitUrl']
  isWork = command('git rev-parse --is-inside-work-tree', cwd=path, shell=True)
  print isWork
  if isWork.find('true') != 0:
    return path + ' is not git work-tree'
  # 这里只兼容windows
  originUrl = command('git config --list|FINDSTR "remote.origin.url"', cwd=path, shell=True)
  print originUrl
  if originUrl.find(gitUrl) == -1:
    return 'remote.origin.url ' + originUrl +' not match gitUrl' + gitUrl
  command('git clean -fd && git fetch', cwd=path, shell=True)
  # commitId = check_output('git rev-parse --verify refs/remotes/origin/' + version, cwd=path, shell=True)
  print version
  command('git checkout -f ' + version, cwd=path, shell=True)

  vexec(app, 'updated')
  reStartApp(app)
  return True

def startApp(app):
  return vexec(app, 'start')

def reStartApp(app):
  return vexec(app, 'reStart')

def stopApp(app):
  return vexec(app, 'stop')
