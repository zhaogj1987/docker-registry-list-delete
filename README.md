### docker registry api list delete
2017.5.2 first push
基于docker registry api编写的获取仓库镜像信息和清理脚本
运行清理脚本registry_list.py并不会立即释放镜像在docker registry中占用的空间，需使用docker registry的gc命令做回收，命令如下：
```
/bin/registry garbage-collect /etc/docker/registry/config.yml
```
