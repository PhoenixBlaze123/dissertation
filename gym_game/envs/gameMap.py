import random
import numpy as np

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
                else:
                    self.reward -= 1
                self.paintBlock(game_map)
                self.countMovement += 1

        # left direction movement logic
        elif direction == "LEFT":
            if self.column > 0:
                self.column -= 1
                if self.isBlue(game_map) == False and self.isRed(game_map) == False:
                    self.reward += 1
                else:
                    self.reward -= 1
                self.paintBlock(game_map)
                self.countMovement += 1

        elif direction == "RIGHT":
            if self.column < 16 - 1:
                self.column += 1
                if self.isBlue(game_map) == False and self.isRed(game_map) == False:
                    self.reward += 1
                else:
                    self.reward -= 1
                self.paintBlock(game_map)
                self.countMovement += 1

        elif direction == "DOWN":
            if self.row < 16 - 1:
                self.row += 1
                if self.isBlue(game_map) == False and self.isRed(game_map) == False:
                    self.reward += 1
                else:
                    self.reward -= 1
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
        self.create_map(0)
        # type of game play -> "solo_play", "team_play", "team_vs"
        self.game_type = game_type
        # assign amount of dirt to static variable so that we can use this for the game_over function
        self.amount_of_dirt = self.count_dirt()
        # create players and place them on the map
        self.create_players(game_type)

    # creates the map including where the player is placed
    def create_map(self, seed):
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

        if seed == 0:
            list_of_tiles = [(2,6), (2, 7), (2, 9), (3,3), (3,4), (3,11), (3,13), (4,8), (4,11), (5,2), (5,3), (5,4), (5,7), (5,8), (5,11), (5,12), (5,13),
                             (6,3), (6,4), (6,5), (6,12), (7,7), (7,8), (8,4), (8,12), (9,2), (9,7), (9,8), (9,9), (10,2), (10,3), (10,8), (10,11), (10,13),
                             (11,7), (11,8), (11,10), (11,12), (12,3), (12,6), (12,9), (12,12), (13,2), (13,3), (13,7), (13,11), (13,12)]
            for i in range(len(list_of_tiles)):
                tempTile = MapTile("Wall", list_of_tiles[i][1], list_of_tiles[i][0])
                for j in range(len(self.grid[list_of_tiles[i][1]][list_of_tiles[i][0]])):
                    if self.grid[list_of_tiles[i][1]][list_of_tiles[i][0]][j].name == "Dirt":
                        self.grid[list_of_tiles[i][1]][list_of_tiles[i][0]].remove(self.grid[list_of_tiles[i][1]][list_of_tiles[i][0]][j])
                self.grid[list_of_tiles[i][1]][list_of_tiles[i][0]].append(tempTile)
        else:
            # placing random walls
            for i in range(50):
                randomRow = random.randint(2, self.mapSize - 3)
                randomColumn = random.randint(2, self.mapSize - 3)
                tempTile = MapTile("Wall", randomColumn, randomRow)
                for i in range(len(self.grid[randomColumn][randomRow])):
                    if self.grid[randomColumn][randomRow][i].name == "Dirt" or self.grid[randomColumn][randomRow][i].name == "Wall":
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

    # count the amount of dirt on the map
    def count_dirt(self):
        dirt = 0
        for column in range(16):
            for row in range(16):
                for i in range(len(self.grid[column][row])):
                    if self.grid[column][row][i].name == "Dirt":
                        dirt += 1
        return dirt

    # count the amount of team colours on the map
    def count_team_colours(self):
        team_colours = 0
        for column in range(16):
            for row in range(16):
                for i in range(len(self.grid[column][row])):
                    if self.grid[column][row][i].name == "Red Team" or self.grid[column][row][i].name == "Blue Team":
                        team_colours += 1
        return team_colours

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