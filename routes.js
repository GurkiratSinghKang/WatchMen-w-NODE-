module.exports = function(app,io){

	app.get('/', function(req, res){

		// Render views/home.html
		res.render('home');
	});

	app.get('/start',function  (req,res) {
		
		res.render('start');
	});

	app.get('/database',function  (req,res) {
		res.render('database');
	});

	app.get('/display',function  (req,res) {
		var PythonShell = require('python-shell');

		PythonShell.run('test.py', function (err) {
		  console.log('finished');
		});

		res.redirect('/start');
	});

	app.get('/train',function  (req,res) {
		var PythonShell = require('python-shell');

		PythonShell.run('Train.py', function (err) {
		  console.log('finished');
		});

		res.redirect('/start');
	});

	var chat = io.of('/socket').on('connection', function (socket) {
				socket.on('getLastKnown',function  (data) {
					console.log("Person  " + data.person_name );
					var PythonShell = require('python-shell');

					var pyshell = new PythonShell('getLastKnown.py');
					pyshell.send(data.person_name);
					 pyshell.on('message', function (message) {
					  socket.emit('setLastKnown',{result:message});
					});
					 pyshell.end(function (err) {
					  if (err) throw err;
					  console.log('finished');
					});
				

				});

				socket.on('getTrack',function  (data) {
					console.log("Person  " + data.person_name );
					var PythonShell = require('python-shell');

					var pyshell = new PythonShell('getTrack.py');
					pyshell.send(data.person_name);
					var msgs = []
					 pyshell.on('message', function (message) {
					  	msgs.push(message);
					});
					 pyshell.end(function (err) {
					 	socket.emit('setTrack',{result:msgs,person:data.person_name});
					  if (err) throw err;
					  console.log('finished');
					});

					});
				socket.on('initCamera',function  (data) {
					var PythonShell = require('python-shell');

					var pyshell = new PythonShell('initialize.py');
					pyshell.send(data.number);
					 pyshell.on('message', function (message) {
					  	console.log(message);
					});
					 for (var i = 0; i < data.number; i++) {
					 	pyshell.send(data.cams[i]); 
					 };
					 pyshell.on('message', function (message) {
					  	msgs.push(message);
					});
					 pyshell.end(function (err) {
					 	socket.emit('initDone');
					  if (err) throw err;
					  console.log('finished');
					
				});
				

				});
		});
}