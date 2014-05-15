#!/bin/bash

usage() {
    echo "Usage: $0 [-p] LETTUCE_FILE"
    echo
    echo "Options:"
    echo "  -p  only print the list of scenarios, do not run them"
    echo "  -h  print this help"
    exit 1
}

print_scenarios() {
    file=$1
    grep -i 'scenario\( outline\)\?:' $file | sed 's/^ *Scenario\( Outline\)\?: *//gI' | awk '{print NR " - " $file}'
}

execute_scenario() {
    file=$1
    read -p 'Which scenario do you want to run ? number: ' number
    lettuce $file -s${number}
}

RUN_LETTUCE=1

while getopts ":hp" opt; do
    case "$opt" in
        p)
            RUN_LETTUCE=0
            ;;
        h)
            usage
            ;;
        \?)
            usage
            ;;
        esac
done

LETTUCE_FILE=${@:$OPTIND}

print_scenarios $LETTUCE_FILE

if [ $RUN_LETTUCE = 1 ]; then
    execute_scenario $LETTUCE_FILE
fi
