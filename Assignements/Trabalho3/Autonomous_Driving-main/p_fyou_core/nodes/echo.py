#!/usr/bin/env python

import math
import time
import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist, PoseStamped
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBot:
    def __init__(self):
        rospy.init_node('p_fyou_DRIVER', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/p_fyou/cmd_vel',Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/gazebo/model_states/',ModelStates, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(60)
        self.goal_pose = Pose()

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data.pose[2]  # search player
        self.pose.position.x = round(self.pose.position.x, 4)
        self.pose.position.y = round(self.pose.position.y, 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.position.x), 2) +pow((goal_pose.y - self.pose.position.y), 2))

    def linear_vel(self, goal_pose, constant=0.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        if constant * self.euclidean_distance(goal_pose) > 0.26:
            return 0.26
        elif constant * self.euclidean_distance(goal_pose) < -0.26:
            return -0.26
        else:
            return constant * self.euclidean_distance(goal_pose)
    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""

        #print (atan2(goal_pose.y - self.pose.position.y, goal_pose.x - self.pose.position.x))
        return atan2(goal_pose.y - self.pose.position.y, goal_pose.x - self.pose.position.x)

    def angular_vel(self, goal_pose, constant=1.2):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        Z_robot = quaternion_to_euler(self.pose.orientation.x, self.pose.orientation.y, self.pose.orientation.z,
                                      self.pose.orientation.w)

        if constant * (self.steering_angle(goal_pose) - Z_robot * math.pi / 180) > 1.0:
            return 1.0
        elif constant * (self.steering_angle(goal_pose) - Z_robot * math.pi / 180) < -1.0:
            return -1.0
        else:
            return constant * (self.steering_angle(goal_pose) - Z_robot * math.pi / 180)




    def update_goal(self,data):
        self.goal_pose.x = data.pose.position.x
        self.goal_pose.y = data.pose.position.y

    def direction(self, data):
        print('!!!!!! Novo objectivo !!!!!!')
        x.pose_subscriber = rospy.Subscriber('/gazebo/model_states/',ModelStates, x.update_pose)
        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        # Goal
        """Moves the turtle to the goal."""
        # goal_pose = Pose()
        self.goal_pose.x = data.pose.position.x
        self.goal_pose.y = data.pose.position.y

        # create the message for send
        vel_msg = Twist()
        Orientation = quaternion_to_euler(self.pose.orientation.x, self.pose.orientation.y, self.pose.orientation.z,
                                          self.pose.orientation.w)
        while self.euclidean_distance(self.goal_pose) >= 0.2:

            Orientation = quaternion_to_euler(self.pose.orientation.x, self.pose.orientation.y, self.pose.orientation.z,
                                              self.pose.orientation.w)

            vel_msg.linear.x = self.linear_vel(self.goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(self.goal_pose)
            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            # Publish at the desired rate.
            self.rate.sleep()
        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)


def quaternion_to_euler(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.degrees(math.atan2(t0, t1))
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.degrees(math.atan2(t3, t4))
    return Z


if __name__ == '__main__':
    try:
        x = TurtleBot()
        rospy.Subscriber("move_base_simple/goal", PoseStamped, x.direction)  # subscribe gazebo/model_states
        rospy.spin()

    except rospy.ROSInterruptException:
        pass



