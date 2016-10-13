#!/usr/bin/python3
##
## File:    hw_client.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Initial "hello world" client program for RabbitMQ using pika
##

import pika
#### GLOBALS    ####

#### FUNCTIONS  ####

#### MAIN       ####

def main():
    '''
    Main execution point of the program
    '''
    # establish connection to server
    socket = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = socket.channel()
    # send information to a specific RabbitMQ queue
    channel.queue_declare(queue="hello")
    # actually submit the message
    channel.basic_publish(exchange="",
        routing_key="hello",
        body="Hello World");
    print("SENT!")
    # close the connection
    socket.close()

if __name__ == "__main__":
    main()
