import numpy as np
import cv2
import random
import matplotlib.animation as ani
from matplotlib import pyplot as plt


class Animator:
    grid = None
    robot_res = 50

    def __init__(self):
        robot_img = cv2.imread('animation/static/robot.png')
        self.robot = cv2.resize(robot_img, (self.robot_res, self.robot_res),
                                interpolation=cv2.INTER_LINEAR)
        item_img = cv2.imread('animation/static/package.png')
        self.item = cv2.resize(item_img, (self.robot_res, self.robot_res))
        truck_img = cv2.imread('animation/static/truck.png')
        self.truck = cv2.resize(truck_img, (self.robot_res, self.robot_res))

    def create_grid(self, fig, state):
        ax = fig.gca()
        ax.set_xticks(np.arange(0, state.x*self.robot_res, self.robot_res))
        ax.set_yticks(np.arange(0, state.y*self.robot_res, self.robot_res))
        ax.set_xlim([0, state.x*self.robot_res])
        ax.set_ylim([0, state.y*self.robot_res])
        plt.grid()
        plt.imshow(cv2.cvtColor(self.truck, cv2.COLOR_BGR2RGB),
                   extent=[state.x//2 * self.robot_res,
                           (state.x//2 + 1) * self.robot_res,
                           state.y//2 * self.robot_res,
                           (state.y//2+ 1) * self.robot_res])
        return ax

    def run(self, state, routing):
        fig = plt.figure()
        self.grid = self.create_grid(fig, state)

        interval=100
        ims = []
        for i in range(interval):
            state.move_random()
            ims.append(self.animate(state))

        animator = ani.ArtistAnimation(fig, ims, interval=180, repeat=False, repeat_delay=1000)
        plt.show()

    def run_routing(self,state, routing):
        fig = plt.figure()
        self.grid = self.create_grid(fig, state)

        ims = []
        for change in routing:
            state.apply(change)
            ims.append(self.animate(state))

        animator = ani.ArtistAnimation(fig, ims, interval=300, repeat=False,
                                       repeat_delay=1000)
        plt.show()


    def animate(self, state):
        images = []
        for robot_x, robot_y in state.robot_pos:
            images.append(plt.imshow(cv2.cvtColor(self.robot, cv2.COLOR_BGR2RGB),
                         extent=[robot_x*self.robot_res, (robot_x+1)*self.robot_res, robot_y*self.robot_res, (robot_y+1)*self.robot_res]))
        for item_x, item_y in state.item_pos:
            images.append(plt.imshow(cv2.cvtColor(self.item, cv2.COLOR_BGR2RGB),
                         extent=[item_x*self.robot_res, (item_x+0.5)*self.robot_res, item_y*self.robot_res, (item_y+0.5)*self.robot_res]))

        return images


class State:
    def __init__(self, x, y):
        self.time = 0
        self.robot_pos = []
        self.item_pos = []
        self.x = x
        self.y = y

    def move_random(self):
        self.time += 1
        for i,robot in enumerate(self.robot_pos):
            change = random.choice([-1,1])
            robot_x, robot_y = robot
            if random.random() > 0.5:
                robot_x = (robot_x + change) % self.x
            else:
                robot_y = (robot_y + change) % self.y
            self.robot_pos[i] = (robot_x, robot_y)

    def apply(self, change):
        for i,move in enumerate(change):
            xchg, ychg = move
            robot_x, roboty = self.robot_pos[i]
            self.robot_pos[i] = (robot_x+xchg, roboty+ychg)
            for item in self.item_pos: # slow delete :S
                if item == self.robot_pos[i]:
                    self.item_pos.remove(item)

    def add_robot(self, n=1):
        for i in range(n):
            self.robot_pos.append((random.randint(0,self.x), random.randint(0,self.y)))

    def add_items(self, n=1):
        for i in range(n):
            self.item_pos.append((random.randint(0,self.x), random.randint(0,self.y)))


class Routing:
    pass


if __name__ == '__main__':
    animator = Animator()
    state = State(x=20, y=1)
    state.add_robot(3)
    state.add_items(10)
    animator.run(state, Routing())