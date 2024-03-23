import cv2
import numpy as np
import pytest

from src.demo import detect_faces


def test_detect_faces():
    img = cv2.imread("tests/fixtures/test_input.png")
    result = detect_faces(img)
    expected = cv2.imread("tests/fixtures/expected.png")

    assert np.array_equal(result, expected)


def test_no_error():
    with pytest.raises(Exception) as exc_info:
        detect_faces("tests/fixtures/big_img.jpg")
        detect_faces("tests/fixtures/small_img.jpg")
        assert exc_info.type == pytest.fail.Exception
