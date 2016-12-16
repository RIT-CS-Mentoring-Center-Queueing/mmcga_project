var amqp = require('amqplib');
var express = require('express');
var app = express();
//var bodyParser = require('body-parser');

// Create application/x-www-form-urlencoded parser
//var urlencodedParser = bodyParser.urlencoded({ extended: false })

function receiveFromQueue(fn){
  amqp.connect('amqp://localhost').then(function(conn) {
    process.once('SIGINT', function() { conn.close(); });
    return conn.createChannel().then(function(ch) {

      var ok = ch.assertQueue('UID Queue', {durable: false});

      ok = ok.then(function(_qok) {
        return ch.consume('UID Queue', function(msg) {
          console.log(" [x] Received '%s'", msg.content.toString());
          fn(msg.content.toString());
          ch.close();
        }, {noAck: true});
      });

      return ok.then(function(_consumeOk) {
        console.log(' [*] Waiting for messages. To exit press CTRL+C');
      });
    });
  }).catch(console.warn);
}

function sendToQueue(str){
  console.log(str);
  amqp.connect('amqp://localhost').then(function(conn) {
    return conn.createChannel().then(function(ch) {
      var q = 'Default Queue';
      //var str = {"get_method" : "tut_enters", "user_name" : "mrb5960", "user_passwd" : "mrb5960", "user_f_name" : "Mandar", "user_l_name" : "Badave", "user_title" : "TA"};
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
}

app.use(express.static('/home/mrb5960/Git Projects/mmcga_project/ui/'));
app.get('/index.htm', function (req, res) {
   res.sendFile( __dirname + "/" + "index.htm" );
})

app.get('/process_get', function (req, res) {
   // Prepare output in JSON format
   response = {
      user_f_name:req.query.user_f_name,
      user_l_name:req.query.user_l_name,
      user_name:req.query.user_name,
      user_passwd:req.query.user_passwd,
      get_method:req.query.get_method
   };
   console.log(response);
   sendToQueue(response);
     receiveFromQueue(function(send_string){
       console.log('inside receiveFromQueue');
       res.send(JSON.parse(send_string));
  });
})

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://%s:%s", host, port)

})

//home/mrb5960/Documents/CSCI759/mmcga
