import cv2
from utils import get_localization_label
from xmotor import speed_gogo, turn_right, turn_left, stop, do_nothing
import time


def operate(label):
    if label == 0:
        speed_gogo(0.4)
    elif label == 1:
        speed_gogo(0.7)
    elif label == 2:
        speed_gogo(1)
    elif label == 3:
        turn_left()
    elif label == 4:
        turn_right()
    elif label == 5:
        stop()
    else:
        do_nothing()
    return


def main():
    cap = cv2.VideoCapture(0)
    frame_number = 0
    generate_img = False
    save_path = ".\\images\\train\\5\\"
    order_list = ["speed_10", "speed_30", "speed_80", "turn_left", "turn_right", "stop", "do_nothing", "None"]

    while True:
        _, frame = cap.read()
        sign, sign_type, coordinate = get_localization_label(frame)

        box_fra = frame.copy()
        if coordinate:
            cv2.rectangle(box_fra, coordinate[0], coordinate[1], (0, 255, 0), 2)
            if generate_img:
                sav_img = cv2.resize(sign, (32, 32), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(save_path + "%04d" % frame_number + '.png', sav_img)

        operate(int(sign_type))
        print("Order:[", sign_type, "]", order_list[int(sign_type)])
        cv2.imshow("Real-time scene", box_fra)

        k = cv2.waitKey(1)

        if k == 27:
            cv2.destroyAllWindows()
            break

        elif k == ord("s"):
            cv2.imwrite(".\\images\\capture\\capture_%04d" % frame_number + '.png', frame)

        frame_number += 1
        time.sleep(0.1)

    cap.release()


main()
