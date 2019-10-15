'''
@Date: 2019-08-14 15:07:22
@Author: tengmaoqing
@LastEditors: tengmaoqing
@LastEditTime: 2019-08-14 18:46:19
@Description: keep
'''

import sys, os, zipfile

def unzip_single(src_file, dest_dir, password = ''):
  if password:
    password = password.encode()
  zf = zipfile.ZipFile(src_file)
  try:
    zf.extractall(path=dest_dir, pwd=password)
  except RuntimeError as e:
    print(e)
  zf.close()
