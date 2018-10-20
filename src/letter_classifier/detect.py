import time
from argparse import ArgumentParser
from typing import Optional, Tuple
import numpy as np
import cv2

from pic2type_letter import predict_mail_type
from pic2type_letter import SIZE_EXTRACT, SIZE_RESIZE, STDDEV_THRESHOLD, IMPORTANT_MAIL

DIFF_THRESHOLD = 20
DEFFAULT_SLEEP = 1

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
        diff_threshold: int=DIFF_THRESHOLD,
        stddev_threshold: int=STDDEV_THRESHOLD,
        resize: Optional[Tuple[int, int]]=SIZE_RESIZE,
        size_extract: Tuple[int, int]=SIZE_EXTRACT,
        center_position: Tuple=None,
        gray_scale: bool=True,
) -> None:
    cap = cv2.VideoCapture(0)
    frame = None

    while True:
        frame_before = frame
        ret, frame = cap.read()

        if frame_before is None:
            frame_before = frame

        cv2.imshow('frame', frame)

        diff = detect_diff(frame_before, frame)

        if diff:
            importance = predict_mail_type(
                frame,
                resize,
                stddev_threshold,
                size_extract,
            )
            # replace print statement to http requests.
            if importance == IMPORTANT_MAIL:
                pass

            # print(importance)

        time.sleep(DEFFAULT_SLEEP)

        # for gui
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
