var amqp = require('amqplib');

amqp.connect('amqp://localhost').then(function(conn) {
  return conn.createChannel().then(function(ch) {
    var q = 'Default Queue';
    var str = {"get_method" : "tut_enters", "user_name" : "mrb5960", "user_passwd" : "mrb5960", "user_f_name" : "Mandar", "user_l_name" : "Badave", "user_title" : "TA"};
    //var str = {"get_method" : "stu_enters", "user_name" : "mrb5961", "user_passwd" : "mrb5961", "user_f_name" : "Mandy", "user_l_name" : "B"};
    //var str = {"get_method" : "user_leaves", "user_name" : "mrb5961", "user_passwd" : "mrb5961", "user_f_name" : "Mandy", "user_l_name" : "B"};
    var msg = JSON.stringify(str);

    var ok = ch.assertQueue(q, {durable: false});

    return ok.then(function(_qok) {
      // NB: `sentToQueue` and `publish` both return a boolean
      // indicating whether it's OK to send again straight away, or
      // (when `false`) that you should wait for the event `'drain'`
      // to fire before writing again. We're just doing the one write,
      // so we'll ignore it.
      ch.sendToQueue(q, new Buffer(msg));
      console.log(" [x] Sent '%s'", msg);
      return ch.close();
    });
  }).finally(function() { conn.close(); });
}).catch(console.warn);
