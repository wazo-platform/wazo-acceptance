#!/bin/bash
grep -i 'scenario:' $1 | sed 's/^ *Scenario: *//gI' | awk '{print NR " - " $0}'
