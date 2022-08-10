#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
import board
import busio
import adafruit_pca9685

i2c = busio.I2C(board.SCL,board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 1000
right_outer = pca.channels[7]
right_inner = pca.channels[8]

turning = False

mostRecentRightData = -1
mostRecentLeftData = -1

def callback(data):
    global turning
    global mostRecentLeftData
    global mostRecentRightData
    rospy.loginfo(data.data)
    mostRecentRightData = data.data
    
    if mostRecentRightData != -1 and mostRecentLeftData != -1: # if these have been initialized
        # if either is less than 2^15 while the other is greater than 2^15, turning is True
        turning = (mostRecentRightData - 32768 > 0 and mostRecentLeftData - 32768 < 0) or (mostRecentRightData - 32768 < 0 and mostRecentLeftData - 32768 > 0)
    
    if turning:
        right_outer.duty_cycle = int(data.data/(4/3))+8192
        right_inner.duty_cycle = int(data.data/(4/3))+8192
        #right_inner.duty_cycle = int((((data.data-32768)*.793)+32768)/(4/3))+8192
    else:
        right_outer.duty_cycle = int(data.data/(4/3))+8192
        right_inner.duty_cycle = int(data.data/(4/3))+8192
        
def leftCallback(leftData):
    global turning
    global mostRecentLeftData
    #rospy.loginfo(leftData.data)
    mostRecentLeftData = leftData.data
    
    #if mostRecentRightData != -1 and mostRecentLeftData != -1: # if these have been initialized
        # if either is less than 2^15 while the other is greater than 2^15, turning is True
        #turning = (mostRecentRightData - 32768 > 0 and mostRecentLeftData - 32768 < 0) or (mostRecentRightData - 32768 < 0 and mostRecentLeftData - 32768 > 0)

def right_wheels():

    rospy.init_node('right_wheels')
    rospy.Subscriber('right_wheels', Int32, callback)
    rospy.Subscriber('left_wheels', Int32, leftCallback)
    rospy.spin()

if __name__ == '__main__':
    right_wheels()
