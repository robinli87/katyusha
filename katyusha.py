#katyusha, module responsible for doing the physical computations

import math
import logging
import numpy as np
import random

class katyusha:

    def __init__(self, initial_velocity=[0, 0],
                 initial_fuel_mass = 630,
                 shell_mass = 20,
                 rack_length = 5,
                 friction_coefficient = 0.75,
                 dt=0.001,
                 target=[0, 0]):
        #define some features of the missile


        self.dt = dt

        #self.burn_rate = 0.1
        self.initial_fuel_mass = initial_fuel_mass
        self.shell_mass = shell_mass
        self.rack_length = rack_length
        self.friction_coefficient = friction_coefficient
        self.target = target
        #self.exhaust_velocity = 340

    def burn_rate(self, t):
        #leaves the potential for controllable burn rate, especially for solid fuel
        return(40)

    def exhaust_velocity(self, t):
        #potential for variable exhaust_velocity
        return(2100)

    def thrust(self, t):
        #leaves the potential for programmable thrust
        return(self.burn_rate(t) * self.exhaust_velocity(t))

    def mass(self, t):
        fuel_burnt = self.burn_rate(t) * t
        if fuel_burnt < self.initial_fuel_mass:
            #if we have not burnt up all of our fuel
            m = self.initial_fuel_mass + self.shell_mass - fuel_burnt
            return(m)
        else:
            #fuel has been exhausted, we are left with just a shell
            return(self.shell_mass)

    def drag(self, speed):
        k1 = 0.0363 * math.exp(-self.y[-1] / 5000)
        k2 = 4*10**-5 * math.exp(-self.y[-1] / 5000)
        k3 = 10**-5 * math.exp(-self.y[-1] / 5000)
        bernoulli = k1 * speed ** 2
        stokes = k2 * speed
        skin = k3 * speed ** 1.5
        return(bernoulli + stokes + skin)

    def log(self, data):

        with open("log.txt", "a") as output:
            output.write(str(data) + "\n")

    def writeout(self, content):
        length = len(content[0])-1
        with open("track.csv", "a") as output:

            for i in range(0, length):
                line = ""
                for j in range(0, len(content)):
                    line += str(content[j][i]) + ","

                output.write(line + "\n")

    def launch(self, theta, initial_velocity=[0, 0], log=False):
        #thrush pushes the projectile along the rack, experiencing friction force which is assumed to be constant.
        #the rack is angled at theta
        self.x = [0]#np.array([0])
        self.y = [0]#np.array([0])
        self.vx = [initial_velocity[0]]#np.array([initial_velocity[0]])
        self.vy = [initial_velocity[1]]#np.array([initial_velocity[1]])
        self.ax = []#np.array([0])
        self.ay = []#np.array([0])
        self.t = 0
        self.phi = [theta]
        self.angular_velocity = [0]
        dist = 0
        v = [0]
        acceleration = []
        dist = [0]
        #g = self.g(0)
        g = 9.806

        #resolve forces in the rotated diagonal frame of the rack surface
        geometric_factor = self.friction_coefficient * math.cos(theta) + math.sin(theta)

        while (dist[-1] <= self.rack_length) and (self.mass(self.t) > self.shell_mass):

            force = self.thrust(self.t) - self.mass(self.t) * g * geometric_factor - self.drag(v[-1])

            a = force / self.mass(self.t)
            acceleration.append(a) #this is the acceleration in the rack frame
            self.ax.append(a * math.cos(theta))
            self.ay.append(a * math.sin(theta))

            v.append(v[-1] + acceleration[-1] * self.dt)
            if v[-1] < 0:
                v[-1] = 0
            self.vx.append(v[-1] * math.cos(theta))
            self.vy.append(v[-1] * math.sin(theta))

            dist.append(dist[-1] + (v[-1] + v[-2]) * 0.5*self.dt + 0.5 * acceleration[-1] * self.dt ** 2)
            if dist[-1] < 0:
                dist[-1] = 0
            self.x.append(dist[-1] * math.cos(theta))
            self.y.append(dist[-1] * math.sin(theta))

            self.phi.append(theta)
            self.angular_velocity.append(0)

            #self.log(dist[-1]) #artifacts from testing phase
            self.t += self.dt

        #if the rocket doesn't generate enough thrust, it stays there instead of sinking into the ground'
        if (dist[-1] < self.rack_length):
            print("Launch failed. Not enough thrust to leave the launchpad")

        #the rocket has left the launchpad, now we can consider flight with propulsion
        #note down the results

        result = self.propulsion(theta)
        duration = len(self.ax)

        if log == True:
            self.writeout([self.x, self.y, self.vx, self.vy, self.ax, self.ay])

        #print(self.t)

        return(result)

    def propulsion(self, theta):
        g = 9.806


        self.rocket_length = 5
        self.shift = -self.t / 10

        global k5
        global k4
        k5 = 10**-5
        k4 = 40


        while self.mass(self.t) > self.shell_mass:
            #fuel is not fully burnt
            speed_squared = self.vx[-1]**2 + self.vy[-1]**2
            speed = (speed_squared) ** 0.5

            #first resolve horizontal component
            thrust_x = self.thrust(self.t) * math.cos(self.phi[-1])
            drag_x = self.drag(speed) * self.vx[-1] / speed
            force_x = thrust_x - drag_x

            #now the vertical component
            thrust_y = self.thrust(self.t) * math.sin(self.phi[-1])
            drag_y = self.drag(speed) * self.vy[-1] / speed
            weight_y = self.mass(self.t) * g
            force_y = thrust_y - drag_y - weight_y

            # diagonal = self.thrust(self.t) - self.drag(speed)
            #
            # force_x = diagonal * (self.vx[-1]) / speed
            # force_y = diagonal * (self.vy[-1]) / speed - self.mass(self.t) * g

            self.ax.append(force_x / self.mass(self.t))
            self.ay.append(force_y / self.mass(self.t))

            self.vx.append(self.vx[-1]+ self.ax[-1] * self.dt)
            self.vy.append(self.vy[-1] + self.ay[-1] * self.dt)

            dx = 0.5*(self.vx[-1] + self.vx[-2]) * self.dt + 0.5 * self.ax[-1] * self.dt ** 2
            self.x.append(self.x[-1] + dx)

            dy = 0.5*(self.vy[-1] + self.vy[-2]) * self.dt + 0.5 * self.ay[-1] * self.dt ** 2
            self.y.append(self.y[-1] + dy)

            #consider rotational effects due to centre of mass deviation
            sin_alpha = ((self.vx[-1] + self.vx[-2]) * math.sin(self.phi[-1])/ speed - (self.vy[-1] + self.vy[-2]) * math.cos(self.phi[-1]) / speed)
            torque = k4 * speed_squared * sin_alpha * self.shift - k5 * self.rocket_length * self.angular_velocity[-1]**2
            I = self.mass(self.t) * self.rocket_length**2 / 24
            angular_acc = torque / I
            self.angular_velocity.append(self.angular_velocity[-1] + self.dt * angular_acc)
            self.phi.append(self.phi[-1] + self.angular_velocity[-1] * self.dt + angular_acc * 0.5 * self.dt**2)

            self.t += self.dt

        result = self.ballistic()
        return(result)


    def ballistic(self, target=[0,0]):
        g = 9.806
        target_altitude = target[1]

        while self.y[-1] > target_altitude:
            speed_squared = self.vx[-1]**2 + self.vy[-1]**2
            speed = (speed_squared) ** 0.5

            force_x = -self.drag(speed) * self.vx[-1] / (speed * self.mass(self.t))
            self.ax.append(force_x / self.mass(self.t))
            force_y = -self.drag(speed) * self.vy[-1] / speed - self.mass(self.t) * g
            self.ay.append(force_y / self.mass(self.t))

            self.vx.append(self.ax[-1] * self.dt + self.vx[-1])
            self.vy.append(self.ay[-1] * self.dt + self.vy[-1])

            self.x.append(self.x[-1] + self.vx[-1] * self.dt + self.ax[-1]*0.5* self.dt**2)
            self.y.append(self.y[-1] + self.vy[-1] * self.dt + self.ay[-1]*0.5* self.dt**2)
            #
            # self.writeout([self.x[-1], self.y[-1], self.vx[-1], self.vy[-1],
            #                self.ax[-1], self.ay[-1], force_x, force_y, self.t])

            sin_alpha = ((self.vx[-1] + self.vx[-2]) * math.sin(self.phi[-1])/ speed - (self.vy[-1] + self.vy[-2]) * math.cos(self.phi[-1]) / speed)
            torque = k4 * speed_squared * sin_alpha * self.shift - k5 * self.rocket_length * self.angular_velocity[-1]
            I = self.mass(self.t) * self.rocket_length**2 / 24
            angular_acc = torque / I
            self.angular_velocity.append(self.angular_velocity[-1] + self.dt * angular_acc)
            self.phi.append(self.phi[-1] + self.angular_velocity[-1] * self.dt + angular_acc * 0.5 * self.dt**2)

            self.t += self.dt

        return(self.x[-1], self.y[-1])

    def backpropagation(self, learning_rate=10**-9, da=0.000001):
        anglecopy = self.angle
        upper = self.miss(anglecopy + da)
        lower = self.miss(anglecopy - da)
        gradient = (upper - lower) / (2 * da)
        #print(gradient)
        #modifier = learning_rate * gradient * math.exp(-self.epoch/ 10)
        if gradient > 0:
            self.angle -= 0.01 * math.exp(-self.epoch / 10)
        elif gradient <0:
            self.angle += 0.01 * math.exp(-self.epoch / 10)

    def miss(self, theta):
        land = self.launch(theta)
        error = (land[0] - self.target[0]) ** 2 + (land[1] - self.target[1])**2
        #need to damp the error to within a reasonable range
        return(error)

    def train(self, target):

        # stochastic gradient descent fails for extreme training. We need an alternative method, e.g. reward training.
        self.angle = math.pi / 4
        self.target= target
        self.epoch = 0

        benchmark = self.miss(self.angle)#abs(land[0] - target[0])
        print("benchmark: ", benchmark)
        self.backpropagation()

        new_miss = self.miss(self.angle)
        print("new_miss: ", new_miss)

        while new_miss > 5:
            benchmark = new_miss
            self.backpropagation()
            new_miss = self.miss(self.angle)
            print("new_miss: ", new_miss)
            print("angle: ", self.angle)
            self.epoch += 1

        return(self.angle)















