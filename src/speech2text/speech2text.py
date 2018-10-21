import os
import requests
import json

ENDPOINT = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=ja-JP_BroadbandModel'
WATSON_USER = os.environ['WATSON_USER']
WATSON_PASSWD = os.environ['WATSON_PASSWD']


def transform(file_path: str) -> str:
    headers = {'Content-Type': 'audio/wav'}
    with open(file_path, 'rb') as raw_audio:
        r = requests.post(
            ENDPOINT,
            data=raw_audio,
            headers=headers,
            auth=(WATSON_USER, WATSON_PASSWD),
        )

    result = json.loads(r.text)
    morphs = result['results'][0]['alternatives'][0]['transcript']
    text = morphs.replace(' ', '')

    return text
