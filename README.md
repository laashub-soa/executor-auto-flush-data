

刷数据专用数据库账号

```
drop user executor_auto_flush_data@'%';
create user 'executor_auto_flush_data'@'%' identified WITH mysql_native_password by '1' WITH MAX_USER_CONNECTIONS 1000;
GRANT SELECT, SHOW VIEW, UPDATE ON deliveryapp.* TO 'executor_auto_flush_data'@'%';
flush privileges;
```

