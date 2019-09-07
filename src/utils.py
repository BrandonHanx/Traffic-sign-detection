import cv2
import numpy as np
from math import sqrt, pow
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import time

norm_size = 32
model = load_model("./model/traffic_sign.model")


# Preprocess image
def constrast_limit(image):
    img_hist_equalized = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    channels = cv2.split(img_hist_equalized)
    channels[1] = cv2.equalizeHist(channels[1])
    # channels[2] = cv2.equalizeHist(channels[2])
    img_hist_equalized = cv2.merge(channels)
    img_hist_equalized = cv2.cvtColor(img_hist_equalized, cv2.COLOR_HSV2BGR)
    # cv2.imwrite("./images/process/hist.png", img_hist_equalized)
    return img_hist_equalized


def adjust_gamma(image, gamma=3, c=1):
    """
    Tooooo slow!!!!
    """
    h, w, d = image.shape[0], image.shape[1], image.shape[2]
    new_img = np.zeros((h, w, d), dtype=np.float32)
    for i in range(h):
        for j in range(w):
            new_img[i, j, 0] = c*pow(image[i, j, 0], gamma)
            new_img[i, j, 1] = c*pow(image[i, j, 1], gamma)
            new_img[i, j, 2] = c*pow(image[i, j, 2], gamma)
    cv2.normalize(new_img, new_img, 0, 255, cv2.NORM_MINMAX)
    new_img = cv2.convertScaleAbs(new_img)
    # cv2.imwrite("./images/process/gamma.png", new_img)
    return new_img


def contrast_brightness_image(src1, a=4, g=20):
    h, w, ch = src1.shape
    src2 = np.zeros([h, w, ch], src1.dtype)
    dst = cv2.addWeighted(src1, a, src2, 1 - a, g)
    # cv2.imwrite("./images/process/bright.png", dst)
    return dst


def remove_green(imgBGR):
    rows, cols, _ = imgBGR.shape
    imgHSV = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2HSV)

    Bmin = np.array([100, 43, 46])
    Bmax = np.array([124, 255, 255])
    img_Bbin = cv2.inRange(imgHSV, Bmin, Bmax)

    # because the HSV model is a circular cone, we need consider red twice
    # Rmin1 = np.array([0, 43, 46])
    # Rmax1 = np.array([5, 255, 255])
    # img_Rbin1 = cv2.inRange(imgHSV, Rmin1, Rmax1)

    Rmin2 = np.array([156, 43, 46])
    Rmax2 = np.array([180, 255, 255])
    img_Rbin2 = cv2.inRange(imgHSV, Rmin2, Rmax2)

    # img_Rbin = np.maximum(img_Rbin1, img_Rbin2)
    img_bin = np.maximum(img_Bbin, img_Rbin2)

    return img_bin


def erode_dilate(image):

    kernelErosion = np.ones((2, 2), np.uint8)
    kernelDilation = np.ones((2, 2), np.uint8)
    # open
    # new_img = cv2.erode(image, kernelErosion, iterations=2)
    # new_img = cv2.dilate(new_img, kernelDilation, iterations=2)
    # close
    new_img = cv2.dilate(image, kernelDilation, iterations=2)
    new_img = cv2.erode(new_img, kernelErosion, iterations=2)

    # cv2.imwrite("./images/process/binary.png", new_img)

    return new_img


def preprocess_image(image):

    # image = adjust_gamma(image)
    # image = constrast_limit(image)
    # image = contrast_brightness_image(image)
    image = remove_green(image)
    image = erode_dilate(image)

    return image


# Find Signs
def removeSmallComponents(image, threshold):
    # find all your connected components (white blobs in your image)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
    sizes = stats[1:, -1]
    nb_components = nb_components - 1

    img2 = np.zeros(output.shape, dtype=np.uint8)
    # for every component in the image, you keep it only if it's above threshold
    for i in range(0, nb_components):
        if sizes[i] >= threshold:
            img2[output == i + 1] = 255
    return img2


def findContour(image):
    # find contours in the thresholded image
    cnts, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts


def contourIsSign(perimeter, centroid, threshold):
    #  perimeter, centroid, threshold
    # # Compute signature of contour
    result = []
    for p in perimeter:
        p = p[0]
        distance = sqrt((p[0] - centroid[0]) ** 2 + (p[1] - centroid[1]) ** 2)
        result.append(distance)
    max_value = max(result)
    signature = [float(dist) / max_value for dist in result]
    # Check signature of contour.
    temp = sum((1 - s) for s in signature)
    temp = temp / len(signature)
    if temp < threshold:  # is  the sign
        return True, max_value + 2
    else:  # is not the sign
        return False, max_value + 2


