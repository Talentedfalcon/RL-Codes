import numpy as np
from gymnasium import Env,spaces
from time import sleep

class CliffBoy(Env):
    def __init__(self,gridshape):
        super(CliffBoy,self).__init__()
        self.gridshape=gridshape

        self.action_space=spaces.Discrete(4)
        self.observation_space=spaces.Discrete(gridshape[0]*gridshape[1])

        self.ground=np.zeros((gridshape[0],gridshape[1]),dtype=object)
        
        self.state=(0,0)

        self.cum_reward=0

        cliff_len=6

        cliff_seed=self.random_position()
        cliff_direction=np.random.randint(0,2)
        for i in range(cliff_len):
            self.ground[
                (cliff_seed[0]+(i*(np.abs(cliff_direction-1))))%gridshape[0],
                (cliff_seed[1]+(i*cliff_direction))%gridshape[1]
            ]='C'

        self.goal=(gridshape[0]-1,gridshape[1]-1)
        self.ground[self.goal[0],self.goal[1]]='G'


    def step(self,action):
        x,y=self.state

        if action == 0:  # Left
            y = max(0, y - 1)
        elif action == 1:  # Down
            x = min(self.gridshape[0] - 1, x + 1)
        elif action == 2:  # Right
            y = min(self.gridshape[1] - 1, y + 1)
        elif action == 3:  # Up
            x = max(0, x - 1)

        self.state = (x, y)

        reward = self.get_reward()
        self.cum_reward+=reward

        done = self.ground[x, y] == 'C' or self.ground[x, y] == 'G'

        return self._get_state_index(), reward, done, {}

    def get_reward(self):
        if(self.state==(self.gridshape[0]-1,self.gridshape[1]-1)):
            return 100
        elif(self.ground[self.state[0],self.state[1]]=='C'):
            return -100
        else:
            return -1

    def reset(self):
        self.state = (0, 0)
        return self._get_state_index()

    def _get_state_index(self):
        return self.state[0] * self.gridshape[0] + self.state[1]

    def random_position(self):
        return [np.random.randint(1,self.gridshape[0]),np.random.randint(1,self.gridshape[1])]

    def render(self,showStep=False):
        if(showStep):
            sleep(0.05)
            print(end='\033[2J')
            print(end='\033[H')

        for i in range(self.gridshape[0]):
            for j in range(self.gridshape[1]):
                if(self.state==(i,j)):
                    print('A',end=' ')
                elif(self.ground[i][j]==0):
                    print('.',end=' ')
                else:
                    print(self.ground[i][j],end=' ')
            print()
      
env=CliffBoy((8,12))
env.render()

done=0

while not done:
    action = env.action_space.sample()
    next_state, reward, done, info = env.step(action)
    print(f"\nAction: {action}")
    env.render(showStep=True)
    print(f"Reward: {reward}")
    print(f"Cumulative Reward: {env.cum_reward}")