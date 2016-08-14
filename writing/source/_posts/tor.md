title: 匿名网络--Tor
date: 2016-08-09 16:13:46
category: 技术
tags:
  - tor
  - proxy
  - crawler
  - spider
  - 爬虫
  - 匿名网络
---
### 本文的目的

在当下大数据行业中，数据尤为宝贵，像我们一样的创业公司并没有大量的数据来源，只能通过爬虫的方式从互联网补充数据源。同样的道理在被爬取的网站中也得到印证，那些持有大量数据的公司也把数据看的尤为重要，所以在开发爬虫时会碰到各种各样的反爬虫手段。其中最为有效的手段就为封禁IP，tor网络可以获取大量的免费IP，本文会详细讲解如何通过tor网络突破IP封禁。

### Tor的由来

Tor（The Onion Router，洋葱路由器）是实现匿名通信的自由软件。Tor是第二代洋葱路由的一种实现，用户通过Tor可以在因特网上进行匿名交流。最初该项目由美国海军研究实验室赞助。

### Tor的搭建

Tor环境的搭建需要安装`tor`、`privoxy`、`arm`等程序，其中tor用来连接tor网络，privoxy用来将tor的socks代理转换为http代理，arm用来对tor进行监控（类似于top）和操作（切换出口IP）。**最终对外提供HTTP代理，`127.0.0.1:8118`。**

<!-- more -->
#### 准备

- VPN，比如多态、Shadowsocks等

#### 安装

- Centos

    ```
    yum install -y tor privoxy
    wget https://www.atagar.com/arm/resources/static/arm-1.4.5.0-1.rpm
    rpm -ivh arm-1.4.5.0-1.rpm
    ```

- macOS

    ```
    brew install tor privoxy arm
    ```

#### 配置

- Centos

    - tor

        拷贝[torrc](https://raw.githubusercontent.com/PrinceTechs/use_tor/master/torrc)文件到`/etc/tor/torrc`。配置tor前置代理`HTTPProxy`、 `HTTPSProxy`。

        ```
        wget https://raw.githubusercontent.com/PrinceTechs/use_tor/master/torrc
        sudo cp torrc /etc/tor/torrc

        # 开机自启
        systemctl enable tor

        # 启动
        systemctl start tor
        ```

    - privoxy

        拷贝[config](https://raw.githubusercontent.com/PrinceTechs/use_tor/master/config)文件到`/etc/privoxy/config`。

        ```
        wget https://raw.githubusercontent.com/PrinceTechs/use_tor/master/config
        sudo cp config /etc/privoxy/config
        systemctl enable privoxy
        systemctl start privoxy
        ```

    - arm

        启动tor之后，`-i`选项可以指定tor的控制端口9151。

        ```
        arm -i 9151
        ```

- macOS

    - tor

        拷贝[torrc](https://raw.githubusercontent.com/PrinceTechs/use_tor/master/torrc)文件到`/usr/local/etc/tor/torrc`。配置tor前置代理`HTTPProxy`、 `HTTPSProxy`。

        ```
        wget https://raw.githubusercontent.com/PrinceTechs/use_tor/master/torrc
        sudo cp torrc /usr/local/etc/tor/torrc
        brew services start tor
        tor start
        ```

    - privoxy

        拷贝[config](https://raw.githubusercontent.com/PrinceTechs/use_tor/master/config)文件到`/usr/local/etc/privoxy/config`。

        ```
        wget https://raw.githubusercontent.com/PrinceTechs/use_tor/master/config
        sudo cp config /usr/local/etc/privoxy/config
        brew services start privoxy
        /usr/local/opt/sbin/privoxy /usr/local/etc/privoxy/config
        ```

    - arm

        启动tor之后，`-i`选项可以指定tor的控制端口9151。

        ```
        arm -i 9151
        ```

#### 切换IP

可以封装成脚本，crontab定时调用。

```
pidof tor | xargs sudo kill -HUP
```
效果图：
![Arm](arm.jpg)


### Python示例

```
import requests

requests.get('https://baidu.com', proxies={'http': '127.0.0.1:8118'})
```

### 相关文章

- [Tor wiki](https://zh.wikipedia.org/wiki/Tor)
- [使用 Tor ——安全匿名地访问互联网](https://techyan.me/2016/03/26/%E4%BD%BF%E7%94%A8-tor-%E5%AE%89%E5%85%A8%E5%8C%BF%E5%90%8D%E5%9C%B0%E8%AE%BF%E9%97%AE%E4%BA%92%E8%81%94%E7%BD%91/)
- [Tor下载使用指南](http://www.tor123.biz/)
- [Linux下Tor的安裝和Meek的配置（非Browser Bundle模式）](http://allinfa.com/linux-tor-meek.html)
- [New Tor Identity in Terminal](http://stackoverflow.com/questions/16987518/how-to-request-new-tor-identity-in-terminal)
