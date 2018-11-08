from argparse import ArgumentParser
from pathlib import Path
import time
import numpy as np
import cv2
from datetime import datetime
import requests

DIFF_THRESHOLD = 30
DEFFAULT_SLEEP = 1
LINE_ENDPOINT = 'https://uketori.herokuapp.com/important'
VISION_ENDPOINT = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/2d6dff05-36fb-493e-a387-1093bbbb175b/image'
TMP_DIR = Path('../../src/public/images/')

vision_headers = {
    'Prediction-Key': '',
    'Content-Type': 'application/octet-stream',
    'Prediction-Key': '4fdd8e3729b04880af66cdb52d0b5c73',
}

line_headers = {'Content-Type': 'application/json'}

IMPORTANT_TAG = 'important'
NOT_IMPORTANT_TAG = 'not_important'

def detect_diff(img_before, img_after, diff_threthold=DIFF_THRESHOLD):
    '''
    detect difference between two images.

    :param img_before: image to be compared.
    :param img_after: image to compare with.
    :return: two image is differ or not.
    '''
    gray_before = cv2.cvtColor(img_before, cv2.COLOR_RGB2GRAY)
    gray_after = cv2.cvtColor(img_after, cv2.COLOR_RGB2GRAY)

    (width, height) = gray_before.shape
    pix_num = width * height

    diff = cv2.absdiff(gray_before, gray_after)
    mean_diff = np.sum(diff) / pix_num

    return mean_diff > diff_threthold


def main(cam_device=0):
    if not TMP_DIR.exists():
        TMP_DIR.mkdir(parents=True)

    cap = cv2.VideoCapture(cam_device)
    frame = None

    while True:
        frame_before = frame
        ret, frame = cap.read()

        if frame_before is None:
            frame_before = frame

        cv2.imshow('frame', frame)

        diff = detect_diff(frame_before, frame)

        if diff:
            print(True)
            now_time = datetime.now().strftime('%Y%m%d%H%M%S')
            target_name = '%s/%s.jpg' % (str(TMP_DIR), now_time)
            cv2.imwrite(target_name, frame)

            r =requests.post(
                VISION_ENDPOINT,
                data=open(target_name, "rb"),
                headers=vision_headers
            ).json()

            results = r['predictions']
            result_tag = results[0]['tagName']
            print(result_tag)
            if result_tag == IMPORTANT_TAG:
                payload = {'result': '%s.jpg' % now_time}
                requests.post(LINE_ENDPOINT, data=json.dumps(payload), header=line_headers)

        time.sleep(DEFFAULT_SLEEP)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--cam_device', type=int, default=0)
    args = parser.parse_args()
    main(args.cam_device)
