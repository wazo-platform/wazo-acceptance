#!/bin/bash

set -xeuo pipefail

if grep -q 'You can implement step definitions for undefined steps with these snippets' acceptance.log ; then
	  echo 'ERROR: SOME STEPS ARE MISSING'
	  exit 1
fi
