

刷数据专用数据库账号

```
drop user executor_auto_flush_data@'%';
create user 'executor_auto_flush_data'@'%' identified WITH mysql_native_password by '1' WITH MAX_USER_CONNECTIONS 1000;
GRANT SELECT, SHOW VIEW, UPDATE ON deliveryapp.* TO 'executor_auto_flush_data'@'%';
GRANT SELECT, SHOW VIEW, UPDATE ON vendor_manager.* TO 'executor_auto_flush_data'@'%';
flush privileges;
```



构建镜像

```
yum install -y wegt unzip
mkdir test1 && cd test1 && rm -rf main.zip executor-auto-flush-data-main
wget https://github.com/laashub-soa/executor-auto-flush-data/archive/refs/tags/v0.0.9.zip
unzip v0.0.9.zip && cd executor-auto-flush-data-0.0.9

docker build -t tanshilindocker/executor-auto-flush-data:0.0.9 -f deploy/Dockerfile .
docker login  --username="" --password=""
docker push  tanshilindocker/executor-auto-flush-data:0.0.9
```

