var express = require('express');
var app = express();
var http = require('http').Server(app);
var fs = require('fs');
var formidable = require('formidable');
var path = require('path');

const PORT = 8080;

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');
});

app.post('/upload', function(req, res){
    // create an incoming form object
    var form = new formidable.IncomingForm();

    // specify that we want to allow the user to upload multiple files in a single req
    form.multiples = true;

    // store all uploads in the /uploads directory
    form.uploadDir = path.join(__dirname, '/uploads');

    // every time a file has been uploaded successfully,
    // rename it to it's orignal name
    form.on('file', function(field, file) {
      fs.rename(file.path, path.join(form.uploadDir, file.name));
    });

    // log any errors that occur
    form.on('error', function(err) {
      console.log('An error has occured: \n' + err);
    });

    // once all the files have been uploaded, send a res to the client
    form.on('end', function() {
      res.end('success');
    });

    // parse the incoming req containing the form data
    form.parse(req);
    res.sendStatus(200);
});

http.listen(PORT, function(){
    console.log("Server listening on: http://localhost:%s", PORT);
});
