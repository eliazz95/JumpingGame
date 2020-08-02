import time, random
import pygame

screen_w = 800
screen_h = 600

# Create the window
screen = pygame.display.set_mode((screen_w,screen_h))

black = (0,0, 0)
red = (255,0,0)
green = (0, 200, 0)

class Game(object):

	def __init__(self):
		self.screen = pygame.display.set_mode((800,600))
		self.score = 0
		self.oldScore = 0
		self.speed = 5
		self.speedMultiplier = 1

	def gameInit(self):
		pygame.init()

	def gameName(self, name):
		pygame.display.set_caption(name)

	def setFPS(self, fps):
		pygame.time.Clock().tick(fps)

	def screenColor(self):
		self.screen.fill(green)

	def incSpeed(self, newSpeed):
		self.speed = newSpeed

	def resetGame(self):
		self.oldScore = self.score
		self.score = 0
		self.speed = 5
		self.speedMultiplier = 1


# Player Class
class Player(object):
	init_x = 150
	init_y = 405

	def __init__(self):
		self.x = Player.init_x
		self.y = Player.init_y
		self.width = 50
		self.height = 50
		self.vel = 10
		self.isJump = False
		self.jumpCount = 10


	# Function to draw the players geometry, in this case just a red square
	def draw(self):
		# Red square as player
		pygame.draw.rect(screen, red, [self.x, self.y, self.width, self.height])
		# Black contour defined by hitbox
		pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height), 3)


	def jump(self):
		# Using a mathematical equation with square calculations for jumping.
		# When the player reaches a certain height, jumpCount will get a negative value
		# so that the player starts falling down.
		if self.jumpCount >= -10:
			neg = 1
			if self.jumpCount < 0:
				neg = -1
			# Math equation
			self.y -= (self.jumpCount ** 2) * 0.8 * neg
			self.jumpCount -= 1
		else:
			self.isJump = False
			self.jumpCount = 10

	def setVel(self, vel):
		self.vel = vel

	# Reset position after death
	def reset(self):
		self.x = 150
		self.y = 405
		self.width = 50
		self.height = 50


# Enemy Class
class Enemy(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self. width = width
		self.height = height
		self.end = screen_w
		self.vel = 10

	# Function to draw the geometry of the enemies, in this case just a polygon in the form of a triangle
	def draw(self):
		# Calling function move() to actually draw the movement on the screen
		self.move()

		# If the enemy moves out of the screen it will appear on the other side again, looping
		if self.x < 0:
			self.x = self.end + random.randint(0,350)

		# Pointlist is a set of coordinates for the polygon [(x1,y1),(x2,y2) and so on]
		pointlist = [(self.x - self.width/2, self.y - self.width), (self.x - self.height/2, self.y - self.height), (self.x, self.y), (self.x - self.width, self.y)]
		# Draw the red contour
		pygame.draw.polygon(screen, red, pointlist, 3)
		# Draw the black triangle defined by pointlist
		pygame.draw.polygon(screen, black, pointlist, 0)

	# Function to move the enemy to the left towards the player at a certain velocity
	def move(self):
		self.x -= self.vel

	def setVel(self, newVel):
		self.vel = newVel

	# Resets position after death
	def reset(self, offset):
		self.x = random.randint(750,850) + offset
		self.y = 454
		self.width = 30
		self.height = 30
		self.vel = 10

# Function to call all class related functions to upload the drawings to the screen
def redrawGameWindow(player, enemyList):
	player.draw()
	for enemy in enemyList:
		enemy.draw()

	# Draws the red base in the game
	pygame.draw.rect(screen, red, [0,456, screen_w, 200])

	# Updates the screen with the drawings applied
	pygame.display.update()

# Whenever the player is touches the enemy this function is called and displayes the message DEAD on screen
def printMSG(msg, x, y, size):
	# Define font and size
	font = pygame.font.Font(None, size)
	# Define what message to display and it's color
	text_surface = font.render(msg, True, (0, 0, 0))
	# Print the message to screen using coordinates
	screen.blit(text_surface, (x,y))

# Collision calculation with enemies, when the square touches the triangles it will display message "DEAD"
def checkCollision(game, player, enemies):
	for enemy in enemies:
		if (player.x + player.width) >= (enemy.x - enemy.width) and player.x <= enemy.x:
			if (player.y + player.height) >= (enemy.y - enemy.height) and player.y <= enemy.y:
				printMSG("DEAD", 355, 250, 50)
				redrawGameWindow(player, enemies)
				time.sleep(1)
				# When collision occurs the game resets
				player.reset()
				enemies[0].reset(100)
				enemies[1].reset(450)
				game.resetGame()


# Increases and prints score as well as the old score
def scoreUpdate(game):
	game.score += game.speed
	printMSG(("Score: " + str(game.score)), 50, 50, 40)	
	printMSG(("Old Score: " + str(game.oldScore)), 500, 50, 40)

# Function that increases the speed every 1000 score
def speedUpdate(game, enemylist):
	if game.score >= 3000 * game.speedMultiplier:
		game.speedMultiplier += 1
		for enemy in enemylist:
			enemy.setVel(enemy.vel + 1)


def main():

	# Game instance
	game = Game()
	game.gameInit()
	game.gameName("Running Game 2")

	# Player 1
	sq = Player()

	# Enemies 1 and 2
	ey = Enemy(random.randint(750,850),454,30,30)
	ey2 = Enemy(random.randint(1200,1400), 454, 30, 30)

	# Enemy list, if several add here
	enemyList = [ey, ey2]

	# Game condition
	running = True

	# Game loop
	while running:

		# Set screen color in RGB
		game.screenColor()

		# Continously check all events that are happening in the game
		for event in pygame.event.get():

			# Check if window is closed when the cross is pressed
			if event.type == pygame.QUIT:
				running = False

		# Variable for checking if any key is pressed
		keys = pygame.key.get_pressed()

		# Arrow key movements of player
		if keys[pygame.K_LEFT] and sq.x > 0:
			# Move player to the left with the given velocity when left key is pressed
			sq.x -= sq.vel
		if keys[pygame.K_RIGHT] and sq.x < screen_w - sq.width:
			sq.x += sq.vel

		# Jump function
		if not(sq.isJump):
			if keys[pygame.K_SPACE]:
				sq.isJump = True
		else:
			sq.jump()
			
		# Updates score every loop
		scoreUpdate(game)

		# Increases speed every 1000 score
		speedUpdate(game, enemyList)

		# Collision detection between player and enemies
		checkCollision(game, sq, enemyList)	

		# Calling this function every loop to update the drawings to screen
		redrawGameWindow(sq, enemyList)

		# Frames per second
		game.setFPS(30)

if __name__ == "__main__":
	main()

pygame.quit()
