#!/bin/bash

lettuce --with-xunit --verbosity=3 features/!(wizard).feature
