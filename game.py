# -*- coding: utf-8 -*-
import numpy as np
import tank
import time

class game:
    def __init__(self):
        self.map = [[ 1, 0, 0,-1, 0, 0, 0, 2],
                    [ 0, 0, 0,-1, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0,-1,-1],
                    [-1,-1, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0,-1, 0, 0, 0],
                    [ 3, 0, 0, 0,-1, 0, 0, 4]]
        
        self.players = [tank.tank(player_id=1),
                        tank.tank(player_id=2),
                        tank.tank(player_id=3),
                        tank.tank(player_id=4)]
        
        self.bullets = []

        self.players[0].set_pos(0,0,1)
        self.players[1].set_pos(0,7,2)
        self.players[2].set_pos(7,0,3)
        self.players[3].set_pos(7,7,0)
    
    def print_map(self,step):
        print("\n------------- map -------------")
        for i in range(8):
            print("  ",end="")
            for j in range(8):
                if self.map[i][j] == 0:
                    print("\033[30m ■ \033[0m",end="")
                elif self.map[i][j] == 1:
                    print("\033[31m ■ \033[0m",end="")
                elif self.map[i][j] == 2:
                    print("\033[32m ■ \033[0m",end="")
                elif self.map[i][j] == 3:
                    print("\033[33m ■ \033[0m",end="")
                elif self.map[i][j] == 4:
                    print("\033[34m ■ \033[0m",end="")
                elif self.map[i][j] == -1:
                    print("\033[35m ■ \033[0m",end="")
                elif self.map[i][j] == 11:
                    print("\033[31m ● \033[0m",end="")
                elif self.map[i][j] == 12:
                    print("\033[32m ● \033[0m",end="")
                elif self.map[i][j] == 13:
                    print("\033[33m ● \033[0m",end="")
                elif self.map[i][j] == 14:
                    print("\033[34m ● \033[0m",end="")

            print("\n")
        #print("player_list: {}".format(self.players))
        #print("bullet_list: {}".format(self.bullets))

    def update_map(self):

        if 1 >= len(self.players):
            winner = self.players.pop(0)
            print("winner : {}".format(winner.player_id))
            exit()

        next_map = self.map
        walls = [(0,3),(1,3),(3,6),(3,7),(4,0),(4,1),(6,4),(7,4)]

        # 移動処理
        print("------------- move -------------")
        for i in range(len(self.players)):
            # 座標の取得
            y_pos, x_pos, direction = self.players[i].get_pos()

            # 行動の取得
            start = time.perf_counter()
            action = self.players[i].action()
            elapsed_time = (time.perf_counter() - start) * 1000
            print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

            print("player action: {} direction: {}".format(self.players[i].player_id,action))

            # 移動
            if action == 0:
                to_y = y_pos - 1
                to_x = x_pos
            elif action == 1:
                to_y = y_pos
                to_x = x_pos + 1
            elif action == 2:
                to_y = y_pos + 1
                to_x = x_pos
            else:
                to_y = y_pos
                to_x = x_pos - 1
            
            # 他の車体がある場合
            if 5 > next_map[to_y][to_x] > 0:
                print("\033[31m"+"cannot move"+"\033[0m")
                print("player {} position ({},{})".format(self.players[i].player_id,y_pos,x_pos))
            else:        
                # 更新
                #print("to_y: {}, to_x: {}".format(to_y,to_x))
                next_map[y_pos][x_pos] = 0
                next_map[to_y][to_x] = self.players[i].player_id
                self.players[i].set_pos(to_y,to_x,action)

                print("player {} position ({},{}) -> ({},{})" \
                      .format(self.players[i].player_id,y_pos,x_pos,to_y,to_x))

        # 発射処理
        print("\n------------- fire -------------")
        n = 0
        num = len(self.players)
        while n < num:
            player = self.players.pop(0)
            fire = player.fire_bullet()
            # 座標の取得
            y_pos, x_pos, direction = player.get_pos()
            #print("x: {}, y: {}, direction: {}".format(y_pos,x_pos,direction))
            # 発射処理
            if fire and not self.is_limited_bullets(player.player_id):
                print("player {} fired! ".format(player.player_id))
                bullet = tank.bullet(10 + player.player_id)
                bullet.set_pos(y_pos,x_pos,direction)
                self.bullets.append(bullet)
            
            self.players.append(player)
            
            n += 1

        # すでに発射した弾の移動処理
        print("\n------------- bullets -------------")
        n = 0
        num = len(self.bullets)
        while n < num:
            is_delete = False
            is_wall = False
            is_outrange = False
            is_clush = False
            bullet = self.bullets.pop(0)
            past_y, past_x, direction = bullet.get_pos()
            for _ in range(2):
                y_pos, x_pos, direction = bullet.get_pos()

                # 移動処理
                if direction == 0:
                    to_y = y_pos - 1
                    to_x = x_pos
                elif direction == 1:
                    to_y = y_pos
                    to_x = x_pos + 1
                elif direction == 2:
                    to_y = y_pos + 1
                    to_x = x_pos
                else:
                    to_y = y_pos
                    to_x = x_pos - 1

                # 移動先がマップ内かどうか
                if (to_y >= 0 and to_y <= 7) and (to_x >= 0 and to_x <= 7):
                    if 5 > next_map[to_y][to_x] > 0:
                        # 移動先に相手がいる場合
                        m = 0
                        while m < len(self.players):
                            player = self.players.pop(0)
                            y, x, direction = player.get_pos()
                            if (to_y == y and to_x == x) and (bullet.bullet_id != player.player_id + 10):
                                is_delete = True
                                is_clush = True
                                next_map[to_y][to_x] = 0
                                if next_map[y_pos][x_pos] == bullet.bullet_id:
                                    next_map[y_pos][x_pos] = 0
                            else:
                                self.players.append(player)
                            m += 1

                    elif (to_y,to_x) in walls:
                        # 移動先が壁の場合
                        if next_map[y_pos][x_pos] == bullet.bullet_id:
                            next_map[y_pos][x_pos] = 0
                        is_delete = True
                        is_wall = True

                    else:
                        # 移動先に何もない場合
                        bullet.set_pos(to_y,to_x,direction)
                        next_map[to_y][to_x] = bullet.bullet_id
                        if next_map[y_pos][x_pos] == bullet.bullet_id:
                            next_map[y_pos][x_pos] = 0
                else:
                    # マップ外に出る場合
                    if next_map[y_pos][x_pos] == bullet.bullet_id:
                        next_map[y_pos][x_pos] = 0
                    is_delete = True
                    is_outrange = True

            # 削除フラグ
            if not is_delete:
                if not 5 > next_map[past_y][past_x] > 0:
                    next_map[past_y][past_x] = 0
                print("bullet {}: position ({},{}) -> ({},{})" \
                      .format(bullet.bullet_id,past_y,past_x,to_y,to_x))
                next_map[to_y][to_x] = bullet.bullet_id
                bullet.set_pos(to_y,to_x,direction)
                self.bullets.append(bullet)

            else:
                if is_wall:
                    print("bullet {}: position ({},{}) -> clush by walls" \
                        .format(bullet.bullet_id,past_y,past_x))
                if is_outrange:
                    print("bullet {} position ({},{}) -> map out" \
                          .format(bullet.bullet_id,past_y,past_x))
                if is_clush:
                    print("bullet {} killed player {}" \
                            .format(bullet.bullet_id,player.player_id))
            n += 1
        
        self.map = next_map
    
    def is_limited_bullets(self,player_id):
        # 発射した弾が２発以上存在するなら発射失敗にする
        bullet_id = 10 + player_id
        count = 0
        for idx in range(len(self.bullets)):
            if bullet_id == self.bullets[idx].bullet_id:
                count += 1
        
        return True if count >= 2 else False

    def clash():
        pass

if __name__ == "__main__":
    g = game()

    print("\n--------  game state turn {} -------- \n".format(0))
    g.print_map(0)
    for step in range(64):
        #print("\n################# {} #################\n".format(step))
        print("\n--------  game state turn {} -------- \n".format(step+1))
        g.update_map()
        g.print_map(step)