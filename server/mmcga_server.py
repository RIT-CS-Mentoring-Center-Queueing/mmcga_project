#!/usr/bin/python3
##
## File:    mmcga_server.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Main server program for the MMCGA Project
##

import pika

#### GLOBALS    ####

#### FUNCTIONS  ####

def callback(ch, method, properties, body):
    print("Got: " + str(body))

#### MAIN       ####

def main():
    '''
    Main execution point of the program
    '''
    print("Starting MMCGA Server...")
    # establish connection to server
    socket = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = socket.channel()
    # send information to a specific RabbitMQ queue; building this queue for
    # the first time
    channel.queue_declare(queue="hello")
    # actually submit the message
    channel.basic_consume(callback,
        queue="hello",
        no_ack=True);
    print("Waiting for messages. CTRL-C to exit")
    # busy loop that waits for messages to come in; will clean up itself?
    channel.start_consuming()

if __name__ == "__main__":
    main()
