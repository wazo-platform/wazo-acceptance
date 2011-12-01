#!/usr/bin/env bash

function usage {
    echo "Usage : $0"
}

echo "See https://wiki.xivo.fr/index.php/JenkinsAndTestlink for instructions about Testlink."
echo "Here are the classnames, sorted from the more recently edited to the most ancient."
echo "You can filter automated tests in Testlink to see if some tests are missing from Testlink."
echo

# Sort the files by git modification date
for file in $(ls features/*.feature) ; do
    files+=$(git log -1 --format=%ct $file):$file"
"
done
files=$(sort -rg <<< "$files"|cut -d: -f2)

# Print Feature : Scenario
for file in $files; do
    feature=$(grep Feature $file|cut -f2 -d:|sed 's/^ *\(.*\) *$/\1/')
    scenarios+=$(grep Scenario $file | sed "s/ *Scenario.*:/$feature :/")"
"
done

echo "$scenarios"
echo Total : $(wc -l <<< "$scenarios")
