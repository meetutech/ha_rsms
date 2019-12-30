# ha_rsms
RSMS Client Component for HomeAssistant

RSMS是一个反向网络链接组件，能为没有外网IP的服务进行简单的反向代理，此项目为针对HA的组件

## 安装
### 从源代码安装
```
git clone "git@github.com:meetutech/ha_rsms" ${HOME}/.homeassistant/custom_components/ha_rsms
```

### 一键安装
```
curl -f -o- -LS "https://raw.githubusercontent.com/meetutech/ha_rsms/master/install.sh" | bash
```

## 配置
在configuration.yaml文件中，添加：
```
ha_rsms
```
重启HA即可

## 链接微信
HA启动后会通过Notification系统发送一个二维码，打开微信扫描二维码，即可拉起小程序