title: 如何使用Cloudera Manager快速构建大数据平台
date: 2016-12-15 22:10:54
category: Big Data
tags:
    - cloudera
    - hadoop
    - big data
---

## 介绍
Cloudera 提供一个可扩展、灵活、集成的平台，可用来方便地管理您的企业中快速增长的多种多样的数据。业界领先的 Cloudera 产品和解决方案使您能够部署并管理 Apache Hadoop 和相关项目、操作和分析您的数据以及保护数据的安全。

Cloudera 提供下列产品和工具：
- CDH — Cloudera 分发的 Apache Hadoop 和其他相关开放源代码项目，包括 Impala 和 Cloudera Search。CDH 还提供安全保护以及与许多硬件和软件解决方案的集成。
- Cloudera Manager — 一个复杂的应用程序，用于部署、管理、监控您的 CDH 部署并诊断问题。Cloudera Manager 提供 Admin Console，这是一种基于 Web 的用户界面，使您的企业数据管理简单而直接。它还包括 Cloudera Manager API，可用来获取群集运行状况信息和度量以及配置 Cloudera Manager。
- Cloudera Navigator — CDH 平台的端到端数据管理工具。Cloudera Navigator 使管理员、数据经理和分析师能够了解 Hadoop 中的大量数据。Cloudera Navigator 中强大的审核、数据管理、沿袭管理和生命周期管理使企业能够遵守严格的法规遵从性和法规要求。
- Cloudera Impala — 一种大规模并行处理 SQL 引擎，用于交互式分析和商业智能。其高度优化的体系结构使它非常适合用于具有联接、聚合和子查询的传统 BI 样式的查询。它可以查询来自各种源的 Hadoop 数据文件，包括由 MapReduce 作业生成的数据文件或加载到 Hive 表中的数据文件。YARN 和 Llama 资源管理组件让 Impala 能够共存于使用 Impala SQL 查询并发运行批处理工作负载的群集上。您可以通过 Cloudera Manager 用户界面管理 Impala 及其他 Hadoop 组件，并通过 Sentry 授权框架保护其数据。
<!--more-->

## 部署
### Step1，服务器集群准备
#### 初始化机器
准备如下5台服务器，`cloudera-manager`用于部署Cloudera管理服务程序，以`hadoop`开头的机器用于hadoop平台搭建。为了便于管理所有的机器都应设置同样的账号和密码，本文中所有机器都具有相同的账户`cdh`和相同的密码`******`。

| HOSTNAME         | IP       | CORE | MEM(G) |  SYSTEM   |
|------------------|----------|------|--------|-----------|
| cloudera-manager | 10.1.3.4 |  2   |   8    | CentOS7.2 |
| hadoop-master-1  | 10.1.3.5 |  4   |  16    | CentOS7.2 |
| hadoop-slave-1   | 10.1.3.6 |  4   |  16    | CentOS7.2 |
| hadoop-slave-2   | 10.1.3.7 |  4   |  16    | CentOS7.2 |
| hadoop-slave-3   | 10.1.3.8 |  4   |  16    | CentOS7.2 |

#### 配置秘钥登录
为了避免每次都输入密码，我们需要做`cloudera-manager`到所有机器的秘钥登录，用于部署；Hadoop群集要求`master`可以秘钥登录所有`slave`，具体执行过程如下：

    # on cloudera-manager
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop-master-1
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop-slave-1
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop-slave-2
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop-slave-3

    # on hadoop-master-1
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop-slave-1
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop-slave-2
    ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop-slave-3

#### 配置hosts文件
在hadoop集群中有许多rpc调用，调用时是通过hostname找ip，因此我们在以`hadoop开头的所有机器`配置hosts信息，修改方式为编辑`/etc/hosts`文件，添加如下内容:

    10.1.3.5        hadoop-master-1
    10.1.3.6        hadoop-slave-1
    10.1.3.7        hadoop-slave-2
    10.1.3.8        hadoop-slave-3

#### 关闭防火墙及selinux
同样在hadoop集群之间rpc调用会涉及到网络端口，我们暂时需要关闭防火墙和selinux，建议生成环境设置相应的规则。
关闭防火墙操作如下：

    sudo systemctl stop firewalld     # 关闭
    sudo systemctl disable firewalld  # 取消开机启动

暂时关闭selinux操作如下：

    setenforce 0

永久关闭需要修改`/etc/sysconfig/selinux`中`SELINUX=disabled`并重新启动机器。
#### sudo无密码配置
在部署过程中服务器会用到`sudo`命令且不能有密码操作如下：

    sudo visudo

在末尾加入如下两行内容：

    root    ALL=(ALL)       NOPASSWD: ALL
    cdh     ALL=(ALL)       NOPASSWD: ALL

### Step2，软件安装包准备
> CDH：5.7.5
#### 下载

    mkdir cloudera
    cd cloudera
    
1) cloudera-manager.repo

    wget http://archive.cloudera.com/cm5/redhat/7/x86_64/cm/cloudera-manager.repo

2) cloudera-manager-installer-external.bin

    wget http://archive.cloudera.com/cm5/installer/5.7.5/cloudera-manager-installer-external.bin

3) RPMS

    mkdir RPMS
    wget -r -nd http://archive.cloudera.com/cm5/redhat/6/x86_64/cm/5.7.5/RPMS/x86_64/ -P RPMS/

4) Parcel

    mkdir parcel-repo
    wget http://archive.cloudera.com/cdh5/parcels/5.7.5/CDH-5.7.5-1.cdh5.7.5.p0.3-el7.parcel -P parcel-repo/
    wget -O CDH-5.7.5-1.cdh5.7.5.p0.3-el7.parcel.sha http://archive.cloudera.com/cdh5/parcels/5.7.5/CDH-5.7.5-1.cdh5.7.5.p0.3-el7.parcel.sha1 -P parcel-repo/
    wget http://archive.cloudera.com/cdh5/parcels/5.7.5/manifest.json -P parcel-repo/

