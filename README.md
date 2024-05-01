# katyusha
Models the trajectory of a self-propelled missile after launch. Takes into consideration drag, change in atmospheric pressure, angle of attack and varying thrust output. 

There are 3 stages of fllight:
1. On the launch rack. The rocket accelerates along the direciton of the rack, subject to friction, air resistance and a diagonal component of weight.
2. Flight with propulsion. The rocket aims at the original direction specified by the rack but its actual velocity is no longer parallel. The rocket is accelerating.
3. Flight without propulsion. After the fuel has been burnt out, the rocket is essentially a ballistic missile.

run main.py to generate results on the trajectory.
run plotter2.py for a realistic plot and animation!

Physical effects considered:
Drag: Form Drag, Stokes Drag and Skin Friction
Fuel burning and mass changes
Specific impulse

To be improved on:
1. Considerations of rotation in flight
2. Varying air pressure, density and viscosity with altitude
3. Find the angle of launch required to hit a target at (x,y)
