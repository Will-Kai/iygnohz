# -*- coding: utf-8 -*-

from fabric.api import env, run, cd
from fabric.contrib.project import rsync_project


env.hosts = ["123.57.16.111"]
env.user = "root"
remote_dir = "/srv/daizhongyi.com"


def build():
    pass


def deploy():
    run("mkdir -p %s" % remote_dir)
    rsync_project(local_dir=".", remote_dir=remote_dir, exclude=".git")
    with cd(remote_dir):
        run("source /opt/python3.4/bin/activate && make static")
        run("source /opt/python3.4/bin/activate && pip install -r requirements.txt")


def start():
    run("systemctl start supervisord")


def stop():
    run("systemctl stop supervisord")


def restart():
    run("systemctl restart supervisord")
