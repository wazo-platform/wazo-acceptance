#!/bin/bash

find tests/ \( ! -name '__*' -a -name '*.py' \) -exec sh -c 'PYTHONPATH=.. nosetests {} --with-xunit' \;
