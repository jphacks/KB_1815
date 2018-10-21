import os
from datetime import datetime
import werkzeug
from flask import Flask, jsonify, request, make_response
from speech2text import transform

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

UPLOAD_DIR = "./tmp/"


@app.route('/transform', methods=['POST'])
def speech2text():

    if 'uploadFile' not in request.files:
        make_response(jsonify({'result': 'uploadFile is required.'}))

    uploaded = request.files['uploadFile']
    fileName = uploaded.filename

    saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") \
        + werkzeug.utils.secure_filename(fileName)

    output_name = os.path.join(UPLOAD_DIR, saveFileName)
    uploaded.save(output_name)

    result = transform(output_name)

    return make_response(jsonify({'result': result}))

    @app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
    def handle_over_max_file_size(error):
        print("werkzeug.exceptions.RequestEntityTooLarge")
        return 'result : file size is overed.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6006, debug=True)
