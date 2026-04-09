import random

import pygame

import math

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BACKGROUND_COLOR = (20, 20, 30)
SQUARE_COUNT = 15
FPS = 60

# Substep to do better checks
SUBSTEP = 4


class Square:
	cap = 40
	pity = 0
	def __init__(self) -> None:
		self.square_size = random.randint(10, WINDOW_WIDTH//30)
		self.x = random.randint(0, WINDOW_WIDTH - self.square_size)
		self.y = random.randint(0, WINDOW_HEIGHT - self.square_size)
		self.topspd = (25/self.square_size)*3
		self.minspd = (25/self.square_size)
		self.vx = random.choice([-1, 1]) * random.uniform(self.minspd, self.topspd)
		self.vy = random.choice([-1, 1]) * random.uniform(self.minspd, self.topspd)
		self.color = (
			random.randint(60, 255),
			random.randint(60, 255),
			random.randint(60, 255),
		)
		self.pulse = 0
		self.tired = 0

	def getrect(self):
		return pygame.Rect(self.x, self.y, self.square_size, self.square_size)

	@staticmethod
	def squarecreation(listofsquares):
		new = Square()
		listofsquares.append(new)
		return listofsquares

	def i_want_to_KILL_you(self, other: 'Square', listofsquares: list):
		if random.randint(1, 250) == 1:
			#kill smaller square, or
			if self.square_size <= other.square_size:
				
				listofsquares.remove(self)
				del self
			else:
				listofsquares.remove(other)
				del other


	def squarecollision(self, other, listofsquares):
		a = self.getrect()
		b = other.getrect()
		if a.colliderect(b):
			self.pulse = FPS//3
			other.pulse = FPS//3
			overlap_x = min(a.right, b.right) - max(a.left, b.left)
			overlap_y = min(a.bottom, b.bottom) - max(a.top, b.top)
			if overlap_x < overlap_y:
				if self.cap > len(listofsquares):
					if random.randint(1, 100-Square.pity) == 1:
						Square.pity = 0
						self.squarecreation(listofsquares)
					else:
						Square.pity += 1
				
				# self is to the left
				if a.x < b.x:
					if self.vx - other.vx > 0:
						self.vx *= -1
						self.vx += random.uniform(-2.0, 2.0)
						# fix the bug where sometimes the small square move with the big square
						if other.vx < 0:
							other.vx *= -1
							other.vx += random.uniform(-2.0, 2.0)
						self.x = b.x - a.width
					self.i_want_to_KILL_you(other, listofsquares)
					return True
				# self is to the right
				elif a.x > b.x:
					if self.vx - other.vx < 0:
						self.vx *= -1
						self.vx += random.uniform(-2.0, 2.0)
						if other.vx > 0:
							other.vx *= -1
							other.vx += random.uniform(-2.0, 2.0)
						self.x = b.x + b.width
					self.i_want_to_KILL_you(other, listofsquares)
					return True
						
			else:
				# self is above
				if a.y < b.y:
					if self.vy - other.vy > 0:
						self.vy *= -1
						self.vy += random.uniform(-2.0, 2.0)
						if other.vy < 0:
							other.vy *= -1
							other.vy += random.uniform(-2.0, 2.0)
						self.y = b.y - a.height
					self.i_want_to_KILL_you(other, listofsquares)
					return True
				# self is below
				elif a.y > b.y:
					if self.vy - other.vy < 0:
						self.vy *= -1
						self.vy += random.uniform(-2.0, 2.0)
						if other.vy > 0:
							other.vy *= -1
							other.vy += random.uniform(-2.0, 2.0)
						self.y = b.y + b.height
					self.i_want_to_KILL_you(other, listofsquares)
					return True
	
	def flee(self, other: 'Square'):
		# if the self square is the smaller square and satisfies the criteria
		# we do not need to flip the condition since the for loop in main is already doing it
		selfcenter = [self.x + self.square_size/2, self.y + self.square_size/2]
		othercenter = [other.x + other.square_size/2, other.y + other.square_size/2]
		if self.square_size < other.square_size:

			# roe is Radius Of Effect
			roe = other.square_size * 3
			dist = math.sqrt(pow(selfcenter[0] - othercenter[0], 2) + pow(selfcenter[1] - othercenter[1], 2))

			if dist <= roe:
				away_x = (selfcenter[0] - othercenter[0]) / dist
				away_y = (selfcenter[1] - othercenter[1]) / dist
				flee_strength = 0.3
				self.vx += away_x * flee_strength
				self.vy += away_y * flee_strength
		else:
			pass

	def move(self, steps) -> None:
		if random.randint(1, 1000) == 67 and self.tired == 0:
			# At random, squares stops to rest
			self.tired = random.randint(FPS, 3*FPS)
		if self.tired > 0:
			self.tired -= 1
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
			self.x += self.vx / steps
			self.y += self.vy / steps
		
		# Bounce on screen edges by reversing direction.
	def bordercollision(self, listofsquares):
		if self.x <= 0 or self.x >= WINDOW_WIDTH - self.square_size:
			self.pulse = FPS//3
			self.vx *= -1
			self.x = max(0, min(self.x, WINDOW_WIDTH - self.square_size))
			if self.cap > len(listofsquares):
				if random.randint(1, 100-Square.pity) == 1:
					Square.pity = 0
					self.squarecreation(listofsquares)
				else:
					self.pity += 1

		if self.y <= 0 or self.y >= WINDOW_HEIGHT - self.square_size:
			self.pulse = FPS//3
			self.vy *= -1
			self.y = max(0, min(self.y, WINDOW_HEIGHT - self.square_size))
			if self.cap > len(listofsquares):
				if random.randint(1, 100-Square.pity) == 1:
					Square.pity = 0
					self.squarecreation(listofsquares)
				else:
					self.pity += 1

	

	def draw(self, surface: pygame.Surface) -> None:
		# Using pulse boost instead of pulse for easier control of brightness. Pulse_boost spans from 0.0 to 1.0		
		pulse_boost = self.pulse / (FPS//3)
		state_color = tuple(min(255, int(c + pulse_boost*50)) for c in self.color)
		pygame.draw.rect(surface, state_color, (self.x, self.y, self.square_size, self.square_size))
		if self.pulse > 0:
			self.pulse -= 1



def main() -> None:
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Random Moving Squares")
	clock = pygame.time.Clock()
	font = pygame.font.SysFont(None, 36)
	squares = [Square() for _ in range(SQUARE_COUNT)]
	running = True

	while running:
		mousex, mousey = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# Repeat SUBSTEP amount of times to accomodate for the change in movement
		for _ in range(SUBSTEP):
			for square in squares:
				square.move(SUBSTEP)
				square.bordercollision(squares)
			
		# the flags are redundant as theres only 1 check needed
		for squarea in squares:
			for squareb in squares:
				if squarea != squareb:
					squarea.squarecollision(squareb, squares)	
					squarea.flee(squareb)	

		screen.fill(BACKGROUND_COLOR)
		for square in squares:
			if pygame.Rect.collidepoint(pygame.Rect(square.x, square.y, square.square_size, square.square_size), mousex, mousey):
				center = (square.x + square.square_size/2, square.y + square.square_size/2)
				pygame.draw.circle(screen, (79, 39, 39), center, square.square_size*3, 0)
		for square in squares:
			# whatever is on top needs to be drawn later
			# This is in another loop to fix a bug where the AOE effect is on top of the squares
			square.draw(screen)
		text1 = font.render(f"Squares: {len(squares)} / {Square.cap}", True, (255, 255, 255))
		text2 = font.render(f"Spawn Chance: {round((1/(100-Square.pity))*100, 3)}%", True, (255, 255, 255))
		screen.blit(text1, (10, 10))
		screen.blit(text2, (10, 10 + font.get_height()))		
		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()


if __name__ == "__main__":
	main()
