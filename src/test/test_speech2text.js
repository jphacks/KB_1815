const test = require('../speech/speech2text.js')

// The name of the audio file to transcribe
const fileName = '../../resources/askyou.wav';

test.speech2text(fileName, '../../resources/output.txt')
