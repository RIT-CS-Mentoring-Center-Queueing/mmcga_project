#!/bin/bash
#
# rmq.sh
#
# Schuyler Martin <sam8050@rit.edu>
#
# Simple shell script that controls the RabbitMQ server. Will need sudo to run
# Originally written for my Fedora box. May be different in the Ubuntu world
#

# $1 = start | stop | restart
sudo /bin/systemctl $1 rabbitmq-server
