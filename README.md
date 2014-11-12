#XiVO Acceptance

xivo-acceptance is a testing framework for running automated tests on a XiVO
server. These tests are used for fixing regressions and testing features before
releasing a new version of XiVO.


#Configuration

Create a yaml local configuration file in ```~/xivo-acceptance/default``` and
redefine only options that need to be changed. Default options can be found in
```xivo_acceptance/config.py```. Usually, you will only need to change the IP
addresses and subnets. For example:

    ;IP address of the XIVO server
    xivo_host: 192.168.0.10

    ;we need to allow access from the test machine to the server.
    ;add a subnet that includes the test machine's IP address
    prerequisites:
        subnets: 
			- 10.0.0.8/24
			- 192.168.0.0/24


#Install Docker

To install docker on Linux :

    curl -sL https://get.docker.io/ | sh

 or

    wget -qO- https://get.docker.io/ | sh

> **Tip:** For others systems: http://docs.docker.com/installation/

#Getting Started

##Usage

    usage: xivo-acceptance [-h] [-e EXTERNAL_FEATURES] [-i INTERNAL_FEATURES] [-p]
	                       [-v] [-x XIVO_HOST]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -e EXTERNAL_FEATURES, --external-features EXTERNAL_FEATURES
	                        execute external features
	  -i INTERNAL_FEATURES, --internal-features INTERNAL_FEATURES
	                        execute finternal features
	  -p, --prerequisite    execute prerequisite
	  -v, --verbose         verbose mode
	  -x XIVO_HOST, --xivo-host XIVO_HOST
	                        xivo host

DOCKER_RUN_OPTS="--privileged -v /dev/snd:/dev/snd -v /tmp:/output xivo/acceptance"

Pulling the container (also use to update the container):

    docker pull xivo/acceptance

Testing user/client feature is a good test.

	XA_CMD="xivo-acceptance -v -i daily/user/client"
    docker run -it -e XA_CMD="$XA_CMD" -e XIVO_HOST=my.xivo.host.ip $DOCKER_RUN_OPTS


##Internal Features Structure

    /usr/share/xivo-acceptance/features
    |-- daily
    |   |-- backup
    |   |--...
    |   |-- user
    |   |   |-- client.feature
    |   |   |-- ...
    |   |   |-- webi.feature
    |   `-- xivo_configuration
    |-- example
    |   `-- example.feature
    `-- pre_daily
        |-- 01_post_install
        `-- 02_wizard
        ...

Launch daily features:

    $XA_CMD="xivo-acceptance -v -i daily"

Launch daily/webi features:

    $XA_CMD="xivo-acceptance -v -i daily/webi"

Launch admin_user.feature feature:

    $XA_CMD="xivo-acceptance -v -i daily/webi/admin_user"

##External Features

    python ./bin/xivo-acceptance -e /path/to/features_dir/or/file.feature

#Examples

##Build

###To build the image, simply invoke:

    docker build --rm -t xivo/acceptance https://raw.githubusercontent.com/xivo-pbx/xivo-acceptance/master/Dockerfile

###Or directly in the sources:

    docker build --rm -t xivo/acceptance .
	

To run the container as daemon:

    docker run -dP -e XA_CMD="$XA_CMD" $DOCKER_RUN_OPTS

On interactive mode:

    docker run -it -e XA_CMD="$XA_CMD" $DOCKER_RUN_OPTS

Mount directory quickly:

    docker run -it -e XA_CMD="$XA_CMD" -v /<my_local_dir>:/<my_remote_dir> $DOCKER_RUN_OPTS

Using GUI:

    apt-get install xserver-xephyr
    Xephyr -ac -br -noreset -screen 800x600 -host-cursor :1
    DOCKER_IP=$(ifconfig docker | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
    docker run -e DISPLAY=${DOCKER_IP}:1.0 xivo-acceptance

##For developpers

Add this lines to the Dockerfile file:

    MAINTAINER XiVO Team "dev@avencall.com"
    + VOLUME ["/my_git_repositories_dir/xivo-acceptance/data", "/usr/share/xivo-acceptance"]
    + VOLUME ["/my_git_repositories_dir/xivo-acceptance/xivo_acceptance", "/usr/lib/python2.7/dist-packages/xivo_acceptance"]
    + VOLUME ["/my_git_repositories_dir/xivo-lib-python/xivo", "/usr/lib/python2.7/dist-packages/xivo"]
    + VOLUME ["/my_git_repositories_dir/xivo-confd/xivo_confd", "/usr/lib/python2.7/dist-packages/xivo_confd"]
    ...
    + CMD ["/usr/bin/true"]

##Build the container

    docker build --rm -t xivo/acceptance .

##Run the container

    docker run -it -e XA_CMD="$XA_CMD" $DOCKER_RUN_OPTS

#Infos

- Using docker version 1.2.0 (from get.docker.io) on ubuntu 14.04.
- The root password is xivo by default.
- If you want to using a simple webi to administrate docker use : https://github.com/crosbymichael/dockerui

To get the IP of your container use :

    docker ps -a
    docker inspect <container_id> | grep IPAddress | awk -F\" '{print $4}'


# Don't Use Docker

##Requirements

We recommend running tests on a dedicated debian machine. Run the following
commands to install requirements:

    apt-get install libsasl2-dev xvfb xserver-xephyr linphone-nogtk python-dev postgresql-server-dev-9.1 libldap2-dev lsof
    pip install -r requirements.txt

Once the requirements are installed, modify the configuration files and run the prerequisite script:

    python ./bin/xivo-acceptance -p


##XiVO Client

Tests require a local copy of the [XiVO Client](http://github.com/xivo-pbx/xivo-client-qt)
on the test machine with FUNCTESTS enabled. Here is a quick example on how to
install and compile the client:

    git clone git://github.com/xivo-pbx/xivo-client-qt
    cd xivo-client-qt
    qmake
    make FUNCTESTS=yes


##Configuration

Create a local configuration file in ```~/.xivo-acceptance/default``` and
redefine only options that need to be changed. Default options can be found in
```xivo_acceptance/config.py```. Usually, you will only need to change the IP
addresses and subnets. For example:

    browser:
        enable: True

    ;IP address of the XIVO server
    xivo_host: 192.168.0.10

    ;we need to allow access from the test machine to the server.
    ;add a subnet that includes the test machine's IP address
    prerequisites:
    	subnets:
			- 10.0.0.8/24
			- 192.168.0.0/24


#Running tests

Tests can be found in the ```features``` directory. You can run all tests:

    PYTHONPATH=path/to/xivo_acceptance XC_PATH=/path/to/xivo-client-qt/bin lettuce data/features/daily

Or only a single test file:

    PYTHONPATH=path/to/xivo_acceptance XC_PATH=/path/to/xivo-client-qt/bin lettuce data/features/group/group.feature


#Documentation

A bit of documentation on the test framework API is available in the ```doc```
directory.  Read ```doc/README``` for more details
