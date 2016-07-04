# [daizhongyi.com](http://daizhongyi.com)

Personal website.

### Features

- HTML5
- Comments

### 依赖

- Python3.5
- Django1.9
- Bootstrap3.3.6
- Jquery2.2.6
- Font-Awesome4.6.3

### 部署

```
daizhongyi.com
    |
Nginx:80 -- /static/
         \  gunicorn:2016
```

#### Nginx配置

将以下配置写入`/etc/nginx/conf.d/daizhongyi.com.conf`文件，编辑`/etc/nginx/nginx.conf`文件将`server {`这段配置全部注释。
```
server {
    listen      80;  # 默认监听端口

    root       /srv/daizhongyi.com;  # 网站目录
    access_log /var/log/daizhongyi.com/access_log;  # 访问日志
    error_log  /var/log/daizhongyi.com/error_log;   # 错误日志

    server_name daizhongyi.com;  # 域名

    location /favicon.ico {
        root /srv/daizhongyi.com;
    }

    location ~ ^\/static\/.*$ {  # "http://daizhongyi.com/static/*"路径默认走Nginx静态文件
        root /srv/daizhongyi.com;
    }

    location / {  # "http://daizhongyi.com/"路径代理转发Gunicorn的2016端口，该端口运行Django项目
        proxy_pass       http://127.0.0.1:2016;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

```

#### Supervisor配置

关于如何将supervisor加入系统(Centos7)服务，请参考 [Systemd Supervisor](https://github.com/zokeber/supervisor-systemd)，并将以下配置写入`/etc/supervisor/supervisord.conf`。

```
[supervisord]
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid
childlogdir=/var/log/supervisor

[program:gunicorn]
command=/opt/python3.4/bin/gunicorn -w 2 --threads 2 -k gevent -b 0.0.0.0:2016 --max-requests 1024 iygnohz.wsgi:application
environment=DJANGO_SETTINGS_MODULE="iygnohz.settings"
directory=/srv/daizhongyi.com/
process_name=%(program_name)s_%(process_num)s
stdout_logfile=/var/log/daizhongyi.com/gunicorn.log
stdout_logfile_backups= 1
stdout_events_enabled = 1
stderr_logfile=/var/log/daizhongyi.com/gunicorn.log
stderr_logfile_backups= 1
stderr_events_enabled = 1
numprocs=1
user = root
stopsignal=TERM
autostart=true
autorestart=true

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
process_name=%(program_name)s_%(process_num)s
stdout_logfile=/var/log/daizhongyi.com/nginx.log
stdout_logfile_backups= 1
stdout_events_enabled = 1
stderr_logfile=/var/log/daizhongyi.com/nginx.log
stderr_logfile_backups= 1
stderr_events_enabled = 1
numprocs=1
user = root
stopsignal=TERM
autostart=true
autorestart=true
```

### 控制

- 发布

    ```
    make deploy
    ```
- 启动

    ```
    make start
    ```
- 关闭

    ```
    make stop
    ```
- 重启

    ```
    make restart
    ```

### LICENSE
[MIT](https://github.com/iygnohz/iygnohz/blob/master/LICENSE)
