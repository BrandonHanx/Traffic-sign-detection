import sys
import time
import argparse
from order_transfer import Order_Server

parser = argparse.ArgumentParser()
parser.add_argument('--udp', type=bool, default=True)
parser.add_argument('--host', type=str, default='192.168.137.1', help='your PC IP')  # change this for your PC IP
parser.add_argument('--port', type=int, default=10087)

args = parser.parse_args()

IP = args.host
PORT = args.port
UDP = args.udp

if UDP:
    from video_transfer_UDP import Video_Client
else:
    from video_transfer_TCP import Video_Client

if __name__ == '__main__':
    vclient = Video_Client(IP, PORT)
    oserver = Order_Server(PORT + 1)
    vclient.start()
    oserver.start()
    while True:
        time.sleep(1)
        if not vclient.isAlive():
            print("Video connection lost...")
            sys.exit(0)
        if not oserver.isAlive():
            print("Order connection lost...")
            sys.exit(0)
