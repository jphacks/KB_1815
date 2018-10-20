// Imports the Google Cloud client library
const speech = require('@google-cloud/speech');

// Creates a client
const client = new speech.SpeechClient();

// Detects speech in the audio file
// request = {
//      audio: audio={
//          content: audio binary data
//      },
//      config: config
// }
function speech2text(request) {
    client
        .recognize(request)
        .then(data => {
            const response = data[0];
            const transcription = response.results
                .map(result => result.alternatives[0].transcript)
                .join('\n');
            console.log(`Transcription: ${transcription}`);
        })
        .catch(err => {
            console.error('ERROR:', err);
        });
}

exports.speech2text = speech2text;