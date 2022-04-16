from threading import Thread
from foxfsa import FoxFSA
from map import Map


class Game(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

        # initializing states
        self.map = Map(12,12)
        self.foxMachine = FoxFSA()
        self.player_move = ''
        self.pricly_ball_clock = 0

    def run(self):
        while not self.stopped.wait(2.5):

            self.check_user_action()
            self.get_map()
            self.log_state()
            # self.set_map()
            self.update_game()

    def check_user_action(self):
        if self.player_move == 'd':
            self.map.shift_player(1,0)
        elif self.player_move == 'a':
            self.map.shift_player(-1,0)
        elif self.player_move == 'w':
            self.map.shift_player(0,-1)
        elif self.player_move == 's':
            self.map.shift_player(0,1)

        self.player_move = ''

    def set_user_action(self, action):
        self.player_move = action

    def get_map(self):
        if self.map.player_pos == self.map.fox_pos:
            self.foxMachine.send('m')
        elif self.map.player_pos == self.map.powermash_pos:
            self.foxMachine.send('p')
            # update map, remove eaten powermashroom, set pricly ball clock to 10 seconds
            self.pricly_ball_clock = 20
            self.map.remove_powermashroom()
        elif self.map.player_pos in self.map.mashroom_pos_arr:
            # update map, remove eaten mashroom
            self.map.remove_mashroom(self.map.player_pos)
        else:
            self.foxMachine.send('')

    def update_game(self):
        if self.foxState == 'Fox won' or self.foxState == 'Hedgehog won' or self.foxState == 'Stopped':
            self.stopped.set()
            #break
        elif self.foxState == 'Chasing':
            # get closer to hedgehog
            if self.map.fox_pos.x > self.map.player_pos.x:
                self.map.shift_fox(-1, 0)

            elif self.map.fox_pos.x < self.map.player_pos.x:
                self.map.shift_fox(1, 0)

            elif self.map.fox_pos.y > self.map.player_pos.y:
                self.map.shift_fox(0, -1)

            elif self.map.fox_pos.y < self.map.player_pos.y:
                self.map.shift_fox(0, 1)

        elif self.foxState == 'Running' or self.foxState == 'Fox Recovers':
            # get away from hedgehog
            if self.map.fox_pos.x > self.map.player_pos.x:
                self.map.shift_fox(1, 0)

            elif self.map.fox_pos.x < self.map.player_pos.x:
                self.map.shift_fox(-1, 0)

            elif self.map.fox_pos.y > self.map.player_pos.y:
                self.map.shift_fox(0, 1)

            elif self.map.fox_pos.y < self.map.player_pos.y:
                self.map.shift_fox(0, -1)
        else:
            print('State outside of what is expected')

    def log_state(self):
        print(' ')
        self.foxState = self.foxMachine.get_state()
        print(self.foxState)
        print('Fox:')
        print(self.map.fox_pos)
        print('Player:')
        print(self.map.player_pos)
        if self.map.powermash_pos == None and self.map.mashroom_pos_arr == []:
            print('Hedgehog won')
            self.stopped.set()
        if self.pricly_ball_clock > 0:
            print("Pricly Ball Clock: " + str(self.pricly_ball_clock))
            self.pricly_ball_clock -= 1

            if self.pricly_ball_clock == 0:
                self.foxMachine.send('t') # notify fox that Super Mod expired
        print("-------")
        self.map.display_map()
        print('next move > ')
