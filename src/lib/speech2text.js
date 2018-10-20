// Imports the Google Cloud client library
const speech = require('@google-cloud/speech');
const client = new speech.SpeechClient();

// parameter for .wav format
const encoding = 'LINEAR16';
const sampleRateHertz = 44100;
const languageCode = 'ja-JP';

// Detects speech in the audio file
// request = {
//      audio: audio={
//          content: audio binary data
//      },
//      config: config
// }
function speech2text(filename) {
    // Reads a local audio file and converts it to base64
    const file = fs.readFileSync(filename);
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