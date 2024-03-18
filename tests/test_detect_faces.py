import cv2
import numpy as np
import pytest

from src.demo import detect_faces


def test_detect_faces():
    result = detect_faces("tests/fixtures/test_input.png")
    expected = cv2.imread("tests/fixtures/expected.png")

    assert np.array_equal(result, expected)


def test_no_error():
    with pytest.raises(Exception) as exc_info:
        detect_faces("tests/fixtures/big_img.jpg")
        detect_faces("tests/fixtures/small_img.jpg")
        assert exc_info.type == pytest.fail.Exception
