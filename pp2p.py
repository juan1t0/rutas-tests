# testing use of python 2 and 3
# python 2.7 here

#export PYTHONPATH=$HOME/pynaoqi/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages:$PYTHONPATH

import qi
import argparse
import sys
import time
from PIL import Image


def main(session, name):

    posture_service = session.service("ALRobotPosture")
    if posture_service.getPosture() != 'Stand' or posture_service.getPosture() != 'StandInit':
        posture_service.goToPosture("Stand", 0.5)

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

    img = Image.frombytes("RGB", (imageWidth, imageHeight), img_str)

    img.save("captures/"+name+'.png', "PNG")
    #raw_input('')

    # im.show()
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.162",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--name", type=str, help="name to save")
    
    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.name)
