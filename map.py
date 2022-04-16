
class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def __eq__(self, other):
        if not isinstance(other, Point):
            # don't attempt to compare against unrelated types
            return False

        return self.x == other.x and self.y == other.y

    def shift(self, x_incr, y_incr):
        self.x += x_incr
        self.y += y_incr

        # Keep them in the field
        if self.x > 12:
            self.x = 12

        if self.x < 1:
            self.x = 1

        if self.y > 12:
            self.y = 12

        if self.y < 1:
            self.y = 1

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

class Map:
    def __init__(self, x_max, y_max):
        self.fox_pos = Point(2,2)
        self.player_pos = Point(x_max,y_max)
        self.populate_map()

    def populate_map(self):
        self.mashroom_pos_arr = [Point(2,3), Point(5,9), Point(10,1), Point(2,11)]
        self.powermash_pos = Point(10,10)
        self.tree_pos_arr = [Point(5,8), Point(6,8), Point(6,9), Point(6,10), Point(6,11)]

    def shift_fox(self, x_incr, y_incr):
        if not(Point(self.fox_pos.x + x_incr, self.fox_pos.y + y_incr) in self.tree_pos_arr):
            # we don't wanna hit a tree
            self.fox_pos.shift(x_incr,y_incr)

    def shift_player(self, x_incr, y_incr):
        if not(Point(self.player_pos.x + x_incr, self.player_pos.y + y_incr) in self.tree_pos_arr):
            # we don't wanna hit a tree
            self.player_pos.shift(x_incr,y_incr)

    def remove_mashroom(self, pos):
        for shroom_pos in self.mashroom_pos_arr:
            if shroom_pos == pos:
                self.mashroom_pos_arr.remove(shroom_pos)

    def remove_powermashroom(self):
        self.powermash_pos = None

    def display_map(self):
        for j in range(1, 13):
            for i in range(1, 13):
                if Point(i, j) == self.fox_pos:
                    print('F',end="")
                elif Point(i, j) == self.player_pos:
                    print('P', end="")
                elif Point(i, j) == self.powermash_pos:
                    print('+', end="")
                elif Point(i, j) in self.mashroom_pos_arr:
                    print('*', end="")
                elif Point(i, j) in self.tree_pos_arr:
                    print('!', end="")
                else:
                    print('.', end="")
            print("")
