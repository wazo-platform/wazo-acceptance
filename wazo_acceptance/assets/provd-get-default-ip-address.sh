#!/bin/bash

sudo -u postgres psql asterisk --no-align --tuples-only --command "select address from netiface"
