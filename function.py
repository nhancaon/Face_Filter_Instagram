import cv2
import numpy as np
import copy
import face_filter
import threading
import time

def filter(height, size, frame_resize_scale, img, thread, test, prev_frame_time, new_frame_time, filter_name):
    new_frame_time = time.time()
    imgOriginal = copy.deepcopy(img)
    imgOriginal = cv2.resize(imgOriginal, None, fx = 1.0 / frame_resize_scale, fy = 1.0 / frame_resize_scale, interpolation = cv2.INTER_LINEAR)
    try:
        thread[0] = threading.Thread(target = getattr(face_filter, filter_name), args = (imgOriginal, test))
        thread[0].run()
        if (test[0] != None):
            imfilter = test[0]
        else:
            imfilter = imgOriginal
    except:
        imfilter = imgOriginal

    imfilter = np.array(imfilter)
    imfilter = cv2.resize(imfilter, None, fx = frame_resize_scale, fy = frame_resize_scale, interpolation = cv2.INTER_LINEAR)

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # Converting the fps into integer
    fps = int(fps)
    # cv2.putText(imfilter, "{0:.2f}-framePerSecond".format(fps), (50, size[0] - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    return imfilter, prev_frame_time
