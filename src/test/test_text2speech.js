const fs = require('fs');
const test = require('./text2speech.js')


// The text to synthesize
const text = '青森県八戸市で古くから愛される郷土料理せんべい汁りょうや狩りで取った獲物を無罪にした汁物に入った南部せんべいを入れて食べたのがせんべい汁の始まりですだし汁がたっぷり染み込んでいるせんべいの不思議な食感を楽しめます';

// Construct the request
const request = {
    input: { text: text },
    // Select the language and SSML Voice Gender (optional)
    voice: { languageCode: 'ja-JP', ssmlGender: 'NEUTRAL' },
    // Select the type of audio encoding
    audioConfig: { audioEncoding: 'MP3' },
};

test.text2speech(request, './resources/output.mp3')