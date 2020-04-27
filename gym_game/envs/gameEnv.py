import pygame, time
import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
from gym_game.envs.gameMap import Map

class GameEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self, mapSize=16, tileWidth=40, tileHeight=40, tileMargin=2):
        super(GameEnv, self).__init__()
        self.mapSize = mapSize
        self.name = 0
        self.reward_threshold = 0.0
        self.trails = 100
        self.max_episode_steps = 10000
        self.screenSize = 674
        # get action space
        self.possible_actions = ['RIGHT', 'LEFT', 'UP', 'DOWN']
        self.action_space = spaces.Discrete(len(self.possible_actions))

        # Size of each tile on the 16x16 map size and margin between each tile
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.tileMargin = tileMargin

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
        self.white = (255, 255, 255)

        # type of game play, solo_play for 1 player, team_play for 2 players, team_vs for 4 players against each other.
        self.game_type = "team_vs"
        # Movement keys
        self.keyLookup = {pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT", pygame.K_DOWN: "DOWN", pygame.K_UP: "UP"}

        # Initialise map object - create map
        self.game_map = Map(self.game_type)
        self.game_over = False

        self.observation_space = spaces.Box(low=0, high=255, shape=(self.mapSize, self.mapSize, 3), dtype='uint8')

    def init_interface(self):
        # Initialise the PyGame & create the screen
        self.pygame = pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screenSize, self.screenSize))
        self.pygame.display.set_caption("Multi-agent reinforcement learning game!")

    def close_render(self):
        self.pygame.quit()

    def get_colour(self, col, row):
        if self.game_map.grid[col][row][0].name == "Dirt":
            return self.teal
        elif self.game_map.grid[col][row][0].name == "Wall":
            return self.gold
        elif self.game_map.grid[col][row][0].name == "Red Team":
            return self.lightRed
        elif self.game_map.grid[col][row][0].name == "Blue Team":
            return self.blue
        elif self.game_map.grid[col][row][0].name == 0:
            return self.darkBlue
        elif self.game_map.grid[col][row][0].name == 1:
            return self.purpleBlue
        elif self.game_map.grid[col][row][0].name == 2:
            return self.redDark
        elif self.game_map.grid[col][row][0].name == 3:
            return self.red

    def get_state(self):
        rgb_state = []
        # create empty 3D array to match the grid map
        for row in range(16):
            rgb_state.append([])
            for column in range(16):
                rgb_state[row].append([])
        # assign RGB values to array
        for col in range(16):
            for row in range(16):
                rgb_state[col][row].append(self.get_colour(col, row))
        img = np.array(rgb_state)
        img_reshaped = img.reshape(16, 16, 3)
        return img_reshaped

    def step(self, action):
        ''' step method for openai, returns: observation, reward, done, info
        '''
        if self.game_type == "solo_play":
            # moves the player
            self.game_map.player.movePlayer(self.possible_actions[action], self.game_map, self.game_type)
            rwd = self.game_map.player.reward
        elif self.game_type == "team_play":
            self.game_map.player.movePlayer(self.possible_actions[action], self.game_map, self.game_type)
            self.game_map.player2.movePlayer(self.possible_actions[action], self.game_map, self.game_type)
            rwd = self.game_map.player.reward + self.game_map.player2.reward
        elif self.game_type == "team_vs":
            self.game_map.player.movePlayer(self.possible_actions[action], self.game_map, self.game_type)
            self.game_map.player2.movePlayer(self.possible_actions[action], self.game_map, self.game_type)
            rwd = self.game_map.player.reward + self.game_map.player2.reward
            self.game_map.player3.randomMovement(self.game_map, self.game_type)
            self.game_map.player4.randomMovement(self.game_map, self.game_type)
        # get done
        self.check_game_over()
        done = self.game_over
        if done == True:
            rwd += 50
        # get obs
        obs = self.get_state()
        #get more info
        info = {}
        return obs, done, rwd, info

    def get_key_pressed(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
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

    def check_game_over(self):
        if self.game_map.amount_of_dirt == self.game_map.count_team_colours():
            self.game_over = True

    def render_game_over(self):
        if self.game_over:
            myFont = self.pygame.font.SysFont('monaco', 100)
            game_over_surface = myFont.render('Moves Used: ' + str(self.game_map.player.countMovement), True, self.redDark)
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.midtop = ((350, 250))
            self.screen.blit(game_over_surface, game_over_rect)
            self.pygame.display.flip()
            time.sleep(1)
            self.close_render()

    def render_score(self):
        sFont = self.pygame.font.SysFont('monaco', 24)
        Ssurf = sFont.render('Moves Used: ' + str(self.game_map.player.countMovement), True, self.white)
        Srect = Ssurf.get_rect()
        Srect.midtop = ((600, 10))
        self.screen.blit(Ssurf, Srect)

    def play_game(self):
        # run the main code until we exit
        self.init_interface()
        while self.game_over == False:
            self.get_key_pressed()
            self.render()
            self.check_game_over()
        self.render_game_over()

    def reset(self):
        self.game_over = False
        self.game_map = Map(self.game_type)
        return self.get_state()

    def render(self, mode='human'):
        '''Render method for Open AI'''
        self.init_interface()
        self.screen.fill(self.black)

        for row in range(self.mapSize):
            for column in range(self.mapSize):
                for i in range(0, len(self.game_map.grid[column][row])):
                    colour = self.teal

                    # Colour of tiles depending on tile
                    if self.game_map.grid[column][row][i].name == "Wall":
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

        self.render_score()
        # display flip to prevent error
        pygame.display.flip()
        # update the map
        self.clock.tick(144)
        self.game_map.update(self.game_type)