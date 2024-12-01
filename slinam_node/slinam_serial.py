import rclpy
import serial
import sys
import numpy as np
import struct

from rclpy.node import Node

from geometry_msgs.msg import TwistStamped

class SlinamSerial(Node):

    def __init__(self):
        super().__init__('slinam_serial')
        print("slinam_serial v1.0")
        self.subscription = self.create_subscription(TwistStamped, 
                                                     'cmd_vel', 
                                                     self.twist_to_serial,
                                                     10,
                                                     )

        if not sys.argv[1] and sys.argv[2]:
            print("please enter the port and baud rate as arguments")
            # TODO: look for the ros2 equivalent
            exit()

        port = sys.argv[1]
        baud = sys.argv[2]

        self.serial = serial.Serial(port, baud)
        # self.counter = 0

        # self.serialTimer = self.create_timer(1.0 / 10.0, self.serialCallback)


        # velocity/wheel encoder publisher
        # self.publisher = self.create_publisher(


    def serial_callback(self):
        print("Callback Time!")
        print(self.serial.readline())

    def twist_to_serial(self, msg):
        # this is a differential drive system, so only l_x and a_z is used.
        l_x = np.float32(msg.twist.linear.x)
        a_z = np.float32(msg.twist.angular.z)

        # each float32 is 4 bytes each
        self.serial.write(struct.pack('ff', l_x, a_z))
        print("Twistie time!")
        

def main(args=None):
    rclpy.init(args=args)

    slinam_serial = SlinamSerial()

    while rclpy.ok():
        rclpy.spin_once(slinam_serial)
        slinam_serial.serial_callback();


    rclpy.shutdown()

if __name__ == '__main__':
    main()

