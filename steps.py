
import sys
#uncomment the next line, To check if Pepper-python-SDK is correctly installed
 #print "\n".join(sys.path)
 
#if not, type ont terminal
#export PYTHONPATH=$HOME/pynaoqi/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages:$PYTHONPATH


#from naoqi import ALProxy
#tts = ALProxy("ALTextToSpeech", "192.168.0.162", 9559)
#tts.say("Hola equipo RUTAS, mi nombre es Pepper. Saludos")
#tts.say("Voy a avanzar hacia atraz")

import qi
import argparse
import sys
import time
import math


def main(session):
    """
    PoseInit: Small example to make Nao go to an initial position.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)
    #posture_service.goToPosture("StandZero", 0.5)
    # Go to rest position
    #motion_service.rest()
    x     = 0.5
    y     = 0.0
    theta = 0.0
    frequency = 0.5
    motion_service.moveToward(x, y, theta, [["MaxVelXY", frequency]])

    # Lets make him slow down(step length) and turn after 3 seconds
    time.sleep(1)
    x     = 0.5
    theta = 0.6
    # motion_service.moveToward(x, y, theta, [["MaxVelXY", frequency]])

    # Lets make him slow down(frequency) after 3 seconds
    time.sleep(3)
    frequency = 0.2
    motion_service.moveToward(x, y, theta, [["MaxVelXY", frequency]])

    # Lets make him stop after 3 seconds
    time.sleep(2)
    motion_service.stopMove()
    # Note that at any time, you can use a moveTo command
    # to run a precise distance. The last command received,
    # of velocity or position always wins

    motion_service.rest()


    
def stiffness(session):
    """
    Stiffness On - Active Stiffness of All Joints and Actuators.
    This example is only compatible with NAO.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")

    # We use the "Body" name to signify the collection of all joints
    names = "Body"
    stiffnessLists = 1.0
    timeLists = 1.0
    motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

    # print motion state
    #print motion_service.getSummary()

    time.sleep(2.0)

    # Go to rest position
    #motion_service.rest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.162",
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
    #stiffness(session)
