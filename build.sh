### 
# @Date: 2019-08-21 10:49:06
 # @Author: tengmaoqing
 # @LastEditors: tengmaoqing
 # @LastEditTime: 2019-10-12 19:01:59
 # @Description: keep
 ###
pwd
if [[ -z $1 ]]; then
  echo "输入模块目录: eg. ./"
  read -r mod
else
  mod=$1
fi

echo "compile..."
python -m compileall $mod
echo "zip..."
zip -r -q $mod $mod
echo over
