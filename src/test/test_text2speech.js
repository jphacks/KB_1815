// const fs = require('fs');
const test = require('../lib/text2speech.js')

// The text to synthesize
const text = 'どちら様ですか？';

// Construct the request
const request = {
    input: { text: text },
    // Select the language and SSML Voice Gender (optional)
    voice: { languageCode: 'ja-JP', ssmlGender: 'NEUTRAL' },
    // Select the type of audio encoding
    audioConfig: { audioEncoding: 'MP3' },
};

test.text2speech(request, '../../resources/askyou.mp3')