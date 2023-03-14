#!/usr/bin/env python2
# coding=utf-8

#imports
import math
from copy import deepcopy

import cv2
import numpy as np
import tf2_geometry_msgs
import rospy
import tf2_ros
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import Image


class TurtleBot():
    """
    A class used to Control a robot do a desired goal by using  the  “2D_NavGoal” from RVIZ

    ...
    Attributes
    ----------

self.name: str
        the name of the node
self.odom_frame : str
        a formatted string
self.velocity_publisher
	publihes velocity
self.goal_subscriber
self.goal_pose
	Goal of the robot ( initialized as None)
self.move_forward: Boolean
	False
self.base_footprint_frame: str
	a formatted sting
self.tf_buffer
	tf2_ros.Buffer()

    Methods
    -------
Timereceived (event)
	This function verifies if there is a previous goal set
direction(data)
	Initiates a new goal
distance_cal(goal_in_base_link)
	Calculates a distance between the base link and the goal
angle_cal(goal)
	Calculates de angle to reach the goal
def drive(goal):
	Driver of the program where the goal is copied and transformed
    """

    def __init__(self,name):
        self.name=name
        self.node_init=rospy.init_node('Robot_Send', anonymous=True)
        self.odom_frame='p_fyou/odom'
        self.velocity_publisher = rospy.Publisher('/p_fyou/cmd_vel',Twist, queue_size=10)
        self.goal_subscriber=rospy.Subscriber("move_base_simple/goal", PoseStamped, self.direction)  # subscribe gazebo/model_states
        self.goal_pose = None
        self.move_forward=False
        self.base_footprint_frame='p_fyou/base_footprint'
        self.tf_buffer=tf2_ros.Buffer()
        self.tf_listner = tf2_ros.TransformListener(self.tf_buffer)
        self.timer=rospy.Timer(rospy.Duration(0.1), self.timereceived)
        self.my_team = None
      
        # Defining teams
        # name = rospy.get_name().strip('/')
        # names_red = rospy.get_param('/red_players')
        # names_green = rospy.get_param('/green_players')
        # names_blue = rospy.get_param('/blue_players')
        # self.myteam = None
        # self.prey_team_players = None
        # self.hunter_team_players = None
        #
        # if name in names_red:
        #     self.myteam = "red"
        #     self.prey_team_players = names_green
        #     self.hunter_team_players = names_blue
        #
        # elif name in names_green:
        #     self.myteam = "green"
        #     self.prey_team_players = names_blue
        #     self.hunter_team_players = names_red
        #
        # elif name in names_blue:
        #     self.myteam = "blue"
        #     self.prey_team_players = names_red
        #     self.hunter_team_players = names_green
        #
        # else:
        #     rospy.logerr('Something is wrong')
        # print("My name is " + self.name + ". I am team " + str(self.myteam) + " huntig " + str(
        #     self.prey_team_players) + " and fleeing from " + str(self.hunter_team_players))


    def timereceived(self,event):
        """ This function verified if goal was set"""
        if not self.goal_pose is None:
            self.drive(self.goal_pose)


    def direction(self, data):
        """Set to new goal"""
        self.move_forward=True
        print('!!!!!! Novo objectivo !!!!!!')
        self.goal_pose=self.tf_buffer.transform(data,self.odom_frame,rospy.Duration(1))

    def distance_cal(self,goal_in_base_link):
        """calculate distance between base link and goal"""
        d=math.sqrt(goal_in_base_link.pose.position.x ** 2 + goal_in_base_link.pose.position.y ** 2)
        return  d

    def angle_cal(self,goal):
        """calculate the angle"""
        angle=math.atan2(goal.pose.position.y, goal.pose.position.x)
        return angle


    def drive(self, goal):
        """Driver of the program where the goal is copied and transformed """
        #rospy.Subscriber("/p_fyou/camera/rgb/image_raw", Image,self.Image_GET())

        goal_pose = goal
        goal_copy = deepcopy(goal_pose)
        goal_copy.header.stamp = rospy.Time.now()
        goal_in_base_link = self.tf_buffer.transform(goal_copy, self.base_footprint_frame, rospy.Duration(1))

        angle=self.angle_cal(goal_in_base_link)
        distance=self.distance_cal(goal_in_base_link)

        vel_msg = Twist()

        #define velocities
        if distance >= 0.2 and self.move_forward==True:
            # Robot position
            vel_msg.linear.x = distance*0.2 #change constant value to change linear velocity
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = angle #add a contant to change the angular velocity
            self.velocity_publisher.publish(vel_msg)
        else:
            # Stopping our robot after the movement is over.
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)



def main():
    """Create object from the class TurtleBot"""
    player = TurtleBot(name="p_fyou")
    rospy.spin()


if __name__=='__main__':
    main()
