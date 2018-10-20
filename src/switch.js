const fs = require('fs');
const request = require('request');
var GPIO_DIR = '/sys/class/gpio';
var GPIO_PIN_DIR = GPIO_DIR + '/gpio';
var PIN_LIST = [];
const Sound = require('node-aplay');

//使用したGPIOポートの開放
var cleanUp = function() {
　　　　for (var i=0; i < PIN_LIST.length; i++) {
                fs.writeFileSync(GPIO_DIR + '/unexport', PIN_LIST[i]);
        }
};

//使用するGPIOポートの準備設定
var setUp = function(pin, io) {
        try {
                fs.writeFileSync(GPIO_DIR + '/export', pin);
                PIN_LIST.push(pin);
                fs.writeFileSync(GPIO_PIN_DIR + pin + '/direction', io);
        } catch (e) {
                console.log(e);
                cleanUp();
        }
};

//GPIOの入力状態を取得
var getInput = function(pin) {
        try {
                var cntxt = fs.readFileSync(GPIO_PIN_DIR + pin + '/value');
                return cntxt.toString().split('\n')[0];
        } catch (e) {
                console.log(e);
                cleanUp();
        }
};

//GPIOの出力状態を設定
var setOutput = function(pin, value) {
        try {
                fs.writeFileSync(GPIO_PIN_DIR + pin + '/value', value);
        } catch (e) {
                console.log(e);
                cleanUp();
        }
};

try {
        //GPIO 7を入力に設定する。
        setUp(7, 'in');
        //GPIO 8を出力に設定する。
        setUp(8, 'out');

        //0.01毎にGPIO 7の入力状態を確認し、
        //電流が流れている(スイッチが押されている)場合
        //LEDを点灯させる。
	let count = 0;
        var moniter = setInterval(function() {
                var value = getInput(7);
                if (value == '1') {
                        //スイッチが押された状態
 			count += 1;
                        setOutput(8, '1');
			if (count === 1) {
			  new Sound('../resources/askyou.wav').play();
 			  request.post('https://609e058f.ngrok.io/button_on', function (error, response, body) {
                          console.log('ok')})
			}
                } else {
                        //スイッチが離された状態
                        setOutput(8, '0');
                }
        }, 10);
} catch (e) {
        console.log(e);
        cleanUp();
}

process.on('SIGINT', function() {
        cleanUp();
        process.exit(0);
});

process.on('end', function() {
        cleanUp();
        process.exit(0);
});
