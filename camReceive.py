import cv2
import cvzone
import numpy as np
import socket
import struct

UDP_PACKET_SIZE = 65507
PORT = 35100
ADDRESS = '192.168.7.1'

REVERSE_OVERLAY_MODE = 0
DRIVE_CAM_MODE = 1
CAMERA_OFF_MODE = 2

# Return the packet number
def getPacketNum(data):
    return struct.unpack("B", data[0:1])[0]

def getJoystickData(data):
    return struct.unpack("B", data[1:2])[0]

def getPhotoResistorData(data):
    return struct.unpack("B", data[2:3])[0]

def getMode(data):
    return struct.unpack("B", data[3:4])[0]

# Wait for a new frame to be sent over the socket before interpretting data
def waitForNewFrame(socket):
    while True:
        packet = socket.recvfrom(UDP_PACKET_SIZE)[0]
        if getPacketNum(packet) == 1:
            break


def main():
    # Initialize the socket for UDP
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connented = False
    while not connented:
        try:
            receiverSocket.bind((ADDRESS, PORT))
            connented = True
            
        except:
            # print("Error connecting to daCarCam")
            image = cv2.imread("./carcamlines/cameraOff.jpg.png")
            image = addText(image, "Connecting to daCarCam...", 5, 25)
            cv2.imshow('daCarCam',image)
            # If 'q' is press on the keyboard, exit the program
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                receiverSocket.close()
                # print("Exiting daCarCam Viewer")
                return False
            else:
                pass

    # Empty the bytes of the frame and wait for any previous frame to finish
    frame = b''
    waitForNewFrame(receiverSocket)
    isRunning = True

    
    while isRunning:
        # Recieve a pack over the UDP socket
        packet = receiverSocket.recvfrom(UDP_PACKET_SIZE)[0]

        # Add on the packet onto the other packets to form a frame
        frame += packet[4:]
        joystickReading = getJoystickData(packet) - 6
        phototResistorReading =  getPhotoResistorData(packet)
        mode = getMode(packet)

        # On the last packet, show the frame
        if getPacketNum(packet) == 1:
            isRunning = showImage(frame, joystickReading, phototResistorReading, mode)
            frame = b''

    cv2.destroyAllWindows()
    receiverSocket.close()
    print("Exiting daCarCam Viewer")

def showImage(frame, joystickReading, phototResistorReading, mode):
    # Decode the frame into an image
    modeText = ""

    # Mode to display standby
    if mode == CAMERA_OFF_MODE:
        image = cv2.imread("./carcamlines/cameraOff.jpg.png")
        modeText = "Standby Mode"
    # Mode to display the camera image without overlays
    else:
        image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), 1)
        modeText = "Drive Cam Mode"
        if(phototResistorReading < 5):
            image = cv2.convertScaleAbs(image , 1 , 6- (1*phototResistorReading))
    # Mode to display the camera image with the reverse overlay
    if mode == REVERSE_OVERLAY_MODE:
        modeText = "Reverse Cam Mode"
        foreground = cv2.imread('./carcamlines/lines[{}].png'.format(joystickReading), cv2.IMREAD_UNCHANGED)
        image = cvzone.overlayPNG(image, foreground, [0,0])

    image = addText(image, modeText, 5, 25)
    
    # Display the image
    cv2.imshow('daCarCam',image)

    # If 'q' is press on the keyboard, exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    else:
        return True

    
def addText(image, text, x, y):
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    org = (x, y)
    # fontScale
    fontScale = 1
    # White color in BGR
    color = (255, 255, 255)
    # Line thickness of 2 px
    thickness = 2
    # Using cv2.putText() method
    image = cv2.putText(image, text, org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    return image
    
# Tells python to run the main function
if __name__ == "__main__":
    main()
