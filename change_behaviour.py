# python 2.7 here
# script for changing robot behavior, showing images and moving

import qi
import argparse
import sys
import time

reaction1 = {'status': 'positive', 'img_url': 'https://raw.githubusercontent.com/juan1t0/rutas_probes/main/reaction1.png',
                'X_': 0.5, 'Y_': 0.0, 'Theta': 0.0,
                'frequency':0.5, 'time': 2}
reaction2 = {'status': 'neutral', 'img_url': 'https://raw.githubusercontent.com/juan1t0/rutas_probes/main/reaction2.png',
                'X_': 0.3, 'Y_': 0.0, 'Theta': 0.0,
                'frequency':0.2, 'time': 4}
reaction3 = {'status': 'negative', 'img_url': 'https://raw.githubusercontent.com/juan1t0/rutas_probes/main/reaction3.png',
                'X_': -0.5, 'Y_': 0.0, 'Theta': 0.0,
                'frequency':0.3, 'time': 5}

threshold_1 = -2
threshold_2 = 3

'''
reaction{1,2,3} : Dictionary with desire robot reaction, having the image link to show and movement features
threshold_{1,2} : Threshold that define if the robots will react positive, negative or neutral
'''

def main(session, emotional_value):

    # Init Motion and Tablet naoqi services
    motionService = session.service("ALMotion")
    tabletService = session.service("ALTabletService")

    motionService.wakeUp()
    motionService.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    if tabletService.getBrightness() != 1.0:
        tabletService.setBrightness(1.0)    

    # Switch case for assign the reaction
    if emotional_value <= threshold_1:
        react = reaction3
    elif emotional_value > threshold_1 and emotional_value < threshold_2:
        react = reaction2
    else:
        react = reaction1

    # Perform the reactions according to the react dictionary data
    try:
        t0 = time.time()
        motionService.moveToward(react['X_'], react['Y_'], react['Theta'],
                                    [["MaxVelXY", react['frequency']]])
        tabletService.showImageNoCache(react['img_url'])
        t1 = time.time()
        print "feedback delay ", t1 - t0

        time.sleep(react['time'])
    except Exception, e:
        print "Error was: ", e


    motionService.moveToward(0.0, 0.0, 0.0)
    motionService.waitUntilMoveIsFinished()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.162", # Change the ip to the robot's one
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument('--emovalue', type=int, default=0,
                        help='Emotional predicted value')

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.emovalue)