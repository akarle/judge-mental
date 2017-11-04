var path = require('path');
var fs = require('fs');

module.exports = function(app) {
	app.post('/upload', (req, res) => {
		if (!req.files)
			return res.status(400).send("No image uploaded.");
		console.log(req.files.file.name);
		req.files.file.mv(path.join(__dirname+'/../../temp/image.jpg'), (err) => {
			if (err)
				return res.status(500).send(err);
			res.sendFile(path.resolve('./temp/image.jpg'));
		});
	});

	app.get('/image.jpg', (req, res) => {
		res.sendFile(path.resolve('./temp/image.jpg'));
	});

	app.get('/', (req, res) => {
		res.sendFile(path.join(__dirname+'/../pages/upload.html'));
	});
};