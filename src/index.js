const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const portNo = 3000
const raspi = require('raspi');
const pwm = require('raspi-pwm');
require('date-utils');
const childProcess = require('child_process');

app.get('/photo', (req, res, next) => {
  const dt = new Date();
  const formatted = dt.toFormat("YYYYMMDDHH24MISS");
  childProcess.exec(`fswebcam ./public/images/${formatted}.jpg`, (error, stdout, stderr) => {
    if(error) {
      console.log(stderr);
      return;
    }
    else {
      console.log("success");
    }
  const param = {"result": `${formatted}.jpg`};
  res.header('Content-Type', 'application/json; charset=utf-8')
  res.send(param);
  })
})

app.use(bodyParser.urlencoded({
    extended: true
}));

app.use(bodyParser.json());
app.set('view engine', 'ejs');
app.use(express.static('public'));

app.get('/', (req, res, next) => {
  res.render("index")
})

app.post('/open', (req, res, next) => {
  led.write(0.08);
  res.send('opened');
})

app.post('/close', (req, res, next) => {
  led.write(0.13);
  res.send('closed')
})



app.post('/sound', (req, res, next) => {
  console.log(req.body);
  let before = req.body.before
  let after = req.body.after
  childProcess.exec(`python ./okmt/rename.py ${before}.mp3 ${after}.mp3 &`, (error, stdout, stderr) => {
  if(error) {
    console.log(stderr);
    return;
  }
  else {
    console.log("success");
  }
});

})

app.get('/call', (req, res, next) => {
  childProcess.exec('mpg321 ./public/resources/call.mp3')
})
 
raspi.init(() => {
  led = new pwm.PWM('GPIO18');
  app.listen(portNo, () => {
  console.log('起動しました', `http://163.221.126.28:${portNo}`)
  })
});

