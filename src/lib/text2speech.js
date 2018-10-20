// Imports the Google Cloud client library
const fs = require('fs');
const textToSpeech = require('@google-cloud/text-to-speech');

// Creates a client
const client = new textToSpeech.TextToSpeechClient();

// Performs the Text-to-Speech request
// request = {
//      input: {text: text},
//      voice: { languageCode: 'ja-JP', ssmlGender: 'NEUTRAL' },
//      audioConfig: { audioEncoding: 'MP3 },
//}
function text2speech(request, writeFile) {
    client.synthesizeSpeech(request, (err, response) => {
        if (err) {
            console.error('ERROR:', err);
            return;
        }

        // Write the binary audio content to a local file
        fs.writeFile(writeFile, response.audioContent, 'binary', err => {
            if (err) {
                console.error('ERROR:', err);
                return;
            }
            console.log('Audio content written to file: output.mp3');
        });
    });
}

exports.text2speech = text2speech;