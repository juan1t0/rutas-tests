# python 2.7 here
# script for recognizing people faces


import time
from naoqi import ALProxy
import qi
import argparse
import sys
from PIL import Image


def main(session, name):

    posture_service = session.service("ALRobotPosture")
    if posture_service.getPosture() != 'Stand' or posture_service.getPosture() != 'StandInit':
        posture_service.goToPosture("Stand", 0.5)

    face_service = session.service("ALFaceDetection")
    face_service.subscribe("Test_Face", 500, 0.0)
    memoryProxy = session.service("ALMemory")
    while True:
        #print "a"
        time.sleep(0.5)
        val = memoryProxy.getData("FaceDetected",0)
        if len(val) > 0:
            break
    face_service.unsubscribe("Test_Face")

    video_service = session.service("ALVideoDevice")
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)

    t0 = time.time()
    naoImage = video_service.getImageRemote(videoClient)

    t1 = time.time()

    print "acquisition delay ", t1 - t0

    video_service.unsubscribe(videoClient)


    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    img_str = str(bytearray(array))

    img = Image.frombytes("RGB", (imageWidth, imageHeight), img_str)

    img.save("captures/"+name+'.png', "PNG")

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
