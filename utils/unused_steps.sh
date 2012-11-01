#!/usr/bin/env bash

function usage {
    echo "Usage : $0"
}

echo "Here are the definitions of steps that are unused by feature files."

STEP_NOT_FOUND="1"

function project_root {
    this_script_directory="$(dirname $0)"
    relative_path_to_project_root=".."
    echo "$this_script_directory/$relative_path_to_project_root"
}

function escape_pattern {
    raw_pattern="$1"
    echo "$raw_pattern" | \
        # escape word letters
        sed 's/S+/\\S\+/g' | \
        # escape digit letters
        sed 's/\d+/[[:digit:]]\+/g' | \
        # escape regexp special characters
        sed 's/\([()?+]\)/\\\1/g' | \
        # reindent line
        sed 's/^\^/^ \\+/g'
}

function extract_step_pattern {
    step_definition="$1"
    raw_pattern=$(sed "s/.*step(u\?'\(.*\)')/\1/" <<< "$step_definition")
    escaped_pattern=$(escape_pattern "$raw_pattern")
    echo "$escaped_pattern"
}

function find_step_usage {
    step_pattern="$1"
    grep -qrI --include '*.feature' "$step_pattern" .
}

function list_step_definitions {
    find . -name '*.py' | xargs grep -Hn '@step('
}

function remove_used_step_definitions {
    while read step_definition
    do
        step_pattern=$(extract_step_pattern "$step_definition")
        find_step_usage "$step_pattern"
        if [ "$?" -eq "$STEP_NOT_FOUND" ] ; then
            echo "$step_definition"
        fi
    done
}

function list_useless_step_definitions {
    list_step_definitions | remove_used_step_definitions
}

list_useless_step_definitions
