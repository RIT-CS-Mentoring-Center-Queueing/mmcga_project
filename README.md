# Make the Mentoring Center Great Again
This project attempts to improve our utilization of the Computer Science
Department's Mentoring Center at the Rochester Institute of Technology (RIT).

## Server
The server/back-end of this project is written in Python3 and relies on a
RabbitMQ server for message handling, using the Pika Python bindings for
RabbitMQ. For more specific information about the server, read
`server/README.md`

### mmcga_server.sh
Daemonized script that runs the project server as a headless system daemon/
service.

##### Usage:
```shell
./mmcga_server.sh (start | stop | restart)
```

## Front End
TODO
