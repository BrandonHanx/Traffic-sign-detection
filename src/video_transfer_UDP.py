from socket import *
from math import ceil
import threading
import cv2
import numpy as np
import GLOBAL_VAR

generate_img = False
save_path = ".\\images\\train\\5\\"


class Video_Server(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = ('', port)
        self.sock = socket(AF_INET, SOCK_DGRAM)

    def __del__(self):
        self.sock.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def rcv(self):
        data = b''
        while True:
            try:
                r, _ = self.sock.recvfrom(75000)
                a = r.find(b"end_frame")
                if not a == -1:
                    data += r[:a]
                    if not len(data) > 0:
                        data = b''
                        return b'1'
                    return data
                else:
                    data += r
            except Exception as e:
                print(e)
                continue

    def run(self):
        from utils import get_localization_label
        from pedestrian import detect_person

        print("VEDIO server starts...")
        self.sock.bind(self.ADDR)
        frame_number = 0
        while True:
            data = b''
            while data is b'':
                data = self.rcv()
            nparr = np.fromstring(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is None:
                pass
            else:
                try:
                    sign, GLOBAL_VAR.sign_type, coordinate = get_localization_label(frame)
                    frame, GLOBAL_VAR.person_exist = detect_person(frame)

                    box_fra = frame.copy()
                    if coordinate:
                        cv2.rectangle(box_fra, coordinate[0], coordinate[1], (0, 255, 0), 2)
                        if generate_img:
                            sav_img = cv2.resize(sign, (32, 32), interpolation=cv2.INTER_CUBIC)
                            cv2.imwrite(save_path + "%04d" % frame_number + '.png', sav_img)

                    frame_number += 1
                    cv2.imshow('Remote', box_fra)
                    print("Label:", GLOBAL_VAR.sign_type)
                    print("person?:", GLOBAL_VAR.person_exist)
                    if cv2.waitKey(1) & 0xFF == 27:  # ESC for end
                        break
                except:
                    pass


class Video_Client(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.cap = cv2.VideoCapture(0)
        print("VEDIO client starts...")

    def __del__(self):
        self.sock.close()
        self.cap.release()

    def run(self):

        while True:
            ret, frame = self.cap.read()
            data = cv2.imencode('.jpg', frame)[1].tostring()
            i = 1
            k = len(data) / 65000
            m = len(data) % 65000
            k = ceil(k)
            p = 0
            q = 65000
            while not i > k:
                sts = data[p:q]
                self.sock.sendto(sts, self.ADDR)
                if i == k - 1:
                    p += 65000
                    q += m
                    sts = data[p:q]
                    self.sock.sendto(sts, self.ADDR)
                    break
                else:
                    p += 65000
                    q += 65000
                i += 1
            self.sock.sendto(b"end_frame", self.ADDR)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
