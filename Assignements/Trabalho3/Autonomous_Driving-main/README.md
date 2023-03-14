
# PARI 2020/2021 - Job number 3

## Part 1-MANUAL RACE :trophy:

### **Furious speed in the world of Robotics**

The Filipe You Robot, personalized and able to burn tyre on any road is the best bet in this race.  

The challenge of Filipe You is to ride the simulated track in Gabezo in the shortest time possible using manual driving.
 
![fyou](https://github.com/samuelf98/Trabalho3_PARI/blob/main/img/pfyou.png)

#### Procedure
* Opening of Gazebo (race track);
```py
roslaunch p_fyou_bringup bringup_gazebo.launch
```
* RVIZ;
```py
roslaunch p_fyou_bringup visualize.launch
```

* Robot launch from the terminal through the file **spawn.launch**, where you can put the name of the robot and select the desired colour (you can enter more than one Robot in the track);

```py
Ex:roslaunch p_fyou_bringup spawn.launch  player_name:=Beer player_color:=White
```
![multiobos](https://github.com/samuelf98/Trabalho3_PARI/blob/main/img/double.png)

* Automatic driving using the **teleop** and using the **ROS controller** for setting parameters such as maximum speed or acceleration;

```py
roslaunch p_fyou_bringup teleop.launch player_name:=Beer
```

```py
Moving around:
        w
   a    s    d
        x
        
w/x : increase/decrease linear velocity (Burger : ~ 0.22, Waffle and Waffle Pi : ~ 0.26)
a/d : increase/decrease angular velocity (Burger : ~ 2.84, Waffle and Waffle Pi : ~ 1.82)

space key, s : force stop

CTRL-C to quit
        
```
* Extra

In order to optimise driving you use the image the robot is viewing:

```py
rosrun image_view image_view image:=//p_fyou/camera/rgb/image_raw
```
![multiobos](https://github.com/samuelf98/Trabalho3_PARI/blob/main/img/pista.png)

***
## Part 2-Autonomous Driving

### **Follows the destination**:arrow_lower_left::arrow_lower_right::arrow_upper_left::arrow_upper_right::arrow_up::arrow_down::arrow_left::arrow_right:

In this part, Filipe You aims to "pursue" the arrows imposed by the user on the RVIZ, thus tracing its destination.

![goal](https://github.com/samuelf98/Autonomous_Driving/blob/main/img/goal.png)

#### Procedure
* Opening of Gazebo (house);
```py
roslaunch p_fyou_bringup bringup_gazebo.launch
```

* RVIZ;
```py
roslaunch p_fyou_bringup visualize.launch
```

* Robot launch from the terminal through the file **spawn.launch**;

```py
Ex:roslaunch p_fyou_bringup spawn.launch  
```

* Destination and new Goal

On the rviz, the 2D Nav Goal 
will launch the destination of the robot, which must be able to adapt to what is proposed to it

```py
Ex:rosrun p_fyou_core player.py 
```
## Part 3-Team Hunt

### **Hunting between robots: Which is the best to run away and pursue?**

The mission of the robot is to hunt a robot with a different colour than yours and in turn run away from a robot with another distinct colour. For example: if the robot is green, it hunts blue and runs away from red.

#### Procedure
* Gazebo opening and launching of multiple robots
```py
 roslaunch p_fyou_bringup game_spawn.launch
```
This control allows the gazebo to be opened and launches the various robots with the predefined colours

![robots](https://github.com/samuelf98/Autonomous_Driving/blob/main/img/robots.png)

* Launch file that allows the pursuit

The robots move when the launch file is launched in the terminal via the command:

```py
roslaunch p_fyou_bringup robots.launch
```

Each team knows who to run from and who to pursue. And the question is who will win this hunt?

A referee knot has been implemented which dictates the scores obtained by each team. The knot is thrown in the terminal with the command: 

```py
rosrun th_referee th_referee
```

Whenever the robot is hunted it is retained for a while in the central square of the arena, returning later to the game. 

![box](https://github.com/samuelf98/Autonomous_Driving/blob/main/img/box.png)

While the game is running, it is possible to view what is happening by text. In the terminal you insert:

```py
rqt_console
```
rqt allows you to choose the messages you want to exclude and those you want to see for each robot.

In the upper part of the window you can see the messages like for example:
```py
nothing if there are no obstacles
flee if you're running from the robot
chase if you are in pursuit
right if you turn right
left if you turn left
```

At the end of the hunt, the score obtained by each team appears in the terminal, for example:
```py
Team scores:
+-------+-----------+-------------+
|  Team | Raw Score | Final Score |
+-------+-----------+-------------+
|  blue |     0     |      0      |
| green |     -4    |      -4     |
|  red  |     4     |      9      |
+-------+-----------+-------------+
Game time: 80.009 out of 80
Game Over! Team Red wins!!!
```

***
Practical work of the Automation and Industrial Robotics Design unit, Integrated Master in Mechanical Engineering, University of Aveiro

Alex Valadares, Rita Correia and Samuel Ferreira
