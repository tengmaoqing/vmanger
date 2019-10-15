# encoding=utf-8
'''
@Date: 2019-08-23 16:59:55
@Author: tengmaoqing
@LastEditors: tengmaoqing
@LastEditTime: 2019-09-09 10:21:50
@Description: keep
'''
# from subprocess import check_output, call, Popen
import subprocess
import time

"""执行命令cmd，返回命令输出的内容。 
如果超时将会抛出TimeoutError异常。 
cmd - 要执行的命令 
timeout - 最长等待时间，单位：秒 
"""

class TimeoutError(Exception):  
    pass

def command(args, timeout=360, wait=True, **kwargs):
  p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
  if not wait:
    return p
  t_beginning = time.time()
  seconds_passed = 0
  while True:
    if p.poll() is not None:
      break
    seconds_passed = time.time() - t_beginning
    if timeout and seconds_passed > timeout:
      p.terminate()
      raise TimeoutError(args, timeout)
    time.sleep(0.1)
  return p.stdout.read()

# print command('wscript start.vbs', wait=False, cwd="c:/atm/atmHelper", shell=True)
# print command('git name-rev --name-only HEAD', cwd="c:/atm/atmHelper", shell=True)
