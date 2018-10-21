// Imports the Google Cloud client library
const fs = require('fs');
const speech = require('@google-cloud/speech');

const client = new speech.SpeechClient();

// parameter for .wav format
// 先にwavファイルからHeaderを取り出す．
// formatごとにパラメータを変化させる．
const encoding = 'LINEAR16';
const sampleRateHertz = 22050;
const languageCode = 'ja-JP';

// Detects speech in the audio file
// fileName: xxx.wav
// writeFileName: xxx.txt
function speech2text(fileName, writeFileName) {
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
    client
        .recognize(request)
        .then(data => {
            const response = data[0];
            const transcription = response.results
                .map(result => result.alternatives[0].transcript)
                .join('\n');
            fs.writeFile(writeFileName, transcription, err => {
                if (err) {
                    console.error('ERROR:', err);
                    return;
                }
                console.log(`Text content written to file: ${writeFileName}`);
            });
            console.log(`Transcription: ${transcription}`);
        })
        .catch(err => {
            console.error('ERROR:', err);
        });
}

exports.speech2text = speech2text;