// The text to synthesize
const text = 'どちら様ですか？';

// テキストから合成音声ファイルを作成する．
function synthesizeSpeech(text, filename) {
    const ts = require('../lib/text2speech.js')
    const request = {
        input: { text: text },
        // Select the language and SSML Voice Gender (optional)
        voice: { languageCode: 'ja-JP', ssmlGender: 'NEUTRAL' },
        // Select the type of audio encoding
        audioConfig: { audioEncoding: 'LINEAR16' },
    };
    ts.text2speech(request, filename)

}

synthesizeSpeech(request, '../../resources/askyou.wav');