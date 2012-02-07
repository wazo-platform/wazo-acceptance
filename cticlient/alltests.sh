#!/bin/bash

# sh -c is mandatory to have basename working after the substitution of {}
find features/ -name '*.feature' -exec sh -c 'PYTHONPATH=.. lettuce --with-xunit --verbosity=3 {} --xunit-file=$PWD/$(basename {} .feature).xml' \;
