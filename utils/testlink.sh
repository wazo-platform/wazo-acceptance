#!/usr/bin/env bash

function usage {
    echo "Usage : $0"
}

echo "See https://wiki.xivo.fr/index.php/JenkinsAndTestlink for instructions about Testlink."
echo "Here are the classnames, sorted from the more recently edited to the most ancient."
echo "You can filter automated tests in Testlink to see if some tests are missing from Testlink."
echo

function add_git_date {
    while read filename
    do
        git log -1 --format=%ct $filename | sed "s|\$|:$filename|"
    done
}

function extract_features {
    while read filename
    do
        awk \
'
BEGIN {FS = ": "}
/Feature/ {feature = $2}
/Scenario/ {print feature " : " $2 }
' \
        $filename
    done
}

# Get filenames
ls ../webi/features/*.feature ../cticlient/features/*.feature | \

# Add sort indicator
add_git_date | \

# Sort
sort -rg | \

# Remove sort indicator
cut -d: -f2 | \

# Print feature : scenario
extract_features | \

# Count lines and print
tee >(wc -l | awk '{print "\nTotal : " $0}')
