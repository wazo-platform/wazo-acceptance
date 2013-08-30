#!/bin/bash

grep -i 'scenario:' $1 | sed 's/^ *Scenario: *//gI' | awk '{print NR " - " $0}'


read -p 'That scenario you want to run ? number: ' number


lettuce $1 -s${number}