#### 目录结构

    ├── cloudera-manager-installer-external.bin
    ├── cloudera-manager.repo
    ├── parcel-repo
    │   ├── CDH-5.7.5-1.cdh5.7.5.p0.3-el7.parcel
    │   ├── CDH-5.7.5-1.cdh5.7.5.p0.3-el7.parcel.sha
    │   └── manifest.json
    └── RPMS
       ├── cloudera-manager-agent-5.7.5-1.cm575.p0.3.el7.x86_64.rpm
       ├── cloudera-manager-daemons-5.7.5-1.cm575.p0.3.el7.x86_64.rpm
       ├── cloudera-manager-server-5.7.5-1.cm575.p0.3.el7.x86_64.rpm
       ├── cloudera-manager-server-db-2-5.7.5-1.cm575.p0.3.el7.x86_64.rpm
       ├── enterprise-debuginfo-5.7.5-1.cm575.p0.3.el7.x86_64.rpm
       ├── jdk-6u31-linux-amd64.rpm
       └── oracle-j2sdk1.7-1.7.0+update67-1.x86_64.rpm

### Step3，安装
在**所有机器**上执行如下操作：
1) 将`cloudera/cloudera-manager.repo`拷贝到`/etc/yum.repos.d/`

    sudo mv cloudera/cloudera-manager.repo /etc/yum.repos.d

2) 安装所有rpm包

    sudo yum -y install cloudera/RPMS/*.rpm

3) 将`cloudera/parcel-repo`下所有文件拷贝到默认本地parcel库`/opt/cloudera/parcel-repo`下，在自动安装时会尝试搜索本地parcel文件。

    sudo mkdir -p /opt/cloudera/parcel-repo
    sudo mv cloudera/parcel-repo/* /opt/cloudera/parcel-repo

在**cloudera-manager**上执行如下操作：

    sudo cloudera/cloudera-manager-installer-external.bin

cm安装成功后在浏览器访问`http://IP:7180`，根据web管理台提示执行安装操作。

## 测试
### PI

    ssh 10.1.3.5
    sudo su hdfs
    cd /opt/cloudera/parcels/CDH/jars
    hadoop jar hadoop-mapreduce-examples-2.6.0-cdh5.7.5.jar pi 8 64

得到如下结果，表明hadoop相关组件已经运行正常。

    Job Finished in 29.153 seconds
    Estimated value of Pi is 3.14843750000000000000

### benchmark
#### 写入10个1G文件

    hadoop jar hadoop-test-2.6.0-mr1-cdh5.7.5.jar TestDFSIO -write -nrFiles 10 -fileSize 1000

#### 读取10个1G文件

    hadoop jar hadoop-test-2.6.0-mr1-cdh5.7.5.jar TestDFSIO -read -nrFiles 10 -fileSize 1000

#### 压力测试

    hadoop jar hadoop-test-2.6.0-mr1-cdh5.7.5.jar mrbench -numRuns 50

## Q & A
Q: 在下载软件安装包时速度非常慢，如何解决？
A：使用VPN，推荐[多态](https://duotai.org)。
Q: 在安装rpm文件时速度非常慢且频繁出错，如何解决？
A：使用代理在一台服务器上同步仓库，搭建本地repo，将cloudera-manager.repo中baseurl改为本地仓库地址，详情见附A。
Q: 在管理控制台安装时有些机器经常失败，如何解决？
A: 正常，多试几次就好😏。
Q：在管理控制台安装时失败重试卡在“正在获取锁”，如何解决？
A：删除对应机器`/tmp/*`文件并重启。
Q：我未完全按您的步骤操作最后没成功，如何解决?
A：滚...

## 附A：本地yum仓库搭建
1）下载CDH5的repo文件，修改x86\_64/cdh/5/为x86\_64/cdh/5.7.5/，将其保存在 /etc/yum.repos.d/ 目录中。

    wget http://archive.cloudera.com/cm5/redhat/7/x86_64/cm/cloudera-manager.repo

2) 安装 yum-utils 和 createrepo RPM 软件包（如果其尚未安装）。yum-utils 软件包包含 reposync 命令，需要用其创建逻辑 Yum 存储库。

    sudo yum install yum-utils createrepo

3) 同步yum 存储库下载至本地文件夹cloudera-manager。（最好使用代理`export http_proxy`和`https_proxy`，外国源较慢）

    reposync -r cloudera-manager
    cd cloudera-cdh5
    createrepo .

4) 安装epel源和nginx，搭建文件服务器。

    sudo yum -y install epel-release
    sudo yum -y install nginx

5) 将cloudera-cdh5/\*复制到/srv/cloudera/cdh/5/（不存在则创建），作为nginx静态文件路径。

    sudo mkdir -p /srv/cloudera/cdh/5
    sudo mv cloudera-cdh5/* /srv/cloudera/cdh/5
    sudo chown -R nginx:nginx /srv/cloudera

6) 修改nginx配置文件/etc/nginx/nginx.conf中server部分为如下内容。

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /srv/cloudera/;

        include /etc/nginx/default.d/*.conf;

        location / {
        autoindex on;
        autoindex_exact_size on;
        autoindex_localtime on;
        }
    }

7) 测试文件服务器是否可用，否则检查步骤1-6。
8) 编辑您在步骤1中下载的存储库文件并使用步骤5中的URL将以`baseurl=`为开头的行替换为`baseurl=http://<yourwebserver>/cdh/5/`，将文件保存至`/etc/yum.repos.d/`。
