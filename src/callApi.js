const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const portNo = 3000
const raspi = require('raspi');
const pwm = require('raspi-pwm');
require('date-utils');
const childProcess = require('child_process');
const request = require('request');
const fs = require('fs');

app.get('/detection', (req, res, next) => {

const dt = new Date();
const formatted = dt.toFormat("YYYYMMDDHH24MISS");

childProcess.exec(`fswebcam ./public/images/${formatted}.jpg`, (error, stdout, stderr) => {
  if(error) {
    console.log(stderr);
    return;
  } else {
      console.log("took a picture");
      const imgOptions = {
        uri: "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/2d6dff05-36fb-493e-a387-1093bbbb175b/image?iterationId=1db2c270-2956-4fca-b115-3f1e775eaf32",
        headers: {
      	  "Prediction-Key": "4fdd8e3729b04880af66cdb52d0b5c73",
	  "Content-Type": "application/octet-stream"
        },
        formData : {
          "image": fs.createReadStream(`./public/images/${formatted}.jpg`)
        }
      }
    //画像判定APIにリクエストを投げる
    request.post(imgOptions, function (error, response, body) {
      const judge = JSON.parse(body)["predictions"][0]["tagName"]
      if(judge == "important") {
        const options = {
          uri: "https://uketori.herokuapp.com/important",
          headers: {
            "Content-Type": "application/json"
          },
          json: {
            "result": `${formatted}.jpg`
          }
        };
        //Lineに画像のpathを通知する
        request.post(options, function (error, response, body) {
          console.log('sent to Line')
        });
      }
    });
  }
});
});
app.use(bodyParser.urlencoded({
    extended: true
}));

app.use(bodyParser.json());
app.set('view engine', 'ejs');
app.use(express.static('public'));

app.get('/', (req, res, next) => {
  res.render("index")
})

raspi.init(() => {
  app.listen(portNo, () => {
  console.log('起動しました')
  })
});


