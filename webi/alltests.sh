#!/bin/bash

# sh -c is mandatory to have basename working after the substitution of {}
find features/ \( ! -name wizard.feature -a -name '*.feature' \) -exec sh -c 'PYTHONPATH=..:../load-tester/src lettuce --with-xunit --verbosity=3 {} --xunit-file=$PWD/$(basename {} .feature).xml' \;
