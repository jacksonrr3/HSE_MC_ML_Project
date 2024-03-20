import cv2
import numpy as np
import streamlit as st
import torch.nn.functional as F

from src.demo import detect_faces


def run_app():
    def fix_image(image):
        result = detect_faces(image)

        col1.write("Input image")
        col1.image(image)

        col2.write("Faces detected")
        col2.image(result)
        # st.sidebar.markdown("\n")
        # st.sidebar.download_button("Download fixed image", convert_image(fixed), "fixed.png", "image/png")

    st.set_page_config(layout="wide", page_title="Image Background Remover")

    st.header("Detect faces in your image")
    st.write("### ML project")
    st.write(
        "Try uploading an image to watch the faces detected. "
        + "Full quality images can be downloaded from the sidebar. "
        + "This code is open source and available [here](https://github.com/jacksonrr3/HSE_MC_ML_Project)."
    )
    st.sidebar.write("## Upload and download :gear:")
    col1, col2 = st.columns(2)

    uploaded_file = st.sidebar.file_uploader(
        "Upload an image", type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        fix_image(image)
    else:
        image = cv2.imread("data/demo.png")
        fix_image(image)


if __name__ == "__main__":
    run_app()
