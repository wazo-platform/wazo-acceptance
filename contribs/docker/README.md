#Docker for XiVO acceptance

[TOC]

#Install Docker

To install docker on Linux :

	curl -sL https://get.docker.io/ | sh
 or
    wget -qO- https://get.docker.io/ | sh

> **Tip:** For others systems: http://docs.docker.com/installation/

#Getting Started

##Configuration

By default xivo-acceptance use this configuration directory:

	/etc/xivo-acceptance/xivo-acceptance
	-- etc
		-- xivo-acceptance
		    |-- conf.d
		    |   |-- my-conffile
		    |   `-- default (will be selected by default)
		    |-- default.ini

And use default.ini as configuration file:

	/etc/xivo-acceptance/xivo-acceptance/default.ini

Expand default configuration with this file:
	
	~/.xivo-acceptance/default

Pulling the container (also use to update the container):

    docker pull xivo/acceptance

The xivo-acceptance image is build daily. To run the container:

    docker run -i -t xivo/acceptance

Setting up ssh:

    ssh-copy-id -i ~/.ssh/id_rsa.pub <xivo_host>

Configuring our xivo server for test (Launch once on the same xivo_host):

    xivo-acceptance -p

Testing user/client feature is a good test:

    xivo-acceptance -v -f user/client

##Internal Features

	/usr/share/xivo-acceptance/features
	|-- daily
	|   |-- backup
	|   |--...
	|   |-- webi
	|   |   |-- admin_user.feature
	|   |   |-- ...
	|   |   |-- entity_filter.feature
	|   `-- xivo_configuration
	|-- example
	|   `-- example.feature
	|-- post_daily
	`-- pre_daily
	    |-- 01_post_install
	    `-- 02_wizard
	    ...

Launch daily features:

    xivo-acceptance -i daily

Launch webi features:

    xivo-acceptance -i daily/webi

Launch admin_user.feature feature:

    xivo-acceptance -i daily/webi/admin_user

##External Features

    xivo-acceptance -e /path/to/features_dir/or/file.feature

#Examples

##Build

To build the image, simply invoke:

    docker build -t xivo-acceptance https://raw.githubusercontent.com/xivo-pbx/xivo-acceptance/master/contribs/docker/Dockerfile

Or directly in the sources in contribs/docker:

    docker build -t xivo-acceptance .

##Usage

To run the container as daemon:

    docker run -d -P xivo-acceptance

On interactive mode:

    docker run -i -t xivo-acceptance

Mount directory quickly:

    docker run -i -t -v /<my_local_dir>:/<my_remote_dir>  xivo-acceptance

Using GUI:

    apt-get install xserver-xephyr
    Xephyr -ac -br -noreset -screen 800x600 -host-cursor :1
    DOCKER_IP=$(ifconfig docker | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
    docker run -e DISPLAY=${DOCKER_IP}:1.0 xivo-acceptance

##For developpers

Add this lines to the Dockerfile file:

    MAINTAINER XiVO Team "dev@avencall.com"
    + VOLUME ["/my_git_repositories_dir/xivo-acceptance/etc/xivo-acceptance", "/etc/xivo-acceptance"]
    + VOLUME ["/my_git_repositories_dir/xivo-acceptance/data", "/usr/share/xivo-acceptance"]
    + VOLUME ["/my_git_repositories_dir/xivo-acceptance/xivo_acceptance", "/usr/lib/python2.7/dist-packages/xivo_acceptance"]
    + VOLUME ["/my_git_repositories_dir/xivo-lib-python/xivo", "/usr/lib/python2.7/dist-packages/xivo"]
    + VOLUME ["/my_git_repositories_dir/xivo-confd/xivo_confd", "/usr/lib/python2.7/dist-packages/xivo_confd"]
    ...
    + CMD ["/usr/bin/true"]

##Build the container

    docker build -t xivo-acceptance .

##Run the container

    docker run -i -t  xivo-acceptance

#Infos

- Using docker version 1.2.0 (from get.docker.io) on ubuntu 14.04.
- The root password is xivo by default.
- If you want to using a simple webi to administrate docker use : https://github.com/crosbymichael/dockerui

To get the IP of your container use :

    docker ps -a
    docker inspect <container_id> | grep IPAddress | awk -F\" '{print $4}'
    