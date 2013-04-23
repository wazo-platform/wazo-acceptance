#!/usr/bin/env bash

function usage {
    echo "Usage : $0"
}

echo "See https://wiki.xivo.fr/index.php/JenkinsAndTestlink for instructions about Testlink."
echo "Here are the classnames, sorted from the more recently edited to the oldest."
echo "You can filter automated tests in Testlink to see if some tests are missing from Testlink."
echo

function features_path {
    this_script_directory="$(dirname $0)"
    relative_path_to_features=".."
    echo "$this_script_directory/$relative_path_to_features"
}

function add_git_date {
    while read filename
    do
        git_date="$(git log -1 --format=%ct $filename)"
        echo "$git_date:$filename"
    done
}

function sort_numeric {
    sort -g <&0
}

function remove_git_date {
    cut -d: -f2 <&0
}

function list_feature_files {
    find . -name '*.feature' -print
}

function sort_by_git_edit_date {
    add_git_date <&0 | sort_numeric | remove_git_date
}

function extract_classnames {
    while read filename
    do
        awk \
'
BEGIN {FS = ": "}
/^Feature/ {feature = $2}
/Scenario/ {print feature " : " $2 }
' \
        $filename
    done
}

function append_line_count {
    tee <&0 >(wc -l | awk '{print "\nTotal : " $0}')
}

function list_classnames {
    list_feature_files | sort_by_git_edit_date | extract_classnames | append_line_count
}

cd "$(features_path)"
list_classnames
