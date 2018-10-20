const record = require('node-record-lpcm16');
const fs = require('fs');

const filename = '../../resources/speech.wav';
const file = fs.createWriteStream(filename);

const encoding = 'LINEAR16';
const sampleRate = 44100;

record.start({
    sampleRateHertz: sampleRate,
    encoding: encoding
}).pipe(file);

setTimeout(function () {
    record.stop();
}, 7000);