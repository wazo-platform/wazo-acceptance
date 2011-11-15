#!/bin/bash

find features/ \( ! -name wizard.feature -a -name '*.feature' \) -exec lettuce --with-xunit --verbosity=3 {} \;
