import pygame
from pygame.locals import *
import sys

BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
RED       = (255, 8, 0)

SCREEN_SIZE = [320,400]
BAR_SIZE = [20, 5]
BALL_SIZE = [15, 15]

class Game(object):
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(SCREEN_SIZE)
		pygame.display.set_caption('Simple Game')

		self.ball_pos_x = SCREEN_SIZE[0]//2 - BALL_SIZE[0]/2
		self.ball_pos_y = SCREEN_SIZE[1]//2 - BALL_SIZE[1]/2

		self.ball_dir_x = -1 # -1 = left 1 = right
		self.ball_dir_y = -1 # -1 = up   1 = down
		self.ball_pos = pygame.Rect(self.ball_pos_x, self.ball_pos_y, BALL_SIZE[0], BALL_SIZE[1])

		self.score = 0
		self.bar_pos_x = SCREEN_SIZE[0]//2-BAR_SIZE[0]//2
		self.bar_pos = pygame.Rect(self.bar_pos_x, SCREEN_SIZE[1]-BAR_SIZE[1], BAR_SIZE[0], BAR_SIZE[1])

	def bar_move_left(self):
		self.bar_pos_x = self.bar_pos_x - 2
	def bar_move_right(self):
		self.bar_pos_x = self.bar_pos_x + 2

	def run(self):
		pygame.mouse.set_visible(0) # make cursor invisible
		bar_move_left = False
		bar_move_right = False
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
					bar_move_left = True
				elif event.type == pygame.KEYUP and event.key == K_LEFT:
					bar_move_left = False
				elif event.type == pygame.KEYDOWN and event.key == K_RIGHT:
					bar_move_right = True
				elif event.type == pygame.KEYUP and event.key == K_RIGHT:
					bar_move_right = False

			if bar_move_left == True and bar_move_right == False:
				self.bar_move_left()
			if bar_move_left == False and bar_move_right == True:
				self.bar_move_right()

			self.screen.fill(BLACK)
			self.bar_pos.left = self.bar_pos_x
			pygame.draw.rect(self.screen, WHITE, self.bar_pos)

			self.ball_pos.left += self.ball_dir_x * 2
			self.ball_pos.bottom += self.ball_dir_y * 3
			pygame.draw.rect(self.screen, WHITE, self.ball_pos)

			if self.ball_pos.top <= 0 or self.ball_pos.bottom >= (SCREEN_SIZE[1] - BAR_SIZE[1]+1):
				self.ball_dir_y = self.ball_dir_y * -1
			if self.ball_pos.left <= 0 or self.ball_pos.right >= (SCREEN_SIZE[0]):
				self.ball_dir_x = self.ball_dir_x * -1


			if self.bar_pos.top <= self.ball_pos.bottom and (self.bar_pos.left < self.ball_pos.right and self.bar_pos.right > self.ball_pos.left):
				self.score += 1
				print("Score: ", self.score, end='\r')
			elif self.bar_pos.top <= self.ball_pos.bottom and (self.bar_pos.left > self.ball_pos.right or self.bar_pos.right < self.ball_pos.left):
				print("You loose the Game: ", self.score)
				return self.score
			pygame.display.update()
			self.clock.tick(60)


