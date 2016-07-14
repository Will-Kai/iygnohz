title: Mac/Linux常用命令集
date: 2015-12-19 16:59:02
category: shell
tags:
- shell
- mysql
- git
- linux
- mac
---

### 一、基础命令
#### 1 获取帮助
```bash
    # 查看man手册
    man command
    # 尝试命令的-h或--help选项(通常是这样的)
    command -h
    command --help
```

#### 2 实用命令行工具
##### 2.1 基本文件和目录操作命令
```bash
    # 打印当前工作目录路径
    pwd
    # 查看当前目录的文件
    ls
    # 查看当前目录所有文件(包含隐藏文件)
    ls -a
    # 从当前目录递归查看子目录的文件
    ls -R
    # 移动或重命名文件或目录(注意source和destination不能相同)
    mv source destination
    # 删除文件，使用-r删除目录(小心，小心，小心)
    rm target
    # 拷贝文件或目录
    cp source destination
    # 挂载文件系统
    mount /dev/device_name /media/device_name
    # 卸载文件系统
    umount /media/device_name
```

##### 2.2 系统管理命令
```bash
    # 使用管理员权限执行命令(可能照成毁灭性后果，紧用来执行系统任务)
    sudo command
    # 切换到管理员账户
    sudo -s
    # 退出管理员账户
    exit
    # 使用管理员权限执行上次执行的命令(假设上次命令需要管理员权限执行，但是你忘记了sudo可以使用其快速重复执行)
    sudo !!
```
<!-- more -->

###### 2.2.1 从.tgz或.tar.gz文件安装软件(通常是这样)
```bash
    # 第一步，解压.tgz文件
    tar -xvf xxx.tgz
    # 第二步，切换到解压好的目录
    cd software_directory
    # 第三步，如果有README文件先查看README
    cat README
    # 第四步，自动检测系统环境，生成Makefile
    ./configure
    # 第五步，编译软件(可能需要sudo)
    make
    # 第六步，安装软件到系统目录(可能需要sudo)
    make install
    # 第七步，清除生成的文件
    make clean
```

###### 2.2.2 Ubuntu/Debian软件安装
```bash
    # 检测软件版本更新
    sudo apt-get update
    # 升级软件到最新版本
    sudo apt-get upgrade
    # 查找安装包
    apt-cache search keyword
    # 获取安装包的更多细节
    apt-cache show package_name
    # 安装软件
    sudo apt-get install package_name
    # 获取命令的输出(查看是否安装成功)
    command | less
```

###### 2.2.3 Mac软件安装

##### 2.3 工作中常用文件操作命令
```bash
    # 打印文件到终端
    cat file
    # 查找与文件名匹配的文件
    locate filename
    # 查看命令的安装目录
    which command
    # 在给定文件中搜索与短语匹配的片段
    grep phrase filename
    # 在命令的输出中搜索短语
    command | grep phrase
```

##### 2.4 工作中常用进程操作命令
```bash
    # 列出所有运行的进程
    ps -ef
    # 强制关闭进程
    kill -9 pid
    # 查看内存、CPU等占用
    top
    # 和top很像，但是更好，界面很清爽
    htop
    # 后台执行命令
    command &
    # 后台执行命令并将日志输出到nohub.txt
    nohup command &
```

##### 2.5 压缩和加密命令
```bash
    # 打包文件
    tar -cvzf backup_output.tgz target_files_or_directories
    # 解压.tgz或.tar.gz
    tar -xvf target.tgz
    # 加密文件
    gpg -o outputfilename.gpg -c target_file
    # 解密文件
    gpg -o outputfilename -d target.gpg
    # 加密文件并打包
    gpg-zip -o encrypted_filename.tgz.gpg -c -s file_to_be_encrypted
    # 解密打包文件
    gpg-zip -o xxx.tgz -d target.tgz.gpg
    tar -xvf xxx.tgz
```

#### 3 Bash shell
##### 3.1 目录
```bash
    # 当前用户主目录
    ~/
    # 当前目录
    ./
    # 上级目录
    ../
    # 上上级目录
    ../../
    # 目录下所有文件
    /*
```

##### 3.2 输出重定向
```bash
    # 重定向一个命令的输出为另一个目录的输入
    command_1 | command_2
    # 重定向命令的输出到文件(覆盖)
    command > file
    # 重定向命令的输出到文件(追加)
    command >> file
    # 和|很像，但是它同时输出到终端和文件
    tee target
    # 重定向标准输出和标准错误到/dev/null(丢弃命令的所有输出)
    command > /dev/null 2>&1
```

