process.env.TMPDIR= '.';
var express = require('express');
var app = express();
var http = require('http').Server(app);
var fs = require('fs');
var formidable = require('formidable');
var path = require('path');

const PORT = 8080;

app.use("/corrected", express.static(__dirname+'/corrected'));
app.use("/node_modules", express.static(__dirname+'/node_modules'));

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');
});

app.post('/upload', function(req, res){
    // create an incoming form object
    var form = new formidable.IncomingForm();

    // specify that we want to allow the user to upload multiple files in a single req
    form.multiples = true;

    // store all uploads in the /uploads directory
    form.uploadBaroDir = path.join(__dirname, '/uploads/baro');
    form.uploadWellDir = path.join(__dirname, '/uploads/wells');

    // every time a file has been uploaded successfully,
    // rename it to it's orignal name
    form.on('file', function(field, file) {
        if (field == 'baro'){
            fs.rename(file.path, path.join(form.uploadBaroDir, "baro.csv"));
        }
        else{
            fs.rename(file.path, path.join(form.uploadWellDir, file.name));
        }
    });

    // log any errors that occur
    form.on('error', function(err) {
      console.log('An error has occured: \n' + err);
    });

    // once all the files have been uploaded, send a res to the client
    form.on('end', function() {
        //read files in the uploads/wells directory
        fs.readdir(__dirname+"/uploads/wells", function(err, files){
            if (err){
                console.error("Could not access /uploads/wells", err);
                process.exit(1);
            }

            //the location of the selected barometer file & the name of the python script
            var baroFile = "uploads/baro/baro.csv";
            var script = "barocorrect.py";

            //loop through all the uploaded well files
            files.forEach( function(file, index){
                
                //get the path of the current file and the path for the output file
                var currFile = path.join("uploads/wells", file);
                var currCorrect = path.join("corrected", file);

                //run the 'barocorrect.py' script on each well file & save result in 'corrected' directory
                var python = require('child_process').spawn('python',[script, baroFile, currFile, currCorrect]);
                });
        });

        res.end('success');
    });

    // parse the incoming req containing the form data
    form.parse(req);
    res.sendStatus(200);
});



http.listen(PORT, function(){
    console.log("Server listening on: http://localhost:%s", PORT);
});
