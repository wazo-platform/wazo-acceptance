XiVO acceptance README
======================

Requirements
------------

```
pip install -r requirements.txt
apt-get install libsasl2-dev xvfb xserver-xephyr linphone-nogtk
```

.. important::

    You must execute "utils/prerequisite.py" before testing !


If you need to display the browser update config.ini
```
[browser]
visible = 1
```


Execution on your local machine
-------------------------------

You may use a config.ini.local to test on your local vm
Use ip adresses and not names in config.ini.*


```
export XC_PATH - directory of XiVo client binary built with following options:
qmake
make FUNCTESTS=yes -s
export XC_PATH=...
```

Access using ssh to machines in listed in config.ini without password.


Example
-------

Start a test using :

```
cd webi

PYTHONPATH=.. lettuce features/user.feature
```

Lettuce tests are in features/*.feature
Actions for each step are in features/step_definitions/*_steps.py
Common actions are in xivo_lettuce/common_steps_webi.py


Documentation
-------------

See doc/README for more infos
