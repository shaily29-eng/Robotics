## Webots Planar Flying Robot

#### Webots Planar Flying Robot is a simulation of the DJI-Mavic Pro Quadcopter using Webots. It's a project that lets you control the quadcopter's motion based on a set of present and target coordinates in 3D space.

#### When the present and target coordinates lie on the ground plane, the quadcopter moves in a semi-circular trajectory in the altitude space, which is about a center that's also on the ground plane. This is achieved by using the parametric form of a circle, centered at the average of the present and target, (x,z) coordinates. The time it takes the quadcopter to move along this semi-circular path can be controlled by the variable 'n,' which represents the number of time steps.

#### The quadcopter moves along the arc of the semi-circle in small steps defined by the angle subtended by the radius at the present coordinates, with the radius at the target coordinates. The quadcopter sweeps a full semicircle from 180 degrees to 0 degrees and all this is done using a PID controller

#### The plotted path can be seen using the matplotlib library. Overall, the Webots Planar Flying Robot project is a great way to learn about controlling a quadcopter's motion using PID controllers and how it can move along a semi-circular trajectory.
