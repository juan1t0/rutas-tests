#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time
import Image

import numpy as np
import matplotlib.pyplot as plt
import cv2



def process_image(image, emotion=True, size=(224,224)):
    image = cv2.resize(image, size)
    image = np.transpose(image,(2,0,1))
    if emotion:
        prediction = 0
        return (prediction, image)
    return image

def main(session):

    video_service = session.service("ALVideoDevice")
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)

    t0 = time.time()
    naoImage = video_service.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.
    print "acquisition delay ", t1 - t0

    video_service.unsubscribe(videoClient)


    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    img_str = str(bytearray(array))

    img = np.fromstring(img_str, np.uint8)

    res = process_image(img, False)

    if isinstance(res, tuple):
        print(res[0])
        res = res[1]

    plt.imshow(res)
    raw_input('')


    # im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
    # im.save("camImage.png", "PNG")
    # im.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.218.82",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
