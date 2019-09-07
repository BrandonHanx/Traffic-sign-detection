from socket import *
import threading
import time
import GLOBAL_VAR
from xmotor import speed_gogo, turn_right, turn_left, stop, do_nothing, buzzer

order_list = ["speed_10", "speed_30", "speed_80", "turn_left", "turn_right", "stop", "do_nothing", "None"]
buzz_list = ["No", "Yes"]


def operate_order(order):
    if order == "0":
        speed_gogo(duty_ratio=0.4)
    elif order == "1":
        speed_gogo(duty_ratio=0.7)
    elif order == "2":
        speed_gogo(duty_ratio=1)
    elif order == "3":
        turn_left()
    elif order == "4":
        turn_right()
    elif order == "5":
        stop()
    else:
        do_nothing()


def operate_buzz(buzz):
    if buzz == "1":
        buzzer()


class Order_Server(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = ('', port)
        self.sock = socket()
        self.sock.bind(self.ADDR)
        self.sock.listen(1)

    def run(self):
        conn, _ = self.sock.accept()
        while True:
            buf = conn.recv(1024).decode('UTF-8')[-2:]  # Discard heaped instructions due to operate orders
            order, buzz = buf[-2], buf[-1]
            print("Order:[", order, "]", order_list[int(order)])
            print("Buzz:[", buzz, "]", buzz_list[int(buzz)])
            operate_order(order)
            operate_buzz(buzz)


class Order_Client(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        self.sock = socket(AF_INET, SOCK_STREAM)

    def run(self):
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        while True:
            self.sock.sendall((GLOBAL_VAR.sign_type + GLOBAL_VAR.person_exist).encode('utf-8'))
            # change this for appropriate ops(order per second)
            time.sleep(0.1)


