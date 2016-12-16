#!/usr/bin/env node

var amqp = require('amqplib');

amqp.connect('amqp://localhost').then(function(conn) {
  process.once('SIGINT', function() { conn.close(); });
  return conn.createChannel().then(function(ch) {

    var ok = ch.assertQueue('UID Queue', {durable: false});

    ok = ok.then(function(_qok) {
      return ch.consume('UID Queue', function(msg) {
        console.log(" [x] Received '%s'", msg.content.toString());
        ch.close();
      }, {noAck: true});
    });

    return ok.then(function(_consumeOk) {
      console.log(' [*] Waiting for messages. To exit press CTRL+C');
    });
  });
}).catch(console.warn);
