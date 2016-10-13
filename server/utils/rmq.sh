#!/bin/bash
#
# rmq.sh
#
# Schuyler Martin <sam8050@rit.edu>
#
# Simple shell script that controls the RabbitMQ server. Will need sudo to run
# Originally written for my Fedora box. May be different in the Ubuntu world
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

# service logging
if [ "$1" = "start" ]; then
    echo "+ Starting RabbitMQ Server..."
fi
if [ "$1" = "stop" ]; then
    echo "- Stopping RabbitMQ Server..."
fi
if [ "$1" = "restart" ]; then
    echo "* Restarting RabbitMQ Server..."
fi

# $1 = start | stop | restart
sudo /bin/systemctl $1 rabbitmq-server
