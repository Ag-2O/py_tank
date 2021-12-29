import numpy as np
import random
import game
import copy

class greedy:
    def __init__(self, player_id):
        self.player_id = player_id
        self.direction = 0  # 0:north, 1:east, 2:south, 3:west
        self.score = 1000
        self.bullet_num = 0

        self.y_pos = 0
        self.x_pos = 0
    
    def action(self,game_state:game.game):
        value = np.array([0,0,0])
        move_list = [-1,0,1]
        for move in move_list:
            game_copy = copy.deepcopy(game_state)
            game_copy.update_map()


        return action
    
    def fire_bullet(self):
        fire = random.choice([True,False])
        return fire
    
    def score_state(self):
        return

    def is_move(self,action):
        if action == 0:
            to_y = self.y_pos - 1
            to_x = self.x_pos
        elif action == 1:
            to_y = self.y_pos
            to_x = self.x_pos + 1
        elif action == 2:
            to_y = self.y_pos + 1
            to_x = self.x_pos
        else:
            to_y = self.y_pos
            to_x = self.x_pos - 1
        
        if 0 > to_y or 7 < to_y:
            return False
        
        if 0 > to_x or 7 < to_x:
            return False

        walls = [(0,3),(1,3),(3,6),(3,7),(4,0),(4,1),(6,4),(7,4)]

        for wall in walls:
            if to_y == wall[0] and to_x == wall[1]:
                return False
        
        return True

    def get_pos(self):
        return self.y_pos, self.x_pos, self.direction

    def set_pos(self,y,x,d):
        self.y_pos = y
        self.x_pos = x
        self.direction = d