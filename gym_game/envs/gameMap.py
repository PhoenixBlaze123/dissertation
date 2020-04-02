import random

class MapTile(object):
    def __init__(self, name, column, row):
        self.name = name
        self.column = column
        self.row = row

class Character(object):
    def __init__(self, name, column, row):
        self.name = name
        self.column = column
        self.row = row
        self.reward = 0
        self.countMovement = 0

    # if block is dirt, replaced with blue team colour
    def paintBlock(self, game_map):
        for i in range(len(game_map.grid[self.column][(self.row)])):
            if game_map.grid[self.column][(self.row)][i].name == "Dirt":
                game_map.grid[self.column][(self.row)].remove(game_map.grid[self.column][(self.row)][i])
                if self.name == 0 or self.name == 1:
                    game_map.grid[self.column][self.row].append(MapTile("Blue Team", self.column, self.row))
                elif self.name == 2 or self.name == 3:
                    game_map.grid[self.column][self.row].append(MapTile("Red Team", self.column, self.row))

    # bool check to see if tile is blue
    def isBlue(self, game_map):
        for i in range(len(game_map.grid[self.column][(self.row)])):
            if game_map.grid[self.column][(self.row)][i].name == "Blue Team":
                return True
        return False

    def isRed(self, game_map):
        for i in range(len(game_map.grid[self.column][(self.row)])):
            if game_map.grid[self.column][(self.row)][i].name == "Red Team":
                return True
        return False

    # Move player function in 4 directions using arrow keys - reward is given for each successful move
    def movePlayer(self, direction, game_map, game_type):
        if self.canMove(direction, game_map) == False:
            return

        # up direction movement logic
        if direction == "UP":
            if self.row > 0:
                self.row -= 1
                # +1 reward logic
                if self.isBlue(game_map) == False and self.isRed(game_map) == False:
                    self.reward += 1
                self.paintBlock(game_map)
                self.countMovement += 1

        # left direction movement logic
        elif direction == "LEFT":
            if self.column > 0:
                self.column -= 1
                if self.isBlue(game_map) == False and self.isRed(game_map) == False:
                    self.reward += 1
                self.paintBlock(game_map)
                self.countMovement += 1

        elif direction == "RIGHT":
            if self.column < 16 - 1:
                self.column += 1
                if self.isBlue(game_map) == False and self.isRed(game_map) == False:
                    self.reward += 1
                self.paintBlock(game_map)
                self.countMovement += 1

        elif direction == "DOWN":
            if self.row < 16 - 1:
                self.row += 1
                if self.isBlue(game_map) == False and self.isRed(game_map) == False:
                    self.reward += 1
                self.paintBlock(game_map)
                self.countMovement += 1

        # update map after player movement
        game_map.update(game_type)

    # collision detection, if tile that player is looking to move to contains wall then do not allow movement
    def canMove(self, direction, game_map):
        if direction == "UP":
            for i in range(len(game_map.grid[self.column][(self.row) - 1])):
                if game_map.grid[self.column][(self.row) - 1][i].name == "Wall" or game_map.grid[self.column][(self.row) - 1][i].name == 0 or game_map.grid[self.column][(self.row) - 1][i].name == 1:
                    return False

        elif direction == "LEFT":
            for i in range(len(game_map.grid[self.column - 1][(self.row)])):
                if game_map.grid[self.column - 1][(self.row)][i].name == "Wall" or game_map.grid[self.column - 1][(self.row)][i].name == 0 or game_map.grid[self.column - 1][(self.row)][i].name == 1:
                    return False

        elif direction == "RIGHT":
            for i in range(len(game_map.grid[self.column + 1][(self.row)])):
                if game_map.grid[self.column + 1][(self.row)][i].name == "Wall" or game_map.grid[self.column + 1][(self.row)][i].name == 0 or game_map.grid[self.column + 1][(self.row)][i].name == 1:
                    return False

        elif direction == "DOWN":
            for i in range(len(game_map.grid[self.column][(self.row) + 1])):
                if game_map.grid[self.column][(self.row) + 1][i].name == "Wall" or game_map.grid[self.column][(self.row) + 1][i].name == 0 or game_map.grid[self.column][(self.row) + 1][i].name == 1:
                    return False

        return True

    # shows current location of player for debugging reasons
    def location(self):
        print("Coordinates: " + str(self.row)) + ", " + str(self.column)