class AIGame(object):
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(SCREEN_SIZE)
		pygame.display.set_caption('Simple Game')

		self.ball_pos_x = SCREEN_SIZE[0]//2 - BALL_SIZE[0]/2
		self.ball_pos_y = SCREEN_SIZE[1]//2 - BALL_SIZE[1]/2

		self.predict_pos_x = self.ball_pos_x
		self.predict_pos_y = self.ball_pos_y
		# ball's initial position
		self.ball_dir_x = -1 # -1 = left 1 = right
		self.ball_dir_y = -1 # -1 = up   1 = down
		self.ball_pos = pygame.Rect(self.ball_pos_x, self.ball_pos_y, BALL_SIZE[0], BALL_SIZE[1])

		self.predict_dir_x = -1 # -1 = left 1 = right
		self.predict_dir_y = -1 # -1 = up   1 = down
		self.predict_pos = pygame.Rect(self.predict_pos_x, self.predict_pos_y, BALL_SIZE[0], BALL_SIZE[1])

		self.score = 0
		self.bar_pos_x = SCREEN_SIZE[0]//2-BAR_SIZE[0]//2
		self.bar_pos = pygame.Rect(self.bar_pos_x, SCREEN_SIZE[1]-BAR_SIZE[1], BAR_SIZE[0], BAR_SIZE[1])

		self.bar_move_left_v = False
		self.bar_move_right_v = False

	def bar_move_left(self):
		self.bar_pos_x = self.bar_pos_x - 2
	def bar_move_right(self):
		self.bar_pos_x = self.bar_pos_x + 2
	def sensor(self):
		bar_position = self.bar_pos.center[0]
		predict_position = self. predict_pos.center[0]
		return (predict_position, bar_position)

	def right_key_press(self): # this make the bar move to right
		self.bar_move_right_v = True
		self.bar_move_left_v = False
	def left_key_press(self): # this makes the bar move to left
		self.bar_move_left_v = True
		self.bar_move_right_v = False
	def no_press(self): # do not press anything
		self.bar_move_left_v = False
		self.bar_move_right_v = False

	def brain(self):
		predict_value = self.sensor()
		if abs(predict_value[0] - predict_value[1]) <= 2:
			self.no_press()
		elif predict_value[0] > predict_value[1]:
			self.right_key_press()
		elif predict_value[1] > predict_value[0]:
			self.left_key_press()
	def run(self):
		pygame.mouse.set_visible(0) # make cursor invisible
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
					print("Score:", self.score, end='\r')
					print("Game Terminated:", self.score)
					return self.score
			self.brain()
			if self.bar_move_left_v == True and self.bar_move_right_v == False:
				self.bar_move_left()
			if self.bar_move_left_v == False and self.bar_move_right_v == True:
				self.bar_move_right()

			self.screen.fill(BLACK)
			self.bar_pos.left = self.bar_pos_x
			pygame.draw.rect(self.screen, WHITE, self.bar_pos)

			self.ball_pos.left += self.ball_dir_x * 2
			self.ball_pos.bottom += self.ball_dir_y * 3
			pygame.draw.rect(self.screen, WHITE, self.ball_pos)

			if self.bar_pos.top < self.predict_pos.bottom:
			    self.predict_pos.left += self.predict_dir_x * 0
			    self.predict_pos.bottom += self.predict_dir_y * 0
			elif self.bar_pos.top >= self.predict_pos.bottom:
				self.predict_pos.left += self.predict_dir_x * 8
				self.predict_pos.bottom += self.predict_dir_y * 12
			# pygame.draw.rect(self.screen, RED, self.predict_pos)
			# if want to see how the prediction works, you can use the above
			# code to visible the prediction path.

			if self.ball_pos.top <= 0 or self.ball_pos.bottom >= (SCREEN_SIZE[1] - BAR_SIZE[1]+1):
				self.ball_dir_y = self.ball_dir_y * -1
			if self.ball_pos.left <= 0 or self.ball_pos.right >= (SCREEN_SIZE[0]):
				self.ball_dir_x = self.ball_dir_x * -1
			if self.predict_pos.top <= 0 or self.predict_pos.bottom >= (SCREEN_SIZE[1] - BAR_SIZE[1]+1):
				self.predict_dir_y = self.predict_dir_y * -1
			if self.predict_pos.left <= 0:
				self.predict_dir_x = self.predict_dir_x * -1
				self.predict_pos.left = 0
			if self.predict_pos.right >= (SCREEN_SIZE[0]):
				self.predict_dir_x = self.predict_dir_x * -1
				self.predict_pos.right = SCREEN_SIZE[0]

			if self.bar_pos.top <= self.ball_pos.bottom and (self.bar_pos.left < self.ball_pos.right and self.bar_pos.right > self.ball_pos.left):
				self.score += 1
				self.predict_dir_x = self.ball_dir_x
				self.predict_dir_y = self.ball_dir_y
				self.predict_pos.center = self.ball_pos.center
				self.predict_pos.left += self.predict_dir_x * 8
				self.predict_pos.bottom += self.predict_dir_y * 12
				# if the ball touch the bar, the prediction will reset, which
				# based on ball's location and heading direction
				print("Score: ", self.score, end='\r')
				# return self.score
			elif self.bar_pos.top <= self.ball_pos.bottom and (self.bar_pos.left > self.ball_pos.right or self.bar_pos.right < self.ball_pos.left):
				print("AI loose the Game: ", self.score)
				return self.score
			pygame.display.update()
			self.clock.tick(60)

print("Which mode you want to play? self/AI :")
mode = input()
if mode == "AI":
	print("Attenction: You can terminate the AI by pressing Esc key")
	aigame = AIGame()
	aigame.run()
elif mode == "self":
	game = Game()
	game.run()
else:
	print("unrecoganizable command, please type self or type AI")
