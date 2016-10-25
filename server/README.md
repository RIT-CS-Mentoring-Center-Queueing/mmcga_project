# Make the Mentoring Center Great Again - Server

## Author
Schuyler Martin <sam8050@rit.edu>

## Server
This is the server portion of the project, written in Python and uses the Pika
Python Client to interact with the RabbitMQ service.

## Design
What follows is a high-level description of the server design and all the
pieces that make up the server. There are several layers of abstraction to how
the students and tutors get managed and the design follows standard OOP
practices.


### Top-Level "Server" Package

#### mmcga_server.py
This is the primary Python server program for this project that listens to
incoming messages from the primary RabbitMQ queue, manages the state of
Mentoring Center, and dispatches messages to users accordingly.

This program should not be run directly. It should be run from the
`mmcga_server.sh` in the above directory (main project directory).

#### queue_manager.py
This file provides the QueueManager class, the class with the highest-level of
abstraction in the entire project. Effectively, the server program should have
a single QueueManager instance. When the server receives messages such as
`register a user`, `student has a question`, etc. the corresponding QueueManager
function should be called, modifying the state of the Mentoring Center and
dispatching messages to users accordingly.

#### run_tests.sh
This script runs test cases that come packaged with most of the class files in
the server code. Tests can be run individually or all at once.

##### Usage:
```shell
./run_tests.sh [test_#]
```


### rmq_examples Directory
This directory holds some initial "Hello World" code I wrote to test talking to
the RabbitMQ server. Nothing in here is important to the project but it is left
in for debugging purposes.


### Users Package
This directory/package stores information about and controls users who use the
Mentoring Center.

#### user.py
This file defines the User class which is the parent class of all users and
provides state variables and functions common across all users, such as ways of
identifying students (UID, name, etc) along with some statistics trackers.

#### student.py
This file defines the Student class which represents a student asking questions
in the Mentoring Center.

#### tutor.py
This file defines the Tutor class which represents a tutor (SLI/TA) answering
questions in the Mentoring Center.

#### queue_stu.py
This file defines the QueueStu class that represents the queue (aka line) of
students waiting for help. Students follow a strict FIFO queue ordering,
determined by the ordering of question requests.

#### queue_tut.py
This file defines the QueueTut class that represents the "queue" of tutors
available to help. Tutors do not follow a FIFO ordering. Tutors are available
whenever they indicate they have gone on duty and are not currently answering
a question.


### Utils Package

#### macros.py
This file defines global constant variables available across the project, such
as debugging flags, IP addresses, and other important pieces of information
that one would use C macros for.

#### utils.py
This file provide utility functions for file I/O, debug logging, etc.

#### bunny.py
This file defines the Bunny class which stores users currently registered in
the system and provides functions to dispatch messages to the RabbitMQ server.
Registered users have fully formed intialized objects in the Bunny class. All
other classes that manage users just work with UIDs to prevent data redundancy.

#### rmq.sh
This script wraps calls to manage the actual RabbitMQ server. This layer
of abstraction exists since starting the server is slightly different for some
distributions of Linux (RedHat/Fedora starts RabbitMQ with systemctl. I don't
think that is the case for Debian/Ubuntu).

This script is invoked by the other server manager scripts and test scripts.

##### Usage:
```shell
./rmq.sh (start | stop | restart)
```
