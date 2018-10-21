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
const speech2text = (fileName) => {
    return new Promise((resolve) => {
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
        let transcription = ''
        client
            .recognize(request)
            .then(data => {
                const response = data[0];
                transcription = response.results
                    .map(result => result.alternatives[0].transcript)
                    .join('\n');
                console.log(`Transcription: ${transcription}`);
            })
            .catch(err => {
                console.error('ERROR:', err);
            });
        resolve(transcription)
    })
}

speech2text('../../resources/askyou.wav')
    // .then((transcription) => {
    //     console.log('aaa', transcription)
    // })
    .catch((err) => {
        console.error('ERROR:', err);
    });

// exports.speech2text = speech2text;