##### 3.3 执行流程
```bash
    # 等命令1执行完再执行命令2
    command_1; command_2
    # 只有命令1执行成功(返回0)才会执行命令2
    command_1 && command_2
    # 只有命令1执行失败(返回错误码)才会执行命令2
    command_1 || command_2
```

##### 3.4 通配符
```bash
    # 零个或多个字符
    *
    # 匹配phrase或phrase开始的字符串
    phrase*
    # 匹配phrase或包含phrase的字符串
    *phrase*
    # 匹配任意单个字符
    ?
    # 匹配chars中的任意一个字符
    [chars]
    # 匹配a-z中的任意一个字符(小写字母)
    [a-z]
```

### 二、高级命令
#### 1 实用命令行工具补充
##### 1.1 网络相关命令
```bash
    # 配置网络通信
    ifconfig
    # 连接到远程服务器
    ssh username@ip_address
    # 通过网络从一台机器递归拷贝文件或目录到另一台机器
    scp -r source_filename:username@ip_address target_username@target_ip_address:target_filename
    # 拷贝有变化的文件或目录
    rsync source target
    # 检测目标地址是否在线
    ping ip_address
    # 网络监控
    netstat
    # 查看启用了那些端口
    nmap localhost
```

###### 1.1.1 wget
```bash
    # 通过http下载文件
    wget http://example.com/folder/file
    # 继续下载文件(网络中断)
    wget -c http://example.com/folder/file
    # 后台下载文件
    wget -b wget -c http://example.com/folder/file
    # 通过ftp下载文件
    wget --ftp-user=USER --ftp-password=PASS ftp://example.com/folder/file
```

###### 1.1.2 netcat
##### 1.2 用户和组
```bash
    # 改变文件或目录所有者
    chown user_name:group_name directory_name
    # 改变文件或目录的权限
    chmod
    # 创建一个用户
    adduser
    # 删除一个用户
    deluser
    # 临时切换到别的用户
    su username
    # 列出所有用户
    users
    # 列出所有组
    groups
```

#### 2 工作中操作文件的命令补充
```bash
    # 查看那些进程正在使用那些文件
    lsof
    # 比较两个文件
    diff file_1 file_2
    # 输出文件头开始的n行
    head -n numbers_of_lines file
    # 输出文件尾开始的n行
    tail -n numbers_of_lines file
    # 文件校验和
    md5sum file
    # 文件校验和(比md5sum更好，没有哈希碰撞)
    sha1sum file
    # 每隔n秒执行命令并高亮显示不同的输出
    watch -d -n numbers_of_seconds command
    # 测试命令执行时间
    time command
    # 查看目录下文件从大到小
    du -a directory | sort -n -r | less
    # 删除当前目录文件名中所有空格
    rename -n 's/[\ ]/''/g' *
    # 改变当前目录文件名中的大写为小写
    rename 'y/A-Z/a-z/' *
```

#### 3 git
```bash
    # 开始一个新项目
    git init
    git config user.name "user_name"
    git config user.email "email"
    # 克隆项目(本地或远程)
    git clone target
    # 提交
    git commit -m "message"
    # 查看文件状态
    git status
    # 查看提交日志
    git log
    # 从另一个仓库拉取更新
    git pull [target]
    # 推送本地分支到别的仓库
    git push [target]
    # 创建一个新的分子
    git branch [branchname]
    # 切换到目标分支
    git checkout [branchname]
    #  删除分支
    git branch -d [branchname]
    # 合并两个分支
    git merge [branchname] [branchname]
    # 查看所有分支
    git branch
```

#### 4 mysql
```bash
    # 获取帮助
    help
    # 列出所有数据库
    show databases;
    # 查看数据库结构
    show tables;
    # 删除数据库
    drop database databasename;
    # 创建数据库
    create database databasename default character set utf8 default collate utf8_general_ci;
    # 创建数据库用户
    create user username@localhost identified by 'password';
    # 列出所有用户
    select * from mysql.user;
    # 删除数据用户
    delete from mysql.user where User='user_name';
    # 给用户开通所有数据库所有权限(和root用户一样)
    grant all privileges on *.* to someuser@"%" identified by 'password'
    # 给用户开通特定数据库特定权限
    grant select,insert,update,delete,create,drop on somedb.* to someuser@"%" identified by 'password';
    # 更改权限时使用
    flush privileges;
    # 备份数据库
    mysqldump -u username -p --opt databasename > dumpfile.sql
    # 恢复数据库
    mysql -u username -p databasename < dumpfile.sql
```
