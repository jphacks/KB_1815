// Imports the Google Cloud client library
const fs = require('fs');
const textToSpeech = require('@google-cloud/text-to-speech');

// Creates a client
const client = new textToSpeech.TextToSpeechClient();
// Performs the Text-to-Speech request
// fileName: xxx.wav
function text2speech(text, fileName) {
    const request = {
        input: { text: text },
        // Select the language and SSML Voice Gender (optional)
        voice: { languageCode: 'ja-JP', ssmlGender: 'MALE' },
        // Select the type of audio encoding
        audioConfig: { audioEncoding: 'LINEAR16' },
        sampleRateHertz: 44100
    };
    client.synthesizeSpeech(request, (err, response) => {
        if (err) {
            console.error('ERROR:', err);
            return;
        }

        // Write the binary audio content to a local file
        fs.writeFile(fileName, response.audioContent, 'binary', err => {
            if (err) {
                console.error('ERROR:', err);
                return;
            }
            console.log(`Audio content written to file: ${fileName}`);
        });
    });
}

text2speech('ねえクローバ，うけとりを起動して', '../resources/start.wav')
text2speech('ねえクローバ，パパに電話をかけて', '../resources/call.wav')

// exports.text2speech = text2speech;
