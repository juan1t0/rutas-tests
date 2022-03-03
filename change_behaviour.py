import qi
import argparse
import sys
import time

reaction1 = {'status': 'positive', 'img_url': 'https://raw.githubusercontent.com/juan1t0/rutas_probes/main/reaction1.png',
                'X_': 0.8, 'Y_': 0.0, 'Theta': 0.0,
                'frequency':0.5, 'time': 5}
reaction2 = {'status': 'neutral', 'img_url': 'https://raw.githubusercontent.com/juan1t0/rutas_probes/main/reaction2.png',
                'X_': 0.3, 'Y_': 0.0, 'Theta': 0.0,
                'frequency':0.2, 'time': 8}
reaction3 = {'status': 'negative', 'img_url': 'https://raw.githubusercontent.com/juan1t0/rutas_probes/main/reaction3.png',
                'X_': -0.45, 'Y_': 0.0, 'Theta': 0.0,
                'frequency':0.3, 'time': 5}

# thresholds are set in +3 and -2
threshold_1 = -2
threshold_2 = 3

def main(session, emotional_value):
    motionService = session.service("ALMotion")
    tabletService = session.service("ALTabletService")

    motion_service.wakeUp()
    motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    if emotional_value <= -2:
        react = reaction3
    elif emotional_value > -2 and emotional_value < 3:
        react = reaction2
    else:
        react = reaction1

    try:
        motion_service.moveToward(react['X_'], react['Y_'], react['Theta'],
                                    [["MaxVelXY", react['frequency']]])
        tabletService.showImageNoCache(react['img_url'])
        
        time.sleep(react['time'])
    except Exception, e:
        print "Error was: ", e

    tabletService.hideImage()
    motion_service.moveToward(0.0, 0.0, 0.0)
    motion_service.waitUntilMoveIsFinished()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.162",
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