import time
import socket
import cv2
import mss
import numpy
from PIL import Image as converter
from PIL import Image
import struct


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


hote = "192.168.1.67"
port = 15555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print("Connection on {}".format(port))

nb_led_left = 14
left_ratio = 1/6
nb_led_up = 33
nb_led_right = 13
right_ratio = 1/6

with mss.mss() as sct:

    monitor = sct.monitors[2]

    # Capture a bbox using percent values
    left = monitor["left"]
    top = monitor["top"]
    right = left + monitor["width"]
    lower = top + monitor["height"]
    bbox = (left, top, right, lower)

    left_chunk_size = [monitor["width"] / 4,
                       int(monitor["height"] * left_ratio / nb_led_left)]
    upper_chunk_size = [
        int(monitor["width"] / nb_led_up), monitor["height"] / 4]
    right_chunk_size = [
        monitor["width"] / 4, int(monitor["height"] * right_ratio / nb_led_right)]

    while "Screen capturing":
        last_time = time.time()
        im = sct.grab(bbox)
        matrix = numpy.array(im)

        hsvImg = cv2.cvtColor(matrix, cv2.COLOR_BGR2HSV)
        # multiple by a factor to change the saturation
        hsvImg[..., 1] = hsvImg[..., 1]*1.1

        # multiple by a factor of less than 1 to reduce the brightness
        hsvImg[..., 2] = hsvImg[..., 2]*1

        matrix = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR)
        matrix = cv2.cvtColor(matrix, cv2.COLOR_RGB2RGBA)

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
            left = monitor["width"] - int(right_chunk_size[0])
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
        cv2.imshow('frame', cropped)
        dataFormatted = '|'.join(str(v) for v in colors) + '\0'
        socket.send(struct.pack("i", len(dataFormatted.encode())
                                ) + dataFormatted.encode())
        time.sleep(0.2)
        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
