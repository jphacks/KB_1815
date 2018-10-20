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
function text2speech(text, fileName) {
    const request = {
        input: { text: text },
        // Select the language and SSML Voice Gender (optional)
        voice: { languageCode: 'ja-JP', ssmlGender: 'NEUTRAL' },
        // Select the type of audio encoding
        audioConfig: { audioEncoding: 'LINEAR16' },
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

exports.text2speech = text2speech;