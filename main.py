import random

import pygame

import math

import time

START_TIME = time.time()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BACKGROUND_COLOR = (20, 20, 30)
SQUARE_COUNT = 15
FPS = 120

# Substep to do better checks
SUBSTEP = 4

# each squares will now have an id to prevent wrong deletion
ID = 0

# pause
pause = False
toggle_roe_flag = False
toggle_vector_flag = False

class Square:
	cap = 60
	pity = 0
	def __init__(self, size = None) -> None:
		global ID
		self.id = ID
		ID += 1
		if not size: 
			self.square_size = random.randint(10, WINDOW_WIDTH//30)
		else:
			self.square_size = size
		self.x = random.randint(0, WINDOW_WIDTH - self.square_size)
		self.y = random.randint(0, WINDOW_HEIGHT - self.square_size)
		self.topspd = (25/self.square_size)*3*60
		self.minspd = (25/self.square_size)*60
		self.vx = random.choice([-1, 1]) * random.uniform(self.minspd, self.topspd)
		self.vy = random.choice([-1, 1]) * random.uniform(self.minspd, self.topspd)
		self.color = (
			random.randint(60, 255),
			random.randint(60, 255),
			random.randint(60, 255),
		)
		self.pulse = 0
		self.tired = 0
		#Life is proportionate to size. however, min mult is x0.5
		self.max_life = 60 * (0.5 + 0.5 * (self.square_size / (WINDOW_WIDTH // 30)))  # seconds
		# small gets 0.5x, max size get 1x
		self.life = self.max_life
		
		# same scaling logic here
		self.dmg = 1 * round((0.5 + 0.5 * (self.square_size / (WINDOW_WIDTH // 30))), 2)

	def getrect(self):
		return pygame.Rect(self.x, self.y, self.square_size, self.square_size)

	@staticmethod
	def squarecreation(listofsquares: list['Square'], disabledsquares: list['Square']):
		if len(disabledsquares) == 0:
			new = Square()
			listofsquares.append(new)
			return listofsquares
		else:
			# always take the first item in the list and randomize everything
			# ... this might mean having to copy the __init__ thing...
			# please ignore this
			# however, we dont change the id
			#

			disabledsquares[0].square_size = random.randint(10, WINDOW_WIDTH//30)
			disabledsquares[0].x = random.randint(0, WINDOW_WIDTH - disabledsquares[0].square_size)
			disabledsquares[0].y = random.randint(0, WINDOW_HEIGHT - disabledsquares[0].square_size)
			disabledsquares[0].topspd = (25/disabledsquares[0].square_size)*3*60
			disabledsquares[0].minspd = (25/disabledsquares[0].square_size)*60
			disabledsquares[0].vx = random.choice([-1, 1]) * random.uniform(disabledsquares[0].minspd, disabledsquares[0].topspd)
			disabledsquares[0].vy = random.choice([-1, 1]) * random.uniform(disabledsquares[0].minspd, disabledsquares[0].topspd)
			disabledsquares[0].color = (
				random.randint(60, 255),
				random.randint(60, 255),
				random.randint(60, 255),
			)
			disabledsquares[0].pulse = 0
			disabledsquares[0].tired = 0
			disabledsquares[0].max_life = 60*(0.5 + 0.5 * (disabledsquares[0].square_size / (WINDOW_WIDTH // 30)))
			disabledsquares[0].life = disabledsquares[0].max_life
			disabledsquares[0].dmg = 1 * round((0.5 + 0.5 * (disabledsquares[0].square_size / (WINDOW_WIDTH // 30))), 2)
			
			#
			# Now transfer that item and append it to listofsquares
			listofsquares.append(disabledsquares.pop(0))
	
	def bidfarewell(self, listofsquares: list['Square'], disabledsquares: list['Square']) -> None:
		# move it to disabledsquares.
		listofsquares.remove(self)
		disabledsquares.append(self)

	def i_want_to_KILL_you(self, other: 'Square'):
		# both squares will now reduce each other's health
		# i will still keep the name cuz its funny
		self.life -= other.dmg
		other.life -= self.dmg

	def squarecollision(self, other, listofsquares: list['Square'], disabledsquares: list['Square']):
		a = self.getrect()
		b = other.getrect()
		if a.colliderect(b):
			self.pulse = 1/3
			other.pulse = 1/3
			overlap_x = min(a.right, b.right) - max(a.left, b.left)
			overlap_y = min(a.bottom, b.bottom) - max(a.top, b.top)
			if overlap_x < overlap_y:
				if self.cap > len(listofsquares):
					if random.randint(1, 10-Square.pity) == 1:
						Square.pity = 0
						self.squarecreation(listofsquares, disabledsquares)
					else:
						Square.pity = min(Square.pity + 1, 9)
				
				# self is to the left
				if a.x < b.x:
					if self.vx - other.vx > 0:
						self.vx *= -1
						self.vx += random.uniform(-2.0, 2.0)
						# fix the bug where sometimes the small square move with the big square
						if other.vx < 0:
							other.vx *= -1
							other.vx += random.uniform(-2.0, 2.0) * 60
						self.x = b.x - a.width
					self.i_want_to_KILL_you(other)
					return True
				# self is to the right
				elif a.x > b.x:
					if self.vx - other.vx < 0:
						self.vx *= -1
						self.vx += random.uniform(-2.0, 2.0)
						if other.vx > 0:
							other.vx *= -1
							other.vx += random.uniform(-2.0, 2.0)* 60
						self.x = b.x + b.width
					self.i_want_to_KILL_you(other)
					return True
						
			else:
				# self is above
				if a.y < b.y:
					if self.vy - other.vy > 0:
						self.vy *= -1
						self.vy += random.uniform(-2.0, 2.0)
						if other.vy < 0:
							other.vy *= -1
							other.vy += random.uniform(-2.0, 2.0)* 60
						self.y = b.y - a.height
					self.i_want_to_KILL_you(other)
					return True
				# self is below
				elif a.y > b.y:
					if self.vy - other.vy < 0:
						self.vy *= -1
						self.vy += random.uniform(-2.0, 2.0)
						if other.vy > 0:
							other.vy *= -1
							other.vy += random.uniform(-2.0, 2.0)* 60
						self.y = b.y + b.height
					self.i_want_to_KILL_you(other)
					return True
	
	def flee(self, other: 'Square'):
		# if the self square is the smaller square and satisfies the criteria
		# we do not need to flip the condition since the for loop in main is already doing it
		if self.tired > 0:
			return
		selfcenter = [self.x + self.square_size/2, self.y + self.square_size/2]
		othercenter = [other.x + other.square_size/2, other.y + other.square_size/2]
		if self.square_size < other.square_size:

			# roe is Radius Of Effect
			roe = other.square_size * 3
			dist = math.sqrt(pow(selfcenter[0] - othercenter[0], 2) + pow(selfcenter[1] - othercenter[1], 2))

			if dist <= roe:
				away_x = (selfcenter[0] - othercenter[0]) / dist
				away_y = (selfcenter[1] - othercenter[1]) / dist
				flee_strength = 0.3*60
				self.vx += away_x * flee_strength
				self.vy += away_y * flee_strength
		else:
			pass

	def chase(self, other: 'Square'):
		if self.tired > 0:
			return
		selfcenter = [self.x + self.square_size/2, self.y + self.square_size/2]
		othercenter = [other.x + other.square_size/2, other.y + other.square_size/2]
		if self.square_size > other.square_size:

			roe = other.square_size * 3
			dist = math.sqrt(pow(selfcenter[0] - othercenter[0], 2) + pow(selfcenter[1] - othercenter[1], 2))

			if dist <= roe:
				to_x = (- selfcenter[0] + othercenter[0]) / dist
				to_y = (- selfcenter[1] + othercenter[1]) / dist
				strength = 0.3*60
				self.vx += to_x * strength
				self.vy += to_y * strength
		else:
			pass

	def move(self, dt: float, steps: int, listofsquares: list['Square'], disabledsquares: list['Square']) -> None:
		# if the square doesnt exist, simply dont move it or anything.
		if self.life <= 0:
			self.bidfarewell(listofsquares, disabledsquares)
			return
		self.life -= dt / steps
		if random.randint(1, 1000) == 67 and self.tired == 0:
			# At random, squares stops to rest
			self.tired = random.uniform(1, 3)
		if self.pulse > 0:
			self.pulse = max(0, self.pulse - dt)
		if self.tired > 0:
			self.tired = max(0, self.tired - dt)
		else:
			# True speed vector, which is the hypothneuse or something from the triangle made from vx and vy
			
			truespd = math.hypot(self.vx, self.vy)
			if truespd > self.topspd+5.0:
				scale = (self.topspd + 5)/ truespd
				self.vx *= scale
				self.vy *= scale
			if truespd < self.minspd:
				scale = (self.topspd + 5)/ truespd
				self.vx *= scale
				self.vy *= scale
				if random.randint(1, 500) == 1:
				
				# confused, refert movement
					self.vx *= -1
					self.vy *= -1
			
			# We divide the movement into smaller steps so that faster moving squares
			# Don't pass through the collision check
			self.x += self.vx * (dt / steps)
			self.y += self.vy * (dt / steps)
			# reduce life by 1 / step so square lives for like 120s or less secs
			
			# Bounce on screen edges by reversing direction.
	
	def bordercollision(self, listofsquares: list['Square'], disabledsquares: list['Square']):
		if self.x <= 0 or self.x >= WINDOW_WIDTH - self.square_size:
			self.pulse = 1/3
			self.vx *= -1
			self.x = max(0, min(self.x, WINDOW_WIDTH - self.square_size))
			if self.cap > len(listofsquares):
				if random.randint(1, 40-Square.pity) == 1:
					Square.pity = 0
					self.squarecreation(listofsquares, disabledsquares)
				else:
					Square.pity = min(Square.pity + 1, 9)

		if self.y <= 0 or self.y >= WINDOW_HEIGHT - self.square_size:
			self.pulse = 1/3
			self.vy *= -1
			self.y = max(0, min(self.y, WINDOW_HEIGHT - self.square_size))
			if self.cap > len(listofsquares):
				if random.randint(1, 40-Square.pity) == 1:
					Square.pity = 0
					self.squarecreation(listofsquares, disabledsquares)
				else:
					Square.pity = min(Square.pity + 1, 9)

	def draw(self, surface: pygame.Surface) -> None:
		# Using pulse boost instead of pulse for easier control of brightness. Pulse_boost spans from 0.0 to 1.0	
		# same with this, if life <0, dont draw.
		if self.life <= 0:
			return
		else:
			# the lower the health, the more towards white the square is.
			pulse_boost = self.pulse / (1/3)
			life_ratio = self.life / self.max_life
			state_color = tuple(min(255, int(c + pulse_boost*50 + (1-life_ratio)*(255-c))) for c in self.color)
			pygame.draw.rect(surface, state_color, (self.x, self.y, self.square_size, self.square_size))
	
def draw_pause(screen, surface, font, toggle_roe_flag, toggle_vector_flag):
	pygame.draw.rect(surface, (128, 128, 128, 150), [0,0, WINDOW_WIDTH, WINDOW_HEIGHT])
	button_size = [300, 75] # width, height
	reset = pygame.draw.rect(surface, 'white', [WINDOW_WIDTH/2-button_size[0]/2, WINDOW_HEIGHT*1/6, button_size[0], button_size[1]], 0, 10)
	toggle_vector = pygame.draw.rect(surface, 'white', [WINDOW_WIDTH/2-button_size[0]/2, WINDOW_HEIGHT*2.1/5, button_size[0], button_size[1]], 0, 10)
	toggle_roe = pygame.draw.rect(surface, 'white', [WINDOW_WIDTH/2-button_size[0]/2, WINDOW_HEIGHT*2/3, button_size[0], button_size[1]], 0, 10)
	surface.blit(font.render('Reset Squares', True, 'black'), (WINDOW_WIDTH/2-button_size[0]/3.5, WINDOW_HEIGHT*1/6+button_size[1]/3))
	if toggle_vector_flag:
		surface.blit(font.render('Square Vectors: On', True, 'black'), (WINDOW_WIDTH/2-button_size[0]/2.5, WINDOW_HEIGHT*2.1/5+button_size[1]/3))
	else:
		surface.blit(font.render('Square Vectors: Off', True, 'black'), (WINDOW_WIDTH/2-button_size[0]/2.5, WINDOW_HEIGHT*2.1/5+button_size[1]/3))
	if toggle_roe_flag:
		surface.blit(font.render('Radius Of Effect: On', True, 'black'), (WINDOW_WIDTH/2-button_size[0]/2.4, WINDOW_HEIGHT*2/3+button_size[1]/3))
	else:
		surface.blit(font.render('Radius Of Effect: Off', True, 'black'), (WINDOW_WIDTH/2-button_size[0]/2.4, WINDOW_HEIGHT*2/3+button_size[1]/3))
	screen.blit(surface, (0,0))
	return reset, toggle_roe, toggle_vector




def main() -> None:
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
	pygame.display.set_caption("Extra Random Moving Squares")
	clock = pygame.time.Clock()
	font = pygame.font.SysFont(None, 36)
	squares = []

	# 5 quares of 25 pixels
	for i in range(5):
		squares.append(Square(25))
	# 10 squares of 10 pixels
	for i in range(10):
		squares.append(Square(10))
	# 30 squares of size 4 pixels
	for i in range(30):
		squares.append(Square(4))

	disabled_squares = []
	running = True

	while running:
		dt = clock.tick(FPS) / 1000.0
		global pause
		global toggle_roe_flag, toggle_vector_flag
		# current_time = time.time() - START_TIME
		# mousex, mousey = pygame.mouse.get_pos()
		if len(squares) == 0:
			# out of squares, you just lose
			running = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
					if pause:
						pause = False
					else:
						pause = True
			if event.type == pygame.MOUSEBUTTONDOWN and pause:
				if reset.collidepoint(event.pos):
					if len(squares) >= 15:
						for i in range(len(squares)):
							if i < 15:
								# keep the first few squares, however, reset max health
								squares[i].life = squares[i].max_life
							else:
								squares[15].bidfarewell(squares, disabled_squares)
					if len(squares) < 15:
						for i in range(len(squares)):
							squares[i].life = squares[i].max_life
						for i in range(15 - len(squares)):
							squares[i].squarecreation(squares, disabled_squares)
				if toggle_roe.collidepoint(event.pos):
					if toggle_roe_flag:
						toggle_roe_flag = False
					else:
						toggle_roe_flag = True
				if toggle_vector.collidepoint(event.pos):
					if toggle_vector_flag:
						toggle_vector_flag = False
					else:
						toggle_vector_flag = True
				


		if not pause: 
			for _ in range(SUBSTEP):
				for square in list(squares):
					square.move(dt, SUBSTEP, squares, disabled_squares)
					if square in squares:
						square.bordercollision(squares, disabled_squares)
				
			# the flags are redundant as theres only 1 check needed
			for squarea in list(squares):
				for squareb in list(squares):
					if squarea != squareb and squarea in squares and squareb in squares:
						squarea.squarecollision(squareb, squares, disabled_squares)
						squarea.flee(squareb)
						squarea.chase(squareb)
		

		screen.fill(BACKGROUND_COLOR)
		if not pause:
			if toggle_roe_flag or toggle_vector_flag:
				roe_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
				for square in squares:
					center = (square.x + square.square_size/2, square.y + square.square_size/2)
					if toggle_roe_flag:
						pygame.draw.circle(roe_surface, (*square.color, 100), center, square.square_size*3, 3)
					# use line
					# aint using ai for this dawg this is simple enough. Also no arrows.
					if toggle_vector_flag:
						pseudo_destination = (
												center[0] + (square.vx/60) * square.square_size * 1.2 * (0.25 + 0.5 * (square.square_size / (WINDOW_WIDTH // 30))),
												center[1] + (square.vy/60) * square.square_size * 1.2 * (0.25 + 0.5 * (square.square_size / (WINDOW_WIDTH // 30)))
											)
						pygame.draw.line(roe_surface, (*square.color, 100), center, pseudo_destination, 3)
				screen.blit(roe_surface,(0, 0))

		for square in squares:
			# whatever is on top needs to be drawn later
			# This is in another loop to fix a bug where the AOE effect is on top of the squares
			square.draw(screen)
		text1 = font.render(f"Squares: {len(squares)} / {Square.cap}", True, (255, 255, 255))
		text2 = font.render(f"Spawn Chance: {round((1/(min(Square.pity + 1, 9)))*100, 3)}%", True, (255, 255, 255))
		#text2 = font.render(f"Time: {current_time} seconds", True, (255,255,255))
		screen.blit(text1, (10, 10))
		screen.blit(text2, (10, 10 + font.get_height()))
		if pause:
			reset, toggle_roe, toggle_vector = draw_pause(screen, surface, font, toggle_roe_flag, toggle_vector_flag)	
		pygame.display.flip()

	pygame.quit()


if __name__ == "__main__":
	main()
