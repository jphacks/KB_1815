const recorder = require('node-record-lpcm16');
const fs = require('fs');

const filename = '../../resources/speech.wav';

function record(filename) {
    const file = fs.createWriteStream(filename);

    const encoding = 'LINEAR16';
    const sampleRate = 44100;


    recorder.start({
        sampleRateHertz: sampleRateHertz,
        threshold: 0.5,
        silence: '1.0', // 終了させる無音間隔(sec)
        verbose: true,
        recordProgram: 'rec'
    })
        .pipe(recognizeStream)
        .on('error', function () {
            console.log(error);
        });
}

record(filename)