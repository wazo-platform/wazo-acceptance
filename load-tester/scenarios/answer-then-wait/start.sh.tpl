#!/bin/sh

sipp -sf scenario.xml -p {{ bind_port }} {{ sipp_std_options }} {{ sipp_remote_host }}

