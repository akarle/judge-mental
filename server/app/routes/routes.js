var path = require('path');
var fs = require('fs');
var spawn = require('child_process').spawn;

module.exports = function(app) {
	app.post('/upload', (req, res) => {
		if (!req.files)
			return res.status(400).send("No image uploaded.");
		console.log(req.files.file.name);
		req.files.file.mv(path.join(__dirname+'/../../../extract/image.jpg'), (err) => {
			if (err)
				return res.status(500).send(err);
			console.log('got image');
			var extract_evidence = spawn('python', ["/../../../extract/evidence.py", 
				'/../../temp/image.jpg']);
			console.log('waiting for evidence');
			extract_evidence.stdout.on('data', (data) => {
				console.log('got evidence');
				res.send(data);
			});
		});
	});

	app.get('/image.jpg', (req, res) => {
		res.sendFile(path.resolve('./temp/image.jpg'));
	});

	app.get('/', (req, res) => {
		res.sendFile(path.join(__dirname+'/../pages/upload.html'));
	});
};