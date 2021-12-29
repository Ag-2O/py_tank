import numpy as np
import random
import game
import copy

class tank:
    def __init__(self, player_id):
        self.player_id = player_id
        self.direction = 0  # 0:north, 1:east, 2:south, 3:west
        self.score = 1000
        self.bullet_num = 0

        self.y_pos = 0
        self.x_pos = 0
    
    def action(self):
        while True:
            action = random.choice([-1,0,1])
            action = (action + self.direction) % 4
            if action == -1:
                action = 3
            #fire = random.choice([True,False])
            #fire = False

            if self.is_move(action):
                break

            #print("action: {} fire: {}".format(action,fire))

        return action
    
    def fire_bullet(self):
        fire = random.choice([True,False])
        return fire
    
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

class player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.direction = 0  # 0:north, 1:east, 2:south, 3:west
        self.score = 1000
        self.bullet_num = 0

        self.y_pos = 0
        self.x_pos = 0
    
    def action(self):
        while True:
            print("player_id: {} direction : {}" \
                  .format(self.player_id,self.direction))
            print("straight: 0, left: -1, right: 1")
            print("choose actions: -1 or 0 or 1")
            action = input("-1 or 0 or 1 ?   ")

            action = (int(action) + self.direction) % 4
            if action == -1:
                action = 3

            if self.is_move(action):
                break
            else:
                print("cannot move!")

        return int(action)

    def fire_bullet(self):
        print("fire ?   ")
        fire = input("True: 1 or False: 0 ?   ")
        return True if int(fire) == 1 else False
    
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

class bullet:
    def __init__(self, bullet_id):
        self.bullet_id = bullet_id
        self.direction = 0

        self.y_pos = 0
        self.x_pos = 0
    
    def move(self):
        pass
    
    def get_pos(self):
        return self.y_pos, self.x_pos, self.direction
    
    def set_pos(self,y,x,d):
        self.y_pos = y
        self.x_pos = x
        self.direction = d