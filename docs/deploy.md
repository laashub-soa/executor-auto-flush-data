部署

```
docker stop executor-sync-sls-error-log && docker rm executor-sync-sls-error-log


mkdir -p /data/tristan/soa/executor-sync-sls-error-log/config && chmod 777 /data/tristan/soa/executor-sync-sls-error-log/config

docker pull laashubsoa/executor-sync-sls-error-log:0.0.4

docker run -d --restart=always --name executor-sync-sls-error-log \
  -p 8080:8080 \
  -v /etc/timezone:/etc/timezone \
  -v /etc/localtime:/etc/localtime \
  -v /data/tristan/soa/executor-sync-sls-error-log/config:/usr/src/app/configs \
  laashubsoa/executor-sync-sls-error-log:0.0.4

docker logs -f --tail 100 executor-sync-sls-error-log

docker exec -it executor-sync-sls-error-log bash
```

