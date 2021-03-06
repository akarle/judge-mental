var path = require('path');
var fs = require('fs');
var spawn = require('child_process').spawn;
var replace = require('replace');

module.exports = function(app) {
	app.post('/upload', (req, res) => {
		if (!req.files)
			return res.status(400).send("No image uploaded.");
		console.log(req.files.file.name);
		req.files.file.mv(path.join(__dirname+'/../../../court/image-original.jpg'), (err) => {
			if (err)
				return res.status(500).send(err);
			});
			console.log('got image');
			var extract_evidence = spawn('python',
				[path.join(__dirname+'/../../../court/aws_court.py'), 1]);
			console.log('waiting for evidence');
			extract_evidence.stdout.on('data', function(data) {
				console.log('got evidence');
				var text = data.toString('utf8');
				res.send(text);
		});
	});

	app.post('/pipeline', (req, res) => {
		if (!req.files)
			return res.status(400).send("No image uploaded.");
		console.log(req.files.file.name);
		req.files.file.mv(path.join(__dirname+'/../../../court/image-original.jpg'), (err) => {
			if (err)
				return res.status(500).send(err);
			});
			console.log('got image');
			var extract_evidence = spawn('python',
				[path.join(__dirname+'/../../../court/aws_court.py'), 0]);
			console.log('waiting for evidence');
			extract_evidence.stdout.on('data', function(data) {
				console.log('got evidence');
				var text = data.toString('utf8');
                res.sendFile(path.join(__dirname+'/../pages/pipeline.html'));
		});
	});

	app.get('/image.jpg', (req, res) => {
		res.sendFile(path.resolve(__dirname+'/../../../court/image-original.jpg'));
	});

	app.get('/hc.jpg', (req, res) => {
		res.sendFile(path.resolve(__dirname+'/../../../court/image-hc.jpg'));
	});

    app.get('/logo.jpg', (req, res) => {
		res.sendFile(path.join(__dirname+'/../pages/judging-mental-logo_720.png'));
	});
	
    app.get('/judge.jpg',  (req, res) => {
		res.sendFile(path.join(__dirname+'/../pages/if_judge_bailiff_court_justice_man_person_342417_480.png'));
	});

	app.get('/', (req, res) => {
		res.sendFile(path.join(__dirname+'/../pages/upload.html'));
	});
	app.get('/rtext.txt', (req, res) => {
		res.sendFile(path.join(__dirname+'/../../../court/rtext.txt'));
	});
	app.get('/visualize', (req, res) => {
		res.sendFile(path.join(__dirname+'/../pages/pipeline.html'));
	});





};
