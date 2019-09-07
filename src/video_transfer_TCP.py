from socket import *
import threading
import cv2
import struct
import pickle
import time
import zlib
import GLOBAL_VAR

generate_img = False
save_path = ".\\images\\train\\0\\"


class Video_Server(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = ('', port)
        self.sock = socket(AF_INET, SOCK_STREAM)

    def __del__(self):
        self.sock.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def run(self):
        from utils import get_localization_label
        from pedestrian import detect_person

        print("VEDIO server starts...")
        self.sock.bind(self.ADDR)
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        print("remote VEDIO client success connected...")
        data = "".encode("utf-8")
        payload_size = struct.calcsize("L")
        cv2.namedWindow('Remote', cv2.WINDOW_AUTOSIZE)
        frame_number = 0
        while True:
            while len(data) < payload_size:
                data += conn.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]
            while len(data) < msg_size:
                data += conn.recv(81920)
            zframe_data = data[:msg_size]
            data = data[msg_size:]
            frame_data = zlib.decompress(zframe_data)
            frame = pickle.loads(frame_data)
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


class Video_Client(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.cap = cv2.VideoCapture(0)
        print("VEDIO client starts...")

    def __del__(self):
        self.sock.close()
        self.cap.release()

    def run(self):
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue

        print("VEDIO client connected...")
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            sframe = cv2.resize(frame, (400, 300))
            data = pickle.dumps(sframe)
            zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            try:
                self.sock.send(struct.pack("L", len(zdata)) + zdata)
            except:
                break
            self.cap.read()
            # change this for appropriate fps
            time.sleep(0.1)