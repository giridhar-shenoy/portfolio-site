## Intro

Bot & Brew was a robotic coffee kiosk I founded and built with two others between August 2025 and February 2026: a six-axis cobot that made a latte from portafilter to latte art without anyone touching it. 

## Video caption

One autonomous cycle, filmed from several angles in January 2026 in our workshop in Fort Kochi; nobody touched the cell during the run. Shown at 2× speed. The full-length version is linked below.

## What the kiosk did

The arm — a six-axis Fairino FR5 cobot with a gripper I designed — ran the whole sequence a barista does: pick up the portafilter, grind and dose, level and tamp, lock the portafilter into the group head, place a cup, pull the shot, hand the cup to a one-axis tilting holder for the pour, fetch the pitcher, steam the milk, swirl out the large bubbles, pour the latte art, drop the pitcher at a cleaning station, collect the cup and deliver it. A touchscreen was to take orders.

The machines were café equipment adapted to run without hands. The espresso machine was a lever press; I fitted a linear actuator and a PID loop on its pressure sensor so it held nine bar through the shot. The milk steamer's manual valves were replaced with electrically operated ones. The gripper, the latte-art holder, the cup and pitcher stations and the cleaning station were custom.

The control architecture was kept deliberately simple. A LubanCat 5 single-board computer ran a Python state machine; its GPIO lines drove relays wired to the machines and to the cobot's digital inputs, where an op-code selected which taught program the arm ran next. There were no cameras and no force sensing: I laid the cell out in a ROS 2 / MoveIt 2 simulation to check that every station was within reach, then hand-taught every position on the real arm and treated the cell as fully deterministic. On any error, everything stopped.

Three of us — a chef, a robotics engineer and I — went from unboxing the arm to the first fully unattended cycle in about two months, bootstrapped. Over its life the kiosk made between thirty and fifty cups, failed attempts included, in a cell about five feet by five. One cycle took roughly eight minutes; nothing had yet been optimised for speed.



## Entrepreneur First

In September 2026 I joined the Entrepreneur First Bangalore cohort to take the idea further and find a new co-founder. After more conversations with customers and advisors I concluded that it is not a venture-scale business, and I left the programme on 1 November 2026.
