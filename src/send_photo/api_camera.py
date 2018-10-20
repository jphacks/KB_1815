# -*- coding: utf-8 -*-
from flask import Flask, jsonify, make_response
import os


api = Flask(__name__)

@api.route('/snapshot/', methods=['GET'])
def snapshot():
    print("snapshot")
    os.system('sh snapshot.sh')

    result = {
        "result": True,
        "data": {
            "status": "succces"
        }
    }

    return make_response(jsonify(result))

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)
