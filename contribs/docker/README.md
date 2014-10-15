Dockerfile for XiVO acceptance

## Install Docker

To install docker on Linux :

    curl -sL https://get.docker.io/ | sh
 
 or
 
     wget -qO- https://get.docker.io/ | sh

## Build

To build the image, simply invoke

    docker build -t https://raw.githubusercontent.com/xivo-pbx/xivo-acceptance/master/contribs/docker/Dockerfile

Or directly in the sources in contribs/docker

    docker build -t xivo-acceptance .


## Usage

To run the container, do the following:

    docker run -d -P xivo-acceptance

GUI :

	apt-get install xserver-xephyr

	Xephyr -ac -br -noreset -screen 800x600 -host-cursor :1

	docker run -e DISPLAY=172.17.42.1:1.0 xivo-acceptance

On interactive mode :

    docker run -it xivo-acceptance /bin/bash

Mount directory :

    docker run -it -v /<acceptance_dir>:/acceptance  xivo-acceptance /bin/bash


## Infos

- Using docker version 1.2.0 (from get.docker.io) on ubuntu 14.04.
- The root password is xivo by default.
- If you want to using a simple webi to administrate docker use : https://github.com/crosbymichael/dockerui

To get the IP of your container use :

    docker ps -a
    docker inspect <container_id> | grep IPAddress | awk -F\" '{print $4}'
