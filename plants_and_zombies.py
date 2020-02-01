from enum import Enum

class GameState(Enum):
    active=1
    zombie_win = 2
    plant_win = 3

class Game(object):


    def __init__(self, lawn, zombies):
        self._row_size = len(lawn)
        self._col_size = len(lawn[0])
        self._lawn = lawn
        self._zombies = zombies
        self._game = [[None for col in range(self._col_size)] for row in range(self._row_size)]
        self._add_shooter()
        self._move = 0
        self._last_zombie_move = max([zombie[0] for zombie in zombies])
        self._state = GameState.active

    def run(self,verbose = False):
        while self._state == GameState.active:
            self.turn(verbose)
            # if verbose:
            #     print(self)
        if self._state == GameState.zombie_win:
            return self._move
        else:
            return None

    def turn(self,verbose):
        self._zombie_advance()
        self._add_zombies(self._move)
        if verbose:
            print('Game before shoot')
            print(self)
        self._move += 1
        self._numbered_plant_shoot(verbose)
        self._sshooter_plant_shoot(verbose)
        self._reset_plant()
        if verbose:
            print('Game after shoot')
            print(self)
        if not self._check_zombie() and self._move >= self._last_zombie_move:
            self._state = GameState.plant_win

    def _reset_plant(self):
        for i in range(len(self._game)):
            for j in range(len(self._game[i])):
                if isinstance(self._game[i][j], Shooter):
                    self._game[i][j].reset_shoots()

    def _numbered_plant_shoot(self,verbose):
        self._shoot(NumberedShooter,verbose)

    def _sshooter_plant_shoot(self,verbose):
        self._shoot(SShooter,verbose)

    def _shoot(self,type,verbose):
        for i in range(len(self._game)):
            for j in range(len(self._game[i])):
                if isinstance(self._game[i][j], type):
                    shoot = self._game[i][j].shoot()
                    while shoot is not None:
                        zombie = shoot.find_target(self._game,i,j)
                        if zombie is not None:
                            if verbose:
                                print(f'{self._game[i][j]} at ({i},{j}) has shoot on zombie at ')
                            zombie.damage()
                        shoot = self._game[i][j].shoot()

    def _zombie_advance(self):
        for i in range(len(self._game)):
            for j in range(len(self._game[i])):
                cell = self._game[i][j]
                if isinstance(cell, Zombie):
                    if cell.is_dead():
                        self._game[i][j]= None
                    else:
                        if j <= 1:
                            self._state = GameState.zombie_win

                        self._game[i][j-1] = cell
                        self._game[i][j] = None


    def _add_zombies(self, move):
        for zombie in self._zombies:
            if zombie[0] == move:
                self._game[zombie[1]][self._col_size - 1] = Zombie(zombie[2])

    def _check_zombie(self):

        for i in range(len(self._game)):
            for j in range(len(self._game[i])):
                cell = self._game[i][j]
                if isinstance(cell, Zombie):
                    return True
        return False

    def _add_shooter(self):
        for row_index in range(len(self._lawn)):
            row = self._lawn[row_index]
            for col_index in range(len(row)):
                cell = row[col_index]
                if cell.isdigit():
                    try:
                        self._game[row_index][col_index] = NumberedShooter(int(cell))
                    except:
                        print(row_index, col_index)
                        raise
                elif cell == 'S':
                    self._game[row_index][col_index] = SShooter()

    def __str__(self):

        return f'State of game at end of turn{self._move}: {self._state.name}\n' + '\n'.join(['|'.join([str(cell or '   ')  for cell in row]) for row in self._game])

class Shoot(object):
    pass


class StraightShoot(Shoot):

    def find_target(self, game, row_index, col_index):
        row = game[row_index]

        for row_scan in range(col_index, len(row)):
            if isinstance(row[row_scan], Zombie):
                return row[row_scan]


class DiagShoot(Shoot):
    def __init__(self, side):
        self._side = side

    def find_target(self, game, row_index, col_index):
        if self._side == 'up':
            inc = -1
            rows = row_index
        else:
            inc = 1
            rows = len(game) - row_index

        for step in range(0, min([rows, 7 - col_index]),inc):
            if isinstance(game[row_index + step][col_index + step], Zombie):
                return game[row_index + step][col_index + step]


class Shooter(object):

    def __init__(self):
        self._shoots = []
        self.reset_shoots()


    def shoot(self):
        if len(self._shoots) > 0:
            return self._shoots.pop()
        else:
            return None


class NumberedShooter(Shooter):

    def __init__(self, num_of_shoot):
        self._num_of_shoot = num_of_shoot
        super(NumberedShooter, self).__init__()


    def reset_shoots(self):
        self._shoots = [StraightShoot()] * self._num_of_shoot

    def __repr__(self):
        return f'<N{self._num_of_shoot}>'

    def __str__(self):
        return f'N{self._num_of_shoot} '


class SShooter(Shooter):

    def reset_shoots(self):
        self._shoots = [DiagShoot('up'), StraightShoot(), DiagShoot('down')]

    def __repr__(self):
        return '<SS>'

    def __str__(self):
        return 'SS '


class Zombie(object):

    def __init__(self, hit_points):
        self._hit_points = hit_points

    def damage(self):
        self._hit_points -= 1

    def is_dead(self):
        return self._hit_points <= 0

    def __repr__(self):
        return f'<Z{self._hit_points}>'

    def __str__(self):
        return f'Z{self._hit_points}'.ljust(3)


def plants_and_zombies(lawn, zombies):
    game = Game(lawn, zombies)
    return game.run(True)



example_tests = [
	# [
	# 	[
	# 		'2       ',
	# 		'  S     ',
	# 		'21  S   ',
	# 		'13      ',
	# 		'2 3     '],
	# 	[[0,4,28],[1,1,6],[2,0,10],[2,4,15],[3,2,16],[3,3,13]]],
	# [
	# 	[
	# 		'11      ',
	# 		' 2S     ',
	# 		'11S     ',
	# 		'3       ',
	# 		'13      '],
	# 	[[0,3,16],[2,2,15],[2,1,16],[4,4,30],[4,2,12],[5,0,14],[7,3,16],[7,0,13]]],
	[
		[
			'12        ',
			'3S        ',
			'2S        ',
			'1S        ',
			'2         ',
			'3         '],
		[[0,0,18],[2,3,12],[2,5,25],[4,2,21],[6,1,35],[6,4,9],[8,0,22],[8,1,8],[8,2,17],[10,3,18],[11,0,15],[12,4,21]]],
	# [
	# 	[
	# 		'12      ',
	# 		'2S      ',
	# 		'1S      ',
	# 		'2S      ',
	# 		'3       '],
	# 	[[0,0,15],[1,1,18],[2,2,14],[3,3,15],[4,4,13],[5,0,12],[6,1,19],[7,2,11],[8,3,17],[9,4,18],[10,0,15],[11,4,14]]],
	# [
	# 	[
	# 		'1         ',
	# 		'SS        ',
	# 		'SSS       ',
	# 		'SSS       ',
	# 		'SS        ',
	# 		'1         '],
	# 	[[0,2,16],[1,3,19],[2,0,18],[4,2,21],[6,3,20],[7,5,17],[8,1,21],[8,2,11],[9,0,10],[11,4,23],[12,1,15],[13,3,22]]]
]

for i,v in enumerate(example_tests):
    plants_and_zombies(*v)