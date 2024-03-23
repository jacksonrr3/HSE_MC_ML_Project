import os
from argparse import ArgumentParser

import cv2
import numpy as np

# try:
#     from armv7l.openvino.inference_engine import IENetwork, IEPlugin
# except:
# from openvino.inference_engine import IECore
import openvino.runtime as ov
import streamlit as st
import torch
import torch.nn.functional as F

import src.common as common


def nms(objs, iou=0.5):

    if objs is None or len(objs) <= 1:
        return objs

    objs = sorted(objs, key=lambda obj: obj.score, reverse=True)
    keep = []
    flags = [0] * len(objs)
    for index, obj in enumerate(objs):

        if flags[index] != 0:
            continue

        keep.append(obj)
        for j in range(index + 1, len(objs)):
            if flags[j] == 0 and obj.iou(objs[j]) > iou:
                flags[j] = 1
    return keep


def detect(infer_request, image, threshold=0.4, nms_iou=0.5):
    # outputs = compiled_model.infer_new_request(image)
    outputs = infer_request.infer(image)
    # outputs = compiled_model.infer(inputs={input_blob: image})
    # outputs = exec_net.infer(inputs={input_blob: image})
    # print('outputs:', outputs)
    # print('outputs[\'Sigmoid_526\'].shape:', outputs['Sigmoid_526'].shape)
    # print('outputs[\'Exp_527\'].shape:', outputs['Exp_527'].shape)
    # print('outputs[\'Conv_525\'].shape:', outputs['Conv_525'].shape)
    hm, box, landmark = outputs["Sigmoid_526"], outputs["Exp_527"], outputs["Conv_525"]
    # hm, box, landmark = outputs['1028'], outputs['1029'], outputs['1027']

    # print('outputs:', outputs)
    # print('outputs[\'1028\'].shape:', outputs['1028'].shape)
    # print('outputs[\'1029\'].shape:', outputs['1029'].shape)
    # print('outputs[\'1027\'].shape:', outputs['1027'].shape)

    hm = torch.from_numpy(hm).clone()
    box = torch.from_numpy(box).clone()
    landmark = torch.from_numpy(landmark).clone()

    hm_pool = F.max_pool2d(hm, 3, 1, 1)
    scores, indices = ((hm == hm_pool).float() * hm).view(1, -1).cpu().topk(1000)
    hm_height, hm_width = hm.shape[2:]

    scores = scores.squeeze()
    indices = indices.squeeze()
    ys = list((indices / hm_width).int().data.numpy())
    xs = list((indices % hm_width).int().data.numpy())
    # ys = list((indices / hm_height).int().data.numpy())
    # xs = list((indices % hm_width).int().data.numpy())
    scores = list(scores.data.numpy())
    box = box.cpu().squeeze().data.numpy()
    landmark = landmark.cpu().squeeze().data.numpy()

    stride = 4
    objs = []
    for cx, cy, score in zip(xs, ys, scores):
        if score < threshold:
            break

        x, y, r, b = box[:, cy, cx]
        xyrb = (np.array([cx, cy, cx, cy]) + [-x, -y, r, b]) * stride
        x5y5 = landmark[:, cy, cx]
        x5y5 = (common.exp(x5y5 * 4) + ([cx] * 5 + [cy] * 5)) * stride
        box_landmark = list(zip(x5y5[:5], x5y5[5:]))
        objs.append(common.BBox(0, xyrb=xyrb, score=score, landmark=box_landmark))
    return nms(objs, iou=nms_iou)


def process_video(exec_net, input_blob):
    cap = cv2.VideoCapture("data/demo.mp4")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    ok, frame = cap.read()

    while ok:
        img = cv2.resize(frame, (640, 480))
        frame = img.copy()
        # img = ((img / 255.0 - mean) / std).astype(np.float32)
        img = img[np.newaxis, :, :, :]  # Batch size axis add
        img = img.transpose((0, 3, 1, 2))  # NHWC to NCHW
        objs = detect(exec_net, input_blob, img)

        for obj in objs:
            common.drawbbox(frame, obj)

        cv2.imshow("demo DBFace", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        ok, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()


def get_model(model_xml):
    model_bin = os.path.splitext(model_xml)[0] + ".bin"
    ie = ov.Core()
    model = ie.read_model(model=model_xml, weights=model_bin)
    compiled_model = ie.compile_model(model, "CPU")
    return compiled_model.create_infer_request()


def detect_faces(img):
    infer_request = get_model("model/dbface.xml")

    img = cv2.resize(img, (640, 480))
    frame = img.copy()
    img = img[np.newaxis, :, :, :]  # Batch size axis add
    img = img.transpose((0, 3, 1, 2))  # NHWC to NCHW
    objs = detect(infer_request, img)
    for obj in objs:
        common.drawbbox(frame, obj)
    return frame


def run_demo():
    img = cv2.imread("data/demo.png")
    frame = detect_faces(img)
    cv2.imshow("demo DBFace", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Demo run!!!")
    run_demo()
