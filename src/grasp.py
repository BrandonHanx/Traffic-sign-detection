import cv2
import utils
import time
import os
min_size_components = 500
similarity_contour_with_circle = 0.8
path = '.\\images\\process\\'
style = True
out_size = 32

"""
for Single Image
"""
if style:
    img_path = path + 'new.jpg'
    org_img = cv2.imread(img_path)
    # eha_img = utils.constrast_limit(org_img)
    # cv2.imwrite(path + 'enhanced.png', eha_img)
    # gam_img = utils.contrast_brightness_image(eha_img)
    # # gam_img = utils.adjust_gamma(eha_img)
    # cv2.imwrite(path + 'gamma.png', gam_img)
    # time1 = time.clock()
    # pre_img = utils.preprocess_image(org_img)
    # time2 = time.clock()
    # # cv2.imwrite(path + 'preprocess.png', pre_img)
    #
    # bin_img = utils.removeSmallComponents(pre_img, min_size_components)
    # # cv2.imwrite(path + 'binary.png', bin_img)
    # time3 = time.clock()
    #
    # contours = utils.findContour(bin_img)
    # time4 = time.clock()
    #
    # # lab_img = org_img.copy()
    # # for cnt in contours:
    # #     cv2.drawContours(lab_img, cnt, -1, (0, 255, 0), 3)
    # #
    # # cv2.imwrite(path + 'labeled.png', lab_img)
    #
    # sign, coordinate = utils.findLargestSign(org_img, contours, similarity_contour_with_circle, 15)
    # time5 = time.clock()
    # print(time2-time1, time3-time2, time4-time3, time5-time4)
    # # box_img = org_img.copy()
    # # cv2.rectangle(box_img, coordinate[0], coordinate[1], (0, 255, 0), 10)
    # # cv2.imwrite(path + 'box.png', box_img)
    _, sign_type, _ = utils.get_localization_label(org_img)
    print(sign_type)

"""
for video
"""
if not style:
    vdo_path = path + 'test.mp4'
    out_path = path + 'test_out.mp4'
    save_path = '.\\images\\train\\sign_2\\'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    vdo = utils.Video(vdo_path)
    vdo.output_generate(out_path)
    generate_img = True

    time_start = time.clock()
    while True:
        ret, org_fra = vdo.input_movie.read()
        if not ret:
            break

        pre_fra = utils.preprocess_image(org_fra)
        bin_fra = utils.removeSmallComponents(pre_fra, min_size_components)
        contours = utils.findContour(bin_fra)
        sav_img, coordinate = utils.findLargestSign(org_fra, contours, similarity_contour_with_circle, 15)

        box_fra = org_fra.copy()
        if coordinate:
            cv2.rectangle(box_fra, coordinate[0], coordinate[1], (0, 255, 0), 2)
            # print(coordinate)
            if generate_img:
                sav_img = cv2.resize(sav_img, (out_size, out_size), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(save_path + "%04d" % vdo.frame_number + '.png', sav_img)

        print("Writing frame {} / {}".format(vdo.frame_number, vdo.length))
        vdo.output_movie.write(box_fra)
        vdo.frame_number += 1

    time_end = time.clock()
    vdo.frame_number = 0
    print('Total time cost:', time_end-time_start, 's')
    print('Video original time:', vdo.length/vdo.fps, 's')

