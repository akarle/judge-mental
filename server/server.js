const express = require('express');
const bp = require('body-parser');
const fileUpload = require('express-fileupload');

const server = express();

const port = 8080;

server.use(fileUpload());

require('./app/routes')(server);
server.listen(port, () => {
	console.log("Running on port " + port);
});