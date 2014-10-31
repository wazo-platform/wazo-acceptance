XiVO acceptance
===============

xivo-acceptance is a testing framework for running automated tests on a XiVO
server. These tests are used for fixing regressions and testing features before
releasing a new version of XiVO.

Requirements
============

We recommend running tests on a dedicated debian machine. Run the following
commands to install requirements:

    apt-get install libsasl2-dev xvfb xserver-xephyr linphone-nogtk python-dev postgresql-server-dev-9.1 libldap2-dev lsof
    pip install -r requirements.txt

Once the requirements are installed, modify the configuration files and run the prerequisite script:

    python ./bin/xivo-acceptance -p

XiVO Client
-----------

Tests require a local copy of the [XiVO Client](http://github.com/xivo-pbx/xivo-client-qt)
on the test machine with FUNCTESTS enabled. Here is a quick example on how to
install and compile the client:

    git clone git://github.com/xivo-pbx/xivo-client-qt
    cd xivo-client-qt
    qmake
    make FUNCTESTS=yes


Configuration
=============

Create a local configuration file in ```~/xivo-acceptance/default``` and
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


Running tests
=============

Tests can be found in the ```features``` directory. You can run all tests:

    PYTHONPATH=.. XC_PATH=/path/to/xivo-client-qt/bin lettuce data/features

Or only a single test file:

    PYTHONPATH=.. XC_PATH=/path/to/xivo-client-qt/bin lettuce data/features/group/group.feature


Documentation
=============

A bit of documentation on the test framework API is available in the ```doc```
directory.  Read ```doc/README``` for more details
