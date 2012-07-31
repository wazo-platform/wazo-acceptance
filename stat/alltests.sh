#!/bin/bash

# sh -c is mandatory to have basename working after the substitution of {}
find features/ -exec sh -c 'PYTHONPATH=.. lettuce --with-xunit --verbosity=4 {} --xunit-file=$PWD/$(basename {} .feature).xml' \;
