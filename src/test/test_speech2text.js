const fs = require('fs');
const test = require('../lib/speech2text.js')

// The name of the audio file to transcribe
const fileName = '../../resources/senbeijiru.wav';
const encoding = 'LINEAR16';
const sampleRateHertz = 44100;
const languageCode = 'ja-JP';

// Reads a local audio file and converts it to base64
const file = fs.readFileSync(fileName);
const audioBytes = file.toString('base64');

// The audio file's encoding, sample rate in hertz, and BCP-47 language code
const audio = {
    content: audioBytes,
};
const config = {
    encoding: encoding,
    sampleRateHertz: sampleRateHertz,
    languageCode: languageCode,
};
const request = {
    audio: audio,
    config: config,
};

test.speech2text(request)
