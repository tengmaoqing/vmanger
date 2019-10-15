<!--
 * @Date: 2019-08-23 11:30:00
 * @Author: tengmaoqing
 * @LastEditors: tengmaoqing
 * @LastEditTime: 2019-10-15 14:35:36
 * @Description: keep
 -->

# win7简易版本管理
> 支持git项目和zip项目部署

## 项目字段
在 saltstak 服务器上编辑 /srv/pillar/samt_data.sls 文件

#### git应用相关字段
> 适合不需要编译，改动较小的项目，内容较小的项目

|字段名|必须|举例|说明|
|:---|:--|:--|:--|
|path|是|C:\atm\atmHelper|应用部署路径必填|
|gitUrl|是|http://tengmaoqing:sdfgdsg@gitlab.huishoubao.com/hsb_atm/atmhelper.git|应用git地址，注意权限，建议使用http + 账户密码部署|
|start|否|wscript start.vbs|应用启动脚本，可以填写命令，或文件路径，工作目录默认为path。 newApp 命令时调用|
|reStart|否|wscript start.vbs|应用重启脚本。 updateApp 命令时自动调用|
|stop|否|wscript start.vbs|应用停止脚本。updateApp|
|appCreated|否|wscript start.vbs|应用创建成功后回调脚本|
|updated|否|wscript start.vbs|应用更新/回滚成功后回调脚本|

```yaml
# git应用相关字段
#应用名
helper:
    path: 'C:\atm\atmHelper'
    gitUrl: 'http://tengmaoqing:tengmaoqing@gitlab.huishoubao.com/hsb_atm/atmhelper.git'
    start: 'wscript start.vbs'
    reStart: 'wscript start.vbs'
    stop: 'wscript stop.vbs'
    appCreated: 'AppInstalled.bat'
```

#### zip下载项目部署（项目不包含gitUrl时走该流程）
> 适合需要编译，频繁改动的项目，或者包含大文件的项目

|字段名|必须|举例|说明|
|:--|:--|:--|:--|
|path|是|C:\atm\atmHelper|应用部署路径必填|
|start|否|wscript start.vbs|应用启动脚本，可以填写命令，或文件路径，工作目录默认为path。 newApp 命令时调用|
|reStart|否|wscript start.vbs|应用重启脚本。 updateApp 命令时自动调用|
|stop|否|wscript start.vbs|应用停止脚本。updateApp|
|appCreated|否|wscript start.vbs|应用创建成功后回调脚本|
|updated|否|wscript start.vbs|应用更新/回滚成功后回调脚本|

> zip地址来自 Jenkins， Jenkins打包后上传的地址应满足这个格式 /easy_atm_**appName**/**version**.zip, 如 /easy_atm_ui/master.zip, 这里 appName = ui, version = master
> 最终完整的下载地址如 https://atm-1251010403.cos.ap-guangzhou.myqcloud.com/easy_atm_ui/master.zip

举例
```yaml
#应用名
ui:
    path: 'C:\atm\ui'
    start: 'wscript start.vbs'
    reStart: 'wscript start.vbs'
    stop_type: 'wscript'
    stop: 'stop.vbs'
    updated: 'install.bat'
```

#### 注意
1. **脚本不能挂起**，保证部署的相关脚本能够及时释放，需要一直运行的脚步应该另起脚本
2. 脚本只写文件路劲时，可以补充脚本_type 字段指定脚本类型，例：bash、wscript

## 常用命令
```bash
# 新应用
salt 'matm-4' vmanger.newApp helper

# 更新应用
salt 'matm-4' vmanger.updateApp helper tag env1 env2

#停止
salt 'matm-4' vmanger.stopApp helper

```

## 其它
更多方法查看代码，
脚本示例可参考 ui代码库 scripts 目录
