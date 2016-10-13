#!/bin/bash
#
# mmcga_server.sh
#
# Schuyler Martin <sam8050@rit.edu>
#
# Simple shell script that controls the MMCGA project's server
#

USAGE="Usage: ./mmcga_server.sh (start | stop | restart)"

# usage checks
if [ "$#" -ne 1 ]; then
    echo "${USAGE}"
    exit 1
fi
if [ "$1" != "start" ] && [ "$1" != "stop" ] && [ "$1" != "restart" ]; then
    echo "${USAGE}"
    exit 2
fi

# Manage the 
./server/utils/rmq.sh "$1"

# Rabbit MQ server command failed
if [ "$?" -ne 0 ]; then
    echo "ERROR: Rabbit MQ Server Failure!"
    exit 3
fi

# start our python server/request handling system that reads off of queues
# managed by the RabbitMQ server
if [ "$1" = "start" ]; then
    /usr/bin/python3 server/mmcga_server.py
    # TODO Testing: I don't want RabbitMQ running on my box all the time
    ./server/utils/rmq.sh "stop"
fi
