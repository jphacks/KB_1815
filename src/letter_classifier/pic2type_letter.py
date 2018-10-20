from pathlib import Path
from typing import Union, Optional, Tuple
import numpy as np
import cv2

IMPORTANT_MAIL = 'important'
NOT_IMPORTANT_MAIL = 'not_important'
SIZE_EXTRACT = (200, 200)
SIZE_RESIZE = (512, 512)
STDDEV_THRESHOLD = 10

def predict_mail_type(
    img: Union[str, Path, 'np.ndarray'],
    resize: Optional[Tuple[int, int]]=None,
    threshold_stddev: int=STDDEV_THRESHOLD,
    size_extract: Tuple[int, int]=SIZE_EXTRACT,
    center_position: Tuple[int, int]=None,
    gray_scale: bool=True,
) -> str:
    '''
    predict type of mail.

    :param img_path: img path to predict.
    :threshold_stddev: threshold for standard deviation to decide the mail is important.
    :param shape_extract: size of width and height for extractiong image.
    :param center_position: position to get some pixels around specified center.
    :param gray_scale: image is gray scale or not.
    :return numpy array of center.
    '''
    if isinstance(img, str):
        img = Path(img)

    if isinstance(img, Path):
        assert img.exists()

    if isinstance(img, str) or isinstance(img, Path):
        img_arr = cv2.imread(str(img))
    else:
        img_arr = img

    if resize is not None:
        img_arr = cv2.resize(img_arr, resize)

    gray_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    extracted_img = _extract_center_position(gray_arr, size_extract, center_position, gray_scale)
    stddev = int(np.std(extracted_img))

    print(stddev)
    if threshold_stddev > stddev:
        return IMPORTANT_MAIL
    else:
        return NOT_IMPORTANT_MAIL


def _extract_center_position(
    img_array: 'np.ndarray',
    size_extract: Tuple[int, int]=SIZE_EXTRACT,
    center_position: tuple=None,
    gray_scale: bool=True,
) -> 'np.ndarray':
    '''
    get the center position

    :param img_array: img converted to numpy array.
    :param shape_extract: size of width and height for extractiong image.
    :param center_position: position to get some pixels around specified center.
    :param gray_scale: image is gray scale or not.
    :return numpy array of center.
    '''
    half_exp_width = size_extract[0] // 2
    half_exp_height = size_extract[1] // 2

    img_width, img_height = img_array.shape[:2]
    if center_position is None:
        x_center = img_width // 2
        y_center = img_height // 2
    else:
        x_center, y_center = size_extract

    center_left = x_center - half_exp_width if x_center - half_exp_width > 0 else 0
    center_right = x_center + half_exp_width if x_center + half_exp_width < img_width else img_width
    center_bottom = y_center - half_exp_height if y_center + half_exp_height > 0 else 0
    center_top = y_center + half_exp_height if y_center + half_exp_height < img_height else img_height

    if gray_scale:
        extracted = img_array[center_left: center_right, center_bottom: center_top]
    else:
        extracted = img_array[center_left: center_right, center_bottom: center_top, :]

    return extracted
