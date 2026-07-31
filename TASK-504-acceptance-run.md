# TASK-504 acceptance run — DO NOT MERGE

This file exists only to carry a pull request whose `Depends-On:` lines make
Zuul build and install every TASK-504 change on the acceptance stack, so the
daily features run against services configured to reach wazo-auth through
nginx (`localhost:80`, prefix `/api/auth`) instead of `localhost:9497`.

Delete the branch once the run has been read. Nothing here should ever land on
master.
