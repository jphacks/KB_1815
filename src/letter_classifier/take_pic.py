from argparse import ArgumentParser
import time
import numpy as np
import cv2
import requests

DIFF_THRESHOLD = 20
DEFFAULT_SLEEP = 1
END_POINT = 'http://163.221.126.25:3000/detection'

def detect_diff(
        img_before: 'np.ndarray',
        img_after: 'np.ndarray',
        diff_threthold: int=DIFF_THRESHOLD,
) -> bool:
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


def main(
        cam_device: int=0,
        end_point: str=END_POINT,
) -> None:
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
            #print(True)
            requests.get(end_point)

        time.sleep(DEFFAULT_SLEEP)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--cam_device', type=int, default=0)
    parser.add_argument('--end_point', type=str, default=END_POINT)
    args = parser.parse_args()
    main(args.cam_device, args.end_point)
