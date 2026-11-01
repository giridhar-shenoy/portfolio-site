## Intro

Bot & Brew was a robotic coffee kiosk I founded in August 2025 and built with two others in Fort Kochi: a six-axis cobot that made a latte from portafilter to latte art without anyone touching it. Two months after we unboxed the arm it ran its first fully unattended cycle; the video below is one of those cycles.

## Video caption

One autonomous cycle, edited from several camera angles and shown at 2× speed; nobody touched the cell during the run, and the whole cycle took about eight minutes. Filmed January 2026 in our workshop in Fort Kochi.

## What the kiosk did

The arm — a six-axis Fairino FR5 cobot with a custom gripper we designed inhouse — ran the whole sequence a barista does: pick up the portafilter, grind and dose, level and tamp, lock the portafilter into the group head, place a cup, pull the shot, hand the cup to a one-axis tilting holder for the pour, fetch the pitcher, steam the milk, swirl out the large bubbles, pour the latte art, drop the pitcher at a cleaning station, collect the cup and deliver it. A touchscreen was to take orders.

The machines were café equipment adapted to run without hands. The espresso machine was a lever press; I fitted a linear actuator and a PID loop on its pressure sensor so it held nine bar through the shot. The milk steamer's manual valves were replaced with electrically operated ones. The gripper, the latte-art holder, the cup and pitcher stations and the cleaning station were custom.

The control architecture was kept deliberately simple. A LubanCat 5 single-board computer ran a Python state machine; its GPIO lines drove relays wired to the machines and to the cobot's digital inputs, where an op-code selected which taught program the arm ran next. There were no cameras and no force sensing: I laid the cell out in a ROS 2 / MoveIt 2 simulation to check that every station was within reach, then hand-taught every position on the real arm and treated the cell as fully deterministic. On any error, everything stopped.

Three of us — a chef, a robotics engineer and I — went from unboxing the arm to the first fully unattended cycle in about two months, bootstrapped. Over its life the kiosk made between thirty and fifty cups, failed attempts included, in a cell about five feet by five. One cycle took roughly eight minutes; nothing had yet been optimised for speed.

## How it went

We bootstrapped the whole thing, and by February 2026 the money had run out. I took a job in Kochi leading a small AI team so that I could stay near the workshop, and we kept improving the kiosk in the hours around it. That was not enough: the kiosk got better in small ways but did not move towards something we could put in a café, and over the following months the three of us went our separate ways.

In September 2026 I joined the Entrepreneur First Bangalore cohort to find a new co-founder and build the idea into a company. The conversations there with customers, advisors and investors settled the question. People who tried the kiosk liked it, but the market is too small for venture investment, and I could not make the unit economics of a bootstrapped hardware business work. I left the programme on 1 November 2026 to go back to engineering full time.

## What I take from it

A year of owning a whole machine — mechanical design, actuation, a pressure control loop, the state machine, the cell layout and the arm's programs — with nobody to hand a problem to. A working habit of treating a cell as deterministic, every position taught and every error a full stop, which is why one person could keep it running. And what I would do differently: put sensing in from the start so the cell can recover instead of stopping, and work out the complete business side things before building the hardware.
