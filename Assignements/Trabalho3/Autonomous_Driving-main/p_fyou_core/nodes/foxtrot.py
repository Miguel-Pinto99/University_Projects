#!/usr/bin/env python2

import math
import time
import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist, PoseStamped, Pose
from math import pow, atan2, sqrt

class TurtleBot:
    def __init__(self):
        rospy.init_node('Robot_Send', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/p_fyou/cmd_vel',Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/gazebo/model_states/',ModelStates, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(60)
        self.goal_pose = Pose()
        self.move_forward=False




    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data.pose[2]  # search player name
        self.pose.position.x = round(self.pose.position.x, 4)
        self.pose.position.y = round(self.pose.position.y, 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.position.x - self.pose.position.x), 2) + pow((goal_pose.position.y- self.pose.position.y), 2))

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

        return atan2(goal_pose.position.y - self.pose.position.y, goal_pose.position.x - self.pose.position.x)


    def angular_vel(self, goal_pose, constant=1.2):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        Z_robot = round(quaternion_to_euler(self.pose.orientation.x, self.pose.orientation.y, self.pose.orientation.z,self.pose.orientation.w),4)
        print(self.steering_angle(goal_pose))
        if constant * (self.steering_angle(goal_pose) - Z_robot * math.pi / 180) > 1.0:
            return 1
        elif constant * (self.steering_angle(goal_pose) - Z_robot * math.pi / 180) < -1.0:
            return -1
        else:
            return constant * (self.steering_angle(goal_pose) - Z_robot * math.pi / 180)

    def update_goal(self,data):
        self.goal_pose.position.x = data.pose.position.x
        self.goal_pose.position.y = data.pose.position.y

    def direction(self, data):
        self.move_forward=True
        print('!!!!!! Novo objectivo !!!!!!')
        self.pose_subscriber = rospy.Subscriber('/gazebo/model_states/',ModelStates, self.update_pose)

        """Moves the turtle to the goal."""
        self.goal_pose.position.x = data.pose.position.x
        self.goal_pose.position.y = data.pose.position.y


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

def main():
    my_robot = TurtleBot()
    rospy.Subscriber("move_base_simple/goal", PoseStamped, my_robot.direction)  # subscribe gazebo/model_states
    while not rospy.is_shutdown():



        vel_msg = Twist()
        Orientation = quaternion_to_euler(my_robot.pose.orientation.x, my_robot.pose.orientation.y, my_robot.pose.orientation.z,
                                          my_robot.pose.orientation.w)

        if my_robot.euclidean_distance(my_robot.goal_pose) >= 0.2 and my_robot.move_forward==True:
            # Robot position
            Orientation = quaternion_to_euler(my_robot.pose.orientation.x, my_robot.pose.orientation.y, my_robot.pose.orientation.z,
                                              my_robot.pose.orientation.w)

            vel_msg.linear.x = my_robot.linear_vel(my_robot.goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = my_robot.angular_vel(my_robot.goal_pose)
            # Publishing our vel_msg
            my_robot.velocity_publisher.publish(vel_msg)
            # Publish at the desired rate.
            my_robot.rate.sleep()
        else:
            # Stopping our robot after the movement is over.
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            my_robot.velocity_publisher.publish(vel_msg)

        #rospy.spin()


if __name__ == '__main__':
    main()