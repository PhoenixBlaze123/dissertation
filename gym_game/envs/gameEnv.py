import pygame
import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_game.envs.gameMap import Map

class GameEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, mapSize=16, tileWidth=40, tileHeight=40, tileMargin=2):
        self.mapSize = mapSize
        self.name = 0
        self.reward_threshold = 0.0
        self.trails = 100
        self.max_episode_steps = 10000
        self.possible_actions = ['RIGHT', 'LEFT', 'UP', 'DOWN']
        self.action_space = spaces.Discrete(len(self.possible_actions))

        # Size of each tile on the 16x16 map size and margin between each tile
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.tileMargin = tileMargin

        # Important variables
        self.reset()

        # Colour Definitions
        self.black = (0, 0, 0)
        self.lightRed = (255, 153, 153)
        self.red = (255, 0, 0)
        self.redDark = (55, 0, 0)
        self.green = (27, 176, 76)
        self.teal = (47, 79, 79)
        self.gold = (153, 153, 102)
        self.blue = (56, 182, 241)
        self.darkBlue = (0, 0, 255)
        self.purpleBlue = (77, 77, 179)

        # type of game play, solo_play for 1 player, team_play for 2 players, team_vs for 4 players against each other.
        self.game_type = "solo_play"

        # Movement keys
        self.keyLookup = {pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT", pygame.K_DOWN: "DOWN", pygame.K_UP: "UP"}

        # Initialise map object - create map
        self.game_map = Map(self.game_type)

    def init_interface(self):
        # Initialise the PyGame & create the screen
        self.pygame = pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((674, 674))
        self.pygame.display.set_caption("Multi-agent reinforcement learning game!")

    def close_render(self):
        self.pygame.quit()

    def step(self, action):
        ''' step method for openai, returns: observation, reward, done, info
        '''

        # moves the player
        self.game_map.player.movePlayer(self.possible_actions[action])

        # get reward
        rwd = self.game_map.player.reward
        return rwd



    def close(self):
        return

    def get_pressed_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

            # Allow user to see contents of tile when clicking on that tile for debugging reasons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (self.tileWidth + self.tileMargin)
                row = pos[1] // (self.tileHeight + self.tileMargin)
                print(str(row) + ", " + str(column))

                for i in range(len(self.game_map.grid[column][row])):
                    print(str(self.game_map.grid[column][row][i].name))

            # pygame player movement
            elif event.type == pygame.KEYDOWN:
                if self.game_type == "solo_play":
                    self.game_map.player.movePlayer(self.keyLookup[event.key], self.game_map, self.game_type)
                    print("reward: " + str(self.game_map.player.reward))
                if self.game_type == "team_play":
                    self.game_map.player.movePlayer(self.keyLookup[event.key], self.game_map, self.game_type)
                    self.game_map.player2.movePlayer(self.keyLookup[event.key], self.game_map, self.game_type)
                    print("reward: " + str(self.game_map.player.reward + self.game_map.player2.reward) + " -- moves used: " + str(self.game_map.player.countMovement + self.game_map.player2.countMovement))
                elif self.game_type == "team_vs":
                    self.game_map.player.movePlayer(self.keyLookup[event.key], self.game_map, self.game_type)
                    self.game_map.player2.movePlayer(self.keyLookup[event.key], self.game_map, self.game_type)
                    self.game_map.player3.movePlayer(self.keyLookup[event.key], self.game_map, self.game_type)
                    self.game_map.player4.movePlayer(self.keyLookup[event.key], self.game_map, self.game_type)
                    print("BLUE TEAM: " + "reward: " + str(self.game_map.player.reward + self.game_map.player2.reward) + " -- moves used: " + str(self.game_map.player.countMovement + self.game_map.player2.countMovement))
                    print("RED TEAM: " + "reward: " + str(self.game_map.player3.reward + self.game_map.player4.reward) + " -- moves used: " + str(self.game_map.player3.countMovement + self.game_map.player4.countMovement))

    def play_game(self):
        # run the main code until we exit
        self.init_interface()
        running = True
        while running:
            self.get_key_pressed(self)
            self.render()

    def reset(self):
        return
        #self.game_map = Map(self.game_type)

    def render(self, mode='human'):
        '''Render method for Open AI'''
        self.init_interface()
        self.screen.fill(self.black)

        for row in range(self.mapSize):
            for column in range(self.mapSize):
                for i in range(0, len(self.game_map.grid[column][row])):
                    colour = self.teal

                    # Colour of tiles depending on tile
                    if self.game_map.grid[column][row][i].name == "Wall" or self.game_map.grid[column][row][i].name == "Wall":
                        colour = self.gold
                    elif self.game_map.grid[column][row][i].name == "Red Team":
                        colour = self.lightRed
                    elif self.game_map.grid[column][row][i].name == "Blue Team":
                        colour = self.blue
                    elif self.game_map.grid[column][row][i].name == 0:
                        colour = self.darkBlue
                    elif self.game_map.grid[column][row][i].name == 1:
                        colour = self.purpleBlue
                    elif self.game_map.grid[column][row][i].name == 2:
                        colour = self.redDark
                    elif self.game_map.grid[column][row][i].name == 3:
                        colour = self.red

                # draw screen using pygame
                pygame.draw.rect(self.screen, colour, [(self.tileMargin + self.tileWidth) * column + self.tileMargin,
                                                       (self.tileMargin + self.tileHeight) * row + self.tileMargin,
                                                       self.tileWidth, self.tileHeight])
        self.clock.tick(60)

        # display flip to prevent error
        pygame.display.flip()

        # update the map
        self.game_map.update(self.game_type)
