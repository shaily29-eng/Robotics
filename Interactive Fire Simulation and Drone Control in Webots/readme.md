## TOPIC: Interactive Fire Simulation and Drone Control in Webots

#### The Interactive Fire Simulation and Drone Control project in Webots involves simulating a fire scenario with a DJI Mavic 2 Pro drone that can be controlled by varying roll, pitch, yaw angles, and target altitude. The scene is intended to run autonomously from the Webots interface using a Robot node with the supervisor option set to TRUE and with the controller set to '<extern>'.

#### The FireSmoke node is implemented as a Robot node, using two Display nodes for the fire and smoke image. The FireMovement controller manages these nodes using two sprite cheat images to simulate the movement of the fire and smoke in low resolution. However, the fire simulation still needs to consider more realistic aspects such as safe distance and propagation.

#### The safe distance was implemented using a first approach as presented by Butler[1] which defines the safe distance at 4 times the fire's height. The DroneController class achieves the Mavic 2 Pro control by establishing two-way communication with the SimController using an Emitter and Receiver node at each side. The FlightControl class manages all the sensors and actuators of the drone and controls the drone's gimbal and propeller motors using four PID controllers.

#### The drone is equipped with a Camera Node for a 400x240 pixels BGRA channel image over a 3-axis gimbal to smooth the image movement. The image is processed to remove the Alpha channel and keep the BGR channels to be presented during the execution of the sim_controller.py file.

#### Future improvements to the project include the implementation of fire and smoke movement, smoke cloud, and heat propagation.
