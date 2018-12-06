#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def callback(msg):
	global minirange
	minirange = min(msg.ranges)


minirange = 1

scan = rospy.Subscriber('scan',LaserScan,callback)
cmd_vel_pub = rospy.Publisher('cmd_vel',Twist,queue_size=5)
rospy.init_node('wander')

go=Twist()

driving_forward = True

rotation_time = rospy.Time.now()
rate = rospy.Rate(50)

while not rospy.is_shutdown() :
	
	if driving_forward:
		if (minirange < 1 or rotation_time < rospy.Time.now()):

			driving_forward = False 
			rotation_time = rospy.Time.now() + rospy.Duration(5)


	else :
		if rospy.Time.now()>rotation_time :

			driving_forward = True
			rotation_time = rospy.Time.now() + rospy.Duration(30)

	go=Twist()


	if driving_forward:
		go.linear.x = 0.5
		go.linear.y = 0
		go.linear.z = 0
		go.angular.x = 0
		go.angular.y = 0
		go.angular.z = 0
	else :
		go.linear.x =0
		go.linear.y = 0
		go.linear.z=0
		go.angular.z = 1
		go.angular.x = 0
		go.angular.y = 0

	cmd_vel_pub.publish(go)
	rate.sleep()




	










