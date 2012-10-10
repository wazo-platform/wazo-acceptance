#!/bin/sh

sipp -inf users.csv -sf scenario.xml {{ sipp_std_options }} {{ sipp_remote_host }}