class Map(object):
    def __init__(self, game_type):
        self.mapSize = 16
        self.grid = []
        self.create_map()
        self.game_type = game_type
        self.create_players(game_type)

    # creates the map including where the player is placed
    def create_map(self):
        for row in range(self.mapSize):
            self.grid.append([])
            for column in range(self.mapSize):
                self.grid[row].append([])

        # placing all "Dirt" tile within walls
        for row in range(1, self.mapSize - 1):
            for column in range(1, self.mapSize - 1):
                tempTile = MapTile("Dirt", column, row)
                self.grid[column][row].append(tempTile)

        # placing walls on border
        for row in range(self.mapSize):
            for column in range(self.mapSize):
                tempTile = MapTile("Wall", column, row)
                if row == 0:
                    self.grid[column][row].append(tempTile)
                if row == 15:
                    self.grid[column][row].append(tempTile)
                if column == 0:
                    self.grid[column][row].append(tempTile)
                if column == 15:
                    self.grid[column][row].append(tempTile)

        # placing random walls
        for i in range(50):
            randomRow = random.randint(2, self.mapSize - 3)
            randomColumn = random.randint(2, self.mapSize - 3)
            tempTile = MapTile("Wall", randomColumn, randomRow)
            for i in range(len(self.grid[randomColumn][randomRow])):
                if self.grid[randomColumn][randomRow][i].name == "Dirt":
                    self.grid[randomColumn][randomRow].remove(self.grid[randomColumn][randomRow][i])
            self.grid[randomColumn][randomRow].append(tempTile)

    # create players and choose location of player spawn
    # 2 players for regular game mode, and 4 players for vs game mode
    def create_players(self, game_type):
        if game_type == "solo_play":
            self.player = Character(0, 1, 1)
        elif game_type == "team_play":
            self.player = Character(0, 1, 1)
            self.player2 = Character(1, 14, 1)
        elif game_type == "team_vs":
            self.player = Character(0, 1, 1)
            self.player2 = Character(1, 14, 1)
            self.player3 = Character(2, 1, 14)
            self.player4 = Character(3, 14, 14)

    # updates the map when player moves
    def update(self, game_type):
        for column in range(16):
            for row in range(16):
                for i in range(len(self.grid[column][row])):
                    if self.grid[column][row][i].column != column:
                        self.grid[column][row].remove(self.grid[column][row][i])
                    elif self.grid[column][row][i].name == 0:
                        self.grid[column][row].remove(self.grid[column][row][i])
                    elif self.grid[column][row][i].name == 1:
                       self.grid[column][row].remove(self.grid[column][row][i])
                    elif self.grid[column][row][i].name == 2:
                        self.grid[column][row].remove(self.grid[column][row][i])
                    elif self.grid[column][row][i].name == 3:
                        self.grid[column][row].remove(self.grid[column][row][i])
        if game_type == "solo_play":
            self.grid[int(self.player.column)][int(self.player.row)].append(self.player)
        elif game_type == "team_play":
            self.grid[int(self.player.column)][int(self.player.row)].append(self.player)
            self.grid[int(self.player2.column)][int(self.player2.row)].append(self.player2)
        elif game_type == "team_vs":
            self.grid[int(self.player.column)][int(self.player.row)].append(self.player)
            self.grid[int(self.player2.column)][int(self.player2.row)].append(self.player2)
            self.grid[int(self.player3.column)][int(self.player3.row)].append(self.player3)
            self.grid[int(self.player4.column)][int(self.player4.row)].append(self.player4)