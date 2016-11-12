var express = require('express');
var app = express();
var http = require('http').Server(app);
var fs = require('fs');

const PORT = 8080;

app.get('/', function(request, response){
    response.sendFile(__dirname + '/index.html');
});

http.listen(PORT, function(){
    console.log("Server listening on: http://localhost:%s", PORT);
});
