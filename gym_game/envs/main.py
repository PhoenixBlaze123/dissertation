import pygame

from gym_game.envs.gameMap import Map

# Initialise the pygame & create the screen
pygame.init()
screen = pygame.display.set_mode((674, 674))
clock = pygame.time.Clock()
pygame.display.set_caption("Multi-agent reinforcement learning game!")
# Global map size
mapSize = 16

# Size of each tile on the 16x16 map size and margin between each tile
tileWidth = 40
tileHeight = 40
tileMargin = 2

# Colour Definitions
black = (0, 0, 0)
lightRed = (255, 153, 153)
red = (255, 0, 0)
redDark = (55, 0 ,0)
green = (27, 176, 76)
teal = (47, 79, 79)
gold = (153, 153, 102)
blue = (56, 182, 241)
darkBlue = (0, 0, 255)
purpleBlue = (77, 77, 179)

game_type = "solo_play"

# Movement keys
keyLookup = { pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT", pygame.K_DOWN: "DOWN", pygame.K_UP: "UP" }

# Initialise map object
game_map = Map(game_type)

# run the main code until we exit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Allow user to see contents of tile when clicking on that tile for debugging reasons
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (tileWidth + tileMargin)
            row = pos[1] // (tileHeight + tileMargin)
            print(str(row) + ", " + str(column))

            for i in range(len(game_map.grid[column][row])):
                print(str(game_map.grid[column][row][i].name))

        # pygame player movement
        elif event.type == pygame.KEYDOWN:
            if game_type == "solo_play":
                game_map.player.movePlayer(keyLookup[event.key], game_map, game_type)
                print("reward: " + str(game_map.player.reward))
            if game_type == "team_play":
                game_map.player.movePlayer(keyLookup[event.key], game_map, game_type)
                game_map.player2.movePlayer(keyLookup[event.key], game_map, game_type)
                print("reward: " + str(game_map.player.reward + game_map.player2.reward) + " -- moves used: " + str(game_map.player.countMovement + game_map.player2.countMovement))
            elif game_type == "team_vs":
                game_map.player.movePlayer(keyLookup[event.key], game_map, game_type)
                game_map.player2.movePlayer(keyLookup[event.key], game_map, game_type)
                game_map.player3.movePlayer(keyLookup[event.key], game_map, game_type)
                game_map.player4.movePlayer(keyLookup[event.key], game_map, game_type)
                print("BLUE TEAM: " + "reward: " + str(game_map.player.reward + game_map.player2.reward) + " -- moves used: " + str(game_map.player.countMovement + game_map.player2.countMovement))
                print("RED TEAM: " + "reward: " + str(game_map.player3.reward + game_map.player4.reward) + " -- moves used: " + str(game_map.player3.countMovement + game_map.player4.countMovement))

    screen.fill(black)

    for row in range(mapSize):
        for column in range(mapSize):
            for i in range(0, len(game_map.grid[column][row])):
                colour = teal

                # Colour of tiles depending on tile
                if game_map.grid[column][row][i].name == "Wall":
                    colour = gold
                elif game_map.grid[column][row][i].name == "Red Team":
                    colour = lightRed
                elif game_map.grid[column][row][i].name == "Blue Team":
                    colour = blue
                elif game_map.grid[column][row][i].name == 0:
                    colour = darkBlue
                elif game_map.grid[column][row][i].name == 1:
                    colour = purpleBlue
                elif game_map.grid[column][row][i].name == 2:
                    colour = redDark
                elif game_map.grid[column][row][i].name == 3:
                    colour = red

            # draw screen using pygame
            pygame.draw.rect(screen, colour, [(tileMargin + tileWidth) * column + tileMargin,
                                              (tileMargin + tileHeight) * row + tileMargin,
                                              tileWidth, tileHeight])

    clock.tick(30)

    # display flip to prevent error
    pygame.display.flip()

    # update the map
    game_map.update(game_type)

pygame.quit()