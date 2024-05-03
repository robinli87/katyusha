# katyusha
Models the trajectory of a self-propelled missile after launch. Takes into consideration drag, change in atmospheric pressure, angle of attack and varying thrust output. 

There are 3 stages of fllight:
1. On the launch rack. The rocket accelerates along the direciton of the rack, subject to friction, air resistance and a diagonal component of weight.
2. Flight with propulsion. The rocket aims at the original direction specified by the rack but its actual velocity is no longer parallel. The rocket is accelerating.
3. Flight without propulsion. After the fuel has been burnt out, the rocket is essentially a ballistic missile.

run main.py to generate results on the trajectory.
run plotter2.py for a realistic plot and animation!
run all_trajectories.py to see trajectory from all angles of launch!
run aiming.py to compute the loss at each angle for you to decide the best angle of launch!

It turns up that semi ballistic missiles are too sensitive to initial launch angle if we want to hit distant targets accurately. Therefore, we need homing system for long ranges. For short range with air resistance, the idea of stochastic gradient descent works well to find an initial angle.

Physical effects considered:
Drag: Form Drag, Stokes Drag and Skin Friction
Fuel burning and mass changes
Specific impulse

To be improved on:
1. Variable burn rate controls
2. Varying air pressure, density and viscosity with altitude
3. Find the angle of launch required to hit a target at (x,y)
4. Consider the Earth as a sphere and metric distortions (e.g Schwarzschild Metric).

Somebody can write a GUI front end for this, and clean up the code structure a bit :D

Works well for medium ranges.

The scenarios of long ranges need a separate project - guided rockets with homing system and awareness of current position.
