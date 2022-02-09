
import os
import pickle
import cv2 as cv2
import numpy as np


SRC_PATH = "data/videos/file.mp4"
base = os.path.basename(SRC_PATH)

camera = 'camera_1'

color_name = "white"

filename = "hsv_filter_plate_{}.pkl".format(color_name)
PATTERN_PATH = "path" + "/" + camera +"/" + filename

low_H = 0
low_S = 0
low_V = 0
high_H = 360
high_S = 255
high_V = 255

low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
stop = False

cap = cv2.VideoCapture(SRC_PATH)
cv2.namedWindow(camera)

nr_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
curr_frame_pos = 0


def show_hist(hist):
    bin_count = hist.shape[0]
    bin_w = 24
    img = np.zeros((256, bin_count * bin_w, 3), np.uint8)
    for i in range(bin_count):
        h = int(hist[i])
        cv2.rectangle(img, (i * bin_w + 2, 255), ((i + 1) * bin_w - 2, 255 - h), (int(360.0 * i / bin_count), 255, 255),
                      -1)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR_FULL)
    cv2.imshow(camera, img)


def set_frame(val):
    global curr_frame_pos
    curr_frame_pos = val
    cap.set(cv2.CAP_PROP_POS_FRAMES, val)


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H - 1, low_H)
    cv2.setTrackbarPos(low_H_name, camera, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H + 1)
    cv2.setTrackbarPos(high_H_name, camera, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S - 1, low_S)
    cv2.setTrackbarPos(low_S_name, camera, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S + 1)
    cv2.setTrackbarPos(high_S_name, camera, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V - 1, low_V)
    cv2.setTrackbarPos(low_V_name, camera, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V + 1)
    cv2.setTrackbarPos(high_V_name, camera, high_V)


cv2.createTrackbar(low_H_name, camera, low_H, high_H, on_low_H_thresh_trackbar)
cv2.createTrackbar(high_H_name, camera, high_H, high_H, on_high_H_thresh_trackbar)
cv2.createTrackbar(low_S_name, camera, low_S, high_S, on_low_S_thresh_trackbar)
cv2.createTrackbar(high_S_name, camera, high_S, high_S, on_high_S_thresh_trackbar)
cv2.createTrackbar(low_V_name, camera, low_V, high_V, on_low_V_thresh_trackbar)
cv2.createTrackbar(high_V_name, camera, high_V, high_V, on_high_V_thresh_trackbar)
cv2.createTrackbar("FRAME POSITION", filename, 0, nr_of_frames, set_frame)

low_H = low_S = low_V = 0
high_H = high_S = high_V = 255

on_low_H_thresh_trackbar(low_H)
on_high_H_thresh_trackbar(high_H)
on_low_S_thresh_trackbar(low_S)
on_high_S_thresh_trackbar(high_S)
on_low_V_thresh_trackbar(low_V)
on_high_V_thresh_trackbar(high_V)


while cap.isOpened():
    if stop:
        cap.set(cv2.CAP_PROP_POS_FRAMES, curr_frame_pos - 1)
    else:
        curr_frame_pos = curr_frame_pos + 1

    succeed, fra = cap.read()
    if fra is None:
        break

    hsv = cv2.cvtColor(fra, cv2.COLOR_BGR2HSV_FULL)
    hsv_threshold = cv2.inRange(hsv, (low_H, low_S, low_V), (high_H, high_S, high_V))
    hist = cv2.calcHist([hsv], [0], hsv_threshold, [16], [0, 360])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    hist = hist.reshape(-1)
    show_hist(hist)
    fg = cv2.bitwise_and(hsv, hsv, mask=hsv_threshold)
    alpha = 0.2
    fg = cv2.addWeighted(fra, alpha, fg, 1 - alpha, 0)
    cv2.imshow(filename, fg)

    key = cv2.waitKey(30)
    # 104, 138, 109, 217, 025, 255

    if key == ord('s'):
        if stop:
            stop = False
        else:
            stop = True
    if key == ord('r'):
        pickle.dump([low_H, low_S, low_V, high_H, high_S, high_V], open(PATTERN_PATH, "wb"))
    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()
