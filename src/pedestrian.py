import numpy as np
import os
import cv2
import time

net_file= './model/MobileNetSSD_deploy.prototxt'
caffe_model='./model/MobileNetSSD_deploy10695.caffemodel'

if not os.path.exists(caffe_model):
    print("MobileNetSSD_deploy.caffemodel does not exist,")
    exit()

net = cv2.dnn.readNetFromCaffe(net_file, caffe_model)

CLASSES = ('background', 'person')


def detect_person(origimg):
   
    (h, w) = origimg.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(origimg, (300, 300)),
            0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()
    person_exist = "0"
    
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.2:
            # extract the index of the class label from the
            # `detections`
            idx = int(detections[0, 0, i, 1])
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx],
                confidence * 100)
            cv2.rectangle(origimg, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(origimg, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            person_exist = "1"

    return origimg, person_exist


if __name__ == '__main__':

    # video_capture = cv2.VideoCapture(0)
    # while True:
    #     ret, frame = video_capture.read()
    #     frame, person_exist = detect_person(frame)
    #     cv2.imshow("SSD", frame)
    #     print(person_exist)
    #
    #     if cv2.waitKey(1) & 0xFF == 27:
    #         break
    #
    # video_capture.release()
    # cv2.destroyAllWindows()
    img_path = '.\\images\\process\\hhh.png'
    org_img = cv2.imread(img_path)
    time1 = time.clock()
    dec_img, person_exist = detect_person(org_img)
    time2 = time.clock()
    cv2.imwrite('.\\images\\process\\done.png', dec_img)
    print(time2-time1, person_exist)


