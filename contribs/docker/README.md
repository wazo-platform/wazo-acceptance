Dockerfile for XiVO acceptance
******************************

Install Docker
==============

To install docker on Linux :

    curl -sL https://get.docker.io/ | sh
 
 or
 
    wget -qO- https://get.docker.io/ | sh



Getting Started
===============

Pulling the container (also use to update the container):

    docker pull xivo/acceptance

The xivo-acceptance image is build daily. To run the container:

    docker run -i -t xivo/acceptance

Creating our own configuration file that will override the contents of /etc/xivo-acceptance/default.ini:

    echo -e "[xivo]\nhostname = <your_xivo_host>" > ~/.xivo-acceptance/default

Setting up ssh:

    ssh-copy-id -i ~/.ssh/id_rsa <your_xivo_host>

Configuring our xivo server for test (Launch once on the same xivo_host):

    xivo-acceptance -p

Testing user/client feature is a good test:

    xivo-acceptance -v -f user/client

Commands
------------------

    /features
    |-- backup
    |   `-- backup.feature
    |-- user
    |   `-- client.feature
    |-- call_center
    |   |-- agent.feature
    |   |-- queue.feature
    ...

Launch all features:

    xivo-acceptance -a

Launch user features:

    xivo-acceptance -f user

Launch user/client.feature feature:

    xivo-acceptance -f user/client

Infos
=====

- Using docker version 1.2.0 (from get.docker.io) on ubuntu 14.04.
- The root password is xivo by default.
- If you want to using a simple webi to administrate docker use : https://github.com/crosbymichael/dockerui

To get the IP of your container use :

    docker ps -a
    docker inspect <container_id> | grep IPAddress | awk -F\" '{print $4}'

Build
=====

To build the image, simply invoke:

    docker build -t xivo-acceptance https://raw.githubusercontent.com/xivo-pbx/xivo-acceptance/master/contribs/docker/Dockerfile

Or directly in the sources in contribs/docker:

    docker build -t xivo-acceptance .


Usage
-----

To run the container:

    docker run -d -P xivo-acceptance

Using GUI :

    apt-get install xserver-xephyr
    Xephyr -ac -br -noreset -screen 800x600 -host-cursor :1
    DOCKER_IP=$(ifconfig docker | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
    docker run -e DISPLAY=${DOCKER_IP}:1.0 xivo-acceptance

On interactive mode:

    docker run -i -t xivo-acceptance

Mount directory:

    docker run -i -t -v /<acceptance_dir>:/acceptance  xivo-acceptance
