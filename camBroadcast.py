import cv2
import socket
import math
import struct
import joystickModule as joystick
import photoResistorModule as photoResistor
import buttonModule as button

# max payload for IPv4 UDP packet in bytes
UDP_PACKET_SIZE = 65507
#we use first byte of data to store the number of samples
FRAME_DATA_SIZE = UDP_PACKET_SIZE - 4
PORT = 35100
ADDRESS = "192.168.7.1"


def encodeAndSendImage(socket, image, mode):

    #Encode the image as a jpeg
    encodedImage = cv2.imencode('.jpg', image)[1]
    #convert the encoded image to a string
    encodedData = encodedImage.tostring()



    #Find the size of the data to determine the number of UDP packets
    sizeOfData = len(encodedData)
    numPackets = math.ceil(sizeOfData / FRAME_DATA_SIZE)
    joystickY = joystick.joystickYInterpolated()
    photoResistorVal = photoResistor.PhotoResistor_getVoltage()
    #Send UDP packets over the socket with the first byte of the data being the packet number
    #Second byte is the joystick reading, third byte is the photoresistor Value and 
    #The fourth byte is the mode. The rest of the data is the bytesof the image
    startIndex = 0
    for numPackets in range (numPackets, 0, -1):
        endIndex = startIndex + FRAME_DATA_SIZE
        try:
            socket.sendto(struct.pack("B", numPackets) + struct.pack("B", joystickY) + struct.pack("B", photoResistorVal) + struct.pack("B", mode) + encodedData[startIndex:endIndex], (ADDRESS, PORT))
        except:
            print("Error sending packet")
        startIndex = endIndex


def main():
    # initialize the socket (UDP)
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    mode = 0

    # Capture the camera image and send it over the socket
    capturedImage = cv2.VideoCapture(0)

    prevButtonState = button.Tactile_isRedPressed()

    # While the camera is still running send data through the socket
    while (capturedImage.isOpened()):
        imageRead = capturedImage.read()[1]
        ButtonState = button.Tactile_isRedPressed()
        if(ButtonState != prevButtonState):
            if(ButtonState == True):
                mode = (mode + 1) % 3
            prevButtonState = ButtonState

        encodeAndSendImage(senderSocket,imageRead, mode)
        

    # Stop sending packets
    capturedImage.release()
    cv2.destroyAllWindows()
    socket.close()

# Tells python to run the main function
if __name__ == "__main__":
    main()