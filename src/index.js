const express = require('express')
const app = express()
const portNo = 3000
const raspi = require('raspi');
const pwm = require('raspi-pwm');


app.set('view engine', 'ejs');

app.get('/', (req, res, next) => {
  res.render("index")
})

app.post('/open', (req, res, next) => {
  led.write(0.07);
  res.send('opened');
})

app.post('/close', (req, res, next) => {
  led.write(0.11);
  res.send('closed')
})
 
raspi.init(() => {
  led = new pwm.PWM('GPIO18');
  app.listen(portNo, () => {
  console.log('起動しました', `http://192.168.100.125:${portNo}`)
  })
});
