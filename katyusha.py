#katyusha, module responsible for doing the physical computations

import math
import logging
import numpy as np
import random

class katyusha:

    def __init__(self, initial_velocity):
        #define some features of the missile
        self.x = [0]#np.array([0])
        self.y = [0]#np.array([0])
        self.vx = [initial_velocity[0]]#np.array([initial_velocity[0]])
        self.vy = [initial_velocity[1]]#np.array([initial_velocity[1]])
        self.ax = []#np.array([0])
        self.ay = []#np.array([0])

        self.dt = 0.001

        #self.burn_rate = 0.1
        self.initial_fuel_mass = 42
        self.shell_mass = 10
        self.rack_length = 5
        self.friction_coefficient = 0.75
        #self.exhaust_velocity = 340

    def burn_rate(self, t):
        #leaves the potential for controllable burn rate, especially for solid fuel
        return(1)

    def exhaust_velocity(self, t):
        #potential for variable exhaust_velocity
        return(2700)

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
        k1 = 0.0363
        k2 = 4*10**-5
        k3 = 10**-5
        bernoulli = k1 * speed ** 2
        stokes = k2 * speed
        skin = k3 * speed ** 1.5
        return(bernoulli + stokes + skin)

    def log(self, data):

        with open("log.txt", "a") as output:
            output.write(str(data) + "\n")

    def writeout(self, content):
        line = ""
        for item in content:
            line += str(item) + ","

        with open("track.csv", "a") as output:
            output.write(line + "\n")

    def launch(self, theta):
        #thrush pushes the projectile along the rack, experiencing friction force which is assumed to be constant.
        #the rack is angled at theta
        self.t = 0
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

            # self.writeout([self.x[-1], self.y[-1], self.vx[-1], self.vy[-1], self.ax[-1], self.ay[-1],
            #                force * math.cos(theta), force*math.sin(theta), self.t])

            #self.log(dist[-1]) #artifacts from testing phase
            self.t += self.dt

        #if the rocket doesn't generate enough thrust, it stays there instead of sinking into the ground'
        if (dist[-1] < self.rack_length):
            print("Launch failed. Not enough thrust to leave the launchpad")


        # del v[0]
        # del dist[0]
        # v = np.array(v)
        # dist = np.array(dist)
        # acceleration = np.array(acceleration)
        # #submit our results to self
        # vx = v * math.cos(theta)
        # vy = v * math.sin(theta)
        # x = dist * math.cos(theta)
        # y = dist * math.sin(theta)
        # ax = acceleration * math.cos(theta)
        # ay = acceleration * math.sin(theta)
        # self.ax = np.concatenate([self.ax, ax])
        # self.ay = np.concatenate([self.ay, ay])
        # self.vx = np.concatenate([self.vx, vx])
        # self.vy = np.concatenate([self.vy, vy])
        # self.x = np.concatenate([self.x, x])
        # self.y = np.concatenate([self.y, y])

        #the rocket has launched the launchpad, now we can consider flight with propulsion
        result = self.propulsion(theta)
        return(result)

    def propulsion(self, theta):
        g = 9.806

        while self.mass(self.t) > self.shell_mass:
            #fuel is not fully burnt
            speed_squared = self.vx[-1]**2 + self.vy[-1]**2
            speed = (speed_squared) ** 0.5

            #first resolve horizontal component
            thrust_x = self.thrust(self.t) * math.cos(theta)
            drag_x = self.drag(speed) * self.vx[-1] / speed
            force_x = thrust_x - drag_x

            #now the vertical component
            thrust_y = self.thrust(self.t) * math.sin(theta)
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

            # self.writeout([self.x[-1], self.y[-1], self.vx[-1], self.vy[-1],
            #                self.ax[-1], self.ay[-1], force_x, force_y, self.t])

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

            self.t += self.dt

        return(self.x[-1], self.y[-1])

    def backpropagation(self, learning_rate=0.000000001, da=0.00001):
        upper = self.miss(self.angle + da)
        lower = self.miss(self.angle - da)
        gradient = (upper - lower) / (2 * da)
        #print(gradient)
        self.angle -= learning_rate * gradient

    def miss(self, theta):
        land = self.launch(theta)
        error = (land[0] - self.target[0]) ** 2
        return(error)

    def train(self, target):
        self.angle = random.random() * math.pi/2
        self.target= target

        benchmark = self.miss(self.angle)#abs(land[0] - target[0])
        print("benchmark: ", benchmark)
        self.backpropagation()

        new_miss = self.miss(self.angle)
        print("new_miss: ", new_miss)

        while new_miss < benchmark:
            benchmark = new_miss
            self.backpropagation()
            new_miss = self.miss(self.angle)
            print("new_miss: ", new_miss)

        return(self.angle)