# crop sign
def cropContour(image, center, max_distance):
    width = image.shape[1]
    height = image.shape[0]
    top = max([int(center[0] - max_distance), 0])
    bottom = min([int(center[0] + max_distance + 1), height - 1])
    left = max([int(center[1] - max_distance), 0])
    right = min([int(center[1] + max_distance + 1), width - 1])
    print(left, right, top, bottom)
    return image[left:right, top:bottom]


def cropSign(image, coordinate):
    width = image.shape[1]
    height = image.shape[0]
    top = max([int(coordinate[0][1]), 0])
    bottom = min([int(coordinate[1][1]), height - 1])
    left = max([int(coordinate[0][0]), 0])
    right = min([int(coordinate[1][0]), width - 1])
    # print(top,left,bottom,right)
    return image[top:bottom, left:right]


def findLargestSign(image, contours, threshold, distance_theshold):
    max_distance = 0
    coordinate = None
    sign = None
    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        is_sign, distance = contourIsSign(c, [cX, cY], 1 - threshold)
        if is_sign and distance > max_distance and distance > distance_theshold:
            max_distance = distance
            coordinate = np.reshape(c, [-1, 2])
            left, top = np.amin(coordinate, axis=0)
            right, bottom = np.amax(coordinate, axis=0)
            coordinate = [(left - 2, top - 2), (right + 3, bottom + 1)]
            sign = cropSign(image, coordinate)
    return sign, coordinate


def findSigns(image, contours, threshold, distance_theshold):
    signs = []
    coordinates = []
    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        is_sign, max_distance = contourIsSign(c, [cX, cY], 1 - threshold)
        if is_sign and max_distance > distance_theshold:
            sign = cropContour(image, [cX, cY], max_distance)
            signs.append(sign)
            coordinate = np.reshape(c, [-1, 2])
            top, left = np.amin(coordinate, axis=0)
            right, bottom = np.amax(coordinate, axis=0)
            coordinates.append([(top - 2, left - 2), (right + 1, bottom + 1)])
    return signs, coordinates


def remove_line(img):
    gray = img.copy()
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    minLineLength = 5
    maxLineGap = 3
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, minLineLength, maxLineGap)
    mask = np.ones(img.shape[:2], dtype="uint8") * 255
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(mask, (x1, y1), (x2, y2), (0, 0, 0), 2)
    return cv2.bitwise_and(img, img, mask=mask)


def predict(image):
    # pre-process the image for classification
    image = cv2.resize(image, (norm_size, norm_size))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # classify the input image
    result = model.predict(image)[0]
    probability = np.max(result)
    # label = np.where(result == probability)[0]
    label = str(np.where(result == probability)[0])[1]
    # label = "{}: {:.2f}%".format(label, probability * 100)
    return label


def get_localization_label(org_img, min_size_components=500, similarity_contour_with_circle=0.8):
    # time1 = time.clock()
    pre_img = preprocess_image(org_img)
    bin_img = removeSmallComponents(pre_img, min_size_components)
    contours = findContour(bin_img)
    sign, coordinate = findLargestSign(org_img, contours, similarity_contour_with_circle, 15)
    if sign is None:
        # if there is no sign_label recognized, set sign_type with background as default
        sign_type = "6"
    else:
        # time2 = time.clock()
        sign_type = predict(sign)
    # time3 = time.clock()
    # print(time2-time1, time3-time1)
    return sign, sign_type, coordinate


def sharpen(img):
    kernel_sharpen = np.array([
        [1, 1, 1],
        [1, -7, 1],
        [1, 1, 1]])

    output_img = cv2.filter2D(img, -1, kernel_sharpen)
    return output_img


class Video(object):

    def __init__(self, input_source):
        self.input_source = input_source
        self.input_movie = cv2.VideoCapture(input_source)
        self.length = int(self.input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.input_movie.get(cv2.CAP_PROP_FPS)
        self.width = int(self.input_movie.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_number = 0
        self.output_movie = None

    def output_generate(self, output_source):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.output_movie = cv2.VideoWriter(output_source, fourcc, self.fps, (self.width, self.height))
