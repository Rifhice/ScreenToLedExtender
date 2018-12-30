import cv2
import numpy as np
import time
import socket
from PIL import Image as converter
from PIL import Image
import struct

cam = cv2.VideoCapture()
# cam.open("/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0")
cam.open("/dev/v4l/by-id/usb-046d_HD_Webcam_C525_EE9651B0-video-index0")

cv2.namedWindow("test")

hote = "192.168.1.67"
port = 15555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print("Connection on {}".format(port))


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]
    sort = sorted(pixels, key=lambda pix: pix[0])[::-1][0:10]
    r = 0
    g = 0
    b = 0
    sum = 0
    for count, colour in sort:
        sum = sum + count

    for count, colour in sort:
        r = r + colour[0] * count / sum
        g = g + colour[1] * count / sum
        b = b + colour[2] * count / sum
    return (sum, (int(r), int(g), int(b)))


nb_led_left = 14
left_ratio = 1/6
nb_led_up = 33
nb_led_right = 13
right_ratio = 1/6

img_counter = 0

while True:
    ret, frame = cam.read()

    rows, cols, ch = frame.shape
    pts1 = np.float32([[123, 20], [489, 209], [82, 474], [505, 466]])
    pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(frame, M, (300, 300))

    hsvImg = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    # multiple by a factor to change the saturation
    hsvImg[..., 1] = hsvImg[..., 1]*1

    # multiple by a factor of less than 1 to reduce the brightness
    hsvImg[..., 2] = hsvImg[..., 2]*0.9

    matrix = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR)
    matrix = adjust_gamma(matrix, 0.7)
    cv2.imshow('frame', matrix)
    left = 0
    top = 0
    width = left + matrix.shape[0]
    height = top + matrix.shape[0]

    left_chunk_size = [width / 4,
                       int(height * left_ratio / nb_led_left)]
    upper_chunk_size = [
        int(width / nb_led_up), height / 4]
    right_chunk_size = [
        width / 4, int(height * right_ratio / nb_led_right)]

    led_colors = ""
    colors = []
    i = 0
    while i < nb_led_left:
        left = 0
        top = int(i * left_chunk_size[1])
        width = int(left_chunk_size[0])
        height = int(
            i * left_chunk_size[1] + left_chunk_size[1])
        cropped = matrix[top:top + height, left:left + width]
        color = most_frequent_colour(
            converter.fromarray(cropped))[1]
        r = color[2]
        g = color[1]
        b = color[0]
        if abs(r - g) + abs(g - b) < 30 and r < 90:
            r = 0
            g = 0
            b = 0
        if r > g and r > b:
            if r - b > 30:
                b = 0
            if r - g > 30:
                g = 0
        if g > r and g > b:
            if g - b > 30:
                b = 0
            if g - r > 30:
                r = 0
        if b > g and b > r:
            if b - r > 30:
                r = 0
            if b - g > 30:
                g = 0
        colors.insert(0, ', '.join(
            [str(g), str(r), str(b)]))
        i = i + 1
    i = 0
    while i < nb_led_up:
        left = int(i * upper_chunk_size[0])
        top = 0
        width = int(i * upper_chunk_size[0] + upper_chunk_size[0])
        height = int(upper_chunk_size[1])
        cropped = matrix[top:top + height, left:left + width]
        color = most_frequent_colour(
            converter.fromarray(cropped))[1]
        r = color[2]
        g = color[1]
        b = color[0]
        if abs(r - g) + abs(g - b) < 30 and r < 90:
            r = 0
            g = 0
            b = 0
        if r > g and r > b:
            if r - b > 30:
                b = 0
            if r - g > 30:
                g = 0
        if g > r and g > b:
            if g - b > 30:
                b = 0
            if g - r > 30:
                r = 0
        if b > g and b > r:
            if b - r > 30:
                r = 0
            if b - g > 30:
                g = 0
        colors.append(', '.join(
            [str(g), str(r), str(b)]))
        i = i + 1
    tmp = []
    i = 0
    while i < nb_led_right:
        left = width - int(right_chunk_size[0])
        top = int(i * right_chunk_size[1])
        width = int(right_chunk_size[0])
        height = int(
            i * right_chunk_size[1] + right_chunk_size[1])
        cropped = matrix[top:top + height, left:left + width]
        color = most_frequent_colour(
            converter.fromarray(cropped))[1]
        r = color[2]
        g = color[1]
        b = color[0]
        if abs(r - g) + abs(g - b) < 30 and r < 90:
            r = 0
            g = 0
            b = 0
        if r > g and r > b:
            if r - b > 30:
                b = 0
            if r - g > 30:
                g = 0
        if g > r and g > b:
            if g - b > 30:
                b = 0
            if g - r > 30:
                r = 0
        if b > g and b > r:
            if b - r > 30:
                r = 0
            if b - g > 30:
                g = 0
        tmp.insert(0, ', '.join(
            [str(g), str(r), str(b)]))
        i = i + 1
    colors = colors + tmp
    dataFormatted = '|'.join(str(v) for v in colors) + '\0'
    socket.send(struct.pack("i", len(dataFormatted.encode())
                            ) + dataFormatted.encode())
    if not ret:
        break
    k = cv2.waitKey(1)
    time.sleep(0.5)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
