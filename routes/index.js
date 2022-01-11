var express = require('express');
var router = express.Router();
var request = require("request");

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', {
    title: 'Express'
  });

  const { spawn } = require('child_process');
  const api = spawn('python', ['api.py']);

  api.stdout.on('data', function(data) {
    console.log(data.toString());
  });
});

module.exports = router;