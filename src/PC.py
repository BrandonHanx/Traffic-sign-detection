import sys
import time
import argparse
from order_transfer import Order_Client

parser = argparse.ArgumentParser()

parser.add_argument('--udp', type=bool, default=True)
parser.add_argument('--host', type=str, default='192.168.137.104', help='your Pi IP')  # change this for your Pi IP
parser.add_argument('--port', type=int, default=10087)

args = parser.parse_args()

IP = args.host
PORT = args.port
UDP = args.udp

if UDP:
    from video_transfer_UDP import Video_Server
else:
    from video_transfer_TCP import Video_Server

if __name__ == '__main__':
    vserver = Video_Server(PORT)
    oclient = Order_Client(IP, PORT + 1)
    vserver.start()
    oclient.start()
    while True:
        time.sleep(1)
        if not vserver.isAlive():
            print("Video connection lost...")
            sys.exit(0)
        if not oclient.isAlive():
            print("Order connection lost...")
            sys.exit(0)
