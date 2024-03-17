import cv2
import numpy as np

from src.demo import detect_faces


def test_detect_faces():
    # img = cv2.imread('fixtures/marty_test.png')

    result = detect_faces("tests/fixtures/test_input.png")
    expected = cv2.imread("tests/fixtures/expected.png")
    # cv2.imwrite("test.png", frame)
    # assert img.ndim == 2
    # assert img.dtype == np.float64
    # img = imread(fetch('data/camera.png'), as_gray=True)
    # # check that conversion does not happen for a gray image
    # assert np.dtype(img.dtype).char in np.typecodes['AllInteger']
    assert np.array_equal(result, expected)